const fs=require('fs'),path=require('path'),http=require('http');
const {stripTypeScriptTypes}=require('node:module');
const {chromium}=require('/Users/speedpowermac/Documents/projects/CODE_MAIN/NUS/SWE5006/rewind-present-audit/node_modules/playwright');
const ROOT=__dirname,origin='https://d2m6kz76y4kuvm.cloudfront.net';
const mime={'.html':'text/html','.js':'text/javascript','.css':'text/css','.png':'image/png','.jpg':'image/jpeg','.mp4':'video/mp4','.ttf':'font/ttf','.json':'application/json','.mjs':'text/javascript'};
async function startServer(){const server=http.createServer((q,r)=>{let rel=decodeURIComponent(new URL(q.url,'http://localhost').pathname),p=path.resolve(ROOT,'.'+rel);if(!p.startsWith(ROOT+path.sep)){r.writeHead(403);r.end();return;}fs.stat(p,(err,st)=>{if(err||!st.isFile()){r.writeHead(404);r.end();return;}let h={'Content-Type':mime[path.extname(p)]||'application/octet-stream','Cache-Control':'no-store','Accept-Ranges':'bytes'};if(q.headers.range){let m=q.headers.range.match(/bytes=(\d+)-(\d*)/),a=+m[1],b=m[2]?Math.min(+m[2],st.size-1):st.size-1;r.writeHead(206,{...h,'Content-Length':b-a+1,'Content-Range':`bytes ${a}-${b}/${st.size}`});fs.createReadStream(p,{start:a,end:b}).pipe(r);}else{r.writeHead(200,{...h,'Content-Length':st.size});fs.createReadStream(p).pipe(r);}});});await new Promise(ok=>server.listen(8896,'127.0.0.1',ok));return server;}
(async()=>{
 fs.mkdirSync(path.join(ROOT,'assets/fonts'),{recursive:true});
 const audit=path.resolve(ROOT,'../../../../rewind-present-audit');
 const retro=fs.readFileSync(path.join(audit,'src/capture/retro-looks.ts'),'utf8').replace(/^import type .*;\n/m,'');
 const look=fs.readFileSync(path.join(audit,'src/capture/LookPreview.tsx'),'utf8');
 const fn=look.slice(look.indexOf('export function lookOverlays('),look.indexOf('/** Web presentation only;'));
 const moduleCode=stripTypeScriptTypes(retro+'\nlet capturedGrainUrl="none"; export function setGrain(s:string){capturedGrainUrl=s} function grainImage(){return capturedGrainUrl}\n'+fn,{mode:'strip'});
 fs.writeFileSync(path.join(ROOT,'source/retro.mjs'),moduleCode);

 let sources=fs.readdirSync(path.join(ROOT,'source')).filter(n=>n.endsWith('.html'));
 const urls=new Set();for(const n of sources){const s=fs.readFileSync(path.join(ROOT,'source',n),'utf8');for(const m of s.matchAll(/url\(["']?(\/assets\/[^)"']+)["']?\)/g))urls.add(m[1]);}
 for(const u of urls){const r=await fetch(origin+u);if(!r.ok)throw Error('font fetch '+r.status);fs.writeFileSync(path.join(ROOT,'assets/fonts',path.basename(u)),Buffer.from(await r.arrayBuffer()));}
 for(const n of sources){let s=fs.readFileSync(path.join(ROOT,'source',n),'utf8');for(const u of urls)s=s.split(u).join('../assets/fonts/'+path.basename(u));fs.writeFileSync(path.join(ROOT,'source',n),s);}
 const server=await startServer();const browser=await chromium.launch({headless:true,channel:'chrome'});const context=await browser.newContext({viewport:{width:402,height:714},deviceScaleFactor:3});const p=await context.newPage();
 async function load(name){await p.goto('http://127.0.0.1:8896/source/'+name+'.html');await p.evaluate(()=>document.fonts.ready);}
 async function fixLook(kind,variant){await p.evaluate(async({kind,variant})=>{
 const mod=await import('./retro.mjs');const root=document.querySelector('[data-testid="'+(kind==='photo'?'photo-live-look':'video-live-look')+'"]');
 const media=root.firstElementChild;const grain=root.querySelector('[data-rw="look-grain"]');mod.setGrain(grain?grain.style.backgroundImage:'none');
 const w=kind==='photo'?1600:720,h=kind==='photo'?2400:1280,scale=Math.max(402/w,714/h),bw=w*scale,bh=h*scale;
 const overlay=document.createElement('div');Object.assign(overlay.style,{pointerEvents:'none',position:'absolute',left:(402-bw)/2+'px',top:(714-bh)/2+'px',width:bw+'px',height:bh+'px'});
 const src=mod.fitWithin(w,h,2160),mode=kind==='video'?'vhs':variant==='default'?'ccd':'disposable-flash';
 for(const spec of mod.lookOverlays(mode,{width:bw,height:bh},src)){const layer=document.createElement('div');Object.assign(layer.style,{position:'absolute',inset:'0',pointerEvents:'none'},spec.style);if(spec.rw)layer.dataset.rw=spec.rw;overlay.append(layer)}
 root.replaceChildren(media,overlay);
 },{kind,variant});}
 async function save(name){fs.writeFileSync(path.join(ROOT,'source',name+'.html'),await p.content());await p.screenshot({path:path.join(ROOT,'states',name+'.png'),animations:'disabled'});console.log('built',name);}
 async function live(kind,count,variant){
  await load(variant==='default'?'photo-default-real':kind+'-live-real');
  const ref=fs.readFileSync(path.join(ROOT,'source',kind+'-review.html'),'utf8');
  await p.evaluate(html=>{const doc=new DOMParser().parseFromString(html,'text/html');document.querySelector('[data-testid="camera-allowance"]').replaceWith(doc.querySelector('[data-testid="camera-allowance"]').cloneNode(true));},ref);
  await p.evaluate(({kind,count})=>{
   const root=document.querySelector('[data-rw="viewfinder"]');
   
   const moments=root.querySelector('[data-testid="camera-your-moments"]');
   if(kind==='photo')moments.remove();else{for(const el of moments.querySelectorAll('*'))if(!el.children.length&&el.textContent==='2')el.textContent='1';moments.setAttribute('aria-label','Your moments: 1 sealed');}
   const look=root.querySelector(`[data-testid="${kind==='photo'?'photo':'video'}-live-look"]`),layer=look.firstElementChild;
   const media=document.createElement(kind==='photo'?'img':'video');
   media.src='../assets/'+(kind==='photo'?'friends-selfie.jpg':'friends-food.mp4');media.style.cssText='position:absolute;inset:0;width:100%;height:100%;object-fit:cover';
   if(kind==='video'){media.muted=true;media.setAttribute('muted','');media.autoplay=true;media.loop=true;media.playsInline=true;}
   layer.replaceChildren(media);
   root.style.height='714px';
  },{kind,count});
  await fixLook(kind,variant);await p.waitForTimeout(500);await save(variant==='default'?'photo-default':kind+'-live');
 }
 await live('photo',0,'default');await live('photo',0);await live('video',1);
 await load('video-recording-real');
 await p.evaluate(()=>{
  const root=document.querySelector('[data-rw="viewfinder"]');
  
  const look=root.querySelector('[data-testid="video-live-look"]');const v=document.createElement('video');v.src='../assets/friends-food.mp4';v.autoplay=true;v.muted=true;v.setAttribute('muted','');v.playsInline=true;v.loop=true;v.style.cssText='position:absolute;inset:0;width:100%;height:100%;object-fit:cover';look.firstElementChild.replaceChildren(v);
 });await fixLook('video');await p.waitForTimeout(400);
 const ref=fs.readFileSync(path.join(ROOT,'source/video-review.html'),'utf8');await p.evaluate(html=>{const d=new DOMParser().parseFromString(html,'text/html');document.querySelector('[data-testid="camera-allowance"]').replaceWith(d.querySelector('[data-testid="camera-allowance"]').cloneNode(true));},ref);await save('video-recording');
 await load('video-review');
 
 await p.evaluate(()=>{for(const v of document.querySelectorAll('video')){v.src='../assets/friends-food.mp4';v.muted=true;v.setAttribute('muted','');v.playsInline=true;v.preload='auto';v.autoplay=true;v.loop=true;}});await p.waitForTimeout(800);
 await p.locator('video').first().evaluate(async v=>{await v.play();v.currentTime=1;await new Promise(r=>v.addEventListener('seeked',r,{once:true}));v.pause();});
 await save('video-review-ready');
 await browser.close();await new Promise(ok=>server.close(ok));
 console.log('BUILD_COMPLETE');
})();
