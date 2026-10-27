from pathlib import Path
import subprocess,json,numpy as np,concurrent.futures
ROOT=Path(__file__).resolve().parent;RAW=ROOT.parent.parent/'raw';Q=ROOT/'qa/source'
def scan(name):
 data=subprocess.check_output(['ffmpeg','-v','error','-i',str(RAW/(name+'.mov')),'-vf','fps=30,crop=1206:2100:0:180,scale=60:105,format=gray','-f','rawvideo','-'])
 a=np.frombuffer(data,dtype=np.uint8).reshape(-1,105,60);means=a.mean((1,2));good=means>20
 groups=[];start=0
 for i in range(1,len(good)+1):
  if i==len(good) or good[i]!=good[start]:groups.append({'start':round(start/30,4),'end':round(i/30,4),'good':bool(good[start]),'mean':round(float(means[start:i].mean()),2)});start=i
 (Q/(name+'-validity.json')).write_text(json.dumps(groups,indent=2));print(name,groups,flush=True)
 # Dense sheet of valid review/upload/seal frames.
 times=[i/30 for i in range(0,len(good),15) if good[i] and i/30>=16]
 args=['magick','montage','-font','/System/Library/Fonts/Supplemental/Arial.ttf','-pointsize','18']
 for t in times:
  p=Q/name/f'dense-{t:06.2f}.jpg';subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(RAW/(name+'.mov')),'-frames:v','1','-vf','scale=300:-1','-y',str(p)],check=True);args+=['-label',f'{t:g}s',str(p)]
 if times:subprocess.run(args+['-background','#f6efe5','-geometry','240x522+6+12','-tile','6x',str(Q/(name+'-valid-detail.jpg'))],check=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as p:list(p.map(scan,['05-photo','06-video']))
