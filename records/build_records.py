"""Rebuild presentation records from saved read-only gh snapshots. No repository writes."""
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parent
os.environ['MPLCONFIGDIR'] = str(ROOT / '.mplconfig')
import csv
import json
from collections import Counter
from datetime import datetime, date, time, timedelta, timezone
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

DATA = ROOT / 'data'
REPO = Path('/Users/speedpowermac/Documents/projects/CODE_MAIN/NUS/SWE5006/rewind-app')
WT = REPO.parent / 'rewind-present-audit'
URL = 'https://github.com/Collaboration95/rewind-app'
SGT = timezone(timedelta(hours=8))
ISSUES = json.loads((DATA / 'issues.json').read_text())
PRS = json.loads((DATA / 'prs.json').read_text())
TIMELINE = json.loads((DATA / 'issue-timeline.json').read_text())
OPEN = json.loads((DATA / 'open-mvp.json').read_text())
WINDOWS = [(date(2026,9,1),date(2026,9,12)), (date(2026,9,13),date(2026,9,26)),
           (date(2026,9,27),date(2026,10,10)), (date(2026,10,11),date(2026,10,24))]
def ts(x): return datetime.fromisoformat(x.replace('Z','+00:00'))
def sod(d): return datetime.combine(d,time(),SGT)
def milestone(x): return (x.get('milestone') or {}).get('title','Unassigned')
def csv_write(name, rows):
    with (DATA / name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def issue(n): return f'[{n}]({URL}/issues/{n})'
def pr(n): return f'[PR #{n}]({URL}/pull/{n})'
def doc(path, label=None): return f'[{label or Path(path).name}]({URL}/blob/f6cd896/{path})'
def mdtable(headers,rows):
    return '| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+''.join('| '+' | '.join(map(str,r))+' |\n' for r in rows)

EVENTS={}
for x in TIMELINE:
    ev=[(ts(x['createdAt']),'Created',None)]
    for e in x['timelineItems']['nodes']:
        ev.append((ts(e['createdAt']),e['__typename'],e.get('milestoneTitle')))
    EVENTS[x['number']]=sorted(ev,key=lambda e:e[0])
def state_at(number,cutoff):
    exists=False;m=None;op=True
    for t,k,v in EVENTS[number]:
        if t>=cutoff: break
        if k=='Created':exists=True
        elif k=='MilestonedEvent':m=v
        elif k=='DemilestonedEvent':m=None
        elif k=='ClosedEvent':op=False
        elif k=='ReopenedEvent':op=True
    return exists,m,op
assert {x['number'] for x in ISSUES}==set(EVENTS)
bad=[]
for x in TIMELINE:
    c,m,o=state_at(x['number'],datetime.max.replace(tzinfo=timezone.utc))
    if m!=(x['milestone'] or {}).get('title') or o!=(x['state']=='OPEN'):bad.append(x['number'])
assert not bad, bad
csv_write('issue-events.csv',[{'issue':n,'timestamp_utc':t.isoformat(),'event':k,'milestone':v or ''}
                             for n,events in EVENTS.items() for t,k,v in events])
csv_write('issues.csv',[{'number':x['number'],'title':x['title'],'milestone_current':milestone(x),
    'state':x['state'],'state_reason':x['stateReason'],'created_at_utc':x['createdAt'],
    'closed_at_utc':x['closedAt'] or '', 'closed_date_sgt':ts(x['closedAt']).astimezone(SGT).date().isoformat() if x['closedAt'] else '',
    'labels_current':';'.join(l['name'] for l in x['labels']),'url':x['url']} for x in ISSUES])
csv_write('prs.csv',[{'number':x['number'],'title':x['title'],'milestone_current':milestone(x),'state':x['state'],
    'base':x['baseRefName'],'merged_at_utc':x['mergedAt'] or '',
    'merged_date_sgt':ts(x['mergedAt']).astimezone(SGT).date().isoformat() if x['mergedAt'] else '', 'url':x['url']} for x in PRS])

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':16,'axes.titlesize':24,'axes.labelsize':17,
                     'xtick.labelsize':16,'ytick.labelsize':16,'legend.fontsize':16,
                     'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'white'})
velocity=[];scope_summary=[]
for i,(start,end) in enumerate(WINDOWS):
    name=f'Sprint {i}';dates=[start+timedelta(days=j) for j in range((end-start).days+1)]
    def snap(cut):
        states=[state_at(n,cut) for n in EVENTS];states=[s for s in states if s[0] and s[1]==name]
        return len(states),sum(s[2] for s in states)
    ss,so=snap(sod(start));es,eo=snap(sod(end+timedelta(days=1)))
    rows=[]
    for d in dates:
        sc,op=snap(sod(d+timedelta(days=1)))
        rows.append({'date_sgt':d.isoformat(),'milestone':name,'scope_issues':sc,'open_issues':op,'closed_in_scope':sc-op})
    csv_write(f'burndown-sprint-{i}.csv',rows)
    scope_summary.append([name,ss,so,es,eo])
    fig,ax=plt.subplots(figsize=(12.8,7.2),dpi=100)
    fig.subplots_adjust(left=.09,right=.965,bottom=.23,top=.83)
    plot_dates=[sod(start)]+[sod(d+timedelta(days=1)) for d in dates]
    ax.step(plot_dates,[ss]+[r['scope_issues'] for r in rows],where='post',color='#94a3b8',lw=2.8,ls='--',label='Total scope (milestone)')
    ax.step(plot_dates,[so]+[r['open_issues'] for r in rows],where='post',color='#1764ab',lw=3.5,marker='o',ms=5,label='Open issues')
    ax.fill_between(plot_dates,[so]+[r['open_issues'] for r in rows],step='post',alpha=.08,color='#1764ab')
    fig.text(.09,.935,f'{name} · issue burndown',fontsize=24,fontweight='bold')
    fig.text(.09,.88,f'{start:%d %b}–{end:%d %b %Y} · opening 00:00 and daily closes · SGT',fontsize=16,color='#475569')
    ax.set_ylabel('Issue count');ax.set_ylim(bottom=0,top=max(es,max(r['scope_issues'] for r in rows))*1.22+2)
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=2,tz=SGT));ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b',tz=SGT))
    ax.set_xlim(sod(start),sod(end+timedelta(days=1)))
    ax.grid(axis='y',alpha=.18);ax.legend(loc='upper right',frameon=False)
    fig.text(.09,.125,f'Opening scope/open: {ss}/{so}    |    Closing scope/open: {es}/{eo}',fontsize=17,fontweight='bold')
    fig.savefig(ROOT/'charts'/f'burndown-sprint-{i}.png',dpi=100);plt.close(fig)
    a,b=sod(start),sod(end+timedelta(days=1))
    closed=[x for x in ISSUES if x['closedAt'] and a<=ts(x['closedAt'])<b]
    merged=[x for x in PRS if x['mergedAt'] and a<=ts(x['mergedAt'])<b]
    velocity.append({'sprint':name,'start_sgt':start.isoformat(),'end_sgt':end.isoformat(),
        'closed_issues_all_milestones':len(closed),'closed_issues_current_own_milestone':sum(milestone(x)==name for x in closed),
        'closed_issues_completed':sum(x['stateReason']=='COMPLETED' for x in closed),
        'closed_issues_not_planned':sum(x['stateReason']=='NOT_PLANNED' for x in closed),
        'closed_issues_duplicate':sum(x['stateReason']=='DUPLICATE' for x in closed),
        'merged_prs_all_bases':len(merged),'merged_prs_dev':sum(x['baseRefName']=='dev' for x in merged),
        'merged_prs_main':sum(x['baseRefName']=='main' for x in merged),
        'merged_prs_other':sum(x['baseRefName'] not in ['dev','main'] for x in merged)})
