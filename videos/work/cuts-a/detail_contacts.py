from pathlib import Path
import subprocess,concurrent.futures
ROOT=Path(__file__).resolve().parent
RAW=ROOT.parent.parent/'raw'
JOBS={
'01-install-clean':[6,7,8,46,47,48,49,60,61,62,63,64,85,86,87,88,89,90,131,132,133,134,135,135.8,136],
'02-signin-clean':[6,7,8,9,10,25,26,27,28,29,30,31,32,33,34],
'03-create':[11,12,13,14,15,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,71,72,73,74,75,76,94,95,96,97,98,99],
'04-invite':[6,7,8,9,10,60,61,62,63,64,65,105,106,107,108,109,118,119,120,121,222,223,224,225,226,227,230,231,232,233,234,235,236],
'07-chat':[0,0.1,1,27,28,29,30,31,40,41,42,43,44,45,55,56,57,58,59,60,115,116,117,118,119,120,128,129,130,131,132,133,134]}
def run(args):
 p=subprocess.run([str(a) for a in args],capture_output=True)
 if p.returncode:raise RuntimeError(p.stderr.decode()[-1000:])
def frame(job):
 name,t=job;dest=ROOT/'detail-qa'/name;dest.mkdir(parents=True,exist_ok=True)
 p=dest/f'{t:07.2f}.png'
 run(['ffmpeg','-v','error','-ss',t,'-i',RAW/(name+'.mov'),'-frames:v','1','-vf','scale=-2:600','-y',p]);return p
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(frame,[(n,t) for n,ts in JOBS.items() for t in ts]))
for name,ts in JOBS.items():
 args=['magick','montage']
 for t in ts:args+=['-label',f'{t:g}s',ROOT/'detail-qa'/name/f'{t:07.2f}.png']
 args+=['-font','/System/Library/Fonts/Supplemental/Arial.ttf','-pointsize','20','-background','#eee8df','-fill','#30251c','-geometry','276x600+8+8','-tile','5x',ROOT/'detail-qa'/(name+'-contact.jpg')]
 run(args);print(name,'detail ready',flush=True)
