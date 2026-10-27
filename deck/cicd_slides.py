"""CI/CD section (Section 4): replaces s18 with C1-C18, drops B28/B29, adds CB1-CB3.
Staged source: cicd-section/ (figures, crops, README). Called from build_deck.py after finalise()."""
import html

GH = 'https://github.com/Collaboration95/rewind-app'
_new = []


def slide(sid, title, body, t, spoken, transition, asked='', kind='main', cls='', source=''):
    refs = [r.strip().lstrip('→').strip() for r in asked.split('·')] if asked else []
    _new.append(dict(id=sid, sec=4, tag='DEVSECOPS', title=title, body=body, secs=t, say=[spoken[0][:160]],
                     transition=transition, refs=[r for r in refs if r], source='', script='\n\n'.join(spoken),
                     kind=kind, extra=cls))


def figure(fid, caption, alt, attr='data-figure'):
    return (f'<figure class="figure diagram" {attr}="{fid}"><figcaption>{caption}</figcaption>'
            f'<img src="cicd-section/{fid}.svg" alt="{alt}"></figure>')


def a(href, text):
    return f'<a href="{href}" target="_blank" rel="noopener">{text}</a>'


def tag(kind, text):
    return f'<span class="cx-tag {kind}">{text}</span>'


def pre(text):
    return f'<pre class="cx-pre">{html.escape(text)}</pre>'


def facts(rows):
    return '<dl class="cx-facts">' + ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in rows) + '</dl>'


def shot(src, caption, alt, extra=None):
    inner = f'<div class="figuretitle">{caption}</div><img src="{src}" alt="{alt}">'
    if extra:
        inner += f'<div class="figuretitle cx-after">{extra[1]}</div><img src="{extra[0]}" alt="{extra[2]}">'
    return f'<figure class="figure cx-shot diagram">{inner}</figure>'


def cat(left, right):
    return f'<div class="cx-cat">{left}<div class="cx-side">{right}</div></div>'


def links(*items):
    return '<p class="cx-links">' + ''.join(items) + '</p>'


# ---------------------------------------------------------------- C1 overview
slide('C1', 'One change passes four gates before it reaches hosted dev',
      figure('cicd-1-overview', 'Pipeline view · commit → PR → Deploy dev → hosted dev',
             'Pipeline overview: developer push, PR Quality gate, Deploy dev gates, hosted dev with DAST and promotion'),
      55, [
        'This is the whole pipeline on one page; the next pages zoom into each band. A developer commits on an issue branch. Local git hooks run format, lint, architecture and typecheck, and GitHub push protection rejects known secret patterns at push time.',
        'Band one is the pull request into dev. Quality checks is the only required check, so it is the merge gate. CodeQL, Gitleaks, Trivy and GitGuardian run beside it and report; their results are visible on the PR but do not block the merge.',
        'Band two starts on the same push to dev. Deploy dev first waits for the Quality run on the merge commit, builds one release bundle, scans the exact images inside it, writes the SBOMs and manifest, signs provenance, and only then uploads. The host activates the release only if its health check passes; otherwise it restores the previous release.',
        'Band three is hosted dev. After every deployment, OWASP ZAP scans the running site and reports. Promotion to main is a separate pull request with one human approval.'],
      'Before the detail, a quick key to the shapes and colours.', '→ C2 legend · → C3 source and artifacts',
      cls='figure-slide')

# ---------------------------------------------------------------- C2 legend
slide('C2', 'Colour says what a failure blocks; shape says what the element is',
      '<div class="cx-legend">' + figure('cicd-0-legend', 'Legend · symbols used on every pipeline page',
                                        'Legend: enforcement tags and shapes', attr='data-cxfigure') +
      '<div class="cx-strip"><p><b>Frame</b> = swimlane: where the work runs (developer, GitHub runner, AWS, Lightsail host).</p>'
      '<p><b>Arrow</b> = control flow; its label is the condition (yes / no) or the trigger.</p>'
      '<p><b>Hexagon</b> = gate. Its colour names what a “no” blocks: the merge, the deploy, or the promotion.</p></div></div>',
      30, [
        'Every pipeline page uses the same key. The colour and the first word of a box tell you what happens when it fails. Orange, BLOCKS MERGE: the required Quality check turns red and the pull request cannot merge. Blue, BLOCKS DEPLOY: the deploy stops before upload or before activation, and hosted dev keeps the release it already has. Purple: a platform rule or a human approval, such as push protection or the review on main. Dashed grey, REPORTS: the finding is recorded and visible, but it never stops a merge or a deployment.',
        'Hexagons are decision points. A yes continues the flow; a no stops it. The yellow page shape is a retained artifact, a cylinder is a store, and a box with depth is a running host.'],
      'With that key, start with how source and results are managed.', '→ C3', source='')