csv_write('velocity.csv',velocity)
fig,ax=plt.subplots(figsize=(12.8,7.2),dpi=100);fig.subplots_adjust(left=.09,right=.965,bottom=.22,top=.82)
x=list(range(4));w=.24
for off,key,label,color in [(-w,'closed_issues_all_milestones','Issues closed (all milestones)','#1764ab'),(0,'merged_prs_all_bases','PRs merged (all targets)','#1b8c72'),(w,'merged_prs_dev','PRs merged to dev','#edaa34')]:
    bars=ax.bar([j+off for j in x],[r[key] for r in velocity],width=w,label=label,color=color)
    ax.bar_label(bars,padding=4,fontsize=17,fontweight='bold')
ax.set_xticks(x,[f'Sprint {i}\n{a:%d %b}–{b:%d %b}' for i,(a,b) in enumerate(WINDOWS)])
ax.set_ylabel('Count');ax.set_ylim(0,190);ax.grid(axis='y',alpha=.16);ax.set_axisbelow(True)
fig.text(.09,.935,'Delivery throughput by sprint',fontsize=24,fontweight='bold')
fig.text(.09,.88,'Calendar windows in SGT · issue closures and merged PRs',fontsize=16,color='#475569')
ax.legend(loc='upper left',ncol=1,frameon=False,fontsize=16)
fig.savefig(ROOT/'charts'/'velocity.png',dpi=100);plt.close(fig)

