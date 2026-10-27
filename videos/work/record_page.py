import subprocess,time,signal,sys
from pathlib import Path
name,url,duration=sys.argv[1],sys.argv[2],float(sys.argv[3])
root=Path(__file__).resolve().parents[1]
log=(root/'raw'/f'{name}.log').open('w')
p=subprocess.Popen(['xcrun','simctl','io','booted','recordVideo','--codec=h264',str(root/'raw'/f'{name}.mov')],stdout=log,stderr=log)
time.sleep(.8)
subprocess.run(['xcrun','simctl','openurl','booted',url],check=True)
start=time.monotonic()
while time.monotonic()-start<duration:time.sleep(min(1,duration-(time.monotonic()-start)))
p.send_signal(signal.SIGINT)
p.wait(timeout=30)
print(name,'recorded',duration,'s')
