import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {session,save,notes,note,context,api,persist,origin} from './hosted.mjs';
const kind=process.argv[2]||'film';const g=notes.groups[kind];if(!g)throw Error('Group missing');const gid=g.group.id;
const owner=await context('maya');
if(!g.junJoined){
 if(!g.joinInvite){const i=await api(owner,`/real/groups/${gid}/invites`,{});if(i.status!==201)throw Error(JSON.stringify(i));g.joinInvite=i.body.invite;note('invite_created',{kind,invite:g.joinInvite});}
 const jun=await context('jun');let j=await api(jun,'/real/invites/accept',{code:g.joinInvite.code});if(j.status!==200)throw Error(JSON.stringify(j));g.junJoined=true;note('member_joined',{kind,account:'jun',status:j.status});await persist('jun',jun);await jun.dispose();
}
await owner.dispose();
if(process.argv.includes('--join-only'))process.exit(0);
const manifest=JSON.parse(fs.readFileSync(new URL('./upload-plan.json',import.meta.url)));
notes.uploads??=[];
for(const item of manifest){
 let rec=notes.uploads.find(x=>x.kind===kind&&x.key===item.key);
 if(rec?.status==='ready'||rec?.status==='failed')continue;
 if(!rec){rec={kind,...item,idempotencyKey:'film_'+crypto.randomBytes(14).toString('hex'),status:'prepared'};notes.uploads.push(rec);note('upload_prepared',{key:rec.key,account:rec.account});}
 const ctx=await context(rec.account);let select=await api(ctx,'/real/groups/current',{groupId:gid});if(select.status!==200)throw Error(JSON.stringify(select));await persist(rec.account,ctx);
 if(!rec.upload){
 const probe=JSON.parse(execFileSync('ffprobe',['-v','error','-show_streams','-show_format','-of','json',rec.file],{encoding:'utf8'}));const v=probe.streams.find(s=>s.codec_type==='video');const photo=/\.(jpg|jpeg|png)$/i.test(rec.file);const data=fs.readFileSync(rec.file);const mime=photo?(/png$/i.test(rec.file)?'image/png':'image/jpeg'):'video/mp4';const dur=photo?3:Number(probe.format.duration);
 if(data.length>(photo?10:50)*1024*1024||(!photo&&(dur>15||!probe.streams.some(s=>s.codec_type==='audio'))))throw Error('Input limits failed '+rec.file);
 const sr=await ctx.post(`/api/contributions/upload/source?groupId=${encodeURIComponent(gid)}&idempotencyKey=${rec.idempotencyKey}`,{headers:{'Content-Type':mime},data,timeout:60000});const source=await sr.json();note('source_uploaded',{key:rec.key,status:sr.status(),bytes:data.length});if(sr.status()!==201&&sr.status()!==200)throw Error(JSON.stringify(source));
 const u=await api(ctx,`/contributions/upload?groupId=${gid}`,{idempotencyKey:rec.idempotencyKey,sourceUri:source.source.uri,mediaType:photo?'photo':'video',mimeType:mime,byteLength:data.length,durationSeconds:dur,width:v.width,height:v.height,hasAudio:true,mode:rec.mode||'ccd',clientProcessed:false});
 if(u.status!==201&&u.status!==200)throw Error(JSON.stringify(u));rec.upload=u.body.upload;rec.status='pending';note('upload_created',{key:rec.key,upload:rec.upload});
 }
 if(rec.status==='pending'){const p=await api(ctx,`/contributions/jobs/${rec.upload.job.id}/process?groupId=${gid}`,{});note('processing_response',{key:rec.key,status:p.status,result:p.body});}
 const s=await api(ctx,`/clips/${rec.upload.job.id}?groupId=${gid}`);rec.status=s.body.clip?.status||'unknown';note('clip_status',{key:rec.key,status:rec.status});console.log(rec.key,rec.status);await persist(rec.account,ctx);await ctx.dispose();if(rec.status==='unknown')throw Error('Clip status unknown');
}
