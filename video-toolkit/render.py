#!/usr/bin/env python3
"""render.py - edit list -> finished 1920x1080 30 fps H.264/AAC video.

Needs only ffmpeg/ffprobe + ImageMagick (`magick`) + PyYAML (for .yaml lists; .csv/.json work without).
The stock Homebrew ffmpeg here has NO drawtext/subtitles/ass filters, so every piece of text (corner
stamp, captions, title cards, SRT cues) is rendered to a transparent PNG with ImageMagick and laid on
with ffmpeg's `overlay` filter. Same look, no extra install.

Usage:
  render.py EDIT.yaml [-o out.mp4] [--stamp TEXT] [--srt FILE] [--crf N] [--draft] [--plan] [--work DIR] [-v]

Edit list (YAML, see example.yaml; CSV columns: source,in,out,speed,caption,layout,source2,in2,vo,stamp,crop):
  output, stamp, stamp_pos(br|bl|tr|tl), bg, srt (final-timeline captions .srt/.ass), loudnorm, voiceover:[{file,at}]
  clips: list of
    {title: "CI/CD pipeline", sub: "...", kicker: "Section 1", dur: 3}          # title card
    {source, in, out, speed, caption, layout: fit|fill|phone|sbs, source2, in2, crop: "x:y:w:h", vo, vo_delay, stamp}
  Times: seconds (12.5), m:ss or h:mm:ss. `out` blank = end of file. caption supports {actual} and {speed}.
  layout sbs = phone (source, left-of-centre) beside desktop (source2). `in2` defaults to 0.
Segments are cached by content hash in the work dir, so re-running after an edit re-renders only what changed.
"""
import argparse, csv, hashlib, json, re, shutil, subprocess, sys
from pathlib import Path

W, H, FPS = 1920, 1080, 30
SUP = "/System/Library/Fonts/Supplemental"
FONT = {"r": f"{SUP}/Arial.ttf", "b": f"{SUP}/Arial Bold.ttf", "m": f"{SUP}/Andale Mono.ttf"}
BOTTOM = 1004  # bottom edge (y) of the lowest caption pill; the stamp sits below it
STYLES = {  # fg, bg (RRGGBBAA), font, pointsize, pad x/y, radius
    "lower": dict(fg="white", bg="#0b1220e0", font="b", pt=44, px=30, py=16, r=22),
    "wait": dict(fg="#111827", bg="#fbbf24f2", font="b", pt=44, px=30, py=16, r=22),
    "stamp": dict(fg="#e2e8f0", bg="#000000b8", font="m", pt=28, px=16, py=8, r=12),
}
# geometry of the framed layouts: screen holes (x, y, w, h, corner radius)
PHONE = dict(x=766, y=30, w=388, h=840, r=54, bezel=14)
SBS_PHONE = dict(x=1406, y=100, w=352, h=760, r=50, bezel=13)
SBS_DESK = dict(x=148, y=148, w=1180, h=664, r=14, bezel=2)

LOG = []
TAG = ",setparams=colorspace=bt709:color_primaries=bt709:color_trc=bt709:range=tv"  # tag every frame BT.709 limited range


def sh(cmd, verbose=False):
    cmd = [str(c) for c in cmd]
    LOG.append(" ".join(f"'{c}'" if re.search(r"[\s;\[\]()|<>]", c) else c for c in cmd))
    if verbose:
        print("+", LOG[-1], file=sys.stderr)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"command failed ({r.returncode}): {LOG[-1][:400]}\n{r.stderr[-1500:]}")
    return r.stdout


VERSION = hashlib.sha1(Path(__file__).read_bytes()).hexdigest()[:8]  # any edit to this script invalidates cached assets/segments


def sha(*parts):
    return hashlib.sha1("|".join(map(str, (VERSION, *parts))).encode()).hexdigest()[:10]


def tsec(v, default=None):
    if v is None or v == "":
        return default
    if isinstance(v, (int, float)):
        return float(v)
    parts = [float(p) for p in str(v).split(":")]
    return sum(p * 60 ** i for i, p in enumerate(reversed(parts)))


def fmt_actual(s):
    s = round(s)
    return f"{s} s" if s < 120 else f"{s // 60} min {s % 60:02d} s"


