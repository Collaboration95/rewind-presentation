from pathlib import Path
import subprocess,json,concurrent.futures,hashlib
r=Path(__file__).resolve().parents[2];q=r/'work/final-qa';manifest=json.loads((r/'work/clip-manifest.json').read_text());jobs=[];cursor=0
for i,m in enumerate(manifest,1):
 jobs.extend([(i,'card',cursor+.5),(i,'clip',cursor+1+m['duration']/2)])
 cursor+=1+m['duration']
def grab(job):
 i,kind,t=job;p=q/f'join-{i:02}-{kind}.png'
 if p.exists():return p
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(r/'demo.mp4'),'-frames:v','1',str(p)],check=True)
 return p
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(grab,jobs))
for kind in ['card','clip']:
 files=sorted(q.glob('join-??-'+kind+'.png'))
 subprocess.run(['magick','montage','-font','/System/Library/Fonts/Supplemental/Arial.ttf',*[str(p) for p in files],'-tile','3x4','-geometry','480x270+4+4','-background','#f6efe5',str(q/f'demo-{kind}-contact.jpg')],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_format','-show_streams','-of','json',str(r/'demo.mp4')]))
v=next(x for x in probe['streams'] if x['codec_type']=='video');a=next(x for x in probe['streams'] if x['codec_type']=='audio')
checks={'duration_672s':abs(float(probe['format']['duration'])-672)<.04,'frames_20160':int(v['nb_read_frames'])==20160,'1080p':(v['width'],v['height'])==(1920,1080),'30fps':v['r_frame_rate']=='30/1','h264':v['codec_name']=='h264','yuv420p':v['pix_fmt']=='yuv420p','aac_stereo':a['codec_name']=='aac' and a['channels']==2 and a['sample_rate']=='48000','12_clips':len(list((r/'clips').glob('*.mp4')))==12}
assert all(checks.values()),checks
report={'checks':checks,'duration':probe['format']['duration'],'bytes':probe['format']['size'],'sha256':hashlib.sha256((r/'demo.mp4').read_bytes()).hexdigest(),'sampled_join_frames':len(jobs),'frame_contacts':['demo-card-contact.jpg','demo-clip-contact.jpg'],'visual_review':'pending'}
(q/'demo-validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
