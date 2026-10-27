// Capture the CI/CD video frames (everything except 00-pipeline and 99-decisions).
// Live frames: public GitHub pages, logged out. Replica frames: built only from
// gh CLI evidence in ./evidence. Terminal frames: real command output in ./evidence/terminal.
// Usage: node capture-frames.cjs [frame-id ...]
const {chromium}=require('/Users/speedpowermac/Documents/projects/CODE_MAIN/NUS/SWE5006/rewind-present-audit/node_modules/playwright');
const fs=require('fs');const path=require('path');
const root=__dirname, EV=path.join(root,'evidence'), FR=path.join(root,'frames'), PG=path.join(root,'pages');
const REPO='https://github.com/Collaboration95/rewind-app';
// Both Playwright Chromium contexts are viewport 1920x1080, deviceScaleFactor 2 -> 3840x2160 PNG. Public pages are
// clipped to the top 1920x1025 and placed under a 55 px URL bar in the wrapper. Legibility: html{zoom:1.25}, so layouts are 1536x864 / 1536x820 CSS px.
const W=1920, H=1080, DSF=2, Z=1.25, VW=W/Z, VH=H/Z, BAR=44, ZOOM=`html{zoom:${Z}}`;
const J=f=>JSON.parse(fs.readFileSync(path.join(EV,f),'utf8'));
const T=f=>fs.readFileSync(path.join(EV,f),'utf8');
const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const ago=(iso)=>new Date(iso).toUTCString().replace(' GMT',' UTC');