# ---------------------------------------------------------------- C3 source + artifacts
slide('C3', 'Protected branches carry source; every run leaves results we can inspect',
      figure('cicd-7-source-artifacts', 'Source and artifact view · branches, protection, retention',
             'Source and artifact management: issue branch to protected dev to protected main; Git, Actions artifacts, Security tab, attestations, host releases'),
      50, [
        'Source management: work starts on an issue branch from the latest dev and enters dev only through a pull request. The dev rule requires the check named Format, lint, typecheck, and test, requires the branch to be up to date, requires conversations to be resolved, applies to administrators, and forbids force-pushes and deletion. Main has the same rule plus one approving review, including approval of the last push, and its Quality run adds the browser and PWA checks.',
        'Artifact management: Git keeps source, the lockfile, workflows, Terraform and Dockerfiles permanently. Each workflow run keeps its machine-readable results as Actions artifacts named with the commit SHA: thirty days for JUnit, npm audit, SARIF, Trivy, IaC, SBOMs, the manifest and the release tar; fourteen days for coverage; ninety days for the ZAP reports. CodeQL and Gitleaks results go to the Security tab. Signed provenance sits in GitHub attestations. The host keeps only the current, previous and pending releases, so rollback always has a target.'],
      'Now zoom into the pull request band.', '→ CB2 branch protection settings', cls='figure-slide')

# ---------------------------------------------------------------- C4 PR quality
slide('C4', 'The Quality workflow fans out nine jobs into one required merge check',
      figure('cicd-2-pr-quality', 'Activity view · quality.yml on a pull request',
             'Quality workflow: classify change scope, eight parallel jobs, required gate'),
      45, [
        'This is quality.yml on a pull request. The first job classifies the change. If only Markdown documentation changed, every job is skipped and the gate passes in about twenty seconds. Otherwise eight lanes run in parallel: four static checks, the production dependency audit, root and IaC tests, server tests on SQLite with coverage, the same server suite on PostgreSQL 17, frontend Jest with a seventy percent statement threshold, and the deployment fixtures. Main-bound pull requests also run the web export, PWA and accessibility checks.',
        'The last job, Format, lint, typecheck, and test, requires every lane to succeed. It is the one check named in branch protection, so a red lane means the merge button stays disabled.'],
      'Beside Quality, the security workflows run and report.', '→ C16 tests and coverage numbers', cls='figure-slide')

# ---------------------------------------------------------------- C5 PR security
slide('C5', 'Security workflows run beside Quality and keep their findings',
      figure('cicd-3-pr-security', 'Activity view · CodeQL, Secret scan, Release security, GitGuardian, Dependabot',
             'Security workflows on a PR and where their outputs are stored'),
      35, [
        'Five security procedures run on the same pull request. CodeQL is our SAST. Gitleaks scans the full git history for secrets. Release security builds both images, writes a CycloneDX SBOM and fails on High or Critical vulnerabilities, and scans Terraform and Dockerfiles. GitGuardian and Dependabot add secret and dependency alerts.',
        'These are reporting controls: they can turn their own job red, and the findings land in the Security tab or as artifacts, but they are not required checks. The vulnerability gate that does block is in the deployment, on the exact images we ship. That is the next page.'],
      'After merge, the same push starts Deploy dev.', '→ C9 catalogue', cls='figure-slide')

# ---------------------------------------------------------------- C6 deploy build
slide('C6', 'Deploy scans and signs the exact bundle before anything is uploaded',
      figure('cicd-4-deploy-build', 'Activity view · deploy-dev.yml stage 1 of 2',
             'Deploy dev stage 1: Quality wait, bundle build, exact-bundle scan, artifacts, attestation'),
      45, [
        'The merge to dev starts Deploy dev. Its first gate polls the Quality run for this exact merge commit; if that run fails, the deploy refuses and the host is untouched. Then release.py builds one tar containing the runtime and web images and verifies it.',
        'scan-release.py does not rebuild anything. It extracts the two image archives from that tar, runs Trivy to produce a CycloneDX SBOM and a JSON report for each, and checks that Trivy saw the same image IDs and a non-empty Alpine package list. Any High or Critical finding stops the job before upload. The SBOMs, reports and release manifest are kept even when the gate fails.',
        'Finally attest-build-provenance signs the tar and the manifest, and the bundle is kept with its Sigstore attestation.'],
      'Only then does the runner touch AWS.', '→ C14 SBOM and provenance', cls='figure-slide')

# ---------------------------------------------------------------- C7 deploy ship
slide('C7', 'Keyless AWS access and a health check decide activation',
      figure('cicd-5-deploy-ship', 'Activity view · deploy-dev.yml stage 2 of 2',
             'Deploy dev stage 2: OIDC role, temporary SSH, checksum, install, health check, restore'),
      35, [
        'GitHub has no AWS keys. The job exchanges its OIDC token for a one-hour role session, and the role trusts only this repository, the dev environment and refs/heads/dev. The runner checks the host is running, opens port 22 for its own address only with a short-lived key, ships the bundle and streams the hosted settings from a private S3 object.',
        'On the host, the uploaded tar must match the built tar’s SHA-256. The installer starts the candidate images and activates them only when health is ready and the running image IDs match; otherwise it restores the previous release and the job turns red. Then the public health endpoint is checked, SSH is closed and the key deleted, and the DAST job starts.'],
      'The DAST job is the last stage.', '→ CB3 deploy job steps screenshot', cls='figure-slide')

