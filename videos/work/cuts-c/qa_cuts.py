from pathlib import Path
import json,subprocess,concurrent.futures,re,math,array,sys
R=Path(__file__).resolve().parent
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
def run(a,raw=False):
 p=subprocess.run([str(x) for x in a],capture_output=True,check=True)
 return p.stdout if raw else p.stdout.decode()
def pcm(path,start=0,dur=None):
 args=['ffmpeg','-v','error','-ss',str(start),'-i',path]
 if dur is not None:args+=['-t',str(dur)]
 return array.array('f',run(args+['-map','0:a','-ar','8000','-ac','1','-f','f32le','-'],True))
def rms(a):return math.sqrt(sum(x*x for x in a)/len(a)) if a else 0
for specfile in sorted(R.glob('*.edl.json')):
 spec=json.loads(specfile.read_text());out=R/spec['output']
 if len(sys.argv)>1 and out.stem not in sys.argv[1:]:continue
 if not out.exists():continue
 slug=out.stem;q=R/'qa'/slug;q.mkdir(parents=True,exist_ok=True)
 run(['ffmpeg','-v','error','-y','-i',out,'-vf','fps=1,crop=440:957:740:60,scale=660:-1',q/'%03d.png'])
 files=sorted(q.glob('*.png'))
 def ocr(p):return {'second':int(p.stem)-1,'text':run(['tesseract',p,'stdout','--psm','11'])}
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: texts=list(pool.map(ocr,files))
 patterns=[r'week\s*\d+\s*(?:of|/|0f)\s*4',r'minutes?\s+until',r'moments?\s+reset',r'resets?\s+in\s+1\s*day',r'\b(?:1|one)[ -]day\s+cycle',r'cycle\s+(?:length|duration)',r'save\s+password',r'siri\s+suggestions',r'recent\s+searches']
 hits=[{'second':x['second'],'pattern':p,'text':x['text']} for x in texts for p in patterns if re.search(p,x['text'],re.I)]
 (R/(slug+'.ocr.json')).write_text(json.dumps({'sampling':'One phone crop per output second; tesseract PSM 11; visual contact review supplements OCR.','patterns':patterns,'forbidden_hits':hits,'frames':texts},indent=2))
 args=['magick','montage','-font',FONT,'-pointsize','18','-background','#f6efe5','-fill','#342b25']
 for p in files[::5]:args+=['-label',f'{int(p.stem)-1:02}s',p]
 run(args+['-geometry','230x500+8+8','-tile','5x',R/(slug+'.phone-contact.jpg')])
 full=R/(slug+'.frame.png');run(['ffmpeg','-v','error','-y','-ss','1','-i',out,'-frames:v','1',full])
 sound=pcm(out);cur=0;audio=[]
 for s in spec['segments']:
  d=s['duration'];start=round(cur*8000);end=round((cur+d)*8000);samples=sound[start:end]
  record={'output_in':cur,'output_out':cur+d,'external_audio':isinstance(s['audio'],dict),'rms':rms(samples)}
  if isinstance(s['audio'],dict):
   ref=pcm(s['audio']['source'],s['audio'].get('in',0),d);n=min(len(ref),len(samples));dot=sum(ref[i]*samples[i] for i in range(n));den=math.sqrt(sum(x*x for x in ref[:n])*sum(x*x for x in samples[:n]));record['correlation_to_real_film']=dot/den if den else 0
  else:
   # Ignore AAC boundary ringing (50 ms) when checking intended silent regions.
   record['interior_silent_rms']=rms(samples[400:-400]);record['silent_pass']=record['interior_silent_rms']<0.0001
  audio.append(record);cur+=d
 report={'output':str(out),'duration':cur,'forbidden_text_hits':len(hits),'ocr_samples':len(texts),'audio':audio,'encoding_checks':json.loads(out.with_suffix('.validation.json').read_text())['checks']}
 (R/(slug+'.qa.json')).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
