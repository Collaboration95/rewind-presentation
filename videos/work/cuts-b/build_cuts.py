from pathlib import Path
import json,subprocess,concurrent.futures
R=Path(__file__).resolve().parent;RAW=R.parent.parent/'raw';S=R.parent/'stills';H=R/'holds';H.mkdir(exist_ok=True)
def still(name,src,t):
 p=H/(name+'.png')
 subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(src),'-frames:v','1','-y',str(p)],check=True)
 return p
def seg(src,a,b,d=None,note=''):
 return dict(source=str(src),**{'in':a,'out':b},duration=round(d if d is not None else b-a,8),audio=False,note=note)
def hold(src,d,note):return dict(source=str(src),duration=d,audio=False,note=note)
p=R/'sources/05-photo.mp4';v=R/'sources/06-video.mp4'
ph0=still('05-compact-look',p,7.8);phr=still('05-review',p,24);phs=still('05-sealed',p,35)
v0=still('06-before-allowance',v,.5);vl=still('06-vhs-look',v,10);vr=still('06-review',v,24);vs=still('06-sealed',v,35)
b=RAW/'08-banner.mov';bs=still('08-home-final',b,16)
specs=[
 dict(number=5,name='Photo with a look',output='05-photo-with-a-look-review.mp4',segments=[seg(p,0,8,note='Live photo viewfinder, Compact Digital'),hold(ph0,8,'Readable selected-look hold'),seg(p,8,17.8,note='Actual change to Disposable Flash, shutter'),seg(p,18.1,25.9,note='Actual review and Seal'),hold(phr,6,'Review reading hold before Seal upload'),seg(p,26,33.8,note='Actual uploading'),seg(p,34.1,35.1,note='Sealed'),hold(phs,6.6,'Sealed ending; no ledger/black tail')]),
 dict(number=6,name='Video and allowance',output='06-video-and-allowance-review.mp4',segments=[hold(v0,8,'Actual initial ledger: Photo 3s, 1 of 5, 3 of 30s'),seg(v,4.1,11.9,note='Animated VHS viewfinder'),hold(vl,6,'Readable VHS selection before recording'),seg(v,11.9,17.9,note='Six seconds of actual animated recording'),seg(v,18.1,25.9,note='Actual video review'),hold(vr,5,'Readable trim/review hold'),seg(v,26.1,33.9,note='Actual applying-look transition'),seg(v,34.1,35.1,note='Sealed'),hold(vs,7.6,'Sealed reading hold'),hold(S/'06-ledger.png',8,'Native captured final ledger: 2 of 5, 9 of 30s, Photo 3s and Video 6s sealed')]),
 dict(number=8,name='Weekly reminder',output='08-weekly-reminder-review.mp4',segments=[seg(RAW/'08-reminder.mov',180,190,note='Settings scroll to Weekly reminder Off'),seg(RAW/'08-reminder.mov',210,216,note='Off, cut before simultaneous toggle/install modal'),seg(RAW/'08-reminder.mov',257,269,note='On after modal dismissal; no sign-out tail'),seg(b,1,16,note='Safe Home, actual banner arrival and departure'),hold(bs,7,'Last safe Home frame; total banner section 22s')]),
 dict(number=12,name='Outsider denied',output='12-outsider-denied-review.mp4',segments=[hold(S/'12-priya-profile.png',7,'Native Priya identity and no-group profile'),seg(RAW/'12-outsider.mov',13,21,note='Real empty group state then Have an invite'),seg(RAW/'12-outsider.mov',24,29,note='Invite form, before entry'),seg(RAW/'12-outsider.mov',44,50,note='Actual EMX-TVD entry'),seg(RAW/'12-outsider.mov',58,66,note='Actual Accept, Joining, used-invitation error'),hold(S/'12-invite-denied.png',8,'Read actual used-invitation error'),hold(S/'12-outsider-empty.png',8,'Native empty group ending')])]
for s,expected in zip(specs,[55,65,50,50]):
 assert abs(sum(x['duration'] for x in s['segments'])-expected)<1e-6,(s['name'],sum(x['duration'] for x in s['segments']))
 (R/s['output']).with_suffix('.edl.json').write_text(json.dumps(s,indent=2)+'\n')
print('EDLs ready',flush=True)
