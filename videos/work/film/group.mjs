import {execFileSync} from 'node:child_process';
import {session,save,notes,note,context,api,persist} from './hosted.mjs';
const kind=process.argv[2];if(!['collecting','film'].includes(kind))throw Error('kind');
if(notes.groups[kind]){console.log('already created',JSON.stringify(notes.groups[kind]));process.exit(0);}
const runs=JSON.parse(execFileSync('gh',['run','list','--workflow','deploy-dev.yml','--repo','Collaboration95/rewind-app','--limit','8','--json','databaseId,status,conclusion,createdAt,updatedAt,headSha'],{encoding:'utf8'}));
const qualifying=runs.find(r=>r.status==='completed'&&r.conclusion==='success'&&r.updatedAt>'2026-10-26T14:45:00Z');
if(kind==='film'&&!qualifying)throw Error('No qualifying deploy yet');
if(kind==='collecting'&&qualifying)throw Error('Qualifying deploy already complete; do not make compressed collecting group');
if(session.accounts.maya.status!=='ready')throw Error('Maya not ready');
const ctx=await context('maya');
const data={name:kind==='film'?'The little things':'Our everyday',prompt:kind==='film'?'The small moments that made our week':'One small thing worth remembering',maxMembers:6,timeZone:'Asia/Singapore'};
const r=await api(ctx,'/real/groups',data);
if(r.status!==201)throw Error(JSON.stringify(r));
notes.groups[kind]={...r.body,createdAt:new Date().toISOString(),...(qualifying?{deploy:qualifying}:{})};note('group_created',{kind,status:r.status,group:notes.groups[kind]});await persist('maya',ctx);console.log(JSON.stringify(notes.groups[kind]));await ctx.dispose();
