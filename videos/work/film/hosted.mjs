import fs from 'node:fs';
import crypto from 'node:crypto';
import {request} from '/Users/speedpowermac/Documents/projects/CODE_MAIN/NUS/SWE5006/rewind-present-audit/node_modules/playwright/index.mjs';
export const dir = new URL('.',import.meta.url).pathname;
export const origin='https://d2m6kz76y4kuvm.cloudfront.net';
export const sessionFile=dir+'session.json';
export let session=fs.existsSync(sessionFile)?JSON.parse(fs.readFileSync(sessionFile)): {origin,createdAt:new Date().toISOString(),accounts:Object.fromEntries([['maya','maya.chen.27','Maya'],['jun','jun.lee.27','Jun'],['priya','priya.nair.27','Priya']].map(([key,username,displayName])=>[key,{username,displayName,password:'Rw!'+crypto.randomBytes(18).toString('base64url'),status:'prepared',attempts:[]}]))};
export function save(){fs.writeFileSync(sessionFile,JSON.stringify(session,null,2),{mode:0o600});fs.chmodSync(sessionFile,0o600);}
save();
export const notesFile=dir+'production-notes.json';
export let notes=fs.existsSync(notesFile)?JSON.parse(fs.readFileSync(notesFile)): {origin,createdAt:new Date().toISOString(),receipts:[],groups:{}};
export function note(kind,data){notes.receipts.push({at:new Date().toISOString(),kind,...data});fs.writeFileSync(notesFile,JSON.stringify(notes,null,2));}
export async function context(key){return request.newContext({baseURL:origin,extraHTTPHeaders:{Origin:origin},...(session.accounts[key]?.storageState?{storageState:session.accounts[key].storageState}:{})});}
export async function persist(key,ctx){session.accounts[key].storageState=await ctx.storageState();save();}
export async function api(ctx,path,data){let r=await ctx[data===undefined?'get':'post']('/api'+path,data===undefined?{}:{data});let t=await r.text();let b;try{b=JSON.parse(t)}catch{b={text:t.slice(0,300)}};return {status:r.status(),body:b,retryAfter:r.headers()['retry-after']};}
if(process.argv[2]==='accounts'){
 for(const [key,a] of Object.entries(session.accounts)){
  if(a.status==='ready')continue;
  const ctx=await context(key);
  if(a.status==='prepared'||a.status==='rate_limited'){
   if(a.retryAt&&Date.now()<Date.parse(a.retryAt)&&!process.argv.includes('--after-deploy')){console.log(key,'retry scheduled',a.retryAt);await ctx.dispose();break;}
   a.attempts.push({at:new Date().toISOString(),kind:'register',state:'requested'});save();
   const r=await api(ctx,'/auth/register',{username:a.username,password:a.password});
   a.attempts.at(-1).result=r.status;save();note('register',{account:key,status:r.status,retryAfter:r.retryAfter});
   if(r.status===429){a.status='rate_limited';a.retryAt=new Date(Date.now()+Number(r.retryAfter||900)*1000).toISOString();save();console.log(key,'rate limited until',a.retryAt);await ctx.dispose();break;}
   if(r.status!==201)throw Error(JSON.stringify({key,...r}));
   a.status='registered';a.account=r.body.account;save();
  }
  const l=await api(ctx,'/auth/login',{username:a.username,password:a.password,clientType:'browser'});await persist(key,ctx);
  if(l.status!==200)throw Error(JSON.stringify({key,...l}));
  const p=await api(ctx,'/auth/profile',{displayName:a.displayName});await persist(key,ctx);
  if(p.status!==200)throw Error(JSON.stringify({key,...p}));
  a.account=p.body.account;a.status='ready';a.readyAt=new Date().toISOString();save();note('account_ready',{account:key,username:a.username,displayName:a.displayName});console.log(key,'ready',a.username);await ctx.dispose();
 }
}
