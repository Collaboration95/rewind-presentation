#!/usr/bin/env python3
"""Real footage/stills -> framed 1080p30 H.264 High + AAC. See README.md."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
W, H, FPS = 1920, 1080, 30
X, Y, SW, SH = 740, 60, 440, 957
CREAM = '#f6efe5'
FONT = '/System/Library/Fonts/Supplemental/Arial.ttf'
BOLD = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
VERSION = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def run(args):
    p = subprocess.run([str(a) for a in args], capture_output=True, text=True, shell=False)
    if p.returncode:
        raise ValueError(f'{args[0]} failed:\n{p.stderr[-4000:]}')
    return p.stdout


def inside(path):
    p = Path(path).expanduser().resolve()
    if not p.is_relative_to(ROOT):
        raise ValueError(f'All generated files must stay under {ROOT}: {p}')
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def probe(path):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', path]))


def fingerprint(path):
    p = Path(path)
    s = p.stat()
    return [str(p.resolve()), s.st_size, s.st_mtime_ns]


def key(value):
    return hashlib.sha256(json.dumps([VERSION, value], sort_keys=True).encode()).hexdigest()[:20]


def seconds(value):
    f = float(value)
    if not math.isfinite(f) or f < 0:
        raise ValueError('Times must be finite nonnegative seconds')
    return f


def frames(value):
    f = seconds(value) * FPS
    n = round(f)
    if n < 1 or abs(n - f) > 0.00001:
        raise ValueError(f'Duration {value} must be positive and an exact multiple of 1/30 second')
    return n


def source_path(value):
    p = Path(value).expanduser()
    if not p.is_absolute() or not p.is_file():
        raise ValueError(f'Input must be an existing absolute file path: {value}')
    return p.resolve()


def image_asset(cache, label, signature, args):
    p = inside(cache / f'{label}-{key(signature)}.png')
    if not p.exists():
        run(['magick', *args, f'PNG32:{p}'])
    return p


def assets(cache, name, number, island=False, title=False):
    # Orange glow is a soft ImageMagick ellipse on a cream canvas.
    base = ['-size', f'{W}x{H}', f'xc:{CREAM}', '(', '-size', f'{W}x{H}', 'xc:none',
            '-fill', '#f3b27335', '-draw', 'ellipse 960,560 420,460 0,360', '-blur', '0x110', ')', '-composite']
    if title:
        args = base + ['-fill', '#ce7946', '-draw', 'rectangle 80,480 124,483',
                       '-font', BOLD, '-pointsize', '38', '-fill', '#342b25',
                       '-gravity', 'NorthWest', '-annotate', '+80+535', f'{number:02d}  {name}']
    else:
        args = base + ['-alpha', 'set', '(', '-size', f'{W}x{H}', 'xc:none', '-fill', '#00000035',
                       '-draw', 'roundrectangle 730,55 1190,1038 71,71', '-blur', '0x13', ')', '-composite',
                       '-fill', '#111110', '-stroke', '#49433e', '-strokewidth', '2', '-draw',
                       'roundrectangle 728,48 1191,1028 71,71', '-stroke', 'none',
                       '(', '-size', f'{W}x{H}', 'xc:none', '-fill', 'white', '-draw',
                       f'roundrectangle {X},{Y} {X+SW-1},{Y+SH-1} 60,60', ')',
                       '-compose', 'DstOut', '-composite', '-compose', 'Over',
                       '-font', FONT, '-pointsize', '28', '-fill', '#5b4c40', '-gravity', 'NorthWest',
                       '-annotate', '+80+80', f'{number:02d}  {name}']
        if island:
            args += ['-fill', 'black', '-draw', 'roundrectangle 891,75 1028,114 20,20']
    return image_asset(cache, 'title' if title else 'frame', [name, number, island, title], args)


def normalize(row, spec):
    if row.get('type') == 'title':
        if float(row.get('duration', 1)) != 1:
            raise ValueError('Assembly title cards are exactly one second')
        return {'type': 'title', 'frames': 30, 'duration': 1.0}
    src = source_path(row['source'])
    info = probe(src)
    v = next(s for s in info['streams'] if s['codec_type'] == 'video')
    still = src.suffix.lower() == '.png'
    a = seconds(row.get('in', 0))
    b = seconds(row['out']) if 'out' in row else None
    if b is not None and b <= a:
        raise ValueError('out must be greater than in')
    if still and a:
        raise ValueError('PNG in must be zero')
    duration = row.get('duration', b - a if b is not None else None)
    if duration is None:
        raise ValueError('Each segment needs duration, or in/out')
    n = frames(duration)
    source_duration = float(info.get('format', {}).get('duration', 0))
    if not still and a >= source_duration:
        raise ValueError('in is beyond encoded video duration; sparse simulator time is not wall-clock time. Use a PNG hold.')
    crop = row.get('crop')
    if crop:
        if len(crop) != 4 or any(type(z) is not int for z in crop):
            raise ValueError('crop must be integer [x,y,width,height] in source pixels')
        x, y, w, h = crop
        if min(x, y) < 0 or min(w, h) < 1 or x+w > v['width'] or y+h > v['height']:
            raise ValueError('crop is outside the source')
    masks = row.get('mask', [])
    for mask in masks:
        x, y, w, h = [mask[z] for z in ('x', 'y', 'width', 'height')]
        if any(type(z) is not int for z in (x,y,w,h)) or min(x,y) < 0 or min(w,h) < 1 or x+w > v['width'] or y+h > v['height']:
            raise ValueError('mask rectangle must be integer source pixels inside source')
        if ('color' in mask) == ('sample' in mask):
            raise ValueError('mask needs exactly one of color or sample')
    audio = row.get('audio', True)
    afile = None
    audio_in = 0
    gain = 1
    if isinstance(audio, (str, dict)):
        obj = {'source': audio} if isinstance(audio, str) else audio
        afile = source_path(obj['source'])
        audio_in = seconds(obj.get('in', 0))
        gain = seconds(obj.get('volume', 1))
        if not any(s['codec_type'] == 'audio' for s in probe(afile)['streams']):
            raise ValueError('External audio file has no audio stream')
    elif not isinstance(audio, bool):
        raise ValueError('audio must be true, false, an absolute path, or an audio object')
    signature = {'row': row, 'source': fingerprint(src), 'audio': fingerprint(afile) if afile else None}
    for m in masks:
        if 'sample' in m:
            ref = source_path(m.get('reference', str(src)))
            if ref.suffix.lower() != '.png':
                raise ValueError('Mask sample needs a PNG source or reference PNG')
            signature.setdefault('references', []).append(fingerprint(ref))
    return dict(type='phone', source=str(src), still=still, start=a, end=b, frames=n, duration=n/FPS,
                width=v['width'], height=v['height'], crop=crop, masks=masks, audio_file=str(afile) if afile else None,
                audio_in=audio_in, gain=gain, source_audio=audio is True and any(s['codec_type']=='audio' for s in info['streams']),
                island=bool(row.get('add_island', spec.get('add_island', False))), signature=signature)


def mask_asset(cache, s):
    args = ['-size', f"{s['width']}x{s['height']}", 'xc:none']
    for m in s['masks']:
        color = m.get('color')
        if color is None:
            ref = source_path(m.get('reference', s['source']))
            sx, sy = m['sample']
            iw, ih = map(int, run(['magick', 'identify', '-format', '%w %h', ref]).split())
            if not (type(sx) is int and type(sy) is int and 0 <= sx < iw and 0 <= sy < ih):
                raise ValueError('Mask sample pixel is outside reference')
            color = run(['magick', ref, '-format', f'%[pixel:p{{{sx},{sy}}}]', 'info:']).strip()
        x, y, w, h = [m[z] for z in ('x','y','width','height')]
        args += ['-fill', color, '-draw', f'rectangle {x},{y} {x+w-1},{y+h-1}']
    return image_asset(cache, 'mask', s['signature'], args)


def render_segment(cache, s, spec, crf, preset):
    title = s['type'] == 'title'
    frame = assets(cache, spec['name'], spec['number'], s.get('island', False), title)
    dest = inside(cache / f"segment-{key([s, fingerprint(frame), crf, preset])}.mov")
    if dest.exists():
        print(f'Cache: {dest.name}', flush=True)
        return dest
    dur = f"{s['duration']:.12f}"
    cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-filter_complex_threads', '1']
    if title:
        cmd += ['-loop', '1', '-framerate', '30', '-i', str(frame)]
    elif s['still']:
        cmd += ['-loop', '1', '-framerate', '30', '-i', s['source']]
    else:
        cmd += ['-ss', str(s['start']), '-i', s['source']]
    filters = []
    idx = 1
    if title:
        filters += ['[0:v]scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,setsar=1[v]']
    else:
        current = '0:v'
        if s['masks']:
            cmd += ['-i', str(mask_asset(cache, s))]
            filters += [f'[{current}][{idx}:v]overlay=0:0:format=auto[masked]']
            current = 'masked'
            idx += 1
        ops = ['setpts=PTS-STARTPTS']
        if s['end'] is not None:
            ops += [f"trim=duration={s['end']-s['start']:.12f}"]
        if s['crop']:
            x,y,w,h = s['crop']
            ops += [f'crop={w}:{h}:{x}:{y}:exact=1']
        ops += [f'fps={FPS}', f'tpad=stop_mode=clone:stop_duration={dur}',
                f'trim=end_frame={s["frames"]}', 'format=yuv444p',
                f'scale={SW}:{SH}:force_original_aspect_ratio=decrease:flags=lanczos:out_color_matrix=bt709:out_range=tv',
                'format=yuv444p', f'pad={SW}:{SH}:(ow-iw)/2:(oh-ih)/2:color={CREAM}', 'setsar=1',
                f'pad={W}:{H}:{X}:{Y}:color=black', 'format=yuv420p']
        filters += [f'[{current}]'+','.join(ops)+'[phone]']
        cmd += ['-i', str(frame)]
        filters += [f'[{idx}:v]scale=out_color_matrix=bt709:out_range=tv,format=yuva420p[frame]',
                    '[phone][frame]overlay=0:0:format=yuv420[v]']
        idx += 1
    if not title and s['audio_file']:
        cmd += ['-ss', str(s['audio_in']), '-i', s['audio_file']]
        ab = f'{idx}:a'
        atrim = f'atrim=duration={dur},volume={s["gain"]},'
    elif not title and s['source_audio']:
        ab = '0:a'
        span = s['end']-s['start'] if s['end'] is not None else s['duration']
        atrim = f'atrim=duration={min(span,s["duration"]):.12f},'
    else:
        cmd += ['-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo']
        ab = f'{idx}:a'
        atrim = ''
    filters += [f'[{ab}]{atrim}asetpts=PTS-STARTPTS,aresample=48000,aformat=sample_fmts=s16:channel_layouts=stereo,'
                f'apad,atrim=end_sample={s["frames"]*1600}[a]']
    cmd += ['-filter_complex', ';'.join(filters), '-map', '[v]', '-map', '[a]',
            '-t', dur, '-r', '30', '-c:v', 'libx264', '-preset', preset, '-crf', str(crf),
            '-threads', '2', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709',
            '-color_trc', 'bt709', '-color_range', 'tv', '-c:a', 'pcm_s16le', '-ar', '48000', '-ac', '2',
            '-video_track_timescale', '15360']
    temp = inside(dest.with_suffix('.partial.mov'))
    run(cmd + [str(temp)])
    temp.replace(dest)
    return dest


def validate(path, n):
    info = probe(path)
    v = next(s for s in info['streams'] if s['codec_type']=='video')
    a = next(s for s in info['streams'] if s['codec_type']=='audio')
    expected = n/FPS
    checks = {'codec': v['codec_name']=='h264', 'profile': v['profile']=='High',
              'size': (v['width'],v['height'])==(W,H), 'pixel_format': v['pix_fmt']=='yuv420p',
              'fps': v['avg_frame_rate']=='30/1', 'frame_count': int(v['nb_frames'])==n,
              'video_duration': abs(float(v['duration'])-expected)<0.0001,
              'container_duration': abs(float(info['format']['duration'])-expected)<0.001,
              'audio': a['codec_name']=='aac' and a['sample_rate']=='48000' and a['channels']==2,
              'audio_duration': abs(float(a['duration'])-expected)<0.001}
    result = {'output': str(path), 'frames': n, 'duration': expected, 'checks': checks,
              'streams': info['streams'], 'format': info['format']}
    if not all(checks.values()):
        raise ValueError('Validation failed: '+json.dumps(checks))
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('json_file', type=Path)
    ap.add_argument('--plan', action='store_true', help='validate inputs and print timeline without rendering')
    ap.add_argument('--crf', type=int, default=18)
    ap.add_argument('--preset', default='fast', choices=['ultrafast','superfast','veryfast','faster','fast','medium','slow'])
    args = ap.parse_args()
    for tool in ('ffmpeg','ffprobe','magick'):
        if not shutil.which(tool):
            raise ValueError(f'Missing dependency: {tool}')
    if not 0 <= args.crf <= 51:
        raise ValueError('crf must be 0..51')
    spec = json.loads(args.json_file.read_text())
    if type(spec['number']) is not int or spec['number'] < 0:
        raise ValueError('number must be a nonnegative integer')
    if not isinstance(spec['name'], str) or not spec['name'].strip() or len(spec['name'])>40 or '\n' in spec['name']:
        raise ValueError('name must be one line, 1..40 characters')
    out = inside(ROOT / spec['output'])
    if out.suffix.lower() != '.mp4' or out.exists():
        raise ValueError('output must be a new .mp4 under edit/; existing outputs are never overwritten')
    segments = ([{'type':'title'}] if spec.get('title_card', False) else []) + spec['segments']
    if not segments:
        raise ValueError('segments must not be empty')
    segs = [normalize(s, spec) for s in segments]
    n = sum(s['frames'] for s in segs)
    plan = {'output':str(out), 'frames':n, 'duration':n/FPS, 'segments':segs}
    if args.plan:
        print(json.dumps(plan, indent=2))
        return
    cache = inside(ROOT / '.cache' / 'placeholder').parent
    clips = []
    for i,s in enumerate(segs):
        print(f'Rendering {i+1}/{len(segs)} ({s["duration"]:g}s)', flush=True)
        clips.append(render_segment(cache, s, spec, args.crf, args.preset))
    # Only generated hashed paths appear in this manifest. It is parsed by FFmpeg, never a shell.
    manifest = inside(cache / f'join-{key([str(p) for p in clips])}.txt')
    def quote(p):
        return str(p).replace("'", "'\\''")
    manifest.write_text(''.join(f"file '{quote(p)}'\n" for p in clips))
    temporary = inside(out.with_suffix('.partial.mp4'))
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(manifest),
         '-map','0:v:0','-map','0:a:0','-c:v','copy','-c:a','aac','-b:a','160k','-ar','48000','-ac','2',
         '-af',f'atrim=end_sample={n*1600},asetpts=PTS-STARTPTS','-t',f'{n/FPS:.12f}',
         '-movflags','+faststart','-video_track_timescale','15360',str(temporary)])
    result = validate(temporary, n)
    temporary.replace(out)
    result['output'] = str(out)
    inside(out.with_suffix('.validation.json')).write_text(json.dumps(result, indent=2))
    inside(out.with_suffix('.plan.json')).write_text(json.dumps(plan, indent=2))
    print(json.dumps({'output':str(out),'frames':n,'duration':n/FPS,'checks':result['checks']}, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, StopIteration, OSError) as e:
        sys.exit(f'Error: {e}')
