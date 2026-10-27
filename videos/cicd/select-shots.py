from pathlib import Path
import json,copy
R=Path(__file__).resolve().parent
ix={x['id']:x for x in json.loads((R/'frames-index.json').read_text())}
plan=json.loads((R/'narration-plan.json').read_text())
lookup={
'Pipeline decisions':'00-pipeline','PR #595 checks':'02-pr595-checks','Protected dev':'03-protect-dev','Protected main':'25-protect-main','Quality run graph':'04-quality-graph','Quality artifacts':'06-quality-artifacts','JUnit results':'05-quality-summaries','Coverage summaries':'05b-quality-coverage-summaries','Production dependency audit':'08-term-npm-audit','CodeQL security results':'09-codescan-alerts','PR #592 alert triage':'10-codescan-alert-56','Gitleaks full-history scan':'13-gitleaks-summary','Deploy dev run 40344230832':'14-deploy-graph','Exact-bundle Trivy gate':'17-deploy-summaries','CycloneDX SBOM':'18-term-trivy-sbom','Release manifest':'19-term-manifest','Manifest digests':'70-manifest-digests','GitHub build attestation':'21-attestation','Verify the attestation':'22-term-attest-verify','DAST job summary':'17-deploy-summaries','ZAP HTML report':'23-zap-report','Performance summary':'80-performance','Performance chart':'81-performance-chart','Hosted dev health':'24-term-health','Environment controls':'28-environments','Promotion PR #586':'27-promotion-approval','Decisions and retained artifacts':'99-decisions'}
overrides={'00-pipeline':[970,730],'05-quality-summaries':[990,800],'05b-quality-coverage-summaries':[1130,695],'07-term-quality-reports':[950,460],'17-deploy-summaries':[850,500],'18-term-trivy-sbom':[650,340],'19-term-manifest':[800,380],'70-manifest-digests':[850,470],'22-term-attest-verify':[850,550],'80-performance':[1360,785],'81-performance-chart':[1380,720],'99-decisions':[920,760]}
load=R.parents[1]/'load-test';meta=json.loads((load/'status.json').read_text()) if (load/'status.json').exists() else {}
result=Path(meta['outputDir'])/'results.json' if meta.get('outputDir') else load/'results'/'hosted.json'
if result.exists():
 d=json.loads(result.read_text());s=next(s for s in d['stages'] if s['phase']=='steady' and s['vus']==100)
 perf=f"The full profile ran after deployment, with 1, 10, 25, 50 and 100 virtual users. At 100 VUs, the measured p95 is {round(s['p95Ms'])} milliseconds and throughput is {s['throughputRps']:.2f} requests per second, with {s['errors']} errors across {s['requests']} requests. The retained summary records each steady stage."
else:perf='PERFORMANCE_NARRATION'
shots=[]
for n,s in enumerate(plan):
 f=lookup[s['title']];e=ix.get(f,{})
 row={**s,'id':f'shot-{n:02}-{f}','frame':e.get('file',f'frames/{f}.png'),'focus':overrides.get(f,e.get('focus',[1450,600])),'source':e.get('sourceURL','BRIEF-SHARED.md; audit/D-cicd-demo.md §5'),'evidence':e.get('data','')}
 if s['title']=='Performance summary':row['narration']=perf;row['source']='../../load-test/'+str(result.relative_to(load)) if result.exists() else '../../load-test/status.json';row['evidence']='../../load-test/status.json'
 if s['title']=='DAST job summary':row['focus']=[1490,600]
 if s['title']=='Manifest digests':row['source']='https://github.com/Collaboration95/rewind-app/actions/runs/40344230832';row['evidence']='evidence/terminal/manifest-digests.txt'
 if s['title']=='PR #595 checks' and '02b-pr595-checks-security' in ix:
  row['duration']=20;row['narration']='Pull request 595 contains the pipeline artifact changes. Its checks list shows static analysis, tests and the dependency audit feeding the aggregate Quality gate. The individual results remain visible alongside the required merge check.';shots.append(row)
  e=ix['02b-pr595-checks-security'];row={**row,'id':'shot-01b-pr595-security','title':'PR #595 security checks','duration':16,'frame':e['file'],'source':e['sourceURL'],'focus':e['focus'],'narration':'The same pull request also records CodeQL, image and IaC scans, and secret scanning. These results are visible for security review alongside Quality.'}
 if s['title']=='Deploy dev run 40344230832':
  row['duration']=16;row['narration']='Deploy dev 40344230832 records the artifact-rich deployment. The graph orders change classification, the deploy job and the ZAP baseline against hosted dev.';shots.append(row)
  e=ix['15-deploy-steps'];row={**row,'id':'shot-12b-deploy-steps','title':'Deploy job steps','duration':14,'frame':e['file'],'source':e['sourceURL'],'focus':[950,650],'narration':'The steps wait for Quality on the same commit, build and scan the exact bundle, attest the artifacts, obtain temporary OIDC credentials and install the release.'}
 if s['title']=='Release manifest':
  row['duration']=18;row['narration']='The manifest records the commit, workflow run, successful Quality run, scanner and security-gate result. Its image entries and hashes connect the source verification to the retained deployment artifacts.';shots.append(row)
  e=ix['20-deploy-artifacts'];row={**row,'id':'shot-15b-deploy-artifacts','title':'Retained deployment artifacts','duration':12,'frame':e['file'],'source':e['sourceURL'],'focus':[1100,805],'narration':'The run retains the deployable bundle, the security reports and manifest, and the ZAP reports as three downloadable artifact groups.'}
 shots.append(row)
(R/'shots.json').write_text(json.dumps(shots,indent=2)+'\n')
print(len(shots),'shots',sum(s['duration'] for s in shots),'seconds')