# ---------------------------------------------------------------- C8 DAST stage
slide('C8', 'ZAP scans the running hosted site after every deploy',
      figure('cicd-6-dast', 'Activity view · DAST job in deploy-dev.yml',
             'DAST: ZAP baseline against hosted dev, report-only, reports retained'),
      30, [
        'DAST runs as a second job that needs the deploy. It uses the OWASP ZAP baseline action: a spider and an AJAX spider crawl the single-page app for two minutes, and passive rules inspect every response. It is unauthenticated and sends no attacks, because hosted dev holds shared data. The rules file only ignores two noise rules, timestamps in the minified bundle and the “modern web application” note.',
        'The job is report-only: fail_action is false, so findings never fail the run. It publishes a risk table in the run summary and keeps JSON, HTML and Markdown reports for ninety days. This run found zero High and four Medium findings, all about Content Security Policy.'],
      'That completes the pipeline. Here is everything it checks for, in one table.', '→ C15 DAST results', cls='figure-slide')

# ---------------------------------------------------------------- C9 catalogue
cat_rows = [
    ('SAST', 'CodeQL · JS/TS, Python, Actions', 'PR · push · weekly', tag('report', 'REPORTS'), '0 open · alerts 54–56 triaged', a(f'{GH}/actions/runs/40344231062', 'run ↗')),
    ('SCA', 'npm audit HIGH+ · Dependabot', 'PR · push', tag('merge', 'BLOCKS MERGE'), 'zod GHSA blocked PRs → fixed', a(f'{GH}/actions/runs/40140117765/job/121009940136', 'red run ↗')),
    ('Secrets', 'Gitleaks · GitGuardian · push protection', 'push · PR', tag('human', 'BLOCKS PUSH') + ' ' + tag('report', 'REPORTS'), '0 findings, full history', a(f'{GH}/actions/runs/40344231125', 'run ↗')),
    ('Containers', 'Trivy · exact bundled images', 'Deploy dev', tag('deploy', 'BLOCKS DEPLOY'), '0 High / 0 Critical', a(f'{GH}/actions/runs/40344230832/job/121646847180', 'job ↗')),
    ('IaC', 'Trivy config + exact exceptions', 'PR · push', tag('report', 'REPORTS'), '8 High accepted · 7 Low', a(f'{GH}/actions/runs/40344231046/job/121646748045', 'job ↗')),
    ('SBOM', 'CycloneDX 1.6 per image', 'Deploy dev', tag('deploy', 'IN MANIFEST'), '187 + 72 components', a(f'{GH}/actions/runs/40344230832/artifacts/12660009356', 'artifact ↗')),
    ('Provenance', 'attest-build-provenance · Sigstore', 'Deploy dev', tag('deploy', 'BLOCKS DEPLOY'), 'gh attestation verify ✓', a(f'{GH}/attestations/59963857', 'attestation ↗')),
    ('DAST', 'OWASP ZAP baseline · hosted dev', 'after deploy', tag('report', 'REPORTS'), '0 H · 4 M · 7 L · 6 Info', a(f'{GH}/actions/runs/40344230832/job/121650940821', 'job ↗')),
    ('Tests', 'node:test · Jest · PostgreSQL 17', 'PR · push', tag('merge', 'BLOCKS MERGE'), '2,782 passed · 89.6% / 85.5%', a(f'{GH}/actions/runs/40343459119', 'run ↗')),
]
rows = ''.join(f'<tr><td>{c}</td><td>{t}</td><td>{w}</td><td>{d}</td><td>{r}</td><td>{l}</td></tr>' for c, t, w, d, r, l in cat_rows)
slide('C9', 'Nine kinds of check, each with a recorded result and a link',
      f'<table class="data cx-table"><thead><tr><th>Check</th><th>Tool</th><th>Runs on</th><th>Failure</th><th>Result · aea7478</th><th>Open</th></tr></thead><tbody>{rows}</tbody></table>',
      40, [
        'This is the catalogue of what we check for. Each row is a procedure the course asks for, with its tool, its trigger, what a failure blocks, the real result for the commit we deployed, aea7478, and a link to the GitHub page that holds it.',
        'Two rows block merges: the dependency audit and the tests, because both are inside Quality. Three block the deployment: the exact-bundle Trivy scan, a failed attestation step, and the health check. SAST, IaC, Gitleaks and DAST report. The next slides take one row each and show the real artifact behind it.'],
      'First row: SAST.', '→ C10–C16', source='Commit aea7478 · Deploy dev 40344230832 · Quality 40344231052')

# ---------------------------------------------------------------- C10 SAST
alert = '''{
  "number": 56,
  "state": "dismissed",
  "rule": { "id": "js/http-to-file-access",
            "security_severity_level": "medium" },
  "location": { "path": "scripts/load/hosted.mjs",
                "start_line": 417 },
  "dismissed_reason": "used in tests"
}'''
slide('C10', 'SAST: CodeQL findings are triaged with a written reason',
      cat(shot('cicd-section/shots/crop-codeql-run.png', 'CodeQL run 40344231062 · three language analyses', 'CodeQL workflow run with JavaScript/TypeScript, Python and Actions analyses'),
          facts([('Tool', 'CodeQL · <code>security-extended</code> queries · JavaScript/TypeScript, Python, GitHub Actions'),
                 ('Runs on', 'every PR, push to dev / main, Mondays 03:23 UTC'),
                 ('Failure', tag('report', 'REPORTS') + ' alerts go to Security › Code scanning; 0 open'),
                 ('Example', 'PR #592 load-test script: alerts 54–56 (file ↔ network data), dismissed “used in tests”: operator-run harness, never shipped in the app image')]) +
          pre(alert) +
          links(a(f'{GH}/security/code-scanning/56', 'Alert 56 ↗'), a(f'{GH}/security/code-scanning/54', 'Alert 54 ↗'),
                a(f'{GH}/security/code-scanning/55', 'Alert 55 ↗'), a(f'{GH}/actions/runs/40344231062', 'CodeQL run ↗'))),
      35, [
        'SAST is CodeQL with the security-extended query suite on three languages: our TypeScript and JavaScript, the Python deployment scripts, and the workflow files themselves. It runs on every pull request, every push to dev and main, and weekly.',
        'A real example: the load-test pull request, 592, raised three medium alerts in scripts/load/hosted.mjs, because the script sends fixture files over the network and writes the results to a path the operator chooses. We reviewed them and dismissed them as used in tests, with a written reason: it is an operator-run harness that never ships in the application image. The alert, the rule, the line and the reason stay on record. Today there are no open alerts.'],
      'Next, dependencies, where a real advisory blocked us.', '→ alert 56 page live', source='')

