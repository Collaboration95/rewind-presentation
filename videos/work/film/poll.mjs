import fs from 'node:fs';
import crypto from 'node:crypto';
import {dir,session,save,notes,note,context,api,persist} from './hosted.mjs';
const ctx=await context('jun');let previous=null;let changed=false;
try{
const h=await api(ctx,'/health');const now=new Date().toISOString();const g=notes.groups.film;
if(!g){console.log(JSON.stringify({at:now,health:h.status,group:'waiting_for_deploy'}));process.exitCode=0;}
else{
const groupId=g.group.id;const cycleId=g.cycle.id;const group=await api(ctx,`/real/groups/${groupId}`);
const release=group.body.group?.releases?.find(x=>x.cycleId===cycleId);const state=release?.state||'locked';
const summary={at:now,health:h.status,groupStatus:group.status,currentCycle:group.body.group?.cycle,premiere:{state,cycleId}};
console.log(JSON.stringify(summary));notes.lastPoll=summary;note('poll',{health:h.status,groupStatus:group.status,premiere:state});
if(['premiere','archived'].includes(state)&&!notes.film){
 const current=await api(ctx,'/real/groups/current');previous=current.body.group?.group?.id;
 if(previous!==groupId){const select=await api(ctx,'/real/groups/current',{groupId});if(select.status!==200)throw Error('Cannot select film group');changed=true;note('temporary_group_selection',{account:'jun',previous,selected:groupId});}
 const p=await api(ctx,`/cycles/${cycleId}/premiere?groupId=${groupId}`);
 if(p.body.premiere?.state!=='ready')throw Error('Published film not yet servable '+p.status);
 const a=await api(ctx,`/archive?groupId=${groupId}`);if(a.status!==200)throw Error('Archive unavailable '+a.status);
 const film=a.body.archive.films.find(f=>f.cycleId===cycleId)||a.body.archive.films.find(f=>f.id===p.body.premiere.filmId);if(!film?.downloadPath)throw Error('No authorized Archive film download');
 session.media={account:'jun',premiere:p.body.premiere,archive:a.body,refreshedAt:now};save();
 const outsider=await context('priya');const denied=await outsider.get('/api'+film.downloadPath);const outsiderGroup=await api(outsider,`/real/groups/${groupId}`);note('outsider_denial',{downloadStatus:denied.status(),groupStatus:outsiderGroup.status});await outsider.dispose();if(![401,403,404].includes(denied.status()))throw Error('Outsider unexpectedly accessed film');
 const d=await ctx.get('/api'+film.downloadPath,{timeout:60000});if(d.status()!==200)throw Error('Download '+d.status());const b=await d.body();const target=dir+'rewind-hosted-film.mp4';fs.writeFileSync(target,b);
 notes.film={id:film.id,cycleId,groupId,file:target,downloadedAt:now,bytes:b.length,sha256:crypto.createHash('sha256').update(b).digest('hex'),contentType:d.headers()['content-type'],contentDisposition:d.headers()['content-disposition'],segments:p.body.premiere.segments,outsiderDenied:true,archiveSaveReady:true};note('film_downloaded',notes.film);console.log('FILM_READY',target,b.length);
}
}
}finally{if(changed&&previous){const restored=await api(ctx,'/real/groups/current',{groupId:previous});note('group_selection_restored',{account:'jun',groupId:previous,status:restored.status});}await persist('jun',ctx);await ctx.dispose();}