milestones=[f'Sprint {i}' for i in range(4)]+['Unassigned'];backlog=[]
for m in milestones:
    xs=[x for x in ISSUES if milestone(x)==m]
    has=lambda x,l:any(y['name']==l for y in x['labels'])
    backlog.append({'milestone':m,'total':len(xs),'closed':sum(x['state']=='CLOSED' for x in xs),'open':sum(x['state']=='OPEN' for x in xs),
        'mvp':sum(has(x,'mvp') for x in xs),'archived':sum(has(x,'archived') for x in xs),
        'both':sum(has(x,'mvp') and has(x,'archived') for x in xs),
        'neither':sum(not has(x,'mvp') and not has(x,'archived') for x in xs)})
csv_write('backlog-by-milestone.csv',backlog)
labels=Counter(l['name'] for x in ISSUES for l in x['labels'])
csv_write('backlog-by-label.csv',[{'label':l,'total':v,'open':sum(x['state']=='OPEN' and any(y['name']==l for y in x['labels']) for x in ISSUES)} for l,v in sorted(labels.items())])
csv_write('backlog-milestone-label.csv',[{'milestone':m,'label':l,'total':sum(milestone(x)==m and any(y['name']==l for y in x['labels']) for x in ISSUES)} for m in milestones for l in sorted(labels)])

team='''# Rewind — team and agreed effort

SWE5006 Team 14 · presentation **27 October 2026, 14:30 SGT**. Record prepared 26 October.

| Member | Role | Main contributions recorded in progress reports | Effort — agreed split |
| --- | --- | --- | --- |
| Nguyen Kim Long | Developer; requirements and backlog | Sprint 0 backlog and demo profile; Sprint 2 private-group requirements, invitations and access-rule review; final sprint use-case/scope refinement and product/access explanations. | 20%; 10 man-days (80 planned hours) |
| Gopal Guruprasath | Product Owner / Scrum Master; developer and integrator | Sprint 0 capsule summary and pair programming; coordinated implementation, capture/contribution integration, infrastructure and release work; final stabilisation, quality evidence, report structure and demonstration sequence. | 20%; 10 man-days (80 planned hours) |
| Jiang Jiayu | Developer; server and technical integration | Local runtime foundation; persistence, media jobs, compilation and recovery; final recovery/benchmark consolidation, architecture, database and processing-flow explanations. | 20%; 10 man-days (80 planned hours) |
| Phan Mai Tan Loi | Developer; client and UX | App shell, mobile layouts and accessibility; capture/chat/Archive interactions and journey evidence; final fallback/retry/feedback review, user-journey diagrams and demonstration notes. | 20%; 10 man-days (80 planned hours) |
| Sang Haoxiang | Developer; early Scrum/quality support | Minimal overall contribution: Sprint 0 records Scrum facilitation, quality and report evidence. No completed work was reported for Sprint 2 or the final sprint. | 20%; 10 man-days (80 planned hours) |

**Effort basis:** owner-agreed equal split of 50 man-days across five members, using the plan's eight-hour person-day convention: 400 planned hours total. Effort is the **agreed split**: 20% and 10 person-days per member. Gopal's combined PO/Scrum Master assignment follows the owner's fallback decision; The five named members are the presentation roster.

**Attribution limits:** Sprint 2 contributions are the team's reported account. The 24 October report calls the final period “Sprint 4”; here it is **Sprint 3 (11–24 October)**. The presentation uses the owner-agreed split. Sang's minimal wording follows the owner's decision and the reports.

**Sources:** Sprint 0 retained report (`previous-report.txt`, indexed by project-conduct evidence); Sprint 2 report §9; 24 October report §9; Sprint 0 plan capacity assumption. See the source register in AGILE.md. Most implementation was produced with AI coding agents under human direction; GitHub authorship is not an individual labour ledger.
'''
(ROOT/'TEAM.md').write_text(team)

