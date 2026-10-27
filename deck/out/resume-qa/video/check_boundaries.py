from pathlib import Path
import subprocess,json,concurrent.futures,os,re
R=Path(__file__).resolve().parents[4];Q=Path(__file__).resolve().parent
plans={3:'cuts-a/03-create-group-review.edl.json',4:'finalize/04-invite-and-join.plan.json',5:'cuts-b/05-photo-with-a-look-review.edl.json',6:'finalize/06-video-and-allowance.plan.json',7:'cuts-a/07-group-chat-review.edl.json',8:'cuts-b/08-weekly-reminder-review.edl.json',9:'cuts-c/09-cycle-ends-film-ready.edl.json',10:'cuts-c/10-watch-the-film.edl.json',11:'cuts-c/11-archive-and-save.edl.json',12:'cuts-b/12-outsider-denied-review.edl.json'}
jobs=[]
for p in sorted((R/'videos/clips').glob('*.mp4'))[2:]:
 dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(p)]));n=int(p.name[:2]);plan=R/'videos/work'/plans[n]
 j=json.loads(plan.read_text()); times={0,int(round(dur*30))-1};cur=0
 for s in j['segments']:
  cur+=int(round(s['duration']*30))
  times.update(t for t in (cur-1,cur,cur+1) if 0<=t<round(dur*30))
 for f in sorted(times):jobs.append((p,f,plan))
pattern=re.compile(r'\b(?:sign[ -]?in|sign[ -]?up|log[ -]?in|password|onboarding|30\s*[- ]?\s*(?:min(?:ute)?s?|minutes)|half\s+(?:an?\s+)?hour)\b',re.I)
def check(job):
 p,f,plan=job;d=Q/'boundary-frames'/p.stem;d.mkdir(parents=True,exist_ok=True);image=d/f'{f:05d}.jpg'
 subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{f/30:.9f}','-i',str(p),'-frames:v','1','-vf','crop=440:958:740:60,scale=880:1916','-q:v','2',str(image)],check=True,capture_output=True)
 text=subprocess.check_output(['tesseract',str(image),'stdout','--psm','11'],env=dict(os.environ,OMP_THREAD_LIMIT='1'),stderr=subprocess.DEVNULL).decode()
 return dict(clip=p.stem,sourceTime=f/30,frameNumber=f,frame=str(image.relative_to(R)),productionPlan=str(plan.relative_to(R)),text=text,hits=pattern.findall(text))
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:results=list(ex.map(check,jobs))
(Q/'boundary-ocr.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(dict(samples=len(results),hits=[r for r in results if r['hits']]),indent=2))