def probe(path):
    j = json.loads(sh(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", path]))
    v = next(s for s in j["streams"] if s["codec_type"] == "video")
    return dict(dur=float(j["format"]["duration"]), audio=any(s["codec_type"] == "audio" for s in j["streams"]),
                w=v["width"], h=v["height"])


# ---------------------------------------------------------------- edit list
def load_edl(path):
    p = Path(path)
    if p.suffix == ".csv":
        rows = []
        for r in csv.DictReader(p.open(newline="")):
            r = {k: v for k, v in r.items() if v not in ("", None)}
            src = r.get("source", "")
            if src.lower().startswith("title:"):  # title:Section name|subtitle ; out = seconds
                t, _, sub = src[6:].partition("|")
                r = dict(title=t, sub=sub, dur=r.get("out", 3), stamp=r.get("stamp"))
            rows.append(r)
        return {"clips": rows}
    if p.suffix == ".json":
        return json.loads(p.read_text())
    import yaml  # PyYAML: present for /opt/homebrew/bin/python3
    return yaml.safe_load(p.read_text())


def parse_srt(path):
    p = Path(path)
    txt = p.read_text(encoding="utf-8-sig")
    cues = []
    if p.suffix == ".ass":
        def ass_t(s):
            h, m, sec = s.strip().split(":")
            return int(h) * 3600 + int(m) * 60 + float(sec)
        for line in txt.splitlines():
            if line.startswith("Dialogue:"):
                f = line[9:].split(",", 9)
                cues.append((ass_t(f[1]), ass_t(f[2]), re.sub(r"\{[^}]*\}", "", f[9]).replace("\\N", "\n")))
        return cues
    for block in re.split(r"\n\s*\n", txt.strip()):
        lines = block.strip().splitlines()
        m = next((re.match(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)", l) for l in lines if "-->" in l), None)
        if not m:
            continue
        g = [int(x) for x in m.groups()]
        a = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        b = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        body = "\n".join(lines[[i for i, l in enumerate(lines) if "-->" in l][0] + 1:])
        cues.append((a, b, re.sub(r"<[^>]+>", "", body)))
    return cues


# ---------------------------------------------------------------- ImageMagick assets
class Assets:
    def __init__(self, work, verbose):
        self.dir = work / "png"
        self.dir.mkdir(parents=True, exist_ok=True)
        self.v = verbose

    def im(self, *args):
        sh(["magick", *args], self.v)

    def pill(self, text, style, maxw=1560):
        st = STYLES[style]
        out = self.dir / f"pill-{sha(style, text, maxw)}.png"
        if not out.exists():
            raw = out.with_suffix(".t.png")
            self.im("-background", "none", "-fill", st["fg"], "-font", FONT[st["font"]], "-pointsize", st["pt"],
                    "-size", f"{maxw}x", "-gravity", "center", f"caption:{text}", "-trim", "+repage", raw)
            w, h = map(int, sh(["magick", "identify", "-format", "%w %h", raw]).split())
            pw, ph = w + 2 * st["px"], h + 2 * st["py"]
            self.im("-size", f"{pw}x{ph}", "xc:none", "-fill", st["bg"], "-draw",
                    f"roundrectangle 0,0 {pw - 1},{ph - 1} {st['r']},{st['r']}", raw, "-gravity", "center",
                    "-composite", f"PNG32:{out}")
            raw.unlink()
        return out, *map(int, sh(["magick", "identify", "-format", "%w %h", out]).split())

    def canvas(self, stamp, stamp_pos, lines):
        """Full-frame transparent PNG: corner stamp + caption pills stacked upward from BOTTOM."""
        out = self.dir / f"cv-{sha(stamp, stamp_pos, lines)}.png"
        if out.exists():
            return out
        args = ["-size", f"{W}x{H}", "xc:none", "-gravity", "northwest"]
        if stamp:
            f, w, h = self.pill(stamp, "stamp")
            x = W - w - 24 if stamp_pos[1] == "r" else 24
            y = H - h - 18 if stamp_pos[0] == "b" else 18
            args += [f, "-geometry", f"+{x}+{y}", "-composite"]
        y = BOTTOM
        for text, style in lines:
            f, w, h = self.pill(text, style)
            y -= h
            args += [f, "-geometry", f"+{(W - w) // 2}+{y}", "-composite"]
            y -= 12
        self.im(*args, f"PNG32:{out}")
        return out

    def title_card(self, kicker, title, sub, bg):
        out = self.dir / f"title-{sha(kicker, title, sub, bg)}.png"
        if not out.exists():
            a = ["-size", f"{W}x{H}", f"xc:{bg}", "-fill", "#2563eb", "-draw", "rectangle 160,470 260,478",
                 "-gravity", "northwest"]
            if kicker:
                a += ["-font", FONT["b"], "-fill", "#93c5fd", "-pointsize", 38, "-annotate", "+160+250", kicker]
            a += ["-font", FONT["b"], "-fill", "white", "-pointsize", 84, "-annotate", "+160+330", title]
            if sub:
                a += ["-font", FONT["r"], "-fill", "#cbd5e1", "-pointsize", 44, "-annotate", "+160+520", sub]
            self.im(*a, out)
        return out

    def frame(self, kind, bg):
        """Opaque gradient background + device bezels with transparent rounded 'screen' holes."""
        out = self.dir / f"frame-{kind}-{sha(bg)}.png"
        if out.exists():
            return out
        holes = [(PHONE, True)] if kind == "phone" else [(SBS_DESK, False), (SBS_PHONE, True)]
        a = ["-size", f"{W}x{H}", f"radial-gradient:#1e293b-{bg}", "-alpha", "set"]
        for g, is_phone in holes:
            b, x0, y0, x1, y1 = g["bezel"], g["x"], g["y"], g["x"] + g["w"] - 1, g["y"] + g["h"] - 1
            R = g["r"] + b
            a += ["(", "-size", f"{W}x{H}", "xc:none", "-fill", "#00000099", "-draw",
                  f"roundrectangle {x0 - b + 6},{y0 - b + 18} {x1 + b + 6},{y1 + b + 18} {R},{R}", "-blur", "0x22", ")",
                  "-composite", "-fill", "#0b0b0d", "-stroke", "#475569", "-strokewidth", 3, "-draw",
                  f"roundrectangle {x0 - b},{y0 - b} {x1 + b},{y1 + b} {R},{R}", "-stroke", "none",
                  "(", "-size", f"{W}x{H}", "xc:none", "-fill", "white", "-draw",
                  f"roundrectangle {x0},{y0} {x1},{y1} {g['r']},{g['r']}", ")", "-compose", "DstOut", "-composite",
                  "-compose", "Over"]
            if is_phone:  # Dynamic Island
                iw, ih = round(g["w"] * 0.318), round(g["w"] * 0.095)
                ix = x0 + (g["w"] - iw) // 2
                a += ["-fill", "black", "-draw", f"roundrectangle {ix},{y0 + 10} {ix + iw},{y0 + 10 + ih} {ih // 2},{ih // 2}"]
        self.im(*a, f"PNG32:{out}")
        return out


# ---------------------------------------------------------------- planning
def plan(edl, args):
    o = dict(stamp=None, stamp_pos="br", bg="#0f172a", srt=None, loudnorm=False, voiceover=[], output="out.mp4")
    o.update({k: v for k, v in edl.items() if k != "clips"})
    if args.stamp:
        o["stamp"] = args.stamp
    if args.srt:
        o["srt"] = str(Path(args.srt).resolve())
    base = Path(args.edl).resolve().parent
    res = lambda p: str((base / p).resolve()) if p and not Path(p).is_absolute() else p
    t = 0.0
    segs = []
    for i, r in enumerate(edl["clips"]):
        s = dict(i=i, start=t, stamp=r.get("stamp", o["stamp"]) or None, caption=r.get("caption"))
        if "title" in r:
            s.update(kind="title", title=r["title"], sub=r.get("sub", ""), kicker=r.get("kicker", ""),
                     dur=tsec(r.get("dur"), 3.0), speed=1.0, label=f"TITLE {r['title']}")
            s["out"] = round(s["dur"] * FPS) / FPS
        else:
            src = res(r["source"])
            pr = probe(src)
            a = tsec(r.get("in"), 0.0)
            b = tsec(r.get("out"), pr["dur"])
            speed = float(r.get("speed", 1) or 1)
            s.update(kind="clip", source=src, a=a, b=b, speed=speed, layout=r.get("layout", "fit"), crop=r.get("crop"),
                     has_audio=pr["audio"], label=f"{Path(src).name} {a:g}-{b:g}" + (f" x{speed:g}" if speed != 1 else ""))
            if b > pr["dur"] + 0.05:
                print(f"warning: clip {i} out={b:g} beyond end of {Path(src).name} ({pr['dur']:.2f}s): last frame is held", file=sys.stderr)
            if s["layout"] == "sbs":
                s["source2"] = res(r["source2"])
                s["a2"] = tsec(r.get("in2"), 0.0)
            s["out"] = max(1, round((b - a) / speed * FPS)) / FPS
            if s["caption"]:
                s["caption"] = s["caption"].replace("{actual}", fmt_actual(b - a)).replace("{speed}", f"{speed:g}x")
            s["keep_audio"] = bool(r.get("audio", 0.5 <= speed <= 2.0)) and pr["audio"]
        if r.get("vo"):
            o["voiceover"].append(dict(file=res(r["vo"]), at=t + float(r.get("vo_delay", 0))))
        s["end"] = t + s["out"]
        t = s["end"]
        segs.append(s)
    o["voiceover"] = [dict(file=res(v["file"]), at=tsec(v.get("at"), 0.0)) for v in o["voiceover"]]
    o["total"] = t
    o["cues"] = parse_srt(res(o["srt"])) if o["srt"] else []
    o["output"] = args.output or res(o["output"])
    return o, segs


def slices(seg, cues):
    """Split a segment into time slices with constant caption lines -> [(dur, lines)]."""
    t0, t1 = seg["start"], seg["end"]
    pieces = [(max(a, t0) - t0, min(b, t1) - t0, txt) for a, b, txt in cues if b > t0 and a < t1]
    cuts = sorted({0.0, seg["out"], *(p for pc in pieces for p in pc[:2])})
    out = []
    for a, b in zip(cuts, cuts[1:]):
        if b - a < 1e-3:
            continue
        lines = []
        if seg["caption"]:
            lines.append((seg["caption"], "wait" if seg["speed"] != 1 else "lower"))
        lines += [(txt, "lower") for pa, pb, txt in pieces if pa <= a + 1e-6 and pb >= b - 1e-6]
        if out and out[-1][1] == lines:
            out[-1] = (out[-1][0] + b - a, lines)
        else:
            out.append((b - a, lines))
    return out


# ---------------------------------------------------------------- segment render
SRC_V = ("setpts=(PTS-STARTPTS)/{sp},fps=%d,tpad=stop_mode=clone:stop_duration={hold}" % FPS)


def fit(w, h, mode):
    if mode == "fill":
        return f"scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos:out_color_matrix=bt709,crop={w}:{h}"
    return (f"scale={w}:{h}:force_original_aspect_ratio=decrease:flags=lanczos:out_color_matrix=bt709,"
            f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=black")


def render_seg(seg, o, assets, work, args):
    sl = slices(seg, o["cues"])
    key = sha(json.dumps({k: v for k, v in seg.items() if k not in ("start", "end")}, sort_keys=True, default=str),
              o["bg"], o["stamp_pos"], sl, args.draft,
              *(f"{Path(seg[k]).stat().st_mtime_ns}{Path(seg[k]).stat().st_size}" for k in ("source", "source2") if k in seg))
    out = work / f"seg{seg['i']:03d}-{key}.mov"
    seg["file"] = out
    if out.exists():
        return
    # caption/stamp track (variable-frame-rate PNG sequence through the concat demuxer): ONE overlay for any number of cues
    lst = work / f"seg{seg['i']:03d}-{key}.caps.txt"
    body = ["ffconcat version 1.0"]
    for dur, lines in sl:
        body += [f"file '{assets.canvas(seg['stamp'], o['stamp_pos'], tuple(lines))}'", f"duration {dur:.4f}"]
    body.append(body[-2])
    lst.write_text("\n".join(body) + "\n")
    has_caps = bool(seg["stamp"] or any(l for _, l in sl))

    inp, n = [], 0
    def add(*a):
        nonlocal n
        inp.extend(a)
        n += 1
        return n - 1
    g = []
    dur = seg["out"]
    mat = "scale=out_color_matrix=bt709:out_range=tv,format=yuva420p"  # RGB overlays -> BT.709 YUV+alpha
    if seg["kind"] == "title":
        i0 = add("-loop", 1, "-framerate", FPS, "-t", dur, "-i", assets.title_card(seg["kicker"], seg["title"], seg["sub"], o["bg"]))
        fo = max(0.0, dur - 0.4)
        g.append(f"[{i0}:v]scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,fade=t=in:d=0.4,fade=t=out:st={fo}:d=0.4[v0]")
        audio = None
    else:
        sp, hold = seg["speed"], dur
        srcdur = seg["b"] - seg["a"]
        crop = f"crop={':'.join(seg['crop'].split(':')[2:4] + seg['crop'].split(':')[0:2])}," if seg.get("crop") else ""
        pre = lambda lab, ix: f"[{ix}:v]{crop}" + SRC_V.format(sp=sp, hold=hold) + f",{{}}[{lab}]"
        i0 = add("-ss", seg["a"], "-t", srcdur, "-i", seg["source"])
        if seg["layout"] in ("fit", "fill"):
            g.append(pre("v0", i0).format(fit(W, H, seg["layout"]) + ",setsar=1,format=yuv420p"))
        elif seg["layout"] == "phone":
            P = PHONE
            g.append(pre("b", i0).format(fit(P["w"], P["h"], "fit") + f",pad={W}:{H}:{P['x']}:{P['y']}:color=black,setsar=1,format=yuv420p"))
            fr = add("-i", assets.frame("phone", o["bg"]))
            g.append(f"[{fr}:v]{mat}[fr];[b][fr]overlay=0:0:format=yuv420[v0]")
        elif seg["layout"] == "sbs":
            P, D = SBS_PHONE, SBS_DESK
            i1 = add("-ss", seg["a2"], "-t", srcdur, "-i", seg["source2"])
            g.append(pre("p", i0).format(fit(P["w"], P["h"], "fit") + ",setsar=1,format=yuv420p"))
            g.append(pre("d", i1).format(fit(D["w"], D["h"], "fit") + f",pad={W}:{H}:{D['x']}:{D['y']}:color=black,setsar=1,format=yuv420p"))
            fr = add("-i", assets.frame("sbs", o["bg"]))
            g.append(f"[d][p]overlay={P['x']}:{P['y']}:format=yuv420[dp];[{fr}:v]{mat}[fr];[dp][fr]overlay=0:0:format=yuv420[v0]")
        else:
            sys.exit(f"unknown layout {seg['layout']}")
        audio = None
        if seg["keep_audio"]:
            tempo = ""
            if sp != 1:
                tempo = f"atempo={sp},"
            g.append(f"[{i0}:a]{tempo}aresample=48000,aformat=channel_layouts=stereo,apad[a0]")
            audio = "[a0]"
    if has_caps:
        ci = add("-f", "concat", "-safe", 0, "-i", lst)
        g.append(f"[{ci}:v]{mat}[cap];[v0][cap]overlay=0:0:format=yuv420,format=yuv420p"+TAG+"[vout]")
    else:
        g.append("[v0]"+TAG.lstrip(",")+"[vout]")
    if audio is None:
        si = add("-f", "lavfi", "-t", dur, "-i", "anullsrc=r=48000:cl=stereo")
        audio = f"{si}:a"
    enc = ["-c:v", "libx264", "-preset", "ultrafast" if args.draft else "medium", "-crf", 28 if args.draft else args.crf,
           "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", FPS, "-g", FPS * 2, "-colorspace", "bt709",
           "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv",
           "-c:a", "pcm_s16le", "-ar", 48000, "-ac", 2]
    tmp = out.with_suffix(".part.mov")
    sh(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *inp, "-filter_complex", ";".join(g), "-map", "[vout]",
        "-map", audio, *enc, "-t", f"{dur:.4f}", tmp], args.v)
    tmp.rename(out)


# ---------------------------------------------------------------- final assembly
def assemble(o, segs, work, args):
    lst = work / "concat.txt"
    lst.write_text("".join(f"file '{s['file']}'\n" for s in segs))
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", 0, "-i", lst]
    vos = o["voiceover"]
    for v in vos:
        cmd += ["-i", v["file"]]
    af = []
    last = "0:a"
    if vos:
        outs = []
        for k, v in enumerate(vos, 1):
            ms = round(v["at"] * 1000)
            af.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}:all=1[vo{k}]")
            outs.append(f"[vo{k}]")
        af.append(("".join(outs) + f"amix=inputs={len(vos)}:normalize=0:duration=longest[vo]") if len(vos) > 1 else "[vo1]anull[vo]")
        af.append("[vo]apad,asplit=2[vok][vom]")  # pad: sidechaincompress/amix would otherwise stop when the narration ends
        af.append("[0:a][vok]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=400:makeup=1[duck]")  # app audio ducks under narration
        af.append("[duck][vom]amix=inputs=2:normalize=0:duration=first[mix]")
        last = "mix"
    if o["loudnorm"]:
        af.append(f"[{last}]loudnorm=I=-16:TP=-1.5:LRA=11[ln]")
        last = "ln"
    Path(o["output"]).parent.mkdir(parents=True, exist_ok=True)
    if af:
        cmd += ["-filter_complex", ";".join(af), "-map", "0:v", "-map", f"[{last}]" if last != "0:a" else "0:a"]
    cmd += ["-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", 48000, "-ac", 2, "-t", f"{o['total']:.4f}",
            "-movflags", "+faststart", "-tag:v", "avc1", o["output"]]
    sh(cmd, args.v)


def summary(path, total):
    j = json.loads(sh(["ffprobe", "-v", "error", "-print_format", "json", "-count_frames", "-show_format", "-show_streams", path]))
    v = next(s for s in j["streams"] if s["codec_type"] == "video")
    a = next(s for s in j["streams"] if s["codec_type"] == "audio")
    print(f"{path}: {v['codec_name']} {v['profile']} {v['width']}x{v['height']} {v['pix_fmt']} {v['r_frame_rate']} fps, "
          f"{a['codec_name']} {a['sample_rate']} Hz {a['channels']}ch")
    print(f"  duration video {float(v['duration']):.3f}s ({v['nb_read_frames']} frames) / audio {float(a['duration']):.3f}s "
          f"/ planned {total:.3f}s / size {int(j['format']['size']) / 1e6:.1f} MB")
    if abs(float(v["duration"]) - total) > 0.1 or abs(float(a["duration"]) - total) > 0.1:
        print("  WARNING: durations deviate from plan", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("edl")
    ap.add_argument("-o", "--output")
    ap.add_argument("--stamp", help='corner stamp, e.g. "27 Oct 2026 · hosted dev · $(git rev-parse --short HEAD)"')
    ap.add_argument("--srt", help="final-timeline captions (.srt/.ass); overrides the edit list")
    ap.add_argument("--work", default="/tmp/rewind-video/work")
    ap.add_argument("--crf", type=int, default=18, help="x264 quality: 18 = visually lossless (default), 22-23 = smaller upload")
    ap.add_argument("--draft", action="store_true", help="ultrafast x264, crf 28 (previews)")
    ap.add_argument("--plan", action="store_true", help="print the timeline and stop")
    ap.add_argument("-v", action="store_true", help="echo every ffmpeg/magick command")
    args = ap.parse_args()
    for tool in ("ffmpeg", "ffprobe", "magick"):
        if not shutil.which(tool):
            sys.exit(f"{tool} not found on PATH")
    work = Path(args.work)
    work.mkdir(parents=True, exist_ok=True)
    o, segs = plan(load_edl(args.edl), args)
    print(f"{'#':>2} {'start':>8} {'end':>8} {'len':>7}  segment")
    for s in segs:
        print(f"{s['i']:>2} {s['start']:8.2f} {s['end']:8.2f} {s['out']:7.2f}  {s['label']}" + (f"  [{s['caption']}]" if s["caption"] else ""))
    print(f"total {o['total']:.2f}s ({int(o['total'] // 60)}:{o['total'] % 60:04.1f})")
    if args.plan:
        return
    assets = Assets(work, args.v)
    for s in segs:
        render_seg(s, o, assets, work, args)
    assemble(o, segs, work, args)
    summary(o["output"], o["total"])
    (work / "commands.log").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
