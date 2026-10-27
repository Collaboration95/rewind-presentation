const fs=require('fs'),path=require('path'),readline=require('readline');
const {chromium}=require('/Users/speedpowermac/Documents/projects/CODE_MAIN/NUS/SWE5006/rewind-present-audit/node_modules/playwright');
const OUT=__dirname, BASE=path.resolve(OUT,'../..');
const GROUP='real-group-55f1f1de-e005-4421-b591-38c1a12625b6';
let browser,context,page,liveContext,livePage;
async function snap(name,p=page){ await p.screenshot({path:path.join(OUT,'states',name+'.png'),animations:'disabled'});console.log('snapshot',name); }
async function tree(p=page){console.log((await p.locator('body').innerText()).slice(0,18000));console.log('buttons',await p.getByRole('button').evaluateAll(es=>es.map(e=>({name:e.getAttribute('aria-label'),text:e.innerText,test:e.getAttribute('data-testid')}))));}
(async()=>{
 const session=JSON.parse(fs.readFileSync(path.join(BASE,'work/film/session.json'),'utf8'));
 browser=await chromium.launch({headless:true,channel:'chrome',args:['--use-fake-device-for-media-stream','--use-fake-ui-for-media-stream','--autoplay-policy=no-user-gesture-required']});
 context=await browser.newContext({viewport:{width:402,height:714},deviceScaleFactor:3,storageState:session.accounts.maya.storageState,permissions:[]});
 await context.addInitScript(()=>{navigator.mediaDevices.getUserMedia=()=>Promise.reject(new DOMException('Permission denied','NotAllowedError'));});
 page=await context.newPage();
 page.setDefaultTimeout(18000);
 await page.goto(session.origin,{waitUntil:'domcontentloaded'});
 await page.getByTestId('real-home').waitFor({timeout:25000}).catch(()=>{});
 console.log('READY',page.url());await tree();
 const rl=readline.createInterface({input:process.stdin});
 for await(const cmd of rl){try{const out=await eval('(async()=>{'+cmd+'})()');if(out!==undefined)console.log(out);}catch(e){console.log('ERROR',e.message);}console.log('COMMAND_DONE');}
 await browser.close();
})();