agile='''# Rewind — agile project record

SWE5006 · Collaboration95/rewind-app · presentation **27 October 2026, 14:30 SGT**. GitHub snapshot: **26 October 2026, approximately 22:30 SGT**. Sprint names are zero-based; the 24 October “Sprint 4” report describes **Sprint 3**, not an additional sprint.

## Product backlog

'''
agile+=mdtable(['Current milestone','Total','Closed','Open','mvp','archived','Both','Neither'],[[r[k] for k in ['milestone','total','closed','open','mvp','archived','both','neither']] for r in backlog])
agile+='\nLabels overlap: `archived` overrides delivery scope even when `mvp` is also present. Current labels and milestone membership are a snapshot, not original commitments. '
agile+=f"{len(ISSUES)} issues; {sum(x['state']=='CLOSED' for x in ISSUES)} closed; {sum(x['state']=='OPEN' for x in ISSUES)} open. "
agile+='Closure reasons: '+', '.join(f'{v} {k.lower().replace("_"," ")}' for k,v in sorted(Counter(x['stateReason'] for x in ISSUES if x['state']=='CLOSED').items()))+'.\n\n'
agile+=mdtable(['Selected current label','Issues','Open'],[[l,labels[l],sum(x['state']=='OPEN' and any(y['name']==l for y in x['labels']) for x in ISSUES)] for l in ['mvp','archived','bug','duplicate','doing']])
agile+='\nAll label counts and milestone × label counts are in `data/backlog-by-label.csv` and `data/backlog-milestone-label.csv`. `mvp` is the delivery path; `doing` means current work. GitHub Project boards are not maintained.\n\n## Stories and use cases\n\n'
agile+='Foundation stories: '+issue(5)+' **US-01** launch/navigation; '+issue(6)+' **US-02** select a local demo profile; '+issue(7)+' **US-03** understand the group capsule — all **Sprint 0**. Sprint 1 extended the synthetic journey; Sprint 2 implemented the real-account product.\n\n'
agile+='The UC IDs/titles follow `product.json`; the story sentences and milestone links below are an editorial traceability map, not original issue tags or a preserved commitment. “S2” = Sprint 2, “S3” = Sprint 3. Every numbered issue below has that current milestone in the saved GitHub data.\n\n'
ucrows=[
('UC01','Sign in / restore / sign out','As a member, keep my private account session.','S2 '+issue(168)+'; S3 release identity '+issue(515)),
('UC02','Create / select / switch group','As a member, enter the intended private group.','S2 '+issue(168)+'; S3 switching '+issue(565)),
('UC03','Issue / revoke / accept invite','As an owner/invitee, invite friends and join securely.','S2 '+issue(312)+'; S3 journey verification '+issue(527)),
('UC04','Record / review / trim / submit video','As a member, contribute a clip up to 15 seconds.','S2 '+issue(328)+' / '+issue(329)+'; S3 looks '+issue(367)),
('UC05','Contribute photo','As a member, seal a photo as a three-second segment.','S2 '+issue(313)+'; S3 fallback '+issue(545)+' / JPEG '+issue(574)),
('UC06','Allowance and one correction','As a member, see my five-item/30-second budget and correct once.','S2 '+issue(239)+' / '+issue(340)+'; S3 refresh '+issue(521)),
('UC07','Close cycle and start successor','As a member, get a new collecting cycle automatically.','S2 '+issue(342)+' / '+issue(343)),
('UC08','Compile / retry / publish / archive','As a member, receive one film after cycle closure.','S2 '+issue(343)+'; S3 benchmark '+issue(526)),
('UC09','Owner prompt and group time zone','As an owner, set a shared prompt and local reminder time.','S2 '+issue(346)),
('UC10','Reminder preference and delivery','As a member, opt into weekly web-push reminders.','S2 '+issue(347)+' / '+issue(348)+'; S3 truthful feedback '+issue(524)),
('UC11','Private group chat','As a member, chat, reply and react inside the group.','S2 '+issue(239)+'; S3 reactions '+issue(523)+' / streams '+issue(567)),
('UC12','Premiere and released Archive','As a member, watch the 24-hour premiere and revisit films.','S2 '+issue(345)+'; S3 current state '+issue(521)),
('UC13','Download own clip / group film','As a member, save only media I am authorised to access.','S2 '+issue(344)+'; S3 pagination '+issue(522)+' / Android '+issue(525)),
('UC14','Install / update / invitation return','As a member, install the PWA and retain an invitation through entry.','S2 '+issue(350)+'; S3 Safari/Home Screen verification '+issue(527))]
agile+=mdtable(['UC','Use case','User story','Milestone evidence'],ucrows)
agile+='\nCurrent scope: real accounts; private groups; photos and video; sealed contributions; cycle/film/Archive; chat; web push; web/PWA. Synthetic Demo was removed 6 October. Compiled native iOS and native push are outside the active scope. Release identity and physical-device verification remain open.\n\n## Sprint goals and outcomes\n\n'
agile+=mdtable(['Sprint (SGT)','Goal','Recorded outcome'],[
('0 · 1–12 Sep','Runnable local walking skeleton: demo members, group prompt/countdown/quota, navigation and first checks.','Prototype and runtime foundations delivered; local/synthetic, not real authentication. '+issue(25)+' / '+pr(78)),
('1 · 13–26 Sep','Grow local groups/capture/cycle/Archive toward a repeatable hosted synthetic Demo.','Integrated synthetic journey and audit fixes; 26 Sep report says review ready, Sprint not closed, hosted acceptance outstanding. '+pr(204)+' / '+pr(205)+' / '+pr(206)+' / '+pr(207)),
('2 · 27 Sep–10 Oct','Complete the real-account private-group journey and hosted product.','Accounts/groups, photo/video, S3, film/Archive, web push; Demo removed; hosted dev PostgreSQL and Cognito code. Release parity/device proof incomplete. '+pr(506)+' / '+pr(508)+' / '+pr(510)),
('3 · 11–24 Oct','Stabilise user interactions, harden recovery and prepare assessment material.','Live-state/download/reaction/reminder fixes; refactor, recovery rehearsal, models and explainer. Final report, release and target-device items remain. '+pr(529)+' / '+pr(552)+' / '+pr(581)+' / '+pr(582))])
agile+='\n### Delivery counts and charts\n\n'
agile+=mdtable(['Sprint','Issues closed, all milestones','PRs merged, all targets','dev','main','Other'],[[r[k] for k in ['sprint','closed_issues_all_milestones','merged_prs_all_bases','merged_prs_dev','merged_prs_main','merged_prs_other']] for r in velocity])
agile+='\n'+mdtable(['Replayed milestone','Opening scope','Opening open','Closing scope','Closing open'],scope_summary)
agile+='\nCharts: `charts/burndown-sprint-{0,1,2,3}.png` and `charts/velocity.png`, all 1280×720. CSVs and raw gh snapshots are under `data/`. Burndowns replay milestone assignment/removal, closure and reopen events at opening 00:00 and daily closes · SGT; replay matches all 329 current issue states/milestones. Opening values are at 00:00 on day one. No ideal line is invented: there is no preserved opening commitment. Velocity uses final `closedAt` / `mergedAt` in each SGT window, across all milestones/targets; current own-milestone closure counts are an additional CSV column. PR milestones are retained in `prs.csv`, but mostly absent and are not used to invent sprint assignments. Promotions may count the same implementation twice. Neither metric measures effort or story points.\n\n## Definition of Done\n\n'
agents=(WT/'AGENTS.md').read_text();dod=agents.split('## Definition of Done\n',1)[1].split('\n## Verification tiers',1)[0]
agile+=dod.strip()+'\n\nSource: '+doc('AGENTS.md','worktree AGENTS.md at f6cd896')+'. UI checks use a local browser; client logic uses focused tests plus fast tests; server and real-account flows use local server/SQLite or `make run-real`; HTTPS-only camera/PWA/push/S3/Cognito behaviour needs hosted dev. Web export/routing/PWA/accessibility changes and main promotion additionally require slow tests, coverage and accessibility checks.\n\n## Ceremonies held\n\n'
agile+=mdtable(['Ceremony','Record and evidence boundary'],[
('Project planning','Held, per owner confirmation; plans and scope decisions are the retained outputs.'),
('Sprint Planning — Sprints 0–3','Held each sprint, per owner confirmation. Sprint plans and milestone intake support the selected goals; no exact attendance, duration or meeting dates supplied.'),
('Sprint Review — Sprints 0–3','Held each sprint, per owner confirmation. Reports and '+issue(25)+' record increments and limitations; no invented stakeholder acceptance.'),
('Retrospective outcomes — Sprints 0–3','Reflections below come from progress reports and '+issue(27)+'. Sprint reports record reflections and resulting actions.'),
('Daily Scrum / async updates','The working agreement defines daily coordination; retained work updates are in issue comments.')])
agile+='\n## Retrospectives and subsequent changes\n\n'
agile+=mdtable(['Reflection','Action / observed next-sprint change','Boundary'],[
('Sprint 0: runnable increment succeeded; capacity/evidence decisions were late, work bunched late, hours not tracked.','Sprint 1 agreement: five-issue WIP limit, Day 1 LAN/SQLite/FFmpeg gate, single-device fallback and earlier checkpoint. '+issue(27),'Second-machine rehearsal and actual daily effort were not subsequently proven.'),
('Sprint 1: integrated slice and audit were useful; test doubles missed method binding/native transport; seeded media/quota and infrastructure records drifted.','Sprint 2 delivered real-account and remote-reminder contracts, hosted integration checks, S3/PG/Cognito and removed Demo. '+pr(506)+' / '+pr(510),'The next sprint exercised the real adapters and defined bounded work lanes and interfaces.'),
('Sprint 2: real journey, recovery and faster tests improved delivery; scope churn, release lag, device gaps and hours remained.','Sprint 3 delivered lossless export/install rehearsal, state and download fixes, behavioural tests, refactor and assessment models. '+pr(529)+' / '+pr(577)+' / '+pr(581),'Release '+issue(230)+' / '+issue(504)+' / '+issue(515)+', device '+issue(527)+' and report '+issue(362)+' still open.'),
('Sprint 3: whole-interaction tests exposed retry defects; refactoring and traceable design material helped. Release, device proof, report assembly and effort records lagged.','Final-sprint learning: include recovery, state transitions and feedback in completion; keep explanations linked to tested implementation.','No further sprint is committed. These are closing lessons, not a fabricated next-sprint outcome.')])
agile+='\nProcess simplification occurred **during Sprint 2 on 4 October** (lean DoD / no Project board), per G-pm.md; it is not presented as a change caused by the later 10 October retrospective.\n\n## Outstanding mvp issues — 26 October 2026\n\n'
agile+=mdtable(['Issue','Current milestone','Outstanding outcome'],[[issue(x['number']),milestone(x),x['title']] for x in sorted(OPEN,key=lambda x:x['number'])])
agile+='\nSource command: `gh issue list -R Collaboration95/rewind-app --label mvp --state open --limit 1000`. Seven open at the saved snapshot; #587/#588 were created 25 October SGT, after Sprint 3 ended. Release preparation is not an activated release; dev success does not prove physical iPhone camera/audio/push delivery.\n\n## Source register\n\n'
agile+=mdtable(['Source','Use'],[
('`../audit/G-pm.md` (26 Oct)','Audit cross-check, SGT windows, evidence limits and owner questions, superseded by supplied owner decisions.'),
(doc('doc/planning/sprints/sprint-0-plan.md','Sprint 0 plan')+'; '+doc('doc/planning/sprints/sprint-1-plan.md','Sprint 1 plan')+'; '+doc('doc/planning/sprints/sprint-2-user-journey-plan.md','Sprint 2 plan'),'Goals and planning assumptions.'),
(doc('doc/planning/project-conduct-evidence.md','Project-conduct evidence index'),'Indexes retained original Sprint 0 and 26 Sep report extractions; these were read in the main checkout’s local evidence store. The older archived 12 Sep draft is not treated as the 26 Sep report.'),
(doc('doc/planning/sprints/sprint-2-report/rewind-sprint-2-progress-report.docx','Sprint 2 report'),'§§1–3, 8–10: delivery, contributions, problems and reflection.'),
('24 October report, main checkout: `doc/planning/sprints/sprint-4-report-2026-10-24/rewind-sprint-4-progress-report.md`','§§4–10: final sprint outcomes, reported checks, contributions and reflection. Local untracked source; no fabricated GitHub blob link.'),
(doc('docs/site/content/product.json','product.json')+' / '+doc('docs/site/content/scrum.json','scrum.json')+' / '+doc('docs/site/content/owners.json','owners.json'),'UC inventory and historical context. Legacy four-member roster and 20 Oct/UTC counts are superseded here.'),
('`data/issues.json`, `prs.json`, `issue-timeline.json`, `milestones.json`, `open-mvp.json`','Fresh authenticated read-only gh census; see DATA.md for commands and reconstruction.')])
(ROOT/'AGILE.md').write_text(agile)

