from pathlib import Path
import subprocess,concurrent.futures
R=Path(__file__).resolve().parent;O=R/'sources';O.mkdir(exist_ok=True)
def norm(n):
 p=subprocess.run(['ffmpeg','-v','error','-i',str(R.parent.parent/'raw'/(n+'.mov')),'-vf','fps=30','-an','-c:v','libx264','-preset','ultrafast','-crf','16','-pix_fmt','yuv420p','-threads','2','-y',str(O/(n+'.mp4'))],capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr)
 q=R/'qa/source'/('sequential-'+n);q.mkdir(exist_ok=True)
 subprocess.run(['ffmpeg','-v','error','-i',str(O/(n+'.mp4')),'-vf','fps=2,scale=240:-1','-y',str(q/'%03d.jpg')],check=True)
 args=['magick','montage','-font','/System/Library/Fonts/Supplemental/Arial.ttf','-pointsize','18']
 for i,p in enumerate(sorted(q.glob('*.jpg'))):
  if i<30 and i%4:continue
  args+=['-label',f'{i/2:g}s',str(p)]
 subprocess.run(args+['-background','#f6efe5','-geometry','240x522+6+12','-tile','8x',str(R/'qa/source'/('sequential-'+n+'.jpg'))],check=True)
 print(n,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as p:list(p.map(norm,['05-photo','06-video']))
