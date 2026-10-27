from pathlib import Path
import subprocess,concurrent.futures
ROOT=Path(__file__).resolve().parent
RAW=ROOT.parent.parent/'raw'
def run(args):
 subprocess.run([str(a) for a in args],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
def sheet(name):
 dest=ROOT/'source-qa'/name;dest.mkdir(parents=True,exist_ok=True)
 run(['ffmpeg','-v','error','-i',RAW/(name+'.mov'),'-vf','fps=1/5,scale=-2:500','-fps_mode','passthrough',dest/'%03d.png'])
 files=sorted(dest.glob('*.png'));args=['magick','montage']
 for i,p in enumerate(files):args+=['-label',f'{i*5:03d}s',p]
 args+=['-font','/System/Library/Fonts/Supplemental/Arial.ttf','-pointsize','18','-background','#eee8df','-fill','#30251c','-geometry','230x500+7+8','-tile','5x',ROOT/'source-qa'/(name+'-contact.jpg')]
 run(args)
 print(name,'contact ready',flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(sheet,['01-install-clean','02-signin-clean','03-create','04-invite','07-chat']))