# ---------------------------------------------------------------- C11 SCA
zod = '''$ npm audit --omit=dev --audit-level=high
zod  <4.6.6
Severity: high
Zod can exhaust memory while validating oversized constrained
collections - https://github.com/advisories/GHSA-mrhx-c7xc-m3w5
node_modules/expo/node_modules/zod
3 high severity vulnerabilities'''
after = '''"metadata": { "vulnerabilities": { "high": 0, "critical": 0,
  "total": 0 }, "dependencies": { "prod": 674, "total": 1119 } }'''
slide('C11', 'SCA: a new zod advisory blocked merges until we fixed it',
      cat('<figure class="figure cx-shot cx-pre-card"><div class="figuretitle">Job log · Production dependency audit · run 40140117765 · 24 Oct</div>' + pre(zod) +
          '<div class="figuretitle cx-after">After PR #591 · npm-audit.json · Quality 40344231052</div>' + pre(after) + '</figure>',
          facts([('Tool', '<code>npm audit --omit=dev --audit-level=high</code> in Quality · Dependabot alerts and security updates'),
                 ('Runs on', 'every PR and push · inside the required check'),
                 ('Failure', tag('merge', 'BLOCKS MERGE') + ' and, via same-commit Quality, ' + tag('deploy', 'BLOCKS DEPLOY')),
                 ('Fix', 'PR #591: scoped override <code>@expo/cli → zod 4.6.6</code>; no forced Expo major upgrade; audit back to 0')]) +
          links(a('https://github.com/advisories/GHSA-mrhx-c7xc-m3w5', 'GHSA-mrhx-c7xc-m3w5 ↗'),
                a(f'{GH}/actions/runs/40140117765/job/121009940136', 'Failed audit ↗'),
                a(f'{GH}/pull/591', 'PR #591 ↗'),
                a(f'{GH}/actions/runs/40344231052/artifacts/12660088334', 'npm-audit.json ↗'))),
      40, [
        'SCA is the production dependency audit, inside the required check. On 24 October, with no code change from us, a new advisory, GHSA-mrhx-c7xc-m3w5, marked zod below 4.6.6 as high severity: oversized collections can exhaust memory. Our copy came in through Expo’s CLI. Three high findings turned Quality red and two small pull requests could not merge. That is the gate working as designed.',
        'npm suggested a forced, breaking Expo upgrade. Instead PR 591 added a scoped override so only Expo’s CLI uses zod 4.6.6. The retained npm-audit.json for the deployed commit shows zero vulnerabilities at every severity across 674 production dependencies. Dependabot adds alerts and security update pull requests; the one open alert is a development-only package.'],
      'Secrets next.', '→ C17 findings row 1', source='')

# ---------------------------------------------------------------- C12 secrets
toml = """[extend]
useDefault = true

[[allowlists]]
condition = "AND"   # path AND value
targetRules = ["generic-api-key"]
paths = ['''^server/src/(schema|db)\\.ts$''']
regexes = ['''^(contribution-deletion-v1|contribution-ledger-v1|contribution-quota-v1)$''']"""
slide('C12', 'Secrets are checked at push, on the PR and across history',
      cat(shot('cicd-section/shots/crop-secret-scan-run.png', 'Secret scan 40344231125 · Gitleaks full-history job + SARIF artifact', 'Secret scan run with Gitleaks job'),
          facts([('Push', tag('human', 'BLOCKS PUSH') + ' GitHub secret scanning + push protection, enabled · 0 alerts'),
                 ('PR', tag('report', 'REPORTS') + ' GitGuardian app check · “4 commits scanned”'),
                 ('History', tag('report', 'REPORTS') + ' Gitleaks v8.30.1 over full history · redacted SARIF · <b>0 findings</b>')]) +
          pre(toml) +
          links(a(f'{GH}/actions/runs/40344231125', 'Secret scan run ↗'), a(f'{GH}/pull/595/checks', 'PR #595 checks ↗'))),
      30, [
        'Secrets are checked in three places. At push time, GitHub push protection rejects known provider key patterns before they reach the repository. On the pull request, GitGuardian scans the new commits. And the Secret scan workflow runs Gitleaks over the entire git history on every pull request and push, keeping a redacted SARIF report and sending it to the Security tab.',
        'The default rules flagged migration identifiers and two test keys as generic API keys. Rather than silence the rule, the allowlist requires the exact file and the exact value, so a real key in the same file would still be found. The current result is zero findings.'],
      'Containers and infrastructure.', '→ C17 findings', source='')

