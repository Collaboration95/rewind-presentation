import fs from 'node:fs';
import crypto from 'node:crypto';
import {chromium} from '/Users/speedpowermac/Documents/projects/CODE_MAIN/NUS/SWE5006/rewind-present-audit/node_modules/playwright/index.mjs';
import {dir,origin,session,notes,note,context,api} from './hosted.mjs';
if(!notes.film)throw Error('Real film not ready');
const control=await context('jun');const current=await api(control,'/real/groups/current');const previous=current.body.group?.group?.id;const filmGroup=notes.groups.film.group.id;const changed=previous!==filmGroup;if(changed){const selected=await api(control,'/real/groups/current',{groupId:filmGroup});if(selected.status!==200)throw Error('Cannot select released film');}let browser;try{
browser=await chromium.launch({channel:'chrome',headless:true,downloadsPath:dir+'downloads'});
const ctx=await browser.newContext({storageState:session.accounts.jun.storageState,viewport:{width:430,height:932},acceptDownloads:true});const page=await ctx.newPage();
await page.goto(origin,{waitUntil:'domcontentloaded',timeout:60000});await page.getByText('Archive',{exact:true}).click();await page.getByTestId('real-archive-play').waitFor({timeout:20000});
await page.screenshot({path:dir+'archive-ready.png',fullPage:true});
await page.getByTestId('real-archive-play').click();await page.getByTestId('real-film').waitFor({timeout:20000});
await page.screenshot({path:dir+'film-playback.png',fullPage:true});
await page.getByTestId('real-film-end').waitFor({timeout:55000});await page.screenshot({path:dir+'film-end-save.png',fullPage:true});
const downloadPromise=page.waitForEvent('download',{timeout:45000});await page.getByTestId('real-film-save').click();const download=await downloadPromise;const target=dir+'rewind-archive-save.mp4';await download.saveAs(target);const b=fs.readFileSync(target);
notes.uiSave={at:new Date().toISOString(),file:target,bytes:b.length,sha256:crypto.createHash('sha256').update(b).digest('hex'),suggestedFilename:download.suggestedFilename(),matchesAuthenticatedDownload:crypto.createHash('sha256').update(b).digest('hex')===notes.film.sha256};note('ui_save',notes.uiSave);console.log(JSON.stringify(notes.uiSave));await page.screenshot({path:dir+'film-saved.png',fullPage:true});}finally{if(browser)await browser.close();if(changed&&previous){const r=await api(control,'/real/groups/current',{groupId:previous});note('ui_group_selection_restored',{account:'jun',groupId:previous,status:r.status});}await control.dispose();}
