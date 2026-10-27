#!/bin/zsh
# Standalone ffmpeg/ImageMagick templates behind render.py. Every block below was run on the synthetic clips in in/.
# Run all:  ./templates.sh        Run one: ./templates.sh t3
# NOTE: stock Homebrew ffmpeg 9.0.2 has no drawtext/subtitles/libass, so all text is a transparent PNG made with
# ImageMagick and laid on with `overlay`. Outputs go to out/tpl/, scratch to work/tpl/.
set -e
cd "${0:A:h}"; mkdir -p out/tpl work/tpl
FB="/System/Library/Fonts/Supplemental/Arial Bold.ttf"; FR="/System/Library/Fonts/Supplemental/Arial.ttf"; FM="/System/Library/Fonts/Supplemental/Andale Mono.ttf"
TAGS=(-colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv)
ENC=(-c:v libx264 -preset medium -crf 18 -profile:v high -pix_fmt yuv420p -r 30 $TAGS)
AENC=(-c:a aac -b:a 160k -ar 48000 -ac 2)   # every segment must share audio params or the lossless concat breaks
FIT='scale=1920:1080:force_original_aspect_ratio=decrease:flags=lanczos:out_color_matrix=bt709,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0x0f172a,setsar=1,format=yuv420p'
MAT='scale=out_color_matrix=bt709:out_range=tv,format=yuva420p'   # RGB overlay PNG -> BT.709 YUV+alpha (keeps colours right)
STAMP="27 Oct 2026 · hosted dev · abc1234"
chk() { for f in "$@"; do echo "  $(ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,pix_fmt,sample_rate,channels:format=duration -of csv=p=0 "$f" | tr '\n' ' ')  <- $f"; done; }

# pill TEXT FG BG FONT PT OUT : rounded translucent label as a tight RGBA PNG
pill() { magick -background none -fill "$2" -font "$4" -pointsize $5 -size 1560x -gravity center caption:"$1" -trim +repage work/tpl/_t.png
  local w=$(( $(magick identify -format %w work/tpl/_t.png) + 60 )) h=$(( $(magick identify -format %h work/tpl/_t.png) + 32 ))
  magick -size ${w}x${h} xc:none -fill "$3" -draw "roundrectangle 0,0 $((w-1)),$((h-1)) 22,22" work/tpl/_t.png -gravity center -composite PNG32:"$6"; }

