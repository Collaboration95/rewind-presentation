import fs from 'node:fs';
import {chromium} from '/Users/speedpowermac/Documents/projects/CODE_MAIN/NUS/SWE5006/rewind-present-audit/node_modules/playwright/index.mjs';
import {dir,origin,session,save,notes,note} from './hosted.mjs';
const who=process.argv[2]||'maya';const tag=process.argv[3]||'hosted-home';
const browser=await chromium.launch({headless:true,downloadsPath:dir+'downloads'});
const ctx=await browser.newContext({storageState:session.accounts[who].storageState,viewport:{width:430,height:932},deviceScaleFactor:1});
const page=await ctx.newPage();await page.goto(origin,{waitUntil:'domcontentloaded',timeout:60000});await page.getByText(notes.groups.film?.group.name||notes.groups.collecting?.group.name,{exact:true}).first().waitFor({timeout:15000}).catch(()=>{});
await page.screenshot({path:dir+tag+'.png',fullPage:true});console.log((await page.locator('body').innerText()).slice(0,4500));note('screenshot',{account:who,file:tag+'.png',url:page.url()});await browser.close();
