from pathlib import Path
import subprocess,json,concurrent.futures,os,re
ROOT=Path(__file__).resolve().parents[4]
QA=Path(__file__).resolve().parent
SOURCES=sorted((ROOT/'videos/clips').glob('*.mp4'))[2:]
def extract(p):
 d=QA/'source-frames'/p.stem;d.mkdir(parents=True,exist_ok=True)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(p),'-vf',r'select=not(mod(n\,30)),crop=440:958:740:60,scale=880:1916','-fps_mode','vfr','-q:v','2',str(d/'%04d.jpg')],check=True)
 return [(p.stem,int(f.stem)-1,f) for f in sorted(d.glob('*.jpg'))]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
 jobs=[j for group in ex.map(extract,SOURCES) for j in group]
pattern=re.compile(r'\b(?:sign[ -]?in|sign[ -]?up|log[ -]?in|password|onboarding|30\s*[- ]?\s*(?:min(?:ute)?s?|minutes)|half\s+(?:an?\s+)?hour)\b',re.I)
def ocr(j):
 stem,t,f=j
 env=dict(os.environ,OMP_THREAD_LIMIT='1')
 r=subprocess.run(['tesseract',str(f),'stdout','--psm','11'],capture_output=True,text=True,env=env,check=True)
 return dict(clip=stem,sourceTime=t,frame=str(f.relative_to(ROOT)),text=r.stdout,hits=pattern.findall(r.stdout))
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
 result=list(ex.map(ocr,jobs))
(QA/'source-ocr.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(samples=len(result),hits=[r for r in result if r['hits']]),indent=2))