# ---------------------------------------------------------------- C13 containers + IaC
exc = '''{ "id": "AWS-0011",
  "target": "infra/terraform/release/main.tf",
  "resource": "aws_cloudfront_distribution.release",
  "owner": "Guruprasath",
  "expires": "2026-10-31",
  "reason": "Accepted risk: ... without AWS WAF; a web ACL
             adds monthly cost outside this academic deployment." }'''
slide('C13', 'Trivy blocks risky images; IaC risks need dated exceptions',
      cat(shot('cicd-section/shots/crop-release-security-run.png', 'Release security 40344231046 · image + IaC scans, three artifacts', 'Release security run with runtime, web and IaC scan jobs'),
          facts([('Images', 'Trivy v0.70.0 on runtime + web images · PR, push, tags · deploy repeats it on the <b>exact bundle</b> ' + tag('deploy', 'BLOCKS DEPLOY')),
                 ('Bundle result', 'runtime 0 High / 0 Critical · 1 Medium (zlib CVE-2026-85091, fix 1.3.2-r1) · 2 Unknown (musl) · web 0'),
                 ('IaC', '<code>trivy config .</code> on Terraform + Dockerfiles → 15 findings: 8 High, each matched to one exception · 7 Low'),
                 ('Rule', 'unmatched High or an expired exception fails the job · all 8 expire 31 Oct 2026')]) +
          pre(exc) +
          links(a(f'{GH}/actions/runs/40344231046/job/121646748045', 'IaC job ↗'),
                a(f'{GH}/actions/runs/40344231046/artifacts/12661016554', 'iac-full.json ↗'),
                a(f'{GH}/actions/runs/40344230832/job/121646847180', 'Bundle scan job ↗'))),
      35, [
        'Trivy scans our two container images twice. Release security scans candidate images on pull requests and pushes. The deployment then scans the images inside the exact bundle it will upload, and that second scan is the one that blocks: any High or Critical stops the upload. For this deployment both images had zero High and Critical. The runtime image has one Medium in zlib with a fix available, and two Unknown entries in musl.',
        'For infrastructure as code, Trivy config scans Terraform and Dockerfiles. It found fifteen issues: seven Low and eight High. Every High must match exactly one exception with an owner, a reason and an expiry date. Most are about customer-managed KMS keys and a WAF that would add cost. The exceptions expire on 31 October, and after that the job fails until each risk is reviewed again.'],
      'The image scan feeds the SBOM and provenance.', '→ C14', source='')

# ---------------------------------------------------------------- C14 SBOM + provenance
sbom = '''// sbom-runtime.cdx.json · CycloneDX 1.6
{ "name": "ffmpeg", "version": "8.1.3-r0",
  "purl": "pkg:apk/alpine/ffmpeg@8.1.3-r0" }
// release-manifest.json
"security_gate": "pass",
"rewind-release.tar": "fef3c22a19a2…6e01"'''
verify = '''$ gh attestation verify release-manifest.json \\
    --repo Collaboration95/rewind-app
✓ Verification succeeded!   (exit 0)'''
slide('C14', 'SBOM and provenance bind shipped bytes to scans and workflow',
      cat(shot('cicd-section/shots/crop-attestations.png', 'Attestation 59963857 · build provenance for aea7478', 'GitHub attestation page for deploy run 40344230832'),
          facts([('SBOM', 'Trivy CycloneDX 1.6 per bundled image · runtime 187 · web 72 components'),
                 ('Manifest', 'commit, run, Quality run, image IDs, digests, severity counts, SHA-256 of tar + SBOMs + reports'),
                 ('Provenance', '<code>actions/attest-build-provenance</code> · SLSA v1 · Sigstore, signed with the job’s OIDC identity')]) +
          pre(sbom) + pre(verify) +
          links(a(f'{GH}/attestations/59963857', 'Attestation ↗'),
                a(f'{GH}/actions/runs/40344230832/artifacts/12660009356', 'SBOMs + manifest ↗'),
                a(f'{GH}/actions/runs/40344230832/artifacts/12659883748', 'Bundle + Sigstore ↗'))),
      40, [
        'The SBOM is a CycloneDX inventory of each exact bundled image: 187 components in the runtime image, including the FFmpeg package we had to re-pin, and 72 in the web image. The release manifest records the commit, the run, the Quality run that allowed it, both image IDs and digests, the severity counts, and the SHA-256 of the tar, both SBOMs and both reports. So inventory, findings and bytes are bound together.',
        'Provenance: the deploy job signs the tar and the manifest with GitHub’s attest-build-provenance, using Sigstore and the job’s own OIDC identity. Anyone can check it: gh attestation verify on the downloaded manifest succeeds and names deploy-dev.yml on refs/heads/dev as the workflow that built it.'],
      'The last security procedure looks at the running site.', '→ C6', source='')

