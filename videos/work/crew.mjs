import { request,chromium } from '/Users/speedpowermac/Documents/projects/CODE_MAIN/NUS/SWE5006/rewind-present-audit/node_modules/playwright/index.mjs';
import fs from 'node:fs';
const s=JSON.parse(fs.readFileSync('videos/work/film/session.json'));
const who=process.argv[2]||'jun',method=process.argv[3]||'GET',path=process.argv[4]||'/api/real/groups';
const ctx=await request.newContext({baseURL:s.origin,storageState:s.accounts[who].storageState});
const r=await ctx.fetch(path,{method,data:process.argv[5]?JSON.parse(process.argv[5]):undefined});
const body=await r.text();console.log(JSON.stringify({status:r.status(),body:JSON.parse(body)}));
await ctx.dispose();
