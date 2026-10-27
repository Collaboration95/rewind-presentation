import { chromium } from '/Users/speedpowermac/Documents/projects/CODE_MAIN/NUS/SWE5006/rewind-present-audit/node_modules/playwright/index.mjs';
import fs from 'node:fs';
import crypto from 'node:crypto';
const base='https://d2m6kz76y4kuvm.cloudfront.net';
const browser=await chromium.launch({headless:true});
const state={base,password:'Rewind-'+crypto.randomBytes(10).toString('hex'),accounts:{}};
for(const [username,name] of [['maya.tan.27','Maya'],['jun.lim.27','Jun'],['priya.shah.27','Priya']]) {
 const context=await browser.newContext();
 const response=await context.request.post(base+'/api/auth/register',{data:{username,password:state.password}});
 const data=await response.json();
 console.log(name,response.status(),data.account?.id||data.error);
 if(!response.ok()) throw Error(JSON.stringify(data));
 await context.request.patch(base+'/api/auth/profile',{data:{displayName:name}}).then(async r=>console.log('profile',r.status()));
 const account={username,name,storage:await context.storageState(),data};
 state.accounts[name]=account;
}
fs.writeFileSync('videos/work/session.json',JSON.stringify(state,null,2),{mode:0o600});
await browser.close();