# ---------------------------------------------------------------- C15 DAST results
zrows = [
    ('Medium', 'CSP: Failure to Define Directive with No Fallback · Wildcard Directive · script-src unsafe-inline · style-src unsafe-inline'),
    ('Low', 'COEP · COOP · CORP header missing · Permissions-Policy not set · Server version (nginx/1.31.6) · Dangerous JS functions (eval in bundle) · Timestamp disclosure'),
    ('Info', 'CSP Report-Only header found · Suspicious comments (sw.js) · Modern web app · Non-storable · Cache-control · Storable content'),
]
zt = ''.join(f'<tr><td>{r}</td><td>{n}</td></tr>' for r, n in zrows)
ex = '''Alert   CSP: Failure to Define Directive with No Fallback
Risk    Medium (High confidence) · plugin 10055 · CWE-693
URL     GET https://d2m6kz76y4kuvm.cloudfront.net  (+ /robots.txt, /sitemap.xml)
Param   Content-Security-Policy
Evidence  frame-ancestors 'none'
Other   form-action is among the directives that do not fall back to default-src'''
slide('C15', 'DAST: 0 High, 4 Medium, all from one Content Security Policy gap',
      cat(shot('cicd-section/shots/crop-zap-summary.png', 'ZAP report · run 40344230832 · summary of alerts', 'ZAP summary: 0 High, 4 Medium, 7 Low, 6 Informational', ('cicd-section/shots/crop-zap-csp-detail.png', 'Medium · CSP: Wildcard Directive · request and evidence', 'ZAP CSP wildcard finding detail')),
          f'<table class="data cx-table cx-ztable"><tbody>{zt}</tbody></table>' + pre(ex) +
          '<p class="cx-note"><b>Why:</b> the enforced header sets only <code>frame-ancestors</code>; the full policy ships as Report-Only. <b>Next:</b> enforce it.</p>' +
          links(a('../pipeline-run-40344230832/zap/report_html.html#10055', 'ZAP HTML · 10055 ↗'),
                a('../pipeline-run-40344230832/zap/report_html.html#10038', 'Report-Only ↗'),
                a(f'{GH}/actions/runs/40344230832/job/121650940821', 'DAST job ↗'),
                a(f'{GH}/actions/runs/40344230832/artifacts/12660614474', 'zap-baseline ↗'))),
      40, [
        'Here are the real ZAP results for the deployed commit: zero High, four Medium, seven Low and six informational alert types. All four Medium alerts are Content Security Policy findings.',
        'Take the first one. ZAP sent a GET to the hosted home page, robots.txt and sitemap.xml, read the Content-Security-Policy header, and found only frame-ancestors none. Directives such as form-action do not fall back to default-src, so they are effectively unrestricted. The informational alert explains why: our full policy is served as Content-Security-Policy-Report-Only, so browsers report violations but do not enforce them. The fix is to promote that policy to enforced once its reports are clean. The Low findings are missing hardening headers and the nginx version string.'],
      'Tests and coverage complete the catalogue.', '→ open the HTML report', source='')

# ---------------------------------------------------------------- C16 tests
trows = [('Root and IaC', '123 passed · 1 skipped', 'JUnit XML'), ('Server · SQLite', '985 passed · 21 skipped', '85.5% lines'),
         ('Server · PostgreSQL 17', 'same suite, hosted engine', 'pass'), ('Frontend · Jest', '1,674 passed', '89.64% statements · gate 70%'),
         ('Static ×4 · fixtures', 'format, lint, architecture, typecheck · deploy fixtures', 'pass')]
tt = ''.join(f'<tr><td>{a_}</td><td>{b}</td><td>{c}</td></tr>' for a_, b, c in trows)
slide('C16', 'Tests and coverage gate the merge and are kept as artifacts',
      cat(shot('cicd-section/shots/crop-quality-graph-artifacts.png', 'Quality run 40344231052 · retained artifacts', 'Quality checks run with coverage, test and audit artifacts'),
          f'<table class="data cx-table"><thead><tr><th>Lane</th><th>Result · PR run 40343459119</th><th>Kept</th></tr></thead><tbody>{tt}</tbody></table>' +
          facts([('Failure', tag('merge', 'BLOCKS MERGE') + ' any red lane fails the required check')]) +
          links(a(f'{GH}/actions/runs/40343459119', 'PR Quality run ↗'), a(f'{GH}/actions/runs/40344231052', 'dev Quality run ↗'))),
      20, [
        'Tests are part of the same gate. On the filmed pull request run, root tests passed 123, the server suite passed 985 with 85.5 percent line coverage, and the frontend passed 1,674 with 89.6 percent statement coverage against a seventy percent threshold. The server suite also runs on PostgreSQL 17, the hosted engine. Every lane keeps JUnit, Jest JSON or coverage JSON as artifacts on the run.'],
      'What did the pipeline teach us?', '→ C4', source='')