t1() { echo "T1 normalise any input -> 1920x1080 H.264 30 fps yuv420p + AAC 48k stereo (letterbox, silent track added when the source has none)"
  for pair in "iphone-portrait-hevc.mov:t1-iphone" "mac-retina.mov:t1-retina" "sim-iphone17pro.mov:t1-sim" "pw/*.webm:t1-playwright" "desktop-wait-50s.mp4:t1-desktop"; do
    in=(in/${~pair%%:*}); out=out/tpl/${pair##*:}.mp4
    if [[ -n $(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 $in[1]) ]]; then
      ffmpeg -y -loglevel error -i $in[1] -vf "fps=30,$FIT" -af "aresample=48000,aformat=channel_layouts=stereo" $ENC $AENC -movflags +faststart $out
    else
      ffmpeg -y -loglevel error -i $in[1] -f lavfi -i anullsrc=r=48000:cl=stereo -shortest -vf "fps=30,$FIT" $ENC $AENC -movflags +faststart $out
    fi; chk $out; done; }

t2() { echo "T2 phone in a centred phone frame; phone + desktop side by side (frames come from render.py's Assets: bezel PNG with transparent rounded holes)"
  read PF SF <<<$(python3 -c "
import sys; sys.path.insert(0,'.'); import render, pathlib
a=render.Assets(pathlib.Path('work'),False); print(a.frame('phone','#0f172a'), a.frame('sbs','#0f172a'))")
  ffmpeg -y -loglevel error -i in/iphone-portrait-hevc.mov -i $PF -filter_complex \
   "[0:v]fps=30,scale=388:840:force_original_aspect_ratio=decrease:flags=lanczos:out_color_matrix=bt709,pad=388:840:(ow-iw)/2:(oh-ih)/2:color=black,pad=1920:1080:766:30:color=black,setsar=1,format=yuv420p[b];[1:v]${MAT}[fr];[b][fr]overlay=0:0:format=yuv420[v]" \
   -map '[v]' -map 0:a $ENC $AENC -t 6 out/tpl/t2-phone.mp4; chk out/tpl/t2-phone.mp4
  ffmpeg -y -loglevel error -i in/iphone-portrait-hevc.mov -i in/mac-retina.mov -i $SF -filter_complex \
   "[0:v]fps=30,scale=352:760:force_original_aspect_ratio=decrease:flags=lanczos:out_color_matrix=bt709,setsar=1,format=yuv420p[p];[1:v]fps=30,scale=1180:664:force_original_aspect_ratio=decrease:flags=lanczos:out_color_matrix=bt709,pad=1180:664:(ow-iw)/2:(oh-ih)/2:color=black,pad=1920:1080:148:148:color=black,setsar=1,format=yuv420p[d];[d][p]overlay=1406:100:format=yuv420[dp];[2:v]${MAT}[fr];[dp][fr]overlay=0:0:format=yuv420[v]" \
   -map '[v]' -map 0:a $ENC $AENC -t 6 out/tpl/t2-sbs.mp4; chk out/tpl/t2-sbs.mp4; }

t3() { echo "T3 wait segment x8 with burned caption 'wait trimmed: actual 41 s' (10 s..51 s of the source -> 5.1 s)"
  pill "wait trimmed: actual 41 s" "#111827" "#fbbf24f2" "$FB" 44 work/tpl/wait.png
  magick -size 1920x1080 xc:none -gravity northwest work/tpl/wait.png -geometry +$(( (1920-$(magick identify -format %w work/tpl/wait.png))/2 ))+928 -composite PNG32:work/tpl/wait-canvas.png
  ffmpeg -y -loglevel error -ss 10 -t 40 -i in/desktop-wait-50s.mp4 -i work/tpl/wait-canvas.png -filter_complex \
   "[0:v]setpts=(PTS-STARTPTS)/8,fps=30,${FIT}[v0];[1:v]${MAT}[c];[v0][c]overlay=0:0:format=yuv420,format=yuv420p[v]" \
   -map '[v]' -an $ENC -t 5 out/tpl/t3-wait8x.mp4; chk out/tpl/t3-wait8x.mp4; }

t4() { echo "T4 lower-third captions from an .srt (one PNG per cue + transparent gaps, fed through the concat demuxer: ONE overlay for any number of cues)"
  magick -size 1920x1080 xc:none PNG32:work/tpl/blank.png
  : > work/tpl/caps.txt; echo "ffconcat version 1.0" > work/tpl/caps.txt; prev=0; n=0
  while IFS='|' read -r a b text; do n=$((n+1)); pill "$text" white "#0b1220e0" "$FB" 44 work/tpl/cue$n.png
    magick -size 1920x1080 xc:none -gravity northwest work/tpl/cue$n.png -geometry +$(( (1920-$(magick identify -format %w work/tpl/cue$n.png))/2 ))+920 -composite PNG32:work/tpl/cv$n.png
    printf "file '%s'\nduration %.3f\nfile '%s'\nduration %.3f\n" "$PWD/work/tpl/blank.png" $((a-prev)) "$PWD/work/tpl/cv$n.png" $((b-a)) >> work/tpl/caps.txt; prev=$b
  done <<'CUES'
1.0|3.5|Step 1: open the pull request
5.0|8.0|Checks run automatically
CUES
  printf "file '%s'\nduration 3\nfile '%s'\n" "$PWD/work/tpl/blank.png" "$PWD/work/tpl/blank.png" >> work/tpl/caps.txt
  ffmpeg -y -loglevel error -t 10 -i in/desktop-wait-50s.mp4 -f concat -safe 0 -i work/tpl/caps.txt -filter_complex \
   "[0:v]fps=30,${FIT}[v0];[1:v]${MAT}[c];[v0][c]overlay=0:0:format=yuv420,format=yuv420p[v]" -map '[v]' -map 0:a $ENC $AENC -t 10 out/tpl/t4-srt.mp4; chk out/tpl/t4-srt.mp4; }

t5() { echo "T5 persistent corner stamp (bottom-right): '$STAMP'"
  pill "$STAMP" "#e2e8f0" "#000000b8" "$FM" 28 work/tpl/stamp.png
  ffmpeg -y -loglevel error -t 5 -i in/desktop-wait-50s.mp4 -i work/tpl/stamp.png -filter_complex \
   "[0:v]fps=30,${FIT}[v0];[1:v]${MAT}[s];[v0][s]overlay=W-w-24:H-h-18:format=yuv420,format=yuv420p[v]" -map '[v]' -map 0:a $ENC $AENC out/tpl/t5-stamp.mp4; chk out/tpl/t5-stamp.mp4; }

t6() { echo "T6 3-second title card with a section name (fades in/out, silent audio)"
  magick -size 1920x1080 xc:'#0f172a' -fill '#2563eb' -draw 'rectangle 160,470 260,478' -gravity northwest \
    -font "$FB" -fill '#93c5fd' -pointsize 38 -annotate +160+250 "Part 2" -fill white -pointsize 84 -annotate +160+330 "System demo" \
    -font "$FR" -fill '#cbd5e1' -pointsize 44 -annotate +160+520 "iPhone PWA, camera and push" work/tpl/card.png
  ffmpeg -y -loglevel error -loop 1 -framerate 30 -t 3 -i work/tpl/card.png -f lavfi -t 3 -i anullsrc=r=48000:cl=stereo \
   -vf "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,fade=t=in:d=0.4,fade=t=out:st=2.6:d=0.4" $ENC $AENC out/tpl/t6-title.mp4; chk out/tpl/t6-title.mp4; }

t7() { echo "T7 concatenate normalised segments without re-encoding (title + stamp clip + phone clip; all must share codec/size/fps/audio params)"
  printf "file '%s'\n" $PWD/out/tpl/t6-title.mp4 $PWD/out/tpl/t5-stamp.mp4 $PWD/out/tpl/t2-phone.mp4 > work/tpl/list.txt
  ffmpeg -y -loglevel error -f concat -safe 0 -i work/tpl/list.txt -c copy -movflags +faststart out/tpl/t7-concat.mp4; chk out/tpl/t7-concat.mp4
  echo "  sum of parts: $(for f in $(sed "s/file '//;s/'//" work/tpl/list.txt); do ffprobe -v error -show_entries format=duration -of csv=p=0 $f; done | paste -sd+ - | bc)"; }

t8() { echo "T8 voice-over over ducked app audio (say draft voice; bed = 330 Hz tone from the desktop clip)"
  [[ -f vo/intro.aiff ]] || { mkdir -p vo; say -v Samantha -r 170 -o vo/intro.aiff "This is a draft narration track for the pipeline demo."; }
  ffmpeg -y -loglevel error -t 12 -i in/desktop-wait-50s.mp4 -i vo/intro.aiff -filter_complex \
   "[1:a]aresample=48000,aformat=channel_layouts=stereo,adelay=2000:all=1,apad,asplit=2[vk][vm];[0:a]aresample=48000,aformat=channel_layouts=stereo[bed];[bed][vk]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=400:makeup=1[duck];[duck][vm]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-16:TP=-1.5:LRA=11[a]" \
   -map 0:v -map '[a]' -c:v copy -c:a aac -b:a 192k -ar 48000 -ac 2 -t 12 out/tpl/t8-vo.mp4; chk out/tpl/t8-vo.mp4; }

if [[ $# -gt 0 ]]; then "$@"; else for t in t1 t2 t3 t4 t5 t6 t8 t7; do $t; done; fi
