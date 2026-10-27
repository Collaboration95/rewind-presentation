from pathlib import Path
import subprocess,json,concurrent.futures
ROOT=Path(__file__).resolve().parent
RAW=ROOT.parent.parent/'raw';STILLS=ROOT.parent/'stills';QA=ROOT/'qa/source';QA.mkdir(parents=True,exist_ok=True)
def run(a):
 p=subprocess.run(list(map(str,a)),capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr[-2000:])
 return p.stdout
sources={'05-photo':list(range(0,42,2))+[35,36,37,38,39,41.9], '06-video':list(range(0,42,2))+[35,36,37,38,39,41.9], '08-reminder':list(range(0,328,10)), '08-banner':[0,3,4,5,6,8,10,12,14,15,16], '12-outsider':list(range(0,97,5))}
def sheet(item):
 name,times=item;d=QA/name;d.mkdir(exist_ok=True);args=['magick','montage','-font','/System/Library/Fonts/Supplemental/Arial.ttf','-pointsize','18']
 for t in sorted(set(times)):
  p=d/f'{t:06.2f}.jpg';run(['ffmpeg','-v','error','-ss',t,'-i',RAW/(name+'.mov'),'-frames:v','1','-vf','scale=300:-1','-y',p]);args+=['-label',f'{name} {t:g}s',p]
 args+=['-background','#f6efe5','-geometry','240x522+6+12','-tile','6x',QA/(name+'-source-contact.jpg')];run(args)
 print(name,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(sheet,sources.items()))
args=['magick','montage','-font','/System/Library/Fonts/Supplemental/Arial.ttf','-pointsize','18']
for name in ['06-ledger','08-reminder-off','08-reminder-on','12-outsider-empty','12-invite-denied','12-priya-profile']:args+=['-label',name,STILLS/(name+'.png')]
run(args+['-background','#f6efe5','-geometry','300x653+8+12','-tile','3x',QA/'stills-contact.jpg'])
