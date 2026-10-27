import {notes,note,context,api} from './hosted.mjs';
const gid=notes.groups.film.group.id;
for(const u of notes.uploads.filter(x=>x.kind==='film'&&x.upload)){
 const ctx=await context(u.account);const r=await api(ctx,`/clips/${u.upload.job.id}?groupId=${gid}`);u.status=r.body.clip?.status||'unknown';note('clip_status',{key:u.key,status:u.status});console.log(u.key,u.status);
 if(process.argv.includes('--retry')&&u.status==='failed'&&!u.manualRetried){u.manualRetried=true;note('retry_requested',{key:u.key});const p=await api(ctx,`/contributions/jobs/${u.upload.job.id}/process?groupId=${gid}`,{});note('retry_response',{key:u.key,status:p.status,result:p.body});console.log('retry',u.key,p.status);}
 await ctx.dispose();
}
