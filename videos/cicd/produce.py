#!/usr/bin/env python3
"""Animate captured evidence frames, then assemble with the shared video toolkit."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,subprocess,sys,importlib.util
ROOT=Path(__file__).resolve().parent
TOOLKIT=ROOT.parents[1]/'video-toolkit'/'render.py'
spec=importlib.util.spec_from_file_location('video_toolkit',TOOLKIT)
kit=importlib.util.module_from_spec(spec);spec.loader.exec_module(kit)
ASSETS=kit.Assets(ROOT/'work'/'assets',False)

def sh(cmd):
    p=subprocess.run([str(x) for x in cmd],text=True,capture_output=True)
    if p.returncode:raise RuntimeError(p.stderr[-3000:])
    return p.stdout

def make_pointer():
    p=ROOT/'motion'/'pointer.png'
    if not p.exists():
        svg=ROOT/'motion'/'pointer.svg'
        svg.write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96"><circle cx="42" cy="42" r="29" fill="#facc15" fill-opacity=".16" stroke="#eab308" stroke-width="4"/><path d="M40 30 L40 66 L49 56 L57 72 L65 68 L57 52 L70 52 Z" fill="#14202b" stroke="white" stroke-width="2.5" stroke-linejoin="round"/></svg>''')
        sh(['magick','-background','none',svg,'PNG32:'+str(p)])
    return p

def motion(s):
    frame=ROOT/s['frame'];dur=s['duration'];n=round(dur*30)
    digest=hashlib.sha256((json.dumps(s,sort_keys=True)+str(frame.stat().st_mtime_ns)).encode()).hexdigest()[:10]
    out=ROOT/'motion'/f"{s['id']}-{digest}.mp4"
    if out.exists():return out
    label,w,h=ASSETS.pill(s['section'],'stamp',900)
    x,y=s.get('focus',[1450,600]);x=max(90,min(1810,x));y=max(140,min(930,y));amp=s.get('motion',0.022)
    anchor=s.get('anchor',[0.5,0.5])
    vf=f"[0:v]scale=3840:2160,zoompan=z='1.008+{amp}*on/{n-1}':x='(iw-iw/zoom)*{anchor[0]}':y='(ih-ih/zoom)*{anchor[1]}':d={n}:s=1920x1080:fps=30,format=yuv420p[v];[v][1:v]overlay=x=W-w-24:y=18[title];[title][2:v]overlay=x='{x}-42+18*sin(t/5)':y='{y}-42+9*sin(t/7)',setsar=1,format=yuv420p[out]"
    sh(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',frame,'-i',label,'-i',make_pointer(),'-filter_complex_threads','1','-filter_complex',vf,'-map','[out]','-t',dur,'-r','30','-c:v','libx264','-preset','fast','-crf','18','-threads','2','-pix_fmt','yuv420p','-profile:v','high','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-color_range','tv','-movflags','+faststart',out])
    print('motion ready',s['id'],flush=True)
    return out

def main():
    shots=json.loads((ROOT/'shots.json').read_text())
    make_pointer()
    with ThreadPoolExecutor(max_workers=3) as pool:clips=list(pool.map(motion,shots))
    rows=[dict(source=str(p.relative_to(ROOT)),out=s['duration'],audio=False) for p,s in zip(clips,shots)]
    edl={'output':'cicd-demo.mp4','stamp':'Rewind · CI/CD · hosted dev','stamp_pos':'br','loudnorm':False,'clips':rows}
    (ROOT/'edit.json').write_text(json.dumps(edl,indent=2)+'\n')
    at=0;lines=['# CI/CD demonstration shotlist','',f"Total: {sum(s['duration'] for s in shots)//60:.0f}:{sum(s['duration'] for s in shots)%60:02.0f} · 1920×1080 · 30 fps",'', '| Shot | Time | Length | Frame / page | Narration line |','| --- | --- | --- | --- | --- |']
    for i,s in enumerate(shots,1):
        a=f'{at//60:02.0f}:{at%60:02.0f}';at+=s['duration'];b=f'{at//60:02.0f}:{at%60:02.0f}'
        lines.append(f"| {i:02} · {s['title']} | {a}–{b} | {s['duration']} s | `{s['frame']}` | {s['narration']} |")
    lines+=['','## Source records','']
    lines+=list(dict.fromkeys(f"- {s['source']}" for s in shots if s.get('source')))
    lines+=['','## Production','', 'Captured with Chromium at 1920×1080 and deviceScaleFactor 2. Gentle zoom and pan, highlighted cursor and section titles are composed from PNG overlays. The final edit is assembled with `presentation-prep/video-toolkit/render.py`. Narration cues are supplied above for the presenter.','']
    (ROOT/'SHOTLIST.md').write_text('\n'.join(lines))
    validation=sh([sys.executable,TOOLKIT,ROOT/'edit.json','--work',ROOT/'work'/'render','--crf','19'])
    (ROOT/'render-validation.txt').write_text(validation)
    print(validation,flush=True)
    print(sh(['ffprobe','-v','error','-show_entries','stream=codec_name,width,height,r_frame_rate,pix_fmt:format=duration,size','-of','json',ROOT/'cicd-demo.mp4']))
if __name__=='__main__':main()
