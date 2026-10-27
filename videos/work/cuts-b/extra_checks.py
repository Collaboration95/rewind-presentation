from pathlib import Path
import subprocess,json,numpy as np
R=Path(__file__).resolve().parent
results=[]
for p in sorted(R.glob('*-review.mp4')):
 data=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vf','crop=440:760:740:125,scale=44:76,format=gray','-an','-f','rawvideo','-'])
 a=np.frombuffer(data,dtype=np.uint8).reshape(-1,76,44);means=a.mean((1,2));bad=np.where(means<20)[0]
 result={'file':p.name,'frames_scanned':len(a),'blank_phone_frames':bad.tolist(),'min_phone_mean_luma':float(means.min()),'last_phone_mean_luma':float(means[-1])};results.append(result)
 print(result['file'],len(a),'blank',len(bad),flush=True)
(R/'qa/frame-integrity.json').write_text(json.dumps(results,indent=2)+'\n')
