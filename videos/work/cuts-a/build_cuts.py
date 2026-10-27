from pathlib import Path
import json,subprocess,concurrent.futures
ROOT=Path(__file__).resolve().parent
RAW=ROOT.parent.parent/'raw';STILLS=ROOT.parent/'stills'
p=ROOT/'render.py';s=p.read_text()
if "smooth=row.get('smooth', [])" not in s:
    s=s.replace("width=v['width'], height=v['height'], crop=crop, masks=masks,", "width=v['width'], height=v['height'], crop=crop, masks=masks, smooth=row.get('smooth', []),")
    s=s.replace("ops = ['setpts=PTS-STARTPTS']", "ops = ['setpts=PTS-STARTPTS']\n        for rect in s.get('smooth', []):\n            x,y,w,h = rect\n            if any(type(z) is not int for z in rect) or min(x,y) < 1 or min(w,h) < 1 or x+w >= s['width'] or y+h >= s['height']:\n                raise ValueError('Invalid smoothing rectangle')\n            ops += [f'delogo=x={x}:y={y}:w={w}:h={h}']")
    p.write_text(s)
SMOOTH=[[455,1824,620,64],[78,1888,310,54]]
def video(name,a,b,d,note,smooth=False):
 row={'source':str(RAW/name),'in':a,'out':b,'duration':d,'audio':False,'note':note}
 if smooth:row['smooth']=SMOOTH
 return row
def still(name,d,note,island=False):return {'source':str(STILLS/name),'duration':d,'audio':False,'note':note,'add_island':island}
SPECS=[
{'number':1,'name':'Install to Home Screen','output':'01-install-to-home-screen-review.mp4','segments':[
video('01-install-clean.mov',0,6,6,'Real Safari sign-in form; establish browser context'),
video('01-install-clean.mov',8,12,5,'Safari More menu opens; trim following idle pause'),
video('01-install-clean.mov',47,52,6,'Tap Share; native share sheet appears'),
video('01-install-clean.mov',62,67,6,'View More expands native Safari actions'),
still('01-share-actions.png',7,'Read Add to Home Screen in the real native action sheet'),
video('01-install-clean.mov',86,91,7,'Tap Add to Home Screen; real confirmation opens'),
video('01-install-clean.mov',133,136.1,8,'Tap Add; real installed iPhone Home Screen; hold final raw frame')
]},
{'number':2,'name':'Sign in','output':'02-sign-in-review.mp4','segments':[
video('02-signin-clean.mov',0,6,6,'Blank sign-in form'),
video('02-signin-clean.mov',10.5,11.0666666667,6,'Recorded Maya username typing; hold last real frame'),
video('02-signin-clean.mov',11.0666666667,14,8,'Recorded password typing at original speed; masked password'),
video('02-signin-clean.mov',23,31,8,'Read completed form before submitting'),
video('02-signin-clean.mov',31,32.6,9,'Real sign-in progress; freeze safe last frame; omit ALL app Home frames'),
still('02-signedin-settings.png',8,'Cut directly to authenticated Settings and Maya profile')
]},
{'number':3,'name':'Create a group','output':'03-create-group-review.mp4','segments':[
video('03-create.mov',6,12,6,'Settings with Create a group action'),
video('03-create.mov',15,23,8,'Blank New group form and prompt choices',True),
video('03-create.mov',28,34,7,'Read default prompt choices and member limit; omit accidental Spotlight',True),
video('03-create.mov',43,45.5,7,'Real recorded name completion and prompt choice; actual name At table',True),
video('03-create.mov',45.5,50,8,'Real member-limit adjustment down to five',True),
video('03-create.mov',92,99,8,'Read selected third prompt, group name, capacity, and Create group',True),
video('03-create.mov',99.5,100.8,8,'Create press and Creating group progress; hold last safe form; omit ALL Home frames',True),
still('03-created-settings.png',8,'Successful At table group shown in real Settings')
]},
{'number':4,'name':'Invite and join','output':'04-invite-and-join-review.mp4','segments':[
still('04-invite-code.png',8,'Invite code EMX-TVD; start after initial one-person Settings'),
video('04-invite.mov',61,66,8,'Share code opens real native share sheet'),
video('04-invite.mov',100,109,9,'Read invitation share content and available destinations'),
video('04-invite.mov',109,109.3,8,'Real share-sheet dismissal; hold clean invite frame before fallback status; omit stale Members and all Home footage'),
video('04-invite.mov',224.5,234.5,10,'After join: Settings shows 2 of 5 members; no refresh/Home footage'),
video('04-invite.mov',234.5,237,10,'Open fresh Members showing Maya and Jun'),
still('04-members-joined.png',7,'End on verified joined-members still with both Maya and Jun')
]},
{'number':7,'name':'Group chat','output':'07-group-chat-review.mp4','segments':[
video('07-chat.mov',0,6,6,'Real Jun message arrives at recording start'),
video('07-chat.mov',27,33,6,'Focus the group message composer'),
video('07-chat.mov',43,46,8,'Maya types reply at recorded speed; hold completed draft'),
video('07-chat.mov',56,60,8,'Send reply; real sent message appears'),
still('07-chat-exchange.png',7,'Read both real chat messages',True),
video('07-chat.mov',118,126,8,'Select Jun message; real React, Reply, Report actions'),
video('07-chat.mov',134,138,4,'Apply real sparkle reaction; no invented UI'),
still('07-chat-reaction.png',8,'End on real exchange and sparkle reaction')
]}
]
def tc(t):
 n=round(t*30);return f'{n//108000:02}:{n//1800%60:02}:{n//30%60:02}:{n%30:02}'
