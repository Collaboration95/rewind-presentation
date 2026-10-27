from pathlib import Path
import subprocess,concurrent.futures
R=Path(__file__).resolve().parent
def render(p):
 with p.with_suffix('.render.log').open('w') as log:
  ret=subprocess.run(['python3',str(R/'render.py'),str(p),'--preset','veryfast','--crf','18'],stdout=log,stderr=subprocess.STDOUT)
 print(p.stem,ret.returncode,flush=True)
 if ret.returncode:raise RuntimeError(p.read_text())
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(render,sorted(R.glob('*.edl.json'))))