findings='''# Rewind — technical findings and issues encountered

Prepared **26 October 2026** for **27 October, 14:30 SGT**. Historical fixes below are documented outcomes, not tests re-run for this record. PR #591 merged on 26 October at 14:38 UTC; Deploy dev run 40344230832 succeeded at aea7478.

| # | Problem | Impact | Fix / current position | Evidence | Lesson |
| --- | --- | --- | --- | --- | --- |
| 1 | New zod advisory GHSA-mrhx-c7xc-m3w5 affected 3.25.76 under Expo CLI after the last green baseline. | Required production audit turned red; small PRs #589/#590 could not merge. | **Merged:** #591 applies the scoped `@expo/cli` override to zod 4.6.6; the selected Quality run 40344231052 passed its production audit and test lanes. | [PR #591](https://github.com/Collaboration95/rewind-app/pull/591); [failed audit run](https://github.com/Collaboration95/rewind-app/actions/runs/40140117765) | A lockfile does not freeze advisory data; distinguish old green results from current audit status. |
| 2 | Alpine 3.24 dropped pinned `ffmpeg=8.1.2-r0`; index offered 8.1.3-r0. | Runtime image failed before vulnerability scanning; the same Dockerfile would block the next dev bundle build. | **Merged:** #591 updates the pin to 8.1.3-r0; Deploy dev run 40344230832 built, scanned and installed the verified bundle. | [PR #591](https://github.com/Collaboration95/rewind-app/pull/591); [failed image build](https://github.com/Collaboration95/rewind-app/actions/runs/40140169755) | Exact version pins alone do not ensure rebuildability when package repositories remove old versions. |
| 3 | apt-get/setup hangs or long stalls were reported in 8 October CI. | D-cicd-demo records a slow Quality tail; external setup delayed feedback. | Later runs recovered. No dedicated apt root-cause fix is established. #517 reduced repeated setup, cached Playwright and parallelised checks; this is a broader improvement, not proof it fixed apt. | [8 Oct run](https://github.com/Collaboration95/rewind-app/actions/runs/37788822883); [PR #517](https://github.com/Collaboration95/rewind-app/pull/517); audit D §1–2 | Separate external setup delays from product/test failures; preserve the failed/slow run and avoid asserting an unproven cause or fix. |
| 4 | Schema registry moved during refactoring, but deploy packaging still read the old location. | Dev bundle verification failed with “no declared schema migration versions” before touching the host. | **Merged:** #583 reads the schema version from `schema.ts`; later dev deployment at f6cd896 succeeded. | [PR #583](https://github.com/Collaboration95/rewind-app/pull/583); [failed run](https://github.com/Collaboration95/rewind-app/actions/runs/39432025788); [later deployment](https://github.com/Collaboration95/rewind-app/actions/runs/39441043830) | Refactoring must cover packaging and release consumers, not just imports and unit tests. |
| 5 | Cognito code introduced runtime dependencies absent from the packaged server image. | Source/tests could pass while the hosted authentication runtime failed. | **Merged:** #511 packages Cognito dependencies in the image; subsequent delivery continued. | [PR #511](https://github.com/Collaboration95/rewind-app/pull/511) | Exercise the built image; source-level dependency resolution is not runtime packaging evidence. |
| 6 | Long-lived screens retained stale cycle/allowance state; older-film downloads searched only the first clip page. | Budgets/reveal status misled users; “save my moments” silently omitted older clips. | **Merged:** #529 refreshes authoritative state and follows independent clip pagination with deduplication, context fencing and retained access checks. | [#521](https://github.com/Collaboration95/rewind-app/issues/521), [#522](https://github.com/Collaboration95/rewind-app/issues/522); [PR #529](https://github.com/Collaboration95/rewind-app/pull/529) | Test long-lived interactions and paginated data, not only first mount and first page. |
| 7 | Denied-camera photo fallback disappeared after Retake; failed-capture retry could do nothing. | A recoverable file/capture journey became a dead end. | **Merged:** #550 preserves capability-based file fallback; #581 fixes retry to return to the viewfinder, with behavioural regression coverage. | [#545](https://github.com/Collaboration95/rewind-app/issues/545); [PR #550](https://github.com/Collaboration95/rewind-app/pull/550); [PR #581](https://github.com/Collaboration95/rewind-app/pull/581); audit E | Test the user’s retry action and actual permission state; a visible button is not proof of recovery. |
| 8 | PWA service-worker forwarding prevented browser SSE cancellation reaching the upstream. | Repeated group switches exhausted five per-account streams and returned HTTP 429. | **Merged:** #568 keeps realtime SSE GETs browser-owned. Isolated Firefox A/B recorded 16 closed streams across eight switches, at most two active, zero rejects. Private API/media cache restrictions remain. | [#567](https://github.com/Collaboration95/rewind-app/issues/567); [PR #568](https://github.com/Collaboration95/rewind-app/pull/568) | Check connection lifetime through service worker and proxy, not just client `close()`. |
| 9 | Expo Camera returned `.jpg` while the adapter expected `jpg` and declared the JPEG as PNG. | Seal failed with HTTP 400 `upload_intent_invalid_media` although upload bytes/hash were valid. | **Merged:** #575 normalises known JPEG/PNG formats at the adapter and preserves strict server validation. Native/emulator evidence is not physical-device acceptance. | [#574](https://github.com/Collaboration95/rewind-app/issues/574); [PR #575](https://github.com/Collaboration95/rewind-app/pull/575) | Verify runtime library values against real bytes; TypeScript declarations can miss platform differences. |
| 10 | Reminder registration could claim success on failure; browser push discovery could block group switching despite authoritative remote cleanup. | False “enabled” feedback and blocked invitation/group transitions. | **Merged:** #529 uses confirmed registration state; #566 separates optional subscription lookup from authoritative cleanup, preserving uncertainty and context fences. | [#524](https://github.com/Collaboration95/rewind-app/issues/524), [#565](https://github.com/Collaboration95/rewind-app/issues/565); [PR #529](https://github.com/Collaboration95/rewind-app/pull/529); [PR #566](https://github.com/Collaboration95/rewind-app/pull/566) | Registration, preference saving and visible notification delivery are separate outcomes. |
| 11 | Review found sessionless Demo cycle mutation and unsafe malformed-path handling in the early local runtime. | A LAN caller could mutate a cycle without a session; malformed segments produced 500s. | **Merged:** review defects #81–#89 were fixed through #91, including access and malformed-input boundaries. Demo was later removed; these are historical findings. | [#82](https://github.com/Collaboration95/rewind-app/issues/82), [#87](https://github.com/Collaboration95/rewind-app/issues/87); [PR #91](https://github.com/Collaboration95/rewind-app/pull/91) | Negative tests must cross the real HTTP/session boundary; local-only does not remove LAN access risk. |
| 12 | Dev success and release preparation diverged; aggregate Quality is branch-required, and hosted DAST follows dev deployment. | A green historical gate does not prove release activation, target-device delivery or enforced security coverage. | **Open/partial:** release #230/#504/#515 and device #527 remain; Deploy dev run 40344230832 retains the installed ZAP baseline and security artifacts. | [#230](https://github.com/Collaboration95/rewind-app/issues/230), [#504](https://github.com/Collaboration95/rewind-app/issues/504), [#515](https://github.com/Collaboration95/rewind-app/issues/515), [#527](https://github.com/Collaboration95/rewind-app/issues/527); [PR #438](https://github.com/Collaboration95/rewind-app/pull/438); audits C/D | Keep source integration, scan reports, required checks, preparation and live release acceptance distinct. |

Sources: progress reports for Sprints 0–3 (see AGILE.md); closed bug bodies in `data/issues.json`; PR records in `data/prs.json`; `../audit/C-devsecops.md`, `D-cicd-demo.md`, `E-testing.md`, and G-pm.md. The audits describe the 26 October observations; no fixes, deployments, scans or test runs were executed for these records. The later selected runs supersede the early PR snapshot: Quality 40344231052 and Deploy dev 40344230832 both succeeded at aea7478. PR #591 merged at 47ea5f0.
'''
(ROOT/'FINDINGS.md').write_text(findings)