for spec in SPECS:
 spec['add_island']=False
 duration=sum(x['duration'] for x in spec['segments']);assert duration=={1:45,2:45,3:60,4:60,7:55}[spec['number']]
 target=ROOT/(Path(spec['output']).stem+'.edl.json');target.write_text(json.dumps(spec,indent=2)+'\n')
 edl=[f'TITLE: {spec["name"]}','FCM: NON-DROP FRAME','* 30 FPS; STRAIGHT CUTS; REAL FOOTAGE AT 1X; POSTROLL FREEZE WHERE NOTED','* All source audio discarded; final AAC stereo is silent.','* JSON EDL is authoritative for source in/out and postroll hold durations.','']
 cursor=0
 for i,row in enumerate(spec['segments'],1):
  a=row.get('in',0);span=min(row['duration'],row.get('out',a+row['duration'])-a)
  edl += [f'{i:03}  AX       V     C        {tc(a)} {tc(a+span)} {tc(cursor)} {tc(cursor+row["duration"])}',f'* FROM CLIP NAME: {Path(row["source"]).name}',f'* {row["note"]}']
  if row.get('smooth'):edl += ['* AUTHORIZED DELOGO RECTANGLES (1206x2622 SOURCE): '+json.dumps(row['smooth'])]
  if Path(row['source']).suffix=='.mov' and row['duration']>span:edl += [f'* FREEZE LAST SAFE FRAME: {row["duration"]-span:.6f}s']
  edl += [''];cursor+=row['duration']
 (ROOT/(Path(spec['output']).stem+'.edl')).write_text('\n'.join(edl))
print('Wrote five frame-accurate JSON EDLs and readable EDLs',flush=True)
def render(spec):
 name=Path(spec['output']).stem
 with (ROOT/(name+'.render.log')).open('w') as log:
  p=subprocess.run(['python3','-B',str(ROOT/'render.py'),str(ROOT/(name+'.edl.json')),'--crf','18','--preset','fast'],stdout=log,stderr=subprocess.STDOUT)
 if p.returncode:raise RuntimeError(name+' failed; see render.log')
 print(name+' complete',flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(render,SPECS))
