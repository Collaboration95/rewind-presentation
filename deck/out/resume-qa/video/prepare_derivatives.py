from pathlib import Path
import subprocess,json,hashlib,concurrent.futures
ROOT=Path(__file__).resolve().parents[4]; QA=Path(__file__).resolve().parent; OUT=ROOT/'deck/clips/device'
SOURCES=sorted((ROOT/'videos/clips').glob('*.mp4'))[2:]
POSTERS={3:35,4:47,5:28,6:59,7:46,8:34,9:2,10:8,11:2,12:35}
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(p)]))
def run(a):subprocess.run([str(v) for v in a],check=True,capture_output=True)
originals={str(p):sha(p) for p in SOURCES+[ROOT/'videos/demo.mp4']}
(QA/'source-sha256-before.json').write_text(json.dumps(originals,indent=2)+'\n')
def render(p):
 n=int(p.name[:2]); crop=dict(x=752,y=124,width=416,height=858 if n in (4,10,11) else 776)
 duration=float(probe(p)['format']['duration']); dest=OUT/p.name;poster=OUT/(p.stem+'-poster.jpg')
 f='crop={width}:{height}:{x}:{y}'.format(**crop)
 run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',p,'-map','0:v:0','-map','0:a:0','-vf',f,'-c:v','libx264','-preset','slow','-crf','17','-threads','2','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',dest])
 run(['ffmpeg','-v','error','-y','-ss',POSTERS[n],'-i',dest,'-frames:v','1','-q:v','2',poster])
 # Unlabelled derivative overview, sampled every five seconds, like the source overview.
 rows=(int(duration/5)+3)//4
 run(['ffmpeg','-v','error','-y','-i',dest,'-vf',f'fps=1/5,scale=208:-1,tile=4x{rows}:padding=8:margin=8:color=gray','-frames:v','1','-q:v','2',QA/(p.stem+'-device-contact.jpg')])
 info=probe(dest); vs=next(s for s in info['streams'] if s['codec_type']=='video'); aus=next(s for s in info['streams'] if s['codec_type']=='audio')
 # Complete decode checks the entire exported stream.
 run(['ffmpeg','-v','error','-xerror','-i',dest,'-f','null','-'])
 content=dest.read_bytes(); faststart=content.find(b'moov')<content.find(b'mdat')
 # Decoded audio hash proves the AAC track was retained without change.
 hashes=[]
 for a in [p,dest]:
  hashes.append(subprocess.check_output(['ffmpeg','-v','error','-i',str(a),'-map','0:a:0','-f','hash','-hash','sha256','-']).decode().strip())
 result=dict(source=str(p),output=str(dest),poster=str(poster),duration=float(info['format']['duration']),crop=crop,retainedSourceIntervals=[dict(start=0.0,end=duration)],posterTime=POSTERS[n],sourceSha256=originals[str(p)],outputSha256=sha(dest))
 checks=dict(file=p.name,sourceDuration=duration,duration=result['duration'],codec=vs['codec_name'],pixelFormat=vs['pix_fmt'],width=vs['width'],height=vs['height'],frameRate=vs['r_frame_rate'],audioCodec=aus['codec_name'],audioHashUnchanged=hashes[0]==hashes[1],faststart=faststart,fullDecode='PASS')
 assert checks['codec']=='h264' and checks['pixelFormat']=='yuv420p' and faststart and checks['audioHashUnchanged']
 print(p.name, result['duration'],crop,flush=True)
 return result,checks
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: results=list(pool.map(render,SOURCES))
manifest=dict(version=1,sourceTimeUnit='seconds',intervalConvention='[start,end)',clips=[r for r,c in results])
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
after={p:sha(Path(p)) for p in originals}; assert after==originals
(QA/'source-sha256-after.json').write_text(json.dumps(after,indent=2)+'\n')
(QA/'validation.json').write_text(json.dumps(dict(totalDuration=sum(r['duration'] for r,c in results),sourcesAndBackupUnchanged=True,clips=[c for r,c in results]),indent=2)+'\n')
print('Manifest and validation written. Total seconds:',sum(r['duration'] for r,c in results),flush=True)
