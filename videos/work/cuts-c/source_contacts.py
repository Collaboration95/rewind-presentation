from pathlib import Path
import subprocess,sys,io,math

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parents[1]
kind=sys.argv[1]
if kind=='09': src=BASE/'raw/09-premiere.mov'; times=list(range(0,119,5))
elif kind=='10': src=BASE/'raw/10-watch.mov'; times=list(range(0,193,5))
elif kind=='film': src=BASE/'work/film/rewind-hosted-film.mp4'; times=list(range(0,21,2))
else:
 src=Path(sys.argv[2]); times=[float(x) for x in sys.argv[3:]]
w,h=230,530
args=['magick','montage','-font','/System/Library/Fonts/Supplemental/Arial.ttf','-pointsize','18','-background','#ddd8cf','-fill','black']
folder=ROOT/'source-qa'/kind;folder.mkdir(parents=True,exist_ok=True)
for i,t in enumerate(times):
 p=folder/f'{t:08.3f}.png'
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(src),'-frames:v','1','-vf','scale=440:-1',str(p)],check=True)
 args+=['-label',f'{kind} {t:.3f}s',str(p)]
subprocess.run(args+['-geometry','220x500+5+5','-tile','8x',str(ROOT/f'{kind}-contact.jpg')],check=True)
print(ROOT/f'{kind}-contact.jpg')
