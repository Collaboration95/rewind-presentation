from pathlib import Path
import subprocess,json,concurrent.futures
R=Path(__file__).resolve().parents[4];Q=Path(__file__).resolve().parent
manifest=json.loads((R/'deck/clips/device/manifest.json').read_text())
def run(a):subprocess.run([str(x) for x in a],check=True,capture_output=True)
def make(c):
 src=Path(c['source']);stem=src.stem;dur=c['duration'];last=round(dur*30)-1
 times=list(range(0,int(dur),5))+[last/30]
 # Source screenshots are decoded from the supplied export, never a reconstruction.
 paths=[]
 for t in times:
  if isinstance(t,int):p=Q/'source-frames'/stem/f'{t+1:04d}.jpg'
  else:
   p=Q/'source-frames'/stem/'last.jpg'
   run(['ffmpeg','-v','error','-y','-ss',f'{t:.9f}','-i',src,'-frames:v','1','-vf','crop=440:958:740:60,scale=880:1916','-q:v','2',p])
  paths.append(p)
 for kind,frames,geometry,name in [('source',paths,'220x479+8+20',stem+'-source-overview.jpg'),('device',None,'208x+8+20',stem+'-device-contact.jpg')]:
  if kind=='device':
   d=Q/'device-frames'/stem;d.mkdir(parents=True,exist_ok=True)
   run(['ffmpeg','-v','error','-y','-i',c['output'],'-vf',rf'select=not(mod(n\,150))+eq(n\,{last})','-fps_mode','vfr','-q:v','2',d/'%03d.jpg'])
   frames=sorted(d.glob('*.jpg'));assert len(frames)==len(times)
  args=['magick','montage','-font','/System/Library/Fonts/Supplemental/Arial.ttf','-pointsize','18']
  for t,p in zip(times,frames):args+=['-label',f'{t:.3f}s',p]
  args+=['-background','#dedbd5','-fill','#262626','-geometry',geometry,'-tile','4x',Q/name]
  run(args)
 print(stem,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(make,manifest['clips']))
