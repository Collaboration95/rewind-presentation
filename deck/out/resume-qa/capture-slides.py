from pathlib import Path
from playwright.sync_api import sync_playwright
import json,re,base64,xml.etree.ElementTree as E
P=Path('/Users/speedpowermac/Documents/projects/CODE_MAIN/NUS/SWE5006/presentation-prep');O=P/'deck/out/resume-qa';(O/'slides').mkdir(exist_ok=True)
with sync_playwright() as w:
 browser=w.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True,args=['--allow-file-access-from-files'])
 page=browser.new_page(viewport={'width':1280,'height':720},device_scale_factor=1)
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://127.0.0.1:8791/deck/deck.html',wait_until='load');page.evaluate('document.fonts.ready')
 slides=page.evaluate("[...document.querySelectorAll('section.slide')].map(s=>({id:s.id,kind:s.dataset.kind,sec:s.dataset.sec,time:+s.dataset.time,title:s.querySelector('h1').textContent}))")
 report=[]
 for n,s in enumerate(slides):
  page.evaluate('(n)=>window.deck.go(n)',n)
  page.evaluate("Promise.all([...document.querySelectorAll('.slide.active img')].map(i=>i.decode().catch(()=>{})))")
  page.screenshot(path=str(O/'slides'/f'{n+1:02d}-{s["id"]}.png'),animations='disabled')
  d=page.evaluate('''() => {const s=document.querySelector('.slide.active');const bad=[];for(const e of s.querySelectorAll('h1,.body *,.foot')){if(e.closest('[hidden],aside,.commands,.pipeline-overlay,.fig-placeholder'))continue;const c=getComputedStyle(e),b=e.getBoundingClientRect();if(c.display==='none'||c.visibility==='hidden'||b.width===0||b.height===0)continue;if(b.left<-.5||b.top<-.5||b.right>1280.5||b.bottom>720.5)bad.push({tag:e.tagName,cls:e.className,text:e.textContent.slice(0,100),b:b.toJSON()});}return {bad,broken:[...s.querySelectorAll('img')].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.alt),figure:[...s.querySelectorAll('.diagram img')].map(i=>({src:i.src,b:i.getBoundingClientRect().toJSON()}))}}''')
  for f in d['figure']:
   root=E.fromstring(base64.b64decode(f.pop('src').split(',',1)[1]));vb=root.attrib['viewBox'].split();nw,nh=map(float,vb[2:]);m=min(float(t.attrib.get('font-size',100)) for t in root.iter() if t.tag.endswith('}text'));f['minFont']=round(m*min(f['b']['width']/nw,f['b']['height']/nh),3)
  d['textOverflow']=page.evaluate("""() => {const s=document.querySelector('.slide.active'),body=s.querySelector('.body'),br=body.getBoundingClientRect(),a=[];for(const e of s.querySelectorAll('h1,.body td,.body p,.body pre,.body .confirmation,.body .demo-actions')){if(e.closest('[hidden],aside,.commands,.pipeline-overlay,.figure-fallback'))continue;const r=document.createRange();r.selectNodeContents(e);const c=getComputedStyle(e);if(c.display==='none'||c.visibility==='hidden')continue;for(const b of r.getClientRects()){if(b.right>1280.5||b.bottom>720.5||(!s.matches('.figure-slide,.chart-slide')&&e.closest('.body')&&b.bottom>br.bottom+1))a.push({text:e.textContent.slice(0,95),right:b.right,bottom:b.bottom,bodyBottom:br.bottom})}}return a}""")
  report.append({**s,**d})
  if n%8==7:print(f'Rendered {n+1}/{len(slides)}',flush=True)
 # Verify all stage clips load paused/muted and have metadata.
 media=[]
 for s in slides:
  if s['kind']=='clip' or s['id']=='s18':
   page.evaluate('(id)=>window.deck.go(window.deck.slides.findIndex(s=>s.id===id))',s['id'])
   v=page.locator('.slide.active video')
   v.evaluate('(v)=>new Promise((r,j)=>{if(v.readyState>=2)return r();v.addEventListener("loadeddata",r,{once:true});v.addEventListener("error",j,{once:true})})')
   media.append({'id':s['id'],**v.evaluate('(v)=>({duration:v.duration,width:v.videoWidth,height:v.videoHeight,paused:v.paused,muted:v.muted})')})
 (O/'media-check.json').write_text(json.dumps(media,indent=2))
 # Verify keys, notes and overview, clip playback and pause-on-leave.
 page.evaluate('window.deck.go(0)');page.keyboard.press('ArrowRight');keys={'arrow':page.locator('.slide.active').get_attribute('id')=='s2'}
 page.keyboard.press('n');keys['notes']=page.locator('#notes').is_visible();page.keyboard.press('n')
 page.keyboard.press('o');keys['overview']=page.locator('#ov').is_visible();keys['overviewFrames']=page.locator('#ov .th').count();page.locator('#ov .th').nth(3).click();keys['overviewClick']=page.locator('.slide.active').get_attribute('id')=='s4'
 page.goto('http://127.0.0.1:8791/deck/deck.html#F5');keys['hash']=page.locator('.slide.active').get_attribute('id')=='F5'
 page.keyboard.press('Space');v=page.locator('#F5 video');v.evaluate('(v)=>new Promise((r,j)=>{if(v.readyState>=2)return r();v.onloadeddata=r;v.onerror=j})');page.wait_for_timeout(300);keys['clipPlays']=v.evaluate('(v)=>!v.paused');keys['mutedDefault']=v.evaluate('(v)=>v.muted');page.keyboard.press('Space');keys['spacePauses']=v.evaluate('(v)=>v.paused');page.locator('#F5 .iphone-screen').click();keys['clickPlays']=v.evaluate('(v)=>!v.paused');page.keyboard.press('m');keys['manualUnmute']=v.evaluate('(v)=>!v.muted');page.keyboard.press('r');keys['restartPauses']=v.evaluate('(v)=>v.paused&&v.currentTime<0.1');page.keyboard.press('ArrowRight');keys['clipPausesOnLeave']=v.evaluate('(v)=>v.paused')
 page.goto('http://127.0.0.1:8791/deck/deck.html#s18');page.keyboard.press('c');keys['commands']=page.locator('#s18 .commands').is_visible()
 (O/'render-check.json').write_text(json.dumps({'viewport':[1280,720],'slides':report,'pageErrors':errors,'controls':keys},indent=2))
 print(json.dumps({'frames':len(slides),'bounds':[(x['id'],x['bad']) for x in report if x['bad']],'broken':[(x['id'],x['broken']) for x in report if x['broken']],'textOverflow':[(x['id'],x['textOverflow']) for x in report if x['textOverflow']],'smallFigures':[(x['id'],x['figure']) for x in report if any(f['minFont']<14 for f in x['figure'])],'controls':keys,'errors':errors},indent=2))
 browser.close()
