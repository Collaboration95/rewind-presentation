from pathlib import Path
import json
R=Path(__file__).resolve().parent
V=R.parents[1]
S=V/'work/stills'
F=V/'work/film/rewind-hosted-film.mp4'
def seg(src,duration,start=0,end=None,note='',audio=False):
 d={'source':str(src),'in':start,'duration':duration,'audio':audio,'note':note}
 if end is not None:d['out']=end
 return d
def write(number,name,slug,segments,notes):
 spec={'number':number,'name':name,'title_card':False,'output':slug+'.mp4','notes':notes,'segments':segments}
 (R/(slug+'.edl.json')).write_text(json.dumps(spec,indent=2)+'\n')
 lines=[f'TITLE: {number:02} {name}','FCM: NON-DROP FRAME','FPS: 30','']
 def tc(t):
  f=round(t*30);return f'{f//108000:02}:{f//1800%60:02}:{f//30%60:02}:{f%30:02}'
 t=0
 for i,s in enumerate(segments):
  dur=s['duration'];a=s.get('in',0);b=s.get('out',a+dur)
  lines+=[f'{i+1:03} AX V C {tc(a)} {tc(b)} {tc(t)} {tc(t+dur)}',f'* SOURCE: {s["source"]}',f'* {s["note"]}',f'* AUDIO: {json.dumps(s["audio"])}',''];t+=dur
 (R/(slug+'.edl')).write_text('\n'.join(lines)+'\n')
write(9,'Cycle ends, film ready','09-cycle-ends-film-ready',[
 seg(S/'09-premiere-clean.png',8,note='Parent-approved clean actual Premiere Home still; forbidden cycle UI removed.'),
 seg(V/'raw/09-premiere.mov',8,25,32.8,'Read group settings: The little things, owner and 2 of 6 members. Last 0.2 s held.'),
 seg(V/'raw/09-premiere.mov',8,34,42,'Members: Maya and Jun.'),
 seg(V/'raw/09-premiere.mov',8,90,98,'Return to group settings and prompt context.'),
 seg(S/'09-premiere-clean.png',8,note='Return to clean Premiere ready card, Watch and 24 h left preserved.')
],['40 seconds; five 8-second states. No film shown. All Home frames are the parent cleaned actual still. No cycle-length UI. Silence.'])
write(10,'Watch the film','10-watch-the-film',[
 seg(V/'raw/10-watch.mov',131/30,14.8,17.166666667,'Opening film UI only; initial Home excluded. Actual 2.3667 s plus a 2 s loading-frame hold.'),
 seg(V/'raw/10-watch.mov',21.2,17.896666667,39.096666667,'Complete first native film. Native fullscreen startup repeats trimmed to match first photo at film t=0. All five contributions retained.',{'source':str(F),'in':0}),
 seg(V/'raw/10-watch.mov',8,109.72,117.72,'Native last frame paused, then actual replay action at boundary; long idle removed.'),
 seg(V/'raw/10-watch.mov',21.2,117.96,139.16,'Complete native replay, photo and later scene boundaries aligned to real film audio t=0.',{'source':str(F),'in':0}),
 seg(V/'raw/10-watch.mov',8,139.16,147.16,'Native playback finishes; pause controls appear.'),
 seg(V/'raw/10-watch.mov',217/30,155,162.233333333,'Native controls and real Close transition to application end UI.'),
 seg(V/'raw/10-watch.mov',10,168,178,'Actual application The end / Replay / Save film screen, ten seconds.')
],['80 seconds. Only real supplied phone footage. No Home shot. Two complete 21.2-second film intervals use external real film AAC from zero; all other audio silent. Scene-cut matching: source first 20.8967/23.9283/29.9600/35.9933 vs film 3/6.0333/12.0667/18.1; replay 120.9600/123.9933/130.0233/136.0617. Match error <= one 30fps frame after startup-repeat trim.'])
flag=S/'11-done.txt'
if flag.exists():
 (R/'11-source-ready.txt').write_text(flag.read_text())
 write(11,'Archive and save','11-archive-and-save',[
  seg(V/'raw/11-archive-save.mov',8,46,54,'Read real Archive card: Your film is here, Cycle ended 26 Oct. No Home shot.'),
  seg(V/'raw/11-archive-save.mov',4,54,58,'Actual Play and loading transition to native player.'),
  seg(V/'raw/11-archive-save.mov',3,59,62,'Brief actual native film: first photo into second contribution; silent by choice.'),
  seg(V/'raw/11-archive-save.mov',3,74,77,'Brief actual native film near ending; playback shortened for Archive/Save focus.'),
  seg(V/'raw/11-archive-save.mov',3,178.5,181.5,'Actual native Close returning to real app end UI.'),
  seg(V/'raw/11-archive-save.mov',6,184,190,'Read actual The end / Replay / Save film screen.'),
  seg(V/'raw/11-archive-save.mov',5,190.5,195.4,'Actual Save film action and Saving/Saved state. Final 0.1 s held; stops before any browser prompt transition.'),
  seg(V/'raw/11-archive-save.mov',5,294.2,299.2,'Real Safari download confirmation and Download acceptance. Password interlude entirely omitted.'),
  seg(V/'raw/11-archive-save.mov',4,333.5,337.5,'Actual Safari page menu Downloads action and completed-list transition.'),
  seg(S/'11-downloaded.png',8,note='Parent clean actual phone proof: completed film in Safari Downloads, 5.2 MB. Entire later Files/Spotlight tail omitted.'),
  seg(S/'11-archive.png',6,note='Closing real Archive card still; editorial return to feature context, no fabricated tap.')
 ],['55 seconds, entirely silent AAC. Raw 11 first read only after 11-done.txt existed. All film frames are actual native footage; brief playback montage, no replacement film. Real Save -> Download confirmation -> Safari completed 5.2 MB download list. Save Password prompt and entire tail after Downloads omitted. Closing Archive is explicitly an editorial still, not an additional recorded navigation.'])
