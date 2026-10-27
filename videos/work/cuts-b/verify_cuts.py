from pathlib import Path
import json,subprocess,concurrent.futures,re,csv,hashlib
ROOT=Path(__file__).resolve().parent
QA=ROOT/'qa';QA.mkdir(exist_ok=True)
def run(a):
 p=subprocess.run([str(x) for x in a],capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr[-2000:])
 return p.stdout
bad=re.compile(r'week\s*\d+\s*(?:of|0f|/)\s*4|(?:first\s+)?cycle\s+(?:lasts|length|ends|duration)|(?:four|4)\s*[- ]?weeks|(?:minutes?|days?|hours?)\s+until\s+(?:our|the)\s+film|countdown|simulat(?:ion|ed)|disclaimer',re.I)
def scan_frame(job):
 p,t=job;txt=run(['tesseract',p,'stdout','--psm','11']);return {'time':t,'frame':str(p.relative_to(ROOT)),'text':txt,'forbidden_matches':bad.findall(txt)}
def verify(mp4):
 stem=mp4.stem;spec=json.loads(mp4.with_suffix('.edl.json').read_text());duration=int(round(sum(s['duration'] for s in spec['segments'])));out=QA/stem;out.mkdir(exist_ok=True)
 # One full-resolution QA frame at each 5-second mark, plus final frame and all edit boundaries.
 times=set(range(0,duration,5));times.add(duration-1/30);cursor=0
 for row in spec['segments']:
  times.add(cursor);times.add(max(0,cursor-1/30));cursor+=row['duration']
 def frame(t):
  p=out/f'{round(t*30):05d}.png';run(['ffmpeg','-v','error','-ss',f'{t:.8f}','-i',mp4,'-frames:v','1','-y',p]);return p
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:paths=list(pool.map(frame,sorted(times)))
 args=['magick','montage']
 for t in range(0,duration,5):args+=['-label',f'{t:02d}s',out/f'{t*30:05d}.png']
 args+=['-label',f'{duration-1/30:.2f}s END',out/f'{duration*30-1:05d}.png','-font','/System/Library/Fonts/Supplemental/Arial.ttf','-pointsize','20','-background','#f6efe5','-geometry','480x270+8+24','-tile','3x',QA/(stem+'-contact.jpg')]
 run(args)
 # A second, larger phone-only contact sheet makes UI text legible during visual review.
 phone_dir=out/'phones';phone_dir.mkdir(exist_ok=True)
 args=['magick','montage']
 for t in list(range(0,duration,5))+[duration-1/30]:
  src=out/f'{round(t*30):05d}.png';dest=phone_dir/src.name
  run(['magick',src,'-crop','440x957+740+60','+repage',dest]);args+=['-label',f'{t:.2f}s',dest]
 args+=['-font','/System/Library/Fonts/Supplemental/Arial.ttf','-pointsize','18','-background','#f6efe5','-geometry','300x653+8+10','-tile','4x',QA/(stem+'-phone-contact.jpg')];run(args)
 # Scan every second of the final render plus both sides of every edit, independently of source EDL.
 scan_dir=out/'ocr';scan_dir.mkdir(exist_ok=True)
 run(['ffmpeg','-v','error','-i',mp4,'-vf','fps=1:start_time=0,crop=440:957:740:60,scale=880:1914','-fps_mode','passthrough','-y',scan_dir/'%04d.png'])
 jobs=[(p,i) for i,p in enumerate(sorted(scan_dir.glob('[0-9][0-9][0-9][0-9].png'))) ]
 for p,t in zip(paths,sorted(times)):
  cp=scan_dir/('boundary-'+p.name);run(['magick',p,'-crop','440x957+740+60','+repage','-resize','200%',cp]);jobs.append((cp,t))
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:ocr=list(pool.map(scan_frame,jobs))
 (QA/(stem+'-ocr.json')).write_text(json.dumps(ocr,indent=2))
 audio=run(['ffmpeg','-hide_banner','-i',mp4,'-vn','-af','astats=metadata=0:reset=0','-f','null','-']) if False else subprocess.run(['ffmpeg','-hide_banner','-i',str(mp4),'-vn','-af','astats=metadata=0:reset=0','-f','null','-'],capture_output=True,text=True).stderr
 (QA/(stem+'-audio.txt')).write_text(audio)
 checks=json.loads(mp4.with_suffix('.validation.json').read_text())['checks']
 matches=[{'time':r['time'],'matches':r['forbidden_matches']} for r in ocr if r['forbidden_matches']]
 result={'output':str(mp4),'duration_seconds':duration,'frames':duration*30,'encoder_checks':checks,'silent_aac':bool(re.search(r'Peak level dB: -inf',audio)),'ocr_frames_scanned':len(ocr),'forbidden_text_hits':matches,'sha256':hashlib.sha256(mp4.read_bytes()).hexdigest(),'visual_review':'PENDING'}
 (QA/(stem+'-report.json')).write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ('sha256','encoder_checks')}),flush=True)
 return result
if __name__=='__main__':
 import sys
 files=[ROOT/p for p in sys.argv[1:]] if len(sys.argv)>1 else sorted(ROOT.glob('*-review.mp4'))
 for p in files:verify(p)
