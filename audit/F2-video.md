# F2 · Video production pipeline (tested 26 Oct 2026, ~22:00 SGT)

Toolkit: `/tmp/rewind-video/` (`render.py`, `templates.sh`, `example.yaml`, synthetic inputs in `in/`, outputs in `out/`). Nothing in any repo was touched. Nothing was installed. One throwaway simulator (`rewind-video-tmp`) was created, recorded and deleted. /tmp is volatile: copy `render.py`, `templates.sh`, `example.yaml` somewhere durable (not the repo) before you rely on them.

## 0. Verdict

- A working pipeline exists. Edit list in, 1920x1080 30 fps H.264/AAC out, with corner stamp, captions, wait-trimmed badge, title cards, phone frame and side-by-side layouts, SRT/ASS captions and optional ducked voice-over.
- **Stock ffmpeg here cannot burn text** (no `drawtext`, `subtitles`, `ass`: built without libfreetype/libass). Workaround, tested: render text to transparent PNGs with ImageMagick (already installed) and `overlay` them. Same technique the dc2 `edit.sh` used for title cards.
- Measured: a 42-50 s mixed example renders cold in 21 s. A 11:55 video of 25 segments with 57 caption cues renders cold in 3 min 32 s. Editing one row and re-rendering takes 75 s (segments are cached by content hash).
- Untested: real `screencapture`/QuickTime/OBS capture (needs a Screen Recording permission prompt I did not want to trigger) and real iPhone footage. Section 5 says how to test each in 10 s.

## 1. Tool inventory

| Tool | State | Note |
|---|---|---|
| ffmpeg/ffprobe 9.0.2 (`/opt/homebrew/bin`) | OK, **no drawtext/subtitles/ass/freetype/libass** | Has libx264/x265, `h264_/hevc_videotoolbox`, `aac`, `overlay`, `xfade`, `sidechaincompress`, `loudnorm`, `atempo`, `concat` |
| ffmpeg@6 (brew) and the old Cellar ffmpeg 8.1.2 | **Both broken** | dyld error: `libx265.216.dylib` missing. Do not use. Only 9.0.2 runs, so avoid `brew upgrade/uninstall` tonight |
| ImageMagick 7.1.2 (`magick`), librsvg | OK, freetype delegate | Renders all text/frames. Fonts: `/System/Library/Fonts/Supplemental/Arial.ttf`, `Arial Bold.ttf`, `Andale Mono.ttf` (stamp). Arial Bold has no check mark glyph (renders blank) |
| `screencapture` | Present (macOS 26.6.2) | `-v -R x,y,w,h -V secs -k -C -g` all exist. **Not run** |
| QuickTime Player, Screenshot, Photos, Image Capture, Voice Memos | Present | |
| OBS 30.1.2, Loom, KeyCastr 0.10.5, VLC | Installed | OBS = fallback for a fixed 1080p scene. KeyCastr shows keystrokes |
| Xcode 27.1, `xcrun simctl` | OK | iOS 26.5 only. Sims: iPhone 17 Pro/Pro Max/17/17e/Air, iPad set, plus project ones (`Rewind527-PWA-20261019`, `Rewind 308 disposable`). None booted at start |
| Playwright 1.63.0 (in `rewind-present-audit`) | OK | Tested: `recordVideo` gives **VP8 .webm, 25 fps**, 1920x1080. Lowest quality source. Prefer real screen capture |
| whisper | **Broken** | `/opt/homebrew/bin/whisper` shebang points at deleted python3.10. `pip install openai-whisper` fails on Python 3.14 (no numba/tiktoken). Model `large-v3.pt` (3 GB) is cached in `~/.cache/whisper` |
| `say` | OK | en_GB Daniel/Eddy/Flo/Reed, en_AU Karen, en_IN Rishi/Aman, en_US Samantha/Albert/Fred. Draft VO only |
| Python 3.14 + PyYAML, numpy, torch 2.11 | OK | `render.py` needs only PyYAML (or use CSV/JSON) |
| Displays | Main = **3440x1440 at 1x** (UWQHD), built-in = 3024x1964 Retina | A full-screen grab is 21:9. Record a 16:9 region |
| Mics | MacBook Pro Microphone, AirPods Pro 3, `test Microphone`; screens 0 and 1 listed by avfoundation | iPhone only appears once plugged in and trusted |

**Auto-captions: skipped.** If wanted: `brew install whisper-cpp` plus a `base.en` ggml model (~150 MB) is the light route (not done). For tonight, captions from the script (row `caption:` or an SRT) cost less than fixing whisper.

## 2. What the owner's dc2 project did, and what differs here