(ROOT/'DATA.md').write_text('''# Data and reproduction

All GitHub access used authenticated, read-only `gh`; git commands were read-only. No repository file, issue, label, board, PR or workflow was changed. Output is confined to this records folder. Saved data reflects retrieval on 26 October 2026, approximately 22:25–22:30 SGT, not a prediction of tomorrow’s state.

- `gh issue list -R Collaboration95/rewind-app --state all --limit 1000 --json number,title,body,state,stateReason,createdAt,closedAt,milestone,labels,url`
- `gh pr list -R Collaboration95/rewind-app --state all --limit 1000 --json number,title,body,state,createdAt,closedAt,mergedAt,baseRefName,milestone,url`
- `gh issue list -R Collaboration95/rewind-app --label mvp --state open --limit 1000 --json number,title,state,milestone,labels,url`
- `gh api repos/Collaboration95/rewind-app/milestones?state=all&per_page=100`
- Read-only `gh api graphql` query: repository issues, 50/page with cursor pagination, collecting current state/milestone, creation/closure dates, and milestone/demilestone/close/reopen events. All issue pages fetched; no issue exceeded the 100-event page. Raw results: `data/issue-timeline.json`.
- Supplemental read-only `gh pr view`, `gh run list` and `gh run view --log` established the dependency and build repair and the 8 October setup-delay context. Only relevant log extracts are retained, not credentials or full environment logs.

Rebuild with `python3 build_records.py` in an environment with matplotlib installed. This reads the saved JSON and source documents; it does not refresh GitHub. Temporary rendering dependencies were removed after verification; the script creates a local `.mplconfig` cache when run.

Burndown uses exact event timestamps in SGT, at the next midnight (exclusive), for each day. Only issues assigned to that sprint at that instant contribute. The opening snapshot is at day-one midnight. Reopen events restore open status; milestone changes alter scope. Replay was checked against all current timeline issue states and milestones (zero mismatches). A closed issue can move into a milestone later; therefore closed-in-scope is not necessarily work completed inside the sprint. No original commitment or ideal effort line is inferred.

Velocity uses each issue’s final `closedAt` and each PR’s `mergedAt` in half-open SGT sprint windows, independent of present milestone. It counts each issue once, not every historical close event. Sprint 0 uses 1–12 Sep (the first repository issues are 2 Sep); Sprint 1 13–26 Sep; Sprint 2 27 Sep–10 Oct; Sprint 3 11–24 Oct. Counts outside these windows remain in the raw census. PRs to main include promotions, so all-target throughput is not distinct feature delivery. Extra columns retain current own-milestone closure counts and closure reasons. State reasons and labels describe the saved current snapshot, not historic labels at closure.

CSV inventory: `burndown-sprint-0.csv` through `burndown-sprint-3.csv`; `velocity.csv`; `issues.csv`; `prs.csv`; `issue-events.csv`; `backlog-by-milestone.csv`; `backlog-by-label.csv`; `backlog-milestone-label.csv`. PNGs are exactly 1280×720 with a 100 dpi, 12.8×7.2-inch matplotlib canvas. No tests of the application were re-run; record QA checks only reconstruction, arithmetic, dimensions and readability.
''')
print('Velocity:',velocity)
print('Burndown scope:',scope_summary)
print('Backlog:',backlog)
print('All 329 timeline states/milestones match current snapshot.')