# ---------------------------------------------------------------- C17 findings
frows = [
    ('A new advisory hit a locked dependency (zod, GHSA-mrhx-c7xc-m3w5)', 'Audit red; PRs #589, #590 blocked', 'Scoped override to zod 4.6.6 (#591)', a(f'{GH}/actions/runs/40140117765', 'run ↗')),
    ('Alpine dropped the pinned <code>ffmpeg=8.1.2-r0</code>', 'Runtime image failed to build', 'Re-pin to 8.1.3-r0 (#591)', a(f'{GH}/actions/runs/40140169755', 'run ↗')),
    ('Scanned image ≠ deployed image: deploy rebuilt it', 'Scan result did not describe shipped bytes', 'Scan the exact bundle; manifest + attestation (#595)', a(f'{GH}/pull/595', 'PR ↗')),
    ('Gitleaks default rules: 27 false positives in history', 'Secret job would be red from day one', 'Allowlist exact path AND exact value', a(f'{GH}/actions/runs/40344231125', 'run ↗')),
    ('Schema registry moved; packaging read the old path', 'Bundle verify failed before the host', 'Read declared version from schema.ts (#583)', a(f'{GH}/actions/runs/39432025788', 'run ↗')),
    ('Cognito runtime dependencies missing from the image', 'Tests passed; built image could not sign in', 'Package them in the image (#511)', a(f'{GH}/pull/511', 'PR ↗')),
]
ft = ''.join(f'<tr><td>{p}</td><td>{i}</td><td>{f}</td><td>{l}</td></tr>' for p, i, f, l in frows)
slide('C17', 'The pipeline caught problems that source-level tests could not',
      f'<table class="data cx-table cx-findings"><thead><tr><th>Finding</th><th>Impact</th><th>Fix</th><th>Evidence</th></tr></thead><tbody>{ft}</tbody></table>'
      '<div class="takeaway">Verify what ships: the advisory database, the package index and the built image change without a code change.</div>',
      45, [
        'Six technical findings. First, on 24 October a new zod advisory turned the audit red with no change from us, and the gate blocked two pull requests until PR 591 fixed it. Second, the same week Alpine removed the FFmpeg version we pinned, so the runtime image stopped building; we re-pinned to the available version.',
        'Third, an audit of our own pipeline found that the image we scanned was not the image we deployed, because deployment rebuilt it. PR 595 moved the gate onto the exact bundle and added the manifest and attestation. Fourth, Gitleaks’ default rules reported twenty-seven false positives in history; we allowlisted exact values, not whole files.',
        'Fifth, a refactor moved the schema registry while packaging still read the old path; bundle verification caught it before the host was touched. Sixth, Cognito code passed its tests but its runtime dependencies were missing from the built image. The lesson is to verify what ships, not just the source.'],
      'Now the live route through GitHub.', '→ B31 product findings', source='')

# ---------------------------------------------------------------- C18 demo route
steps = [
    ('1', 'PR #595 › Checks', f'{GH}/pull/595/checks', 'Quality, CodeQL, Secret scan, Release security, GitGuardian', '00:20'),
    ('2', 'Quality run graph + artifacts', f'{GH}/actions/runs/40344231052', 'classify → 9 lanes → gate · 4 artifacts', '01:44'),
    ('3', 'Code scanning alert 56', f'{GH}/security/code-scanning/56', 'rule, line, “used in tests” + reason', '04:08'),
    ('4', 'Deploy dev run 40344230832', f'{GH}/actions/runs/40344230832', 'classify → deploy → DAST · 3 artifacts', '05:02'),
    ('5', 'Deploy job steps', f'{GH}/actions/runs/40344230832/job/121646847180', 'Quality wait → scan → attest → OIDC → install', '05:18'),
    ('6', 'Attestation 59963857', f'{GH}/attestations/59963857', 'subjects: tar + manifest · workflow identity', '07:18'),
    ('7', 'ZAP HTML report', '../pipeline-run-40344230832/zap/report_html.html#10055', 'summary table → CSP finding evidence', '08:40'),
    ('8', 'Hosted dev health', 'https://d2m6kz76y4kuvm.cloudfront.net/api/health', 'HTTP 200 · PostgreSQL · schema ready', '10:06'),
]
st = ''.join(f'<tr><td>{n}</td><td>{a(u, p + " ↗")}</td><td>{s}</td></tr>' for n, p, u, s, t in steps)
slide('C18', 'Demo route: eight clicks from pull request to running site',
      f'<table class="data cx-table cx-route"><thead><tr><th>#</th><th>Open</th><th>Point at</th></tr></thead><tbody>{st}</tbody></table>'
      '<p class="cx-note">Terminal: <code>gh attestation verify --repo Collaboration95/rewind-app release-manifest.json</code></p>',
      20, [
        'This is the click route for the live part. Each link opens the real page; if the network fails, play the recorded walkthrough (backup CB1). The order follows the pipeline: pull request checks, the Quality run and its artifacts, a triaged CodeQL alert, the Deploy dev run, its steps, the attestation, the ZAP report, and finally the hosted health endpoint. Keep each page to about fifteen seconds.'],
      'Close the CI/CD section and move to the system demonstration.', '→ CB1 recorded film', source='')

# ================================================================= backups
prot = [('Required status check', 'Format, lint, typecheck, and test', 'same'),
        ('Branch up to date (strict)', 'yes', 'yes'), ('Approving reviews', '0', '1 · last push must be approved'),
        ('Conversation resolution', 'required', 'required'), ('Applies to administrators', 'yes', 'yes'),
        ('Force-push / deletion', 'blocked', 'blocked'), ('Extra Quality lane', '—', 'web export, PWA, accessibility')]