- dc2 `site/clips/D1-D5.mp4`: 1920x1080, H.264 High, yuv420p, 30 fps, **no audio**, 24-78 s, 0.12-0.5 Mbit/s (terminal text compresses well). PRESENTING.md says "the clips have no sound".
- Embedded per slide as `<div class="clip" data-clip="clips/D1.mp4"><video playsinline preload="none">` in an 860x484 box: click or `P` to play, no autoplay. Zoom share: "Share sound" + "Optimize for video clip", QuickTime window as fallback.
- Tooling lived in `~/dc2-demo-private/tools/`: `edit.sh` (ImageMagick title card, per-clip normalise to 1080p30, `xfade` 0.4 s joins, fade out), `rec.py` (Playwright JPEG frames, yellow cursor ring, `pause()` cuts waits), `iterm_rec.py`. No drawtext used.
- STYLE.md §6 asks for a corner stamp, burned wait captions and VO; in practice the stamp was only a footer on the title card. This toolkit burns the stamp on every segment and supports VO. It joins with hard cuts (lossless), with fades only at title cards.

## 3. Tested ffmpeg templates (all in `templates.sh`; run `./templates.sh` or `./templates.sh t3`)

Common: `FIT='scale=1920:1080:force_original_aspect_ratio=decrease:flags=lanczos:out_color_matrix=bt709,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0x0f172a,setsar=1,format=yuv420p'`,
`ENC=(-c:v libx264 -preset medium -crf 18 -profile:v high -pix_fmt yuv420p -r 30 -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv)`, `AENC=(-c:a aac -b:a 160k -ar 48000 -ac 2)`, `MAT='scale=out_color_matrix=bt709:out_range=tv,format=yuva420p'` (converts RGB overlay PNGs with the right matrix; checked: title background came out within 1 level of #0f172a).

| # | Template | Result (ffprobe) |
|---|---|---|
| T1 | Normalise any input: `ffmpeg -i IN -vf "fps=30,$FIT" -af "aresample=48000,aformat=channel_layouts=stereo" $ENC $AENC -movflags +faststart OUT.mp4`. No audio in source: add `-f lavfi -i anullsrc=r=48000:cl=stereo -shortest`. | iPhone-style VFR HEVC 1178x2556 (avg 45 fps), Retina 3024x1964, simulator 1206x2622, Playwright webm, 1080p: all give h264 1920x1080 yuv420p 30/1, aac 48000 2ch, source duration kept (the 0.53 s simulator clip became 0.98 s: last frame held) |
| T2 | Phone in frame: `[0:v]fps=30,scale=388:840:...decrease,pad=388:840:(ow-iw)/2:(oh-ih)/2,pad=1920:1080:766:30,format=yuv420p[b];[1:v]$MAT[fr];[b][fr]overlay=0:0:format=yuv420`. Frame PNG = gradient + bezel with transparent rounded hole (made by `render.py` `Assets.frame`). Side by side: desktop 1180x664 at (148,148), phone 352x760 at (1406,100). | 1920x1080, 6.000 s |
| T3 | Wait x8: `-ss 10 -t 40 -i IN -i canvas.png -filter_complex "[0:v]setpts=(PTS-STARTPTS)/8,fps=30,$FIT[v0];[1:v]$MAT[c];[v0][c]overlay=0:0:format=yuv420,format=yuv420p[v]"`. Badge text "wait trimmed: actual 41 s", amber pill. | 5.000 s |
| T4 | Lower thirds from SRT: one PNG per cue plus a transparent gap PNG, fed through `-f concat -safe 0 -i caps.txt` (`file`/`duration` lines), then a **single** `overlay`. Works for any number of cues. | 10.000 s, cues appear and clear on time |
| T5 | Corner stamp: `[1:v]$MAT[s];[v0][s]overlay=W-w-24:H-h-18:format=yuv420`. Pill, Andale Mono 28 pt. | ok |
| T6 | Title card 3 s: `-loop 1 -framerate 30 -t 3 -i card.png -f lavfi -t 3 -i anullsrc... -vf "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,fade=t=in:d=0.4,fade=t=out:st=2.6:d=0.4"` | 3.000 s |
| T7 | Lossless join: `ffmpeg -f concat -safe 0 -i list.txt -c copy -movflags +faststart OUT.mp4` | 420 video frames = exact sum. Audio 14.021 s (one AAC frame longer). 12 AAC joins drift only 21 ms on ffmpeg 9 |
| T8 | VO over ducked app audio: `[vo]aresample=48000,aformat=channel_layouts=stereo,adelay=2000:all=1,apad,asplit=2[vk][vm];[bed][vk]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=400:makeup=1[duck];[duck][vm]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-16:TP=-1.5:LRA=11` then `-ar 48000 -ac 2` | Measured on a 660 Hz bed tone: -24.3 dB before VO, -32.9 dB during, -24.1 dB after |

## 4. `render.py`: the reusable renderer

```
python3 /tmp/rewind-video/render.py EDIT.yaml [-o out.mp4] [--stamp "27 Oct 2026 · hosted dev · $(git rev-parse --short origin/dev)"]
        [--srt cues.srt] [--crf 23] [--plan] [--draft] [-v]
```
- `--plan` prints the timeline (start/end/length per row) without rendering. Use it to write SRT cue times against the **final** timeline.
- Edit list: YAML (above), CSV (`source,in,out,speed,caption,layout,source2,in2,vo,stamp,crop`; title rows use `source = title:Name|subtitle`, `out` = seconds), or JSON. Paths resolve relative to the list.
- Row keys: `source in out speed caption layout(fit|fill|phone|sbs) source2 in2 crop("x:y:w:h" source px) audio vo vo_delay stamp`. Title row: `title sub kicker dur`. `out` blank = end of file. Times: `12.5`, `1:05`, `1:02:03`. Caption placeholders `{actual}` (out minus in, e.g. "41 s") and `{speed}`. A caption on a sped-up row becomes the amber badge.
- Top level: `output stamp stamp_pos(br|bl|tr|tl) bg srt loudnorm voiceover:[{file,at}]`. Per-row `stamp:` overrides (use for a clip filmed at another commit).
- Example row set (tested, all of it, in `example.yaml`):
  `- {title: "CI/CD pipeline", kicker: "Part 1", sub: "Pull request to hosted dev", dur: 3, vo: vo/intro.aiff}`
  `- {source: in/desktop.mp4, in: 10, out: 51, speed: 8, caption: "wait trimmed: actual {actual}"}`
  `- {source: in/iphone.mov, layout: sbs, source2: in/desktop.mp4, in: 6, out: 11, in2: 2, caption: "Phone and desktop"}`
- Design: each row becomes one H.264 + PCM `.mov` segment (stamp and captions already burned in, constant 1080p30, BT.709-tagged), the joins are `-c copy`, and AAC is encoded once at the end together with any voice-over. Speeds outside 0.5-2x drop source audio (silence). A row running past the end of its file holds the last frame (warns).
- Output verified every run: size, fps, pix_fmt, codec, video frames vs audio vs plan. Example: 1504 frames = 50.133 s planned, audio 50.110 s (AAC granularity).

Gotchas found while testing (all fixed or documented):
1. Simulator video is **sparse**: a 6 s recording of a still screen is 0.53 s long (frames only on change). Keep something moving, or rely on the hold-last-frame.
2. `sidechaincompress` ends when the narration ends: the VO bus needs `apad` (fixed: audio was 28 s of 42 s before).
3. Every segment needs identical audio params (48 kHz stereo) or `-c copy` joins misbehave. T2 initially left 44.1 kHz mono, which would have broken T7.
4. In zsh, `$MAT[fr]` is an array subscript: write `${MAT}[fr]` in filter graphs.
5. Phone layout: keep to **one caption line**; two stacked lines overlap the bottom bezel. Side-by-side has room for two.
6. Avoid check marks and emoji in captions (blank glyph). `→` and `·` render fine. Braces, `%` and a leading `@` render literally.
7. Text is baked in: a typo costs a ~10 s re-render of that segment only. Any edit to `render.py` itself invalidates the whole cache.
8. Synthetic test sources are high-entropy (testsrc2): the 12-min test came out at 849 MB. Real screen captures will be far smaller. Expect a few Mbit/s for GitHub pages [inferred]; use `--crf 23` if a size limit applies.

## 5. Capture method per shot type

**GitHub UI in a desktop browser** (CI/CD video)
- Window: the main display is 1x, so a Chrome window of 1920x1080 points is exactly 1920x1080 px, no scaling. Size it: `osascript -e 'tell application "Google Chrome" to set bounds of front window to {0, 40, 1920, 1120}'` (left, top, right, bottom; adjust top if the menu bar clips).
- Record that region, cursor and clicks included: `screencapture -v -k -C -R0,40,1920,1080 -V 900 -x ~/Desktop/ci-01.mov` (`-V` = max seconds; Ctrl-C stops). **Run a 5 s test first** and `ffprobe` it for 1920x1080: the first run asks for Screen Recording permission for your terminal. Alternative: QuickTime, File > New Screen Recording, drag a 16:9 region. OBS: a 1920x1080 scene with Window Capture is the zero-thinking option.
- Legibility: browser zoom 125% for PR pages, 150% for logs and YAML (a 1080p frame at 100% leaves GitHub's 14 px text hard to read once shared over Zoom). Keep the URL bar visible: run IDs in the URL are evidence.
- Clean profile: new Chrome profile or Guest, no extensions, hide the bookmarks bar (Shift-Cmd-B), signed in to GitHub beforehand, tabs pre-opened in the order you will show them, light theme throughout.
- Record in shots of 1-5 min, not one 40 min take. Record each long wait as its own shot and note the real length (the badge reads it from in/out, so use accurate cut points).
- Cursor: System Settings > Accessibility > Display > Pointer: larger size and a coloured outline. Move slowly and pause on each thing you talk about. `-k` / QuickTime "Show Mouse Clicks" draws click rings. KeyCastr only if you type on screen.

**iPhone screen recording** (system demo: PWA, camera, push)
- Control Centre > Screen Recording (add it in Settings > Control Centre if absent). Long-press for Microphone on or off (off if the VO is added later). Output is portrait ~1179x2556, **variable frame rate**, in Photos. The pipeline normalises it (T1 test used exactly this shape).
- Transfer: AirDrop the originals to the Mac (Photos > Share > AirDrop sends unmodified files), or Image Capture over USB. **Not** WhatsApp, iMessage or Telegram (they recompress). Do not trim on the phone.
- Before recording: Focus mode that silences everything except the Rewind PWA (so the push banner shows and nothing else leaks), Low Power Mode off, battery high, Wi-Fi on, portrait lock on, brightness up, clean Home Screen.
- Unknown until tried on the device, so test each for 10 s: whether the camera viewfinder appears in a screen recording, and whether a lock-screen notification is captured (QuickTime > New Movie Recording with the phone as camera source is the fallback for the second). iOS has no touch indicator: slow taps plus a caption.
- Use `layout: phone` for a single phone shot and `layout: sbs` when the desktop shows the other side.

**Simulator** (fallback only; cannot do camera or real push)
- `xcrun simctl io booted recordVideo --codec=h264 --force out.mov`, stop with `kill -INT` (not -9) so it finalises. Tested here: boot 33 s from cold, output 1206x2622 H.264, BT.709. See gotcha 1 (sparse frames). Screenshot: `xcrun simctl io booted screenshot x.png`.

**Voice-over**: record after the visuals are locked, one file per section, then `vo:` on each row (placed at the row start plus `vo_delay`). QuickTime > New Audio Recording or Voice Memos, quiet room, AirPods Pro 3 or the MacBook mic. `say -v Samantha -o a.aiff "..."` makes a placeholder track for timing.

**Recording tips**: macOS Focus on; quit Teams, Discord, Telegram, WhatsApp, Zoom (all installed); turn off Chrome and Mac notification banners; plug in power; hide the Dock; no Wi-Fi switching; stamp SHA must be the deployed one: read the hosted dev footer `dev-<sha>` (F1 audit says `f6cd896` tonight) and use `--stamp "27 Oct 2026 · hosted dev · f6cd896"`. Note D-cicd-demo.md section 0: a **new PR is red tonight** (npm audit, ffmpeg pin), so staging a green PR-to-dev run needs a fix PR first.

## 6. Realistic time tonight

| Step | CI/CD video (10-12 min) | System demo (12-15 min) |
|---|---|---|
| Prep (profile, tabs, phone Focus, stamp SHA, rehearse) | 20 min | 20 min (plus the short-cycle setup in F1, separate) |
| Capture | 25-40 min: a live PR-to-dev loop is 11-12 min of machine time (D audit), allow 2 takes. Waits are what the x8 badge is for | 45-75 min: 3-4 takes of 10-15 min, plus 10 min AirDrop and checks |
| Edit list: watch raw at 2x, write rows and SRT | 30 min | 40 min |
| Render and review (cold 12-min render about 3.5 min, re-render about 1 min) | 2 passes, 25 min | 2 passes, 30 min |
| VO: record and slot in | 30 min, or narrate live and skip | 30 min |
| **Total** | **about 2.5-3 h** | **about 3-4 h** |

One person doing both: 6-7 h. Split between two people: about 3-4 h each in parallel (copy the toolkit folder to both Macs; it only needs ffmpeg, ImageMagick, Python with PyYAML).
**15-minute fallback if time runs out**: one raw recording, `render.py` with a title row plus one clip row and `--stamp`. Output is still dated, stamped and 1080p30. Checks after any render: `ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate:format=duration -of default=nw=1 out.mp4`; the script already prints frames, audio length and plan. Play the whole file once at 2x before it goes in the deck. For the deck, use the dc2 `.clip` pattern; the file is `+faststart`, H.264 High, AAC 48 kHz.