// ---------- shared look ----------
const FONT=`-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",Helvetica,Arial,sans-serif`;
const MONO=`ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace`;
const chromeCSS=`*{box-sizing:border-box}html,body{margin:0;width:${VW}px;height:${VH}px;overflow:hidden;background:#fff;font-family:${FONT}}
.bar{height:${BAR}px;background:#dee1e6;display:flex;align-items:center;gap:14px;padding:0 16px;border-bottom:1px solid #c4c7cc}
.dots span{display:inline-block;width:12px;height:12px;border-radius:50%;margin-right:7px}.url{flex:1;height:30px;border-radius:15px;background:#fff;display:flex;align-items:center;padding:0 16px;font-size:14px;color:#202124}
.url b{font-weight:400;color:#5f6368}.lock{width:12px;height:12px;margin-right:10px;border:2px solid #5f6368;border-radius:3px}.view{position:absolute;top:${BAR}px;left:0;width:${VW}px;height:${VH-BAR}px;overflow:hidden}`;
const chrome=(url,inner)=>{const u=url.replace(/^https:\/\//,'');const i=u.indexOf('/');return `<div class="bar"><div class="dots"><span style="background:#ff5f57"></span><span style="background:#febc2e"></span><span style="background:#28c840"></span></div><div class="url"><div class="lock"></div>${esc(i<0?u:u.slice(0,i))}<b>${esc(i<0?'':u.slice(i))}</b></div></div><div class="view">${inner}</div>`;};

const ghCSS=`.gh{font-size:14px;color:#1f2328;line-height:1.5}.gh a{color:#0969da;text-decoration:none}
.top{height:64px;background:#f6f8fa;border-bottom:1px solid #d1d9e0;display:flex;align-items:center;padding:0 16px;gap:12px}.top .crumb{font-size:14px}.top .crumb b{font-weight:600}.top .sp{flex:1}.av{width:32px;height:32px;border-radius:50%;background:#8e6b4c;display:inline-block}
.tabs{display:flex;gap:6px;padding:0 16px;background:#f6f8fa;border-bottom:1px solid #d1d9e0;height:48px;align-items:flex-end}.tabs span{padding:0 8px 12px;font-size:14px;color:#1f2328;border-bottom:2px solid transparent}.tabs span.on{border-color:#fd8c73;font-weight:600}.cnt{background:#818b981f;border-radius:10px;padding:0 6px;font-size:12px;margin-left:4px}
.wrap{display:flex;gap:24px;padding:24px 32px}.side{width:256px;flex:none}.side .grp{font-size:12px;color:#59636e;font-weight:600;margin:16px 8px 6px}.side div.it{padding:6px 8px;border-radius:6px;font-size:14px}.side div.it.on{background:#818b981a;font-weight:600;box-shadow:inset 3px 0 #0969da}
.main{flex:1;min-width:0}h2.t{font-size:24px;font-weight:400;margin:0 0 8px;padding-bottom:8px;border-bottom:1px solid #d1d9e0}.box{border:1px solid #d1d9e0;border-radius:6px;background:#fff}.mut{color:#59636e}
.cb{display:flex;gap:10px;margin:14px 0}.cb .k{width:16px;height:16px;border:1px solid #818b98;border-radius:3px;flex:none;margin-top:3px;position:relative}.cb .k.y{background:#0969da;border-color:#0969da}.cb .k.y:after{content:"";position:absolute;left:4px;top:1px;width:5px;height:9px;border:solid #fff;border-width:0 2px 2px 0;transform:rotate(45deg)}.cb b{font-weight:600}.cb .d{color:#59636e;font-size:12px}
.sub{margin-left:26px}.pill{display:inline-block;padding:0 7px;border-radius:2em;font-size:12px;font-weight:500;line-height:20px;border:1px solid transparent}.ok{background:#1f883d;color:#fff}.okl{color:#1a7f37;border-color:#1a7f37}.warn{color:#9a6700;border-color:#d4a72c}.bad{color:#d1242f;border-color:#d1242f}.gray{color:#59636e;border-color:#d1d9e0}.purp{background:#8250df;color:#fff}
table.md{border-collapse:collapse;margin:8px 0 16px}table.md td,table.md th{border:1px solid #d1d9e0;padding:6px 13px;font-size:14px}table.md th{font-weight:600}table.md tr:nth-child(2n) td{background:#f6f8fa}
.ic{display:inline-block;width:16px;height:16px;border-radius:50%;vertical-align:-3px;margin-right:8px}.ic.s{background:#1a7f37}.ic.k{border:1.5px solid #59636e}.ic.p{border:2px solid #9a6700;border-top-color:transparent}
.foc{outline:3px solid #f2c94c;outline-offset:3px;border-radius:6px}`;
const OCTO=`<svg width="32" height="32" viewBox="0 0 16 16"><path fill="#1f2328" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>`;
const ghShell=(tab,inner)=>`<div class="gh"><div class="top">${OCTO}<span class="crumb">Collaboration95 / <b>rewind-app</b></span><span class="sp"></span><span class="av"></span></div><div class="tabs">${['Code','Issues<span class="cnt">10</span>','Pull requests<span class="cnt">8</span>','Discussions','Actions','Projects','Security and quality','Insights','Settings'].map(t=>`<span class="${t.startsWith(tab)?'on':''}">${t}</span>`).join('')}</div>${inner}</div>`;
const settingsSide=on=>`<div class="side">${[['','General'],['Access','Collaborators'],['Code and automation','Branches','Tags','Rules','Actions','Webhooks','Environments','Codespaces','Pages'],['Security','Advanced Security','Deploy keys','Secrets and variables']].map(([g,...it])=>(g?`<div class="grp">${g}</div>`:'')+it.map(x=>`<div class="it ${x===on?'on':''}">${x}</div>`).join('')).join('')}</div>`;
const cb=(on,label,desc='',extra='')=>`<div class="cb"><div class="k ${on?'y':''}"></div><div><b>${label}</b>${desc?`<div class="d">${desc}</div>`:''}${extra}</div></div>`;
const md=(src)=>{ // tiny markdown renderer: headings, tables, paragraphs, bold, code
  const inl=s=>esc(s).replace(/\*\*(.+?)\*\*/g,'<b>$1</b>').replace(/`(.+?)`/g,'<code>$1</code>').replace(/\[ ?(.+?) ?\]\((.+?)\)/g,'<a>$1</a>');
  const L=src.split('\n');let o='',i=0;
  while(i<L.length){const l=L[i];
    if(/^\|/.test(l)){const rows=[];while(i<L.length&&/^\|/.test(L[i])){rows.push(L[i]);i++;}const cells=r=>r.replace(/^\||\|$/g,'').split('|').map(c=>c.trim());
      o+='<table class="md"><tr>'+cells(rows[0]).map(c=>`<th>${inl(c)}</th>`).join('')+'</tr>'+rows.slice(2).map(r=>'<tr>'+cells(r).map(c=>`<td>${inl(c)}</td>`).join('')+'</tr>').join('')+'</table>';continue;}
    const h=l.match(/^(#+) (.*)/);if(h){const n=Math.min(h[1].length+1,4);o+=`<h${n} style="margin:12px 0 8px;font-size:${n===2?22:n===3?18:16}px;font-weight:600">${inl(h[2])}</h${n}>`;}
    else if(l.trim())o+=`<p style="margin:0 0 10px">${inl(l)}</p>`;i++;}
  return o;};
const runHeader=(r,dur,arts,trig)=>`<div class="box" style="padding:16px 20px;display:flex;gap:60px;margin-bottom:16px"><div><div class="mut" style="font-size:12px">${trig}</div><div style="margin-top:4px"><span class="av" style="width:20px;height:20px;vertical-align:-5px"></span> ${esc(r.actor.login)} ${r.event==='push'?'pushed':'opened #595'} <code style="background:#ddf4ff;color:#0969da;border-radius:6px;padding:1px 6px">${esc(r.head_branch)}</code></div></div><div><div class="mut" style="font-size:12px">Status</div><b>${r.conclusion==='success'?'Success':r.conclusion}</b></div><div><div class="mut" style="font-size:12px">Total duration</div><b style="text-decoration:underline">${dur}</b></div><div><div class="mut" style="font-size:12px">Artifacts</div><b style="text-decoration:underline">${arts}</b></div></div>`;
const runSide=(jobs,on)=>`<div class="side"><div class="it ${on==='Summary'?'on':''}">Summary</div><div class="grp">All jobs</div>${jobs.map(j=>`<div class="it ${on===j.name?'on':''}"><span class="ic ${j.conclusion==='success'?'s':'k'}"></span>${esc(j.name)}</div>`).join('')}<div class="grp">Run details</div><div class="it">Usage</div><div class="it">Workflow file</div></div>`;
const runTitle=(wf,title,num)=>`<div style="padding:16px 32px 0"><div class="mut" style="font-size:14px">← ${wf}</div><div style="font-size:24px;margin-top:4px"><span class="ic s" style="width:24px;height:24px;vertical-align:-4px"></span>${esc(title)} <span class="mut">#${num}</span></div></div>`;
const summaryCard=(name,body)=>`<div class="box" style="margin-bottom:16px"><div style="padding:12px 20px;border-bottom:1px solid #d1d9e0;font-weight:600;font-size:16px">${esc(name)} summary</div><div style="padding:12px 20px">${body}</div></div>`;
const dur=(a,b)=>{const s=Math.round((new Date(b)-new Date(a))/1000);return s>=60?`${Math.floor(s/60)}m ${s%60}s`:`${s}s`;};

// terminal
const termCSS=`.term{position:absolute;inset:0;background:linear-gradient(135deg,#1d2b38,#14202B);padding:46px 70px}.win{height:100%;border-radius:12px;overflow:hidden;background:#101820;box-shadow:0 30px 80px #0008;border:1px solid #2b3a47}.wt{height:36px;background:#24313d;display:flex;align-items:center;padding:0 14px;color:#9fb0bf;font:13px ${FONT}}.wt .dots{margin-right:auto}.wt .tt{position:absolute;left:0;right:0;text-align:center;pointer-events:none}
pre{margin:0;padding:22px 26px;font:15.5px/1.5 ${MONO};color:#d7e0e8;white-space:pre-wrap;word-break:break-all}.p{color:#7ee0a0}.c{color:#f2f5f7;font-weight:600}.g{color:#7ee0a0}.y{color:#f2c94c}.dim{color:#7d8d9b}`;
const term=(title,txt,hl=[])=>{const lines=txt.replace(/\s+$/,'').split('\n').map(l=>{let h=esc(l);
  if(l.startsWith('$ '))return `<span class="p">$</span> <span class="c">${esc(l.slice(2))}</span>`;
  for(const [re,cls] of hl) if(re.test(l)) return `<span class="${cls}" ${cls==='y foc'?'id="focus"':''}>${h}</span>`;return h;});
  return `<div class="term"><div class="win"><div class="wt" style="position:relative"><div class="dots"><span style="background:#ff5f57"></span><span style="background:#febc2e"></span><span style="background:#28c840"></span></div><div class="tt">${esc(title)}</div></div><pre>${lines.join('\n')}</pre></div></div>`;};

// ---------- evidence ----------
const run={q:J('run-quality.json'),g:J('run-gitleaks.json'),d:J('run-deploy.json')};
const jobs={q:J('run-quality-jobs.json').jobs,g:J('run-gitleaks-jobs.json').jobs,d:J('run-deploy-jobs.json').jobs};
const prot={dev:J('protection-dev.json'),main:J('protection-main.json')};
const envs=J('environments.json').environments;
const pr586=J('pr586-view.json');
const alerts=J('codescan-dev.json').sort((a,b)=>b.number-a.number);
const a56=J('codescan-alert-56.json');
const deployLog=T('logs/deploy-121646847180.log').split('\n').map(l=>l.split('\t')).filter(p=>p.length>=3).map(([j,s,...r])=>({s,t:r.join('\t').replace(/^﻿/,'').replace(/^\S+Z /,'').replace(/\x1b\[[0-9;]*m/g,'')}));

// ---------- frame definitions ----------
// kind live: {url, prep(page)->void, focus: locator fn}; replica: {url, html}; term: {html}
const F=[];
const live=(id,title,url,o)=>F.push({id,title,kind:'live',url,src:url,...o});
const rep=(id,title,url,data,html,o={})=>F.push({id,title,kind:'replica',url,src:url,data,html,...o});
const trm=(id,title,file,html,o={})=>F.push({id,title,kind:'terminal',src:'local command output',data:file,html,...o});
// GitHub sets smooth scrolling, so scrollIntoView is a no-op here; wheel by the element's viewport offset instead.
const scrollTo=async(p,loc,off=90)=>{const b=await loc.first().boundingBox();if(b){await p.mouse.move(1905,250);await p.mouse.wheel(0,b.y-off);await p.waitForTimeout(1200);}};

live('01-pr595-conversation','PR #595 merged into dev',`${REPO}/pull/595`,{data:'evidence/pr595-view.json',
  findings:['PR #595 "ci: retain DevSecOps artifacts for verified dev releases" merged into dev 26 Oct 14:55:29Z as aea7478','Body lists DAST, exact-bundle Trivy, provenance, manifest, Quality evidence, Gitleaks'],
  focus:p=>p.getByText('Merged',{exact:true}).first()});
const openGroups=async(p,names)=>{await p.evaluate(ns=>{for(const d of document.querySelectorAll('details.checks-list-item')){const t=d.querySelector('summary').textContent.replace(/\s+/g,' ').trim();d.open=ns.some(n=>t.startsWith(n));}},names);await p.waitForTimeout(600);};
live('02-pr595-checks','PR #595 checks: Quality checks workflow, all jobs and the required gate',`${REPO}/pull/595/checks`,{zoom:1,data:'evidence/pr595-view.json',
  prep:async p=>{await openGroups(p,['Quality checks']);await scrollTo(p,p.getByText('Quality checks',{exact:true}).first(),140);},
  findings:['Quality checks on head 38593b2: 12 success, 1 skipped (Web export and browser checks, main-bound only)','Required gate "Format, lint, typecheck, and test" success'],
  focus:p=>p.locator('details.checks-list-item[open]').getByText('Format, lint, typecheck, and test').first()});
live('02b-pr595-checks-security','PR #595 checks: GitGuardian, Release security, CodeQL, Secret scan, code scanning',`${REPO}/pull/595/checks`,{zoom:1,data:'evidence/pr595-view.json',
  prep:async p=>{await openGroups(p,['GitGuardian','Release security','CodeQL','Secret scan','Code scanning results']);await scrollTo(p,p.locator('details.checks-list-item').first(),140);},
  findings:['GitGuardian, Release security (runtime image, web image, IaC), CodeQL (classify, javascript-typescript, python, actions), Gitleaks full-history scan, code scanning results: all success'],
  focus:p=>p.getByText('Gitleaks full-history scan').first()});

const protPage=(b)=>{const p=prot[b],r=p.required_pull_request_reviews,sc=p.required_status_checks;return ghShell('Settings',`<div class="wrap">${settingsSide('Branches')}<div class="main"><h2 class="t">Branch protection rule</h2>
<div style="margin:16px 0 6px;font-weight:600">Branch name pattern</div><div class="box" style="width:360px;padding:5px 12px;font-family:${MONO}">${b}</div>
<div style="margin:22px 0 4px;font-weight:600;font-size:16px">Protect matching branches</div>
${cb(true,'Require a pull request before merging','When enabled, all commits must be made to a non-protected branch and submitted via a pull request before they can be merged into a branch that matches this rule.',
`<div class="sub">${cb(r.required_approving_review_count>0,'Require approvals','When enabled, pull requests targeting a matching branch require a number of approvals and no changes requested before they can be merged.',r.required_approving_review_count>0?`<div style="margin-top:6px" ${b==='main'?'id="focus" class="foc"':''}>Required number of approvals before merging: <span class="box" style="padding:1px 10px;font-weight:600">${r.required_approving_review_count}</span></div>`:'')}
${cb(r.dismiss_stale_reviews,'Dismiss stale pull request approvals when new commits are pushed')}${cb(r.require_code_owner_reviews,'Require review from Code Owners')}${cb(r.require_last_push_approval,'Require approval of the most recent reviewable push')}</div>`)}
${cb(true,'Require status checks to pass before merging','Choose which status checks must pass before branches can be merged into a branch that matches this rule.',
`<div class="sub">${cb(sc.strict,'Require branches to be up to date before merging')}<div class="box" style="margin-top:6px;width:640px" ${b==='dev'?'id="focus"':''}><div style="padding:8px 14px;background:#f6f8fa;border-bottom:1px solid #d1d9e0;font-weight:600">Status checks that are required.</div>${sc.checks.map(c=>`<div style="padding:8px 14px;display:flex"><span style="flex:1">${esc(c.context)}</span><span class="mut">GitHub Actions</span></div>`).join('')}</div></div>`)}
${cb(p.required_conversation_resolution.enabled,'Require conversation resolution before merging')}${cb(p.required_signatures.enabled,'Require signed commits')}${cb(p.required_linear_history.enabled,'Require linear history')}${cb(p.lock_branch.enabled,'Lock branch')}
${cb(p.enforce_admins.enabled,'Do not allow bypassing the above settings','The above settings will apply to administrators and custom roles with the "bypass branch protections" permission.')}
<div style="margin:18px 0 0;font-weight:600;font-size:16px">Rules applied to everyone including administrators</div>${cb(p.allow_force_pushes.enabled,'Allow force pushes')}${cb(p.allow_deletions.enabled,'Allow deletions')}
</div></div>`);};
rep('03-protect-dev','dev branch protection: one required check, up to date, conversations resolved',`${REPO}/settings/branches`,'evidence/protection-dev.json',protPage('dev'),{findings:['Required check: "Format, lint, typecheck, and test" (GitHub Actions app 15368), strict up-to-date','0 required approvals on dev; conversation resolution and enforce_admins on; force push and deletion off']});

live('04-quality-graph','Quality checks run 40343459119: classify, parallel lanes, aggregate gate',`${REPO}/actions/runs/40343459119`,{data:'evidence/run-quality.json; evidence/run-quality-jobs.json',
  findings:['PR run, success, 3m 46s (14:50:44Z to 14:54:30Z), 4 artifacts','Server tests on PostgreSQL 3m 4s is the critical path; gate "Format, lint, typecheck, and test" 3s'],
  prep:async p=>scrollTo(p,p.getByText('quality.yml').first(),150),focus:p=>p.getByText('4 jobs completed').first()});

const qs=['audit','root','server','frontend'].map(k=>[{audit:'Production dependency audit',root:'Root and IaC tests',server:'Server tests and coverage',frontend:'Frontend tests and coverage'}[k],T(`summaries/quality-${k}.md`).replace(/^.*n\/a means not measured.*$/m,'')]); // footer dropped from the rendered replica only
rep('05-quality-summaries','Quality job summaries: npm audit gate and root JUnit counts',`${REPO}/actions/runs/40343459119`,'evidence/summaries/quality-*.md (regenerated with scripts/quality-summary.py logic from run artifacts)',
  ghShell('Actions',runTitle('Quality checks',run.q.display_title,run.q.run_number)+`<div class="wrap">${runSide(jobs.q,'Summary')}<div class="main">${runHeader(run.q,dur(run.q.run_started_at,run.q.updated_at),4,'Triggered via pull request')}${qs.slice(0,2).map(([n,m],i)=>`<div ${i===0?'id="focus"':''}>${summaryCard(n,md(m))}</div>`).join('')}</div></div>`),
  {findings:['npm audit PASS (HIGH+ gate); low 0, moderate 0, high 0, critical 0','root 123 passed / 0 failed / 1 skipped']});
rep('05b-quality-coverage-summaries','Quality job summaries: server and frontend tests with coverage',`${REPO}/actions/runs/40343459119`,'evidence/summaries/quality-server.md; evidence/summaries/quality-frontend.md (regenerated with scripts/quality-summary.py logic from run artifacts)',
  ghShell('Actions',runTitle('Quality checks',run.q.display_title,run.q.run_number)+`<div class="wrap">${runSide(jobs.q,'Summary')}<div class="main">${qs.slice(2).map(([n,m],i)=>`<div ${i===0?'id="focus"':''}>${summaryCard(n,md(m))}</div>`).join('')}</div></div>`),
  {findings:['server 985 passed / 0 failed / 21 skipped, 85.5% lines','frontend 1674 / 0 / 0, 89.64% statements']});

const artOk=names=>async p=>{const h=await p.getByText('Produced during runtime',{exact:true}).first().boundingBox();if(!h||h.y<200||h.y>650)throw new Error('Artifacts heading at y='+(h&&h.y));for(const n of names){const b=await p.getByText(n,{exact:false}).first().boundingBox();if(!b||b.y<0||b.y+b.height>1025)throw new Error(n+' not on screen');}};
live('06-quality-artifacts','Quality run artifacts: JUnit, coverage, npm-audit',`${REPO}/actions/runs/40343459119`,{data:'evidence/run-quality-artifacts.json',
  findings:['frontend-coverage 301 KB, quality-npm-audit 316 B, quality-test-results-root 5.04 KB, server-coverage 9.33 MB'],check:artOk(['frontend-coverage','quality-npm-audit','quality-test-results-root','server-coverage']),
  prep:async p=>scrollTo(p,p.getByText('Produced during runtime',{exact:true}),120),focus:p=>p.getByText('quality-npm-audit').first()});

trm('07-term-quality-reports','Downloaded Quality artifacts: JUnit cases and coverage','evidence/terminal/quality-reports.txt',term('zsh — artifacts/40343459119',T('terminal/quality-reports.txt'),[[/numFailedTests|test-results-server.xml:/,'y foc'],[/"lines"|"statements"/,'g']]),
  {findings:['JUnit testcases: root 124, server 1006','Jest 1674 passed, 0 failed','server lines 85.5 / branches 85.52 / functions 86.41','frontend statements 89.64 / lines 92.33 / branches 85.66']});
trm('08-term-npm-audit','Production npm audit: 0 vulnerabilities across 674 prod dependencies','evidence/terminal/npm-audit.txt',term('zsh — artifacts/40343459119',T('terminal/npm-audit.txt'),[[/"total": 0/,'y foc'],[/"(high|critical)": 0/,'g']]),
  {findings:['npm audit --omit=dev --audit-level=high: 0 at every severity; 674 prod / 1119 total dependencies']});

const nOpen=alerts.filter(a=>a.state==='open').length,nClosed=alerts.length-nOpen;
rep('09-codescan-alerts','Code scanning on dev: 0 open, 23 closed (20 dismissed with reasons, 3 fixed)',`${REPO}/security/code-scanning?query=is%3Aclosed+branch%3Adev`,'evidence/codescan-dev.json',
  ghShell('Security',`<div class="wrap"><div class="side"><div class="grp">Security and quality</div>${['Overview','Reporting','Policy','Advisories'].map(x=>`<div class="it">${x}</div>`).join('')}<div class="grp">Vulnerability alerts</div><div class="it">Dependabot</div><div class="it on">Code scanning</div><div class="it">Secret scanning</div></div><div class="main">
<h2 class="t" style="border:0">Code scanning</h2><div class="mut" style="margin-bottom:12px">Tools: <b style="color:#1f2328">CodeQL</b> · <b style="color:#1f2328">Gitleaks</b> &nbsp; Latest dev analyses ${esc(J('codescan-analyses-dev.json')[0].commit_sha.slice(0,7))}</div>
<div class="box" style="padding:6px 12px;font-family:${MONO};margin-bottom:12px">is:closed branch:dev</div>
<div class="box"><div style="padding:12px 16px;background:#f6f8fa;border-bottom:1px solid #d1d9e0;display:flex;gap:20px"><span class="mut">○ ${nOpen} Open</span><b id="focus">✓ ${nClosed} Closed</b></div>
${alerts.slice(0,9).map(a=>`<div style="padding:10px 16px;border-bottom:1px solid #d1d9e0;${a.number>=54?'background:#fff8c5':''}"><div><b>${esc(a.rule.description)}</b> <span class="pill gray">${esc(a.rule.security_severity_level||a.rule.severity)}</span></div><div class="mut" style="font-size:12px">#${a.number} ${a.state==='fixed'?'fixed':'dismissed as '+esc(a.dismissed_reason)} ${a.state==='fixed'?'':'by '+esc(a.dismissed_by.login)} · ${esc(a.most_recent_instance.location.path)} · ${a.tool.name}</div></div>`).join('')}</div></div></div>`),
  {findings:[`${nOpen} open, ${nClosed} closed on dev (20 dismissed with written reasons, 3 fixed)`,'#54–#56 from PR #592 load harness, dismissed 26 Oct 15:26Z as used in tests']});

const src=T('hosted.mjs-at-alert56.txt').split('\n');
rep('10-codescan-alert-56','CodeQL alert #56 triage from PR #592: dismissed as used in tests',`${REPO}/security/code-scanning/56`,'evidence/codescan-alert-56.json; evidence/codescan-pr592.json',
  ghShell('Security',`<div style="padding:24px 40px"><div style="font-size:26px">${esc(a56.rule.description)} <span class="mut">#56</span></div>
<div style="margin:8px 0 18px"><span class="pill" style="background:#59636e;color:#fff">Dismissed</span> <span class="mut">Collaboration95 dismissed this alert as <b>${esc(a56.dismissed_reason)}</b> · ${ago(a56.dismissed_at)}</span></div>
<div style="display:flex;gap:28px"><div style="flex:1;min-width:0"><div class="box"><div style="padding:8px 14px;background:#f6f8fa;border-bottom:1px solid #d1d9e0;font-family:${MONO};font-size:13px">scripts/load/hosted.mjs:417</div>
<pre style="margin:0;padding:10px 0;font:13px/1.6 ${MONO};white-space:pre;overflow:hidden">${[413,414,415,416,417,418].map(n=>`<div style="padding:0 14px;${n===417?'background:#fff8c5':''}"><span class="mut" style="display:inline-block;width:42px">${n}</span>${esc(src[n-1].slice(0,96))}</div>`).join('')}</pre>
<div style="margin:0 14px 12px;padding:10px 14px;border:1px solid #d4a72c;border-radius:6px;background:#fff8c5">${esc(a56.most_recent_instance.message.text)}</div></div>
<div class="box" style="margin-top:16px;padding:14px 18px" id="focus"><b>Dismissal comment</b><div style="margin-top:6px">${esc(a56.dismissed_comment)}</div></div></div>
<div style="width:300px;flex:none"><div class="mut" style="font-weight:600;font-size:12px">Severity</div><div style="margin-bottom:12px">${esc(a56.rule.security_severity_level)}</div><div class="mut" style="font-weight:600;font-size:12px">Affected branches</div><div style="margin-bottom:12px">dev · pull/586 · pull/592</div><div class="mut" style="font-weight:600;font-size:12px">Rule</div><div style="font-family:${MONO};font-size:13px;margin-bottom:12px">${esc(a56.rule.id)}</div><div class="mut" style="font-weight:600;font-size:12px">Weaknesses</div><div>CWE-434, CWE-912</div><div class="mut" style="font-weight:600;font-size:12px;margin-top:12px">Tool</div><div>CodeQL</div><div class="mut" style="font-weight:600;font-size:12px;margin-top:12px">Also triaged in PR #592</div><div>#54 File data in outbound network request<br>#55 Network data written to file</div></div></div></div>`),
  {findings:['PR #592 raised 3 medium CodeQL alerts (#54, #55, #56) in scripts/load/hosted.mjs','All 3 dismissed by Collaboration95 26 Oct 15:26–15:26:52Z as "used in tests" with a written reason']});

live('11-pr592-checks','PR #592 checks: CodeQL and Gitleaks results',`${REPO}/pull/592/checks`,{data:'evidence/pr592-view.json; evidence/codescan-pr592.json',
  prep:async p=>{await openGroups(p,['CodeQL','Secret scan','Code scanning results']);await scrollTo(p,p.locator('details.checks-list-item').first(),140);},
  findings:['PR #592 "test(perf): scripted load test and performance workflow" merged 15:31:52Z; all checks success'],
  focus:p=>p.getByText('CodeQL (javascript-typescript)').first()});

live('12-gitleaks-run','Secret scan run 40343459282: Gitleaks full-history scan',`${REPO}/actions/runs/40343459282`,{data:'evidence/run-gitleaks.json; evidence/run-gitleaks-artifacts.json',
  findings:['PR run success in 30s; artifact gitleaks-5860b18… (redacted SARIF, 7 KB)'],focus:p=>p.getByText('Gitleaks full-history scan').last()});
rep('13-gitleaks-summary','Gitleaks job summary: 0 findings across full history',`${REPO}/actions/runs/40343459282`,'evidence/summaries/gitleaks.md; evidence/terminal/gitleaks.txt',
  ghShell('Actions',runTitle('Secret scan',run.g.display_title,run.g.run_number)+`<div class="wrap">${runSide(jobs.g,'Summary')}<div class="main">${runHeader(run.g,dur(run.g.run_started_at,run.g.updated_at),1,'Triggered via pull request')}<div id="focus">${summaryCard('Gitleaks full-history scan',md(T('summaries/gitleaks.md')))}</div></div></div>`),
  {findings:['Gitleaks SARIF: 222 rules, 0 results']});

live('14-deploy-graph','Deploy dev run 40344230832: classify → deploy → DAST',`${REPO}/actions/runs/40344230832`,{data:'evidence/run-deploy.json; evidence/run-deploy-jobs.json',
  findings:['push to dev aea7478, success, 9m 6s; deploy job 6m 14s; DAST 1m 49s; 3 artifacts'],
  prep:async p=>scrollTo(p,p.getByText('deploy-dev.yml').first(),150),focus:p=>p.getByText('deploy-dev.yml',{exact:true}).first()});
live('15-deploy-steps','Deploy job steps: Quality wait, bundle, exact scan, attest, OIDC, install, health',`${REPO}/actions/runs/40344230832/job/121646847180`,{data:'evidence/run-deploy-jobs.json',
  findings:['Wait for Quality 123 s, build bundle 53 s, scan 16 s, attest 7 s, OIDC 3 s, ship 54 s, install 76 s'],
  focus:p=>p.getByText('Attest the release bundle and its security manifest').first()});

const stepLines=(s,filter,max)=>deployLog.filter(x=>x.s===s&&!/^##\[|^shell:|^env:|^\s+[A-Z_]+:|36;1m|^\s*$/.test(x.t)&&(!filter||filter.test(x.t))).slice(0,max).map(x=>x.t);
const stepTime=n=>{const s=jobs.d.find(j=>j.name==='Deploy dev to the hosted host').steps.find(x=>x.name===n);return dur(s.started_at,s.completed_at);};
const logBlock=(name,lines,foc)=>`<div style="border-bottom:1px solid #30363d"><div style="padding:9px 16px;display:flex;color:#f0f6fc"><span style="color:#3fb950;margin-right:10px">✓</span><span style="flex:1">${esc(name)}</span><span style="color:#9198a1">${stepTime(name)}</span></div>${lines.length?`<div style="padding:2px 0 10px;font:13px/1.6 ${MONO};color:#d1d7e0" ${foc?'id="focus"':''}>${lines.map((l,i)=>`<div style="padding-left:16px;white-space:pre;overflow:hidden"><span style="color:#6e7681;display:inline-block;width:44px">${i+1}</span>${esc(l.slice(0,130))}</div>`).join('')}</div>`:''}</div>`;
rep('16-deploy-log','Deploy log: Quality gate, attestation, OIDC session, health-checked activation',`${REPO}/actions/runs/40344230832/job/121646847180`,'evidence/logs/deploy-121646847180.log',
  ghShell('Actions',runTitle('Deploy dev',run.d.display_title,run.d.run_number)+`<div class="wrap">${runSide(jobs.d,'Deploy dev to the hosted host')}<div class="main"><div style="background:#0d1117;border-radius:6px;overflow:hidden;font-size:14px"><div style="padding:14px 16px;color:#f0f6fc;border-bottom:1px solid #30363d"><b>Deploy dev to the hosted host</b><div style="color:#9198a1;font-size:12px">succeeded · ${dur(jobs.d[1].started_at,jobs.d[1].completed_at)}</div></div>
${logBlock("Wait for this commit's dev Quality checks",stepLines("Wait for this commit's dev Quality checks",/Quality checks passed/),false)}
${logBlock('Build the verified release bundle',[],false)}${logBlock('Scan the exact bundled images and write the release manifest',[],false)}
${logBlock('Attest the release bundle and its security manifest',stepLines('Attest the release bundle and its security manifest',/Attestation (type|created)|attestations\//),true)}
${logBlock('Assume the deploy role with GitHub OIDC',stepLines('Assume the deploy role with GitHub OIDC',/UserId/),false)}
${logBlock('Install the release on the host',stepLines('Install the release on the host',/runtime  Healthy|web  Started|Activated/),false)}</div></div></div>`),
  {findings:['"Quality checks passed for aea7478…"','"Attestation created for 2 subjects" → attestations/59963857','OIDC session rewind-demo-deploy-40344230832','"Activated release aea7478… after runtime and web health checks."']});

const zapTop=T('summaries/zap.md').split('\n## Insights')[0]; const zapAlerts='## Alerts'+T('summaries/zap.md').split('## Alerts')[1].split('## Alert Detail')[0];
rep('17-deploy-summaries','Deploy dev summaries: exact-bundle security gate and ZAP baseline',`${REPO}/actions/runs/40344230832`,'evidence/summaries/release-gate.md; evidence/summaries/zap.md',
  ghShell('Actions',runTitle('Deploy dev',run.d.display_title,run.d.run_number)+`<div class="wrap">${runSide(jobs.d,'Summary')}<div class="main" style="display:flex;gap:16px;align-items:flex-start"><div style="flex:1" id="focus">${summaryCard('Deploy dev to the hosted host',md(T('summaries/release-gate.md').replace(/^Registry digests may be empty.*$/m,'')))}</div><div style="flex:1.1;font-size:13px">${summaryCard('DAST (ZAP baseline on hosted dev)',md(zapTop.replace(/ZAP by \[Checkmarx\]\(.*\)\./,''))+md(zapAlerts.split('\n').slice(0,10).join('\n')))}</div></div></div>`),
  {findings:['Release gate: runtime HIGH 0 CRITICAL 0 PASS; web HIGH 0 CRITICAL 0 PASS','ZAP: High 0, Medium 4 (CSP), Low 7, Informational 6; report-only']});

trm('18-term-trivy-sbom','Exact-bundle SBOMs and Trivy findings','evidence/terminal/sbom-trivy.txt',term('zsh — dev-release-security-aea7478',T('terminal/sbom-trivy.txt'),[[/^CycloneDX/,'y foc'],[/MEDIUM|UNKNOWN/,'g']]),
  {findings:['CycloneDX 1.6: runtime 187 components, web 72','runtime: musl/musl-utils CVE-2026-107891 UNKNOWN, zlib CVE-2026-85091 MEDIUM (fixed versions available); web 0']});
trm('19-term-manifest','release-manifest.json: commit, run, Quality run, scanner, gate','evidence/terminal/manifest.txt',term('zsh — dev-release-security-aea7478',T('terminal/manifest.txt'),[[/security_gate/,'y foc'],[/"(HIGH|CRITICAL)": 0/,'g']]),
  {findings:['commit aea7478, run 40344230832, quality_run_id 40344231052, Trivy v0.70.0, security_gate pass']});

live('20-deploy-artifacts','Deploy dev artifacts: ZAP reports, security reports, attested bundle',`${REPO}/actions/runs/40344230832`,{data:'evidence/run-deploy-artifacts.json',
  findings:['zap-baseline-aea7478… 34 KB, dev-release-security-aea7478… 80 KB, dev-release-bundle-aea7478… 154 MB'],check:artOk(['zap-baseline-','dev-release-security-','dev-release-bundle-']),
  prep:async p=>scrollTo(p,p.getByText('Produced during runtime',{exact:true}),120),focus:p=>p.getByText('dev-release-bundle-',{exact:false}).first()});
live('21-attestation','Build provenance attestation 59963857 for bundle and manifest',`${REPO}/attestations/59963857`,{data:'evidence/attestation-verify.json',
  findings:['SLSA provenance v1, commit aea7478, workflow deploy-dev.yml@refs/heads/dev','Subjects: release-manifest.json sha256:59d9b9f7…, rewind-release.tar sha256:fef3c22a…'],
  prep:async p=>scrollTo(p,p.getByText('Subjects',{exact:true}).first(),700),check:async p=>{const b=await p.getByText('rewind-release.tar').first().boundingBox();if(!b||b.y+b.height>1025)throw new Error('subjects off screen');},focus:p=>p.getByText('Subjects',{exact:true}).first()});
trm('22-term-attest-verify','gh attestation verify on release-manifest.json','evidence/attestation-verify.txt; evidence/terminal/digest.txt',term('zsh — dev-release-security-aea7478',T('terminal/digest.txt').split('\n').slice(0,3).join('\n')+'\n'+T('attestation-verify.txt'),[[/Verification succeeded/,'y foc'],[/^Loaded|Build workflow|Signer workflow/,'g']]),
  {findings:['sha256 59d9b9f7… matches attestation subject','✓ Verification succeeded! (SLSA v1, OIDC issuer token.actions.githubusercontent.com, exit 0)']});
F.push({id:'23-zap-report',title:'ZAP baseline HTML report on hosted dev',kind:'live',url:'file://'+path.join(EV,'artifacts/40344230832/report_html.html'),barUrl:`${REPO}/actions/runs/40344230832/artifacts/12660614474`,src:'zap-baseline-aea7478… artifact report_html.html',data:'evidence/artifacts/40344230832/report_html.html',
  findings:['High 0, Medium 4, Low 7, Informational 6'],prep:async p=>scrollTo(p,p.getByText('Summary of Alerts').first(),30),focus:p=>p.locator('table').first()});
trm('24-term-health','Hosted dev /api/health: 200, PostgreSQL, schema ready','evidence/health-curl.txt',term('zsh — hosted dev',T('health-curl.txt').replace(/\nx-amz-cf-id:.*$/m,'').replace(/^content-security-policy-report-only:.*$/m,l=>l.slice(0,140)),[[/^\{"ok":true/,'y foc'],[/^HTTP\/2 200/,'g']]),
  {findings:['HTTP/2 200; ok true, ready true, database postgresql, schema ready, expectedMigrationVersion 31','HSTS, X-Frame-Options DENY, nosniff, CSP report-only header']});

rep('25-protect-main','main branch protection: required gate plus 1 approving review',`${REPO}/settings/branches`,'evidence/protection-main.json',protPage('main'),{findings:['Required check "Format, lint, typecheck, and test", strict','1 required approving review, approval of most recent push required, enforce_admins on']});
live('26-pr586','Promotion PR #586 dev → main',`${REPO}/pull/586`,{data:'evidence/pr586-view.json',
  findings:[`PR #586 ${pr586.state}, reviewDecision ${pr586.reviewDecision}, mergeStateStatus ${pr586.mergeStateStatus}`,`Approved by ${pr586.reviews.filter(r=>r.state==='APPROVED').map(r=>r.author.login).join(', ')} ${pr586.reviews.filter(r=>r.state==='APPROVED').map(r=>r.submittedAt).join(', ')}`],
  focus:p=>p.locator('.discussion-sidebar-item').first()});

const chk=pr586.statusCheckRollup, cnt=k=>chk.filter(c=>(c.conclusion||c.state||c.status)===k).length, pend=chk.filter(c=>!(c.conclusion)||c.status==='IN_PROGRESS').filter(c=>c.status&&c.status!=='COMPLETED');
const pm=prot.main.required_pull_request_reviews, appr=pr586.reviews.filter(r=>r.state==='APPROVED');
rep('27-promotion-approval','Promotion rule beside PR #586 approval',`${REPO}/pull/586`,'evidence/protection-main.json; evidence/pr586-view.json',
  ghShell('Pull requests',`<div style="padding:20px 32px 0"><div style="font-size:26px">${esc(pr586.title)} <span class="mut">#586</span></div><div style="margin:6px 0 16px"><span class="pill ok" style="font-size:14px;padding:4px 12px">Open</span> <span class="mut"><b style="color:#1f2328">${esc(pr586.author.login)}</b> wants to merge ${pr586.commits.length} commits into <code>main</code> from <code>dev</code></span></div></div>
<div style="display:flex;gap:24px;padding:0 32px"><div class="box" style="width:520px;flex:none;padding:16px 20px"><div class="mut" style="font-size:12px;font-weight:600">BRANCH PROTECTION · main</div>
${cb(true,'Require a pull request before merging')}<div class="sub">${cb(pm.required_approving_review_count>0,'Require approvals',`Required number of approvals before merging: <b>${pm.required_approving_review_count}</b>`)}${cb(pm.require_last_push_approval,'Require approval of the most recent reviewable push')}</div>${cb(prot.main.required_status_checks.strict,'Require branches to be up to date before merging')}${cb(true,'Required status check',esc(prot.main.required_status_checks.contexts.join(', ')))}${cb(prot.main.enforce_admins.enabled,'Do not allow bypassing the above settings')}</div>
<div style="flex:1;min-width:0"><div class="box" id="focus"><div style="padding:14px 18px;display:flex;gap:12px;border-bottom:1px solid #d1d9e0"><span class="ic s" style="width:28px;height:28px"></span><div><b style="font-size:16px">Changes approved</b><div class="mut">${appr.length} approving review${appr.length===1?'':'s'} by reviewers with write access.</div>${appr.map(r=>`<div style="margin-top:6px"><span class="av" style="width:20px;height:20px;vertical-align:-5px;background:#4a7"></span> <b>${esc(r.author.login)}</b> approved these changes · ${ago(r.submittedAt)}</div>`).join('')}</div></div>
<div style="padding:14px 18px;display:flex;gap:12px;border-bottom:1px solid #d1d9e0"><span class="ic ${pend.length?'p':'s'}" style="width:28px;height:28px"></span><div><b style="font-size:16px">${pend.length?'Some checks haven’t completed yet':'All checks have passed'}</b><div class="mut">${pend.length?pend.length+' in progress, ':''}${cnt('SUCCESS')} successful, ${cnt('SKIPPED')} skipped checks</div>${pend.map(c=>`<div style="margin-top:6px"><span class="ic p"></span>${esc(c.workflowName)} / ${esc(c.name)} <span class="mut">In progress</span></div>`).join('')}<div style="margin-top:6px"><span class="ic s"></span>Quality checks / Format, lint, typecheck, and test <span class="pill gray">Required</span></div></div></div>
<div style="padding:14px 18px;display:flex;gap:12px"><span class="ic s" style="width:28px;height:28px"></span><div><b style="font-size:16px">${pr586.mergeable==='MERGEABLE'?'No conflicts with base branch':'Conflicts'}</b><div class="mut">mergeStateStatus: ${esc(pr586.mergeStateStatus)} · reviewDecision: ${esc(pr586.reviewDecision)}</div></div></div></div></div></div>`),
  {findings:[`main requires ${pm.required_approving_review_count} approving review + last-push approval`,`PR #586 reviewDecision ${pr586.reviewDecision} (${appr.map(r=>r.author.login).join(', ')}), mergeStateStatus ${pr586.mergeStateStatus}; ${cnt('SUCCESS')} success, ${cnt('SKIPPED')} skipped, ${pend.length} in progress at capture`]});

const rel=envs.find(e=>e.name==='release'), relRev=rel.protection_rules.find(r=>r.type==='required_reviewers');
rep('28-environments','Environments: dev unprotected, release needs a second reviewer from main',`${REPO}/settings/environments`,'evidence/environments.json; evidence/env-release-branch-policies.json',
  ghShell('Settings',`<div class="wrap">${settingsSide('Environments')}<div class="main"><h2 class="t">Environments</h2><div class="box">${envs.map(e=>{const rr=(e.protection_rules||[]).find(r=>r.type==='required_reviewers');const bp=e.deployment_branch_policy;return `<div style="padding:14px 18px;border-bottom:1px solid #d1d9e0;${e.name==='release'?'background:#fff8c5':''}" ${e.name==='release'?'id="focus"':''}><b style="font-size:16px">${esc(e.name)}</b><div class="mut" style="margin-top:4px">${(e.protection_rules||[]).length} protection rule${(e.protection_rules||[]).length===1?'':'s'}${rr?` · Required reviewers: <b style="color:#1f2328">${rr.reviewers.map(x=>esc(x.reviewer.login)).join(', ')}</b>${rr.prevent_self_review?' · Prevent self-review':''}`:''}${bp?(bp.custom_branch_policies?' · Deployment branches: <b style="color:#1f2328">'+J('env-release-branch-policies.json').branch_policies.map(b=>esc(b.name)).join(', ')+'</b>':' · Deployment branches: protected branches only'):' · No deployment branch restriction'}</div></div>`;}).join('')}</div></div></div>`),
  {findings:['dev: 0 protection rules',`release: required reviewer ${relRev.reviewers.map(r=>r.reviewer.login).join(', ')}, prevent self-review, branch policy main`,'staging-demo: protected branches only']});

// ---------- capture ----------
(async()=>{
  const only=process.argv.slice(2);fs.mkdirSync(FR,{recursive:true});fs.mkdirSync(PG,{recursive:true});
  const browser=await chromium.launch({headless:true});
  const ctx=await browser.newContext({viewport:{width:W,height:H},deviceScaleFactor:DSF,colorScheme:'light',locale:'en-US',timezoneId:'Asia/Singapore'});
  const page=await ctx.newPage(); const wrap=await (await browser.newContext({viewport:{width:W,height:H},deviceScaleFactor:DSF})).newPage();
  const idxPath=path.join(root,'frames-index.json'); const prev=fs.existsSync(idxPath)?JSON.parse(fs.readFileSync(idxPath)):[]; const index=new Map(prev.map(e=>[e.id,e]));
  for(const f of F){ if(only.length&&!only.includes(f.id))continue; let html, focus=[960,540], barUrl=f.url;
    if(f.kind==='live'){
      await page.goto(f.url,{waitUntil:'networkidle',timeout:60000}).catch(()=>{});await page.addStyleTag({content:`html{zoom:${f.zoom||Z}}`});await page.waitForTimeout(1200);
      if(f.prep)await f.prep(page);await page.waitForTimeout(800);if(f.check)await f.check(page);
      if(f.focus){const b=await f.focus(page).boundingBox().catch(()=>null);if(b)focus=[Math.round(b.x+b.width/2),Math.round(b.y+BAR*Z+b.height/2)];}
      const shot=path.join(PG,f.id+'.view.png');await page.screenshot({path:shot,clip:{x:0,y:0,width:W,height:H-BAR*Z}});barUrl=f.barUrl||page.url();
      html=`<!doctype html><html><head><meta charset="utf-8"><style>${ZOOM}${chromeCSS}</style></head><body>${chrome(barUrl,`<img src="${f.id}.view.png" style="width:${VW}px;height:${VH-BAR}px;display:block">`)}</body></html>`;
    } else if(f.kind==='replica'){
      html=`<!doctype html><html><head><meta charset="utf-8"><style>${ZOOM}${chromeCSS}${ghCSS}</style></head><body>${chrome(f.url,f.html)}</body></html>`;
    } else html=`<!doctype html><html><head><meta charset="utf-8"><style>${ZOOM}${chromeCSS}${termCSS}</style></head><body>${f.html}</body></html>`;
    const hp=path.join(PG,f.id+'.html');fs.writeFileSync(hp,html);await wrap.goto('file://'+hp);await wrap.waitForTimeout(300);
    if(f.kind!=='live'){const b=await wrap.locator('#focus').first().boundingBox().catch(()=>null);if(b)focus=[Math.round(b.x+b.width/2),Math.round(b.y+Math.min(b.height,875)/2)];}
    await wrap.screenshot({path:path.join(FR,f.id+'.png')});
    index.set(f.id,{id:f.id,file:`frames/${f.id}.png`,title:f.title,kind:f.kind,sourceURL:f.kind==='live'?barUrl:(f.src||f.url),data:f.data||'',findings:f.findings||[],focus,page:`pages/${f.id}.html`,screenshot:f.kind==='live'?`Playwright Chromium viewport 1920x1080 DSF 2, html zoom ${f.zoom||Z},`+' screenshot clip {x:0,y:0,width:1920,height:1025} placed in 1920x1080 DSF 2 wrapper (html zoom 1.25) under the URL bar showing page.url() after prep':'Playwright Chromium viewport 1920x1080 DSF 2, html zoom 1.25',capturedAt:new Date().toISOString()});
    console.log(f.id,focus.join(','));
  }
  fs.writeFileSync(idxPath,JSON.stringify([...index.values()].sort((a,b)=>a.id.localeCompare(b.id)),null,2));
  await browser.close();
})();