pt = ''.join(f'<tr><td>{a_}</td><td>{b}</td><td>{c}</td></tr>' for a_, b, c in prot)
slide('CB2', 'Branch protection: dev automates the gate; main adds a human review',
      f'<table class="data cx-table"><thead><tr><th>Rule</th><th>dev</th><th>main</th></tr></thead><tbody>{pt}</tbody></table>'
      '<p class="cx-note">Repository security: secret scanning and push protection on · Dependabot security updates on · all actions pinned to commit SHAs · default token read-only.</p>'
      + links(a(f'{GH}/settings/branches', 'Branch settings ↗'), a(f'{GH}/pull/586', 'Promotion PR #586 ↗')),
      0, ['Values read from the branch-protection API for dev and main on 27 October. Only one check is required on both branches; the other security workflows report. Main adds one approving review with last-push approval and the browser lane.'],
      'Return to C3.', '', kind='back', source='')

slide('CB3', 'Deploy job steps in GitHub, in the order of the stage diagrams',
      cat(shot('cicd-section/shots/15-deploy-steps.png', 'Deploy dev 40344230832 · job steps', 'Deploy job step list'),
          shot('cicd-section/shots/20-deploy-artifacts.png', 'Same run · three retained artifacts', 'Deploy run artifacts list')),
      0, ['Real capture of the deploy job step list and its retained artifacts: dev-release-security, dev-release-bundle and zap-baseline, each named with the commit SHA.'],
      'Return to C7.', '', kind='back', source='')

CICD_CSS = '''
/* CI/CD section additions; scoped by cx- prefix. Text never below 14 px at 1280x720. */
.cx-tag{display:inline-block;font:700 14px var(--sans);letter-spacing:.2px;padding:2px 7px;border-radius:5px;border:2px solid;white-space:nowrap;vertical-align:1px}
.cx-tag.merge{background:#FBE7DA;border-color:#B4501A;color:#7a3511}.cx-tag.deploy{background:#E1ECF7;border-color:#2C64A0;color:#1d4673}
.cx-tag.human{background:#EEE7F3;border-color:#75528F;color:#4f3563}.cx-tag.report{background:#F1F5F4;border-color:#6B7A80;border-style:dashed;color:#3f4b50}
.cx-table{font-size:17px;line-height:1.25}.cx-table th{font-size:14px;padding:6px 8px 8px}.cx-table td{padding:7px 8px}
.cx-table a,.cx-links a,.cx-route a{color:#1d6b62;text-decoration:none;border-bottom:1px solid #9cc7c0}.cx-table a:hover,.cx-links a:hover{color:#B4501A}
.cx-cat{display:grid;grid-template-columns:1.12fr 1fr;gap:24px;height:100%;min-height:0}
.cx-shot{padding:12px;justify-content:flex-start}.cx-shot img{width:100%;flex:1;min-height:0;object-fit:contain;object-position:top center;border:1px solid #e2e2da;border-radius:4px}
.cx-side{display:flex;flex-direction:column;gap:9px;min-height:0;overflow:hidden}
.cx-facts{display:grid;grid-template-columns:96px 1fr;gap:6px 12px;margin:0;font-size:17px;line-height:1.3}
.cx-facts dt{font:700 15px var(--sans);color:var(--accent);padding-top:1px}.cx-facts dd{margin:0;color:#24343d}
.cx-facts code,.cx-note code,.cx-table code{font:15px Menlo,monospace;background:#f1efe6;padding:0 3px;border-radius:3px}
.cx-pre{font:14.5px/1.42 Menlo,monospace;background:#fff;border:1px solid #deded6;border-left:4px solid var(--accent);border-radius:6px;padding:8px 11px;margin:0;color:#1f3440;white-space:pre-wrap}
.cx-pre-card .cx-pre{border:0;border-left:4px solid #B4501A;padding:6px 10px}.cx-pre-card .figuretitle.cx-after{margin-top:16px}
.cx-links{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:15.5px;margin:2px 0 0}
.cx-note{font-size:16px;line-height:1.35;color:#3d4d55;margin:4px 0 0}
.cx-ztable td:first-child{font:700 16px var(--sans);color:#B4501A;width:78px}.cx-ztable{font-size:15.5px}
.cx-findings{font-size:16px}.cx-findings td{padding:7px 8px}
.cx-route td:first-child{font:700 16px var(--sans);width:28px}.cx-route td:last-child{font:600 15px var(--sans);color:#4d5f58}
.cx-legend{display:flex;flex-direction:column;gap:12px;height:100%}.cx-legend .figure{flex:1;min-height:0;padding:10px}
.cx-legend .diagram img{width:100%;height:100%;object-fit:contain}
.cx-strip{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;font-size:17px;line-height:1.3;color:#3d4d55}.cx-strip p{margin:0}.cx-strip b{color:#14202B}
'''



def integrate(slides):
    """Replace s18 with the CI/CD section; remove B28/B29; append CB1-CB3."""
    by_id = {s['id']: s for s in slides}
    film = by_id['s18']
    idx = slides.index(film)
    main = [x for x in _new if x['kind'] == 'main']
    back = [x for x in _new if x['kind'] == 'back']
    cb1 = dict(film, id='CB1', kind='back', secs=0, title='Recorded walkthrough · PR checks to hosted dev',
               transition='Return to C18.', refs=['C18'])
    slides[idx:idx + 1] = main
    slides[:] = [x for x in slides if x['id'] not in ('B28', 'B29')]
    slides.extend([cb1] + back)
    return slides
