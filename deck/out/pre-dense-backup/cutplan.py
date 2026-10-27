"""CUT-PLAN.md (owner approved, 27 Oct): 33:00 of content + 2:00 buffer inside a
hard 35:00. Runs last in build_deck.py, after the figure-slide normalisation.

Main path: S1 3:00 (4) · S2 5:00 (8) · S3 3:00 (5) · S4 10:00 (8, incl. 4:00 live)
· S5 12:00 (11). Everything taken off the main path becomes a backup frame; nothing
is deleted. Paired CI/CD detail frames (C5, C7, C15, C11) sit right after their
main frame as skipped "sub" frames: V opens one and V returns.
"""
import re

SECTION_SECS = {1: 180, 2: 300, 3: 180, 4: 600, 5: 720}
SECTION_NAMES = {1: 'Intro and project management', 2: 'Analysis, design and patterns', 3: 'Testing',
                 4: 'CI/CD demonstration', 5: 'System demo and quality attributes'}

ORDER = [
    ('s1', 10), ('s2', 50), ('s3', 60), ('P1', 60),
    ('s4', 30), ('s5', 35), ('s6', 35), ('s8', 50), ('PAT', 45), ('s9', 40), ('D1', 25), ('D2', 40),
    ('s10', 40), ('TU', 40), ('TI', 35), ('TE', 35), ('T10', 30),
    ('C1', 45), ('C3', 45), ('C4', 50), ('C6', 50), ('C8', 45), ('C10', 50), ('C17', 40), ('C18', 275),
    ('s19', 15), ('F3', 45), ('F4', 60), ('F5', 60), ('F6', 70), ('F7', 55), ('F9', 65), ('F11', 65), ('F12', 60),
    ('PERF', 120), ('s20', 105),
]
SUBS = {'C4': ('C5', 'security workflows beside Quality'), 'C6': ('C7', 'keyless upload and health-gated activation'),
        'C8': ('C15', 'the real ZAP results'), 'C10': ('C11', 'SCA: the zod advisory')}
TO_BACKUP = ['s7', 'C2', 'C9', 'C12', 'C13', 'C14', 'C16', 'T1', 'T2', 's11', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8',
             'T9', 'T11', 'T12', 'F8', 'F10']
FEATURES = [('F3', 'Create a group'), ('F4', 'Invite and join'), ('F5', 'Seal a photo'), ('F6', 'Video and allowance'),
            ('F7', 'Group chat'), ('F9', 'Film ready and watch'), ('F11', 'Archive and save'), ('F12', 'Outsider denied')]
CUE = '[Space to start. Narrate over the clip; press → as soon as the stated result shows. The clip need not finish.]\n\n'

SCRIPTS = {
    's1': 'Good afternoon. I am Gopal Guruprasath, presenting Rewind for Team 14: a month of everyday moments from a small private group, turned into one shared film.',
    's3': ('We used four sprints with zero-based names. Sprint zero built the runnable foundation; Sprint one integrated capture, the cycle and Archive; '
           'Sprint two delivered real accounts, private S3 media, PostgreSQL and Cognito; Sprint three concentrated on stability, recovery and regression tests. '
           'Velocity, as issues closed in each sprint window, was forty-four, one hundred, one hundred and forty-five and thirty. '
           'Today the real-account web and PWA journey runs end to end on hosted dev, and three hundred and nineteen of three hundred and twenty-nine backlog issues are closed. '
           'We held project planning, and Sprint Planning and Sprint Review every sprint. The outstanding items are the focused test runner, chat labels, '
           'the hosted Safari PWA integration check and assembling the report.'),
    'P1': ('This is our Sprint one burndown: fifty issues in scope and thirty-seven open at the start, closed in three steps to zero by the twenty-third of September. '
           'The other sprints are in backup; Sprint two is the counter-example, where scope grew from nine to one hundred and thirty-five as real accounts landed. '
           'Effort is split equally: five members at twenty percent, ten person-days each. Our Definition of Done is the outcome checked in the cheapest real environment, '
           'the fast tests passing, a green Quality check and a merge to dev. Retrospectives changed the next sprint: Sprint one exposed integration gaps, so Sprint two '
           'exercised real adapters; Sprint two exposed stale state, so Sprint three added whole-interaction tests.'),
    's8': ('This sequence is our hardest design problem: a scheduler tick can repeat, and an old worker can finish after its lease expires. '
           'Polling alone finds work but does not make repetition safe, so we compared State and Command object hierarchies with persisted state plus a durable job, '
           'and chose the durable job. One lifecycle transaction closes the cycle, freezes the inputs, queues the film job and opens the successor. '
           'The worker claims the job and renders outside the transaction. At finalisation it proves it still holds the current lease and generation, '
           'so a repeated tick reuses the job and a stale worker cannot publish.'),
    'PAT': ('Three more design problems were solved with named patterns. Media storage differs between local disk and private S3, and we did not want branches in the worker, '
            'so MediaStore is a Strategy and the S3 implementation adapts the AWS SDK. Chat needs every open screen to see a new message, so RealtimeHub is the Observer '
            'subject and each SSE connection subscribes, while stored messages replay on reconnect. Hosted PostgreSQL has a different API from local SQLite, so '
            'PostgresDatabase is an Adapter behind one data-access contract. The full pattern class diagrams are in backup.'),
    's9': ('This is the database schema for the same use case. Membership relates an account to a group and its role, and every access decision uses it. '
           'A group has cycles; a cycle has contributions; media jobs retain processing state. Compilation inputs freeze exactly which media belongs to a film, '
           'so a retry cannot reinterpret a changing collection. We chose PostgreSQL because this path depends on joins and transactions across related records. '
           'Before the screens, one more model: the cycle’s states.'),
    's10': ('Here is the whole test map: twelve types, each with its tool, count and when it runs. The tag says what a failure does. '
            'Blocks merge means the required Quality check turns red and the pull request cannot merge; reports means the result is recorded for review but never stops a merge. '
            'The top six block every pull request; browser, PWA and accessibility checks join for pull requests to main; the real-account journey and the load test run on demand. '
            'I will group them as unit, integration, end-to-end and security.'),
    'TU': ('Unit and component tests run in Jest with Testing Library for the client, one thousand six hundred and seventy-four of them, and node:test for server units. '
           'They check screens and state without a device. Here is a real bug: after a failed photo, Try again did nothing, because retry called capture from a state '
           'whose guard returned at once. The regression test fails the capture, taps Try again and expects the viewfinder and a fresh capture. '
           'It fails on the old code and passes with the fix.'),
    'TI': ('Integration tests start the real server and call its routes over HTTP: one thousand and six server tests covering sessions, membership, media integrity '
           'and the cycle engine. For example, every exposed category must deny a member of another group. The same suite then runs again on PostgreSQL 17, '
           'nine hundred and eighty-nine tests, so a dialect difference or migration drift fails the pull request.'),
    'TE': ('End to end, Playwright drives the exported app in a real browser: forty-one tests, with an owner, an invited member and an outsider. '
           'The PWA build is checked the way it will be installed: manifest, service worker and offline page. Axe and keyboard tests check the main screens '
           'for WCAG 2.1 AA, and any serious or critical violation fails. These join for pull requests to main.'),
    'T10': ('Security is tested at two levels. Inside the suites: privacy denials across groups, rate limits, our patched dependencies and the scan gates themselves. '
            'In the pipeline: SAST, SCA, secrets, IaC, image and DAST scans, which I show next. Performance is shown in the system demo.'),
    'C1': ('This is the whole pipeline on one page. The legend in the corner reads every pipeline figure: colour says what a failure blocks, orange the merge, '
           'blue the deploy, purple a push or promotion rule, and dashed grey only reports; hexagons are decisions. Band one is the pull request into dev: '
           'Quality checks is the one required check, and CodeQL, Gitleaks, Trivy and GitGuardian report beside it. Band two starts on the same push to dev: '
           'wait for Quality on the merge commit, build one bundle, scan the exact images, sign, upload, and activate only if health passes. '
           'Band three is hosted dev, scanned by ZAP after every deploy; promotion to main needs one human approval.'),
    'C3': ('Source management: work starts on an issue branch from the latest dev and enters dev only through a pull request. The dev rule requires the Format, lint, '
           'typecheck, and test check, an up-to-date branch and resolved conversations, applies to administrators, and forbids force-pushes and deletion. '
           'Main adds one approving review and the browser and PWA checks. Artifact management: Git keeps source, the lockfile, workflows, Terraform and Dockerfiles. '
           'Each run keeps its results as artifacts named with the commit SHA: JUnit, npm audit, SARIF, Trivy, SBOMs, the manifest and the release tar for thirty days, '
           'coverage for fourteen and ZAP for ninety. Provenance sits in GitHub attestations, and the host keeps the current, previous and pending releases for rollback.'),
    'C4': ('This is quality.yml on a pull request. The first job classifies the change; a code change fans out into eight parallel lanes: four static checks, '
           'the production dependency audit, root and IaC tests, server tests on SQLite with coverage, the same suite on PostgreSQL 17, frontend Jest with a seventy '
           'percent statement floor, and the deployment fixtures. The last job, Format, lint, typecheck, and test, needs every lane green; it is the one check in branch '
           'protection, so a red lane disables the merge button.\n\n[V shows the security workflows; V again returns.] Beside it, CodeQL, Gitleaks, release security '
           'and GitGuardian report into the Security tab without blocking the merge.'),
    'C6': ('The merge to dev starts Deploy dev. It first waits for the Quality run on this exact merge commit; if that fails, the host is untouched. '
           'release.py builds one tar with the runtime and web images. scan-release.py extracts those exact images, writes a CycloneDX SBOM and Trivy report for each, '
           'and stops on any High or Critical finding before upload. attest-build-provenance then signs the tar and the manifest.\n\n[V shows the second half; V returns.] '
           'For upload, GitHub holds no AWS keys: OIDC gives a one-hour role session limited to this repository and dev. The host checks the tar’s SHA-256, '
           'starts the candidate and activates it only when health is ready; otherwise it restores the previous release.'),
    'C8': ('After every deploy, a second job runs the OWASP ZAP baseline against the hosted site: a spider and an AJAX spider crawl it for two minutes and passive rules '
           'inspect every response, unauthenticated and without attacks, because hosted dev holds shared data. It is report-only.\n\n[V shows the real results; V returns.] '
           'This deploy found zero High and four Medium alerts, all from one Content Security Policy gap: our full policy is served Report-Only, so directives such as '
           'form-action are effectively unrestricted. The fix is to enforce that policy once its reports are clean.'),
    'C10': ('SAST is CodeQL with the security-extended suite on TypeScript, Python and the workflow files, on every pull request, push and weekly. In pull request 592 '
            'it raised three medium alerts, 54 to 56, in the load-test script; we dismissed them as used in tests with a written reason, because that harness never '
            'ships in the image.\n\n[V shows SCA; V returns.] SCA is the production dependency audit inside the required check. On 24 October a new advisory marked zod '
            'below 4.6.6 as high severity; Quality turned red and two pull requests could not merge until PR 591 added a scoped override. The retained audit now shows '
            'zero vulnerabilities across 674 production dependencies.'),
    'C17': ('The technical findings. A new zod advisory blocked merges with no change from us until PR 591 fixed it. Alpine removed the FFmpeg version we pinned, '
            'so the image stopped building. An audit of our own pipeline found we scanned a rebuilt image rather than the deployed one; PR 595 moved the gate onto '
            'the exact bundle and added the manifest and attestation. Gitleaks reported twenty-seven historical false positives, so we allowlisted exact values. '
            'And Cognito code passed its tests while its runtime dependencies were missing from the image. The lesson: verify what ships, not just the source.'),
    'C18': ('[00:00–00:35 on this slide] This is the route for the live part: the pull request checks, the Quality run and its artifacts, a triaged CodeQL alert, '
            'the Deploy dev run and its steps, the attestation, the ZAP report and the hosted health endpoint.\n\n'
            '[00:35–04:35 live in GitHub, about thirty seconds per link. If the network fails, open backup CB1 and play the recorded walkthrough from the Film timestamps.]\n\n'
            '1. Pull request checks: Quality is the required context; the security workflows sit beside it.\n'
            '2. Quality run: the job graph fans out and joins the aggregate; open the artifacts list.\n'
            '3. CodeQL alert 56: the rule, the line and the written dismissal reason.\n'
            '4. Deploy dev 40344230832: wait for Quality, build, scan, attest, install.\n'
            '5. Deploy steps: the exact-image scan and the upload order.\n'
            '6. Attestation: the signed subject is the manifest for this commit.\n'
            '7. ZAP report: 0 High, 4 Medium, all Content Security Policy.\n'
            '8. Hosted health: the installed version and PostgreSQL readiness.\n\n'
            'Return to the slides for the product journey.'),
    's19': 'Two members have their accounts ready. We create the group, invite, contribute a photo and a video, chat, then watch the film, save it, and test the outsider boundary.',
    'F3': CUE + 'The owner names the group, picks a shared prompt and sets the size, two to ten members. The prompt gives contributions a common theme. Pause when the new group and its prompt appear in settings.',
    'F4': CUE + ('The owner creates an invitation code; it works once and expires after twenty-four hours. Our friend accepts it from the prepared account, '
                 'and both accounts now see the same group and member list. Acceptance is a server decision: a valid code and an authenticated account produce one '
                 'durable membership. Reusing the code will not add anyone; we test that at the end.'),
    'F9': CUE + ('Switch to The little things, a completed capsule from Maya and Jun. The premiere card appears because the scheduler closed the cycle, compiled the film '
                 'from the frozen inputs and opened the next cycle: the CU-B path from the design section. Open it: one portrait film, seven-twenty by twelve-eighty '
                 'at thirty frames per second, built from everyone’s sealed moments. Press M only if you want sound. Pause at the end screen.'),
    'PERF': ('Now the quality attributes, starting with performance, measured by a scripted load test against hosted dev. A plain Node HTTP runner drives the real API '
             'through CloudFront, Node and PostgreSQL. It steps through one, ten, twenty-five, fifty and one hundred virtual users; each stage ramps for fifteen seconds '
             'and holds for three minutes. Each user acts, then waits three to seven seconds, and the mix is about ninety-five percent reads. The pass rule for every stage '
             'is p95 under two seconds and errors under one percent. All five stages passed: six thousand and thirty-eight steady requests with zero errors. '
             'At one hundred concurrent users, p95 was one thousand three hundred and thirty-six milliseconds and throughput seventeen point eight four requests per second. '
             'Latency stays flat to fifty users and then rises, which is where the capacity model starts.'),
    's20': ('Scalability asks what happens beyond one hundred users. These curves fit a closed-user model to the measured means: about forty-five milliseconds of '
            'serialized service time per request, a fixed delay near three hundred and eighty milliseconds, and five seconds of think time. One API host approaches '
            'about twenty-two requests per second, with a knee near one hundred and sixteen active users. At two hundred and fifty users the projected mean is six point '
            'four seconds on one host and one point one seconds on two balanced hosts. The mechanism is in the code: the PostgreSQL adapter waits synchronously on one '
            'client, and FFmpeg shares the host CPU. So the scale-out path is to separate media processing, make persistence asynchronous with a connection pool, then add '
            'API hosts that share PostgreSQL and S3. Maintainability is the pipeline we just walked through: those internal changes must pass the same behavioural tests, '
            'both database dialects, the exact-image scan and the health-gated deploy. Thank you; I am ready for questions.'),
}
TITLES = {
    's8': 'Durable claims make a repeated tick safe: close, claim, render, fence',
    'C1': 'One change passes four gates; colour says what a failure blocks',
    'C4': 'Nine Quality jobs feed one required merge check; security reports beside it',
    'C6': 'Deploy scans and signs the exact bundle, then activates only if healthy',
    'C8': 'ZAP scans hosted dev after every deploy: 0 High, 4 Medium (CSP)',
    'C10': 'SAST findings are triaged with reasons; SCA blocked merges until fixed',
    'F9': 'The cycle closes, and the group watches its film',
}


def _g(rx, body, default=''):
    m = re.search(rx, body, re.S)
    return m.group(1) if m else default


def _tt(body):
    return dict(count=_g(r'<div class="tt-count">(.*?)</div>', body), label=_g(r'<div class="tt-countlabel">(.*?)</div>', body),
                tool=_g(r'<div class="tt-tool">(.*?)</div>', body), badges=_g(r'<div class="tt-badges">(.*?)</div></div><div class="tt-right">', body),
                code=_g(r'<div class="tt-label">Example test</div><code>(.*?)</code>', body), name=_g(r'<p class="tt-name[^"]*">(.*?)</p>', body),
                catch=re.sub(r'^<b>Catches:</b>\s*', '', _g(r'<p class="tt-catch">(.*?)</p>', body)))


def _card(kind, p):
    return ('<div class="tc"><div class="tc-kind">' + kind + '</div><div class="tc-head"><span class="tc-n">' + p['count'] + '</span>'
            '<span class="tc-l">' + p['label'] + '</span></div><div class="tc-tool">' + p['tool'] + '</div><div class="tc-b">' + p['badges'] + '</div>'
            '<div class="tc-ex"><code>' + p['code'] + '</code><p class="tc-name">' + p['name'] + '</p><p class="tc-catch"><b>Catches:</b> ' + p['catch'] + '</p></div></div>')


def _new(id, sec, tag, title, body, script, extra='', refs=None):
    return dict(id=id, sec=sec, tag=tag, title=title, body=body, secs=0, say=[title], transition='', refs=refs or [], source='',
                script=script, kind='main', extra=extra)


def apply(slides):
    by = {s['id']: s for s in slides}
    new = {}
    # S1: s3 keeps sprints, velocity, status and outstanding; P1 takes burndown, effort, DoD and retro.
    s3 = by['s3']
    right = ('<p><b>Status.</b> The real-account web/PWA journey runs end to end on hosted dev; 319 of 329 backlog issues are closed.</p>'
             '<p><b>Ceremonies.</b> Project planning; Sprint Planning and Sprint Review every sprint. Backlog → stories → sprint plans → review.</p>'
             '<p><b>Velocity.</b> Issues closed per sprint window: 44 · 100 · 145 · 30.</p>')
    s3['body'] = re.sub(r'(<div class="pm-grid"><div>.*?</div>)<div>.*?</div></div>(<div class="status-strip">)',
                        lambda m: m.group(1) + '<div>' + right + '</div></div>' + m.group(2), s3['body'], count=1, flags=re.S)
    s3['title'] = 'Four sprints took Rewind from foundation to hosted real accounts'
    new['P1'] = _new('P1', 1, 'PM', 'Sprint 1 burned down cleanly; effort was split equally',
                     '<div class="split"><figure class="figure chart"><figcaption>Burndown · Sprint 1 · 13–26 Sep · scope and open issues</figcaption>'
                     '<img src="assets/burndown-sprint-1.png" alt="Sprint 1 burndown: 50 in scope, 37 open at start, 0 open by 23 Sep"></figure><div class="explain">'
                     '<p><b>Effort.</b> Five members, 20% each; 10 person-days each, agreed split.</p>'
                     '<p><b>Done.</b> Outcome checked in the cheapest real environment + fast tests + green Quality + merge to dev.</p>'
                     '<p><b>Retro → next sprint.</b> S1 integration gaps → real adapters in S2; S2 stale state → whole-interaction tests in S3.</p>'
                     '<p><b>Other sprints.</b> Burndowns for S0, S2 and S3 are in backup.</p></div></div>', SCRIPTS['P1'], refs=['B10', 'B21', 'B23'])
    # S2: patterns table replaces the separate class view (s7 moves to backup).
    rows = [('Repeated cycle work', 'A tick repeats; a stale worker finishes late', 'Persisted state + durable job, lease/generation fence', 'lifecycle.ts · jobs/compilation.ts'),
            ('Media storage', 'Disk locally, private S3 when hosted; no branches in the worker', 'Strategy + Adapter', 'MediaStore → LocalMediaStore / PrivateS3MediaStore; privateTransport adapts the AWS SDK'),
            ('Live chat', 'Every open screen needs each new message', 'Observer', 'RealtimeHub subject; SSE subscribers; stored messages replay on reconnect'),
            ('Persistence', 'Hosted PostgreSQL differs from the local SQLite API', 'Adapter', 'PostgresDatabase behind one data-access contract')]
    new['PAT'] = _new('PAT', 2, 'SDP', 'Each design problem has a named pattern in a named place',
                      '<table class="data patterns"><thead><tr><th>Concern</th><th>Problem</th><th>Pattern chosen</th><th>Where it lives</th></tr></thead><tbody>'
                      + ''.join('<tr>' + ''.join('<td>' + c + '</td>' for c in r) + '</tr>' for r in rows) +
                      '</tbody></table><div class="takeaway">Full pattern class views: backups B7 (storage), B8 (Observer), B9 (persistence).</div>',
                      SCRIPTS['PAT'], refs=['B7', 'B8', 'B9', 's7'])
    # S3: five slides.
    t2, t3, t4, t7, t8, t9 = (_tt(by[k]['body']) for k in ('T2', 'T3', 'T4', 'T7', 'T8', 'T9'))
    bug = ('<div class="tc"><div class="tc-kind">Real regression · CU-A photo retry</div><div class="tc-head"><span class="tc-n">“Try again”</span></div>'
           '<div class="tc-steps"><p><em>Given</em> photo capture fails</p><p><em>When</em> the user taps “Try again”</p>'
           '<p><em>Then</em> the viewfinder returns and a fresh capture succeeds</p></div>'
           '<div class="tc-reg"><span>Old code <b class="fail">FAIL</b></span><i>→</i><span>Fixed <b class="ok">PASS</b></span></div>'
           '<div class="tc-ex"><code>camera-capture.characterisation.test.tsx</code></div></div>')
    new['TU'] = _new('TU', 3, 'TESTING', 'Unit and component tests pin behaviour, like the “Try again” bug',
                     '<div class="tcards n2">' + _card('Unit + component · Jest, node:test', t2) + bug + '</div>', SCRIPTS['TU'], refs=['T2', 's11', 'B6'])
    new['TI'] = _new('TI', 3, 'TESTING', 'Integration tests call real routes, then rerun on PostgreSQL 17',
                     '<div class="tcards n2">' + _card('API on a running server', t3) + _card('Same suite on PostgreSQL 17', t4) + '</div>', SCRIPTS['TI'], refs=['T3', 'T4'])
    new['TE'] = _new('TE', 3, 'TESTING', 'End-to-end: a real browser, the installed PWA and WCAG 2.1 AA',
                     '<div class="tcards n3">' + _card('Playwright', t7) + _card('PWA build', t8) + _card('Accessibility', t9) + '</div>', SCRIPTS['TE'], refs=['T7', 'T8', 'T9'])
    # S5: performance on one slide from T11 method + T12 results.
    perf = by['T12']['body']
    new['PERF'] = _new('PERF', 5, 'DEMO', 'A scripted load test: 100 users on hosted dev, p95 1.34 s, zero errors',
                       '<p class="perf-method2"><b>Method.</b> Node HTTP runner → CloudFront → Node → PostgreSQL · 1 → 10 → 25 → 50 → 100 virtual users · '
                       '15 s ramp + 180 s steady per stage · 3–7 s think time · ~95% reads · pass: p95 &lt; 2 s and errors &lt; 1%</p>' + perf,
                       SCRIPTS['PERF'], refs=['T11', 'T12', 'B34', 'B35'])
    # C1 + C2: legend merged into the overview figure.
    by['C1']['body'] += ('<div class="c1-legend"><div class="lg-t">How to read every pipeline figure</div>'
                         '<div class="lg-row"><span class="lg merge">BLOCKS MERGE</span><span class="lg deploy">BLOCKS DEPLOY</span></div>'
                         '<div class="lg-row"><span class="lg push">BLOCKS PUSH · PROMOTION</span><span class="lg report">REPORTS</span></div>'
                         '<div class="lg-s">Colour = what a failure blocks · hexagon = decision · page = artifact · cylinder = store · 3-D box = host</div></div>')
    # Features: trimmed create-group clip; F9 + F10 merged into one 48 s clip.
    f3 = by['F3']
    f3['body'] = f3['body'].replace('clips/device/03-create-group.mp4', 'clips/device/03-create-group-short.mp4').replace(
        'clips/device/03-create-group-poster.jpg', 'clips/device/03-create-group-short-poster.jpg')
    f9 = by['F9']
    f9['body'] = re.sub(r'--screen-aspect:[\d.]+', '--screen-aspect:' + str(416 / 858), f9['body'])
    f9['body'] = f9['body'].replace('clips/device/09-cycle-ends-film-ready.mp4', 'clips/device/09-10-ready-and-watch.mp4').replace(
        'clips/device/09-cycle-ends-film-ready-poster.jpg', 'clips/device/09-10-ready-and-watch-poster.jpg')
    f9['body'] = re.sub(r'(<div class="feature-number">.*?</div>).*?(<div class="feature-control">)',
                        r'\1<p><b>Observe.</b> The premiere card on Home, then one portrait film from everyone’s sealed moments.</p>'
                        r'<p><b>Design.</b> The scheduler closed the cycle and compiled the frozen inputs (CU-B).</p>'
                        r'<p><b>Output.</b> 720 × 1280 · 30 fps · normalised audio.</p>\2', f9['body'], count=1, flags=re.S)
    for n, (fid, name) in enumerate(FEATURES, 1):
        by[fid]['body'] = re.sub(r'<div class="feature-number">.*?</div>', f'<div class="feature-number">{n:02d} / 08 · {name}</div>', by[fid]['body'], count=1)
    for fid in ('F5', 'F6', 'F11', 'F12'):
        by[fid]['script'] = CUE + by[fid]['script'].split(']\n\n', 1)[-1]
    by['F7']['script'] = CUE + by['F7']['script'].split(']\n\n', 1)[-1].replace('the Observer design in backup B8', 'the Observer pattern from the design section')
    by['s19']['body'] = ('<div class="journey-map"><div><em>01–02</em><h2>Create and invite</h2><p>Prompt · one private membership</p></div>'
                         '<div><em>03–05</em><h2>Contribute</h2><p>Photo · video and allowance · chat</p></div>'
                         '<div><em>06–08</em><h2>Reveal and retain</h2><p>Ready and watch · save · outsider check</p></div></div>'
                         '<div class="rule">28-day product cycle · private groups · one feature per slide</div>')
    # Titles, scripts, refs.
    by.update(new)
    for k, t in TITLES.items():
        by[k]['title'] = t
    for k, t in SCRIPTS.items():
        if k in by:
            by[k]['script'] = t
    by['s8']['refs'] = ['s7', 'B16', 'B17']
    by['s8']['transition'] = 'The same reasoning gave three more named patterns.'
    by['C18']['transition'] = 'Now the product journey on hosted dev.'
    # Sub frames: paired detail right after its main frame, skipped by the arrows.
    for parent, (child, what) in SUBS.items():
        c = by[child]
        c.update(kind='back', secs=0, extra=(c.get('extra', '') + ' fallback subview'))
        c['script'] = '[Detail for ' + parent + ': press V to return.] ' + c['script']
        by[parent]['body'] += f'<i class="subref" data-sub="{child}" hidden></i>'
        c['body'] += f'<i class="subref" data-parent="{parent}" hidden></i>'
    # Assemble: main path (with subs and storyboards attached), then backups, then newly cut frames.
    main = []
    for k, secs in ORDER:
        s = by[k]
        s['secs'] = secs
        if s['kind'] == 'back':
            s['kind'] = 'main'
        main.append(s)
        if k in SUBS:
            main.append(by[SUBS[k][0]])
        if k == 'D2':
            main += [x for x in slides if x['id'].startswith('U') and 'fallback' in x.get('extra', '')]
    used = {id(x) for x in main}
    cut = []
    for k in TO_BACKUP:
        s = by[k]
        s.update(kind='back', secs=0)
        s['extra'] = s.get('extra', '').replace('device-slide', 'device-slide')
        cut.append(s)
    used |= {id(x) for x in cut}
    rest = [x for x in slides if id(x) not in used]
    for x in rest:
        if x['kind'] != 'back':
            raise SystemExit('unplaced main slide ' + x['id'])
    slides[:] = main + rest + cut
    for sec, budget in SECTION_SECS.items():
        got = sum(x['secs'] for x in main if x['sec'] == sec and x['kind'] != 'back')
        assert got == budget, (sec, got, budget)


CUT_CSS = r'''
.data.patterns{font-size:20px;table-layout:fixed}.data.patterns th:nth-child(1){width:17%}.data.patterns th:nth-child(2){width:28%}
.data.patterns th:nth-child(3){width:22%}.data.patterns th:nth-child(4){width:33%}.data.patterns td{padding:13px 10px;line-height:1.3}
.data.patterns td:nth-child(3){font-weight:650;color:#A84A1A}.data.patterns td:nth-child(4){font-size:18px;color:#5E4D43}
.tcards{display:grid;gap:24px;height:100%;align-items:stretch}.tcards.n2{grid-template-columns:1fr 1fr}.tcards.n3{grid-template-columns:1fr 1fr 1fr}
.tc{background:rgba(255,255,255,.72);border:1px solid rgba(255,255,255,.9);border-radius:24px;padding:22px 26px;display:flex;flex-direction:column;gap:10px;
 box-shadow:inset 0 1px 1px #fff,0 18px 36px -18px rgba(160,90,40,.30)}
.tc-kind{font:600 14px var(--sans);letter-spacing:1.2px;text-transform:uppercase;color:#A84A1A}
.tc-head{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
.tc-n{font-family:var(--serif);font-variation-settings:'SOFT' 100,'opsz' 144;font-weight:520;font-size:52px;line-height:1;color:#33231A}
.tc-l{font-size:18px;color:#5E4D43}.tc-tool{font-size:18px;line-height:1.35}.tc-b .badge{font-size:14px;padding:4px 10px}
.tc-ex{margin-top:auto;border-top:1px solid #EADBCB;padding-top:12px}.tc-ex code{font-size:15px;overflow-wrap:anywhere}
.tc-name{font-size:18px;line-height:1.35;font-style:italic;margin:8px 0}.tc-catch{font-size:18px;line-height:1.35;margin:0;color:#5E4D43}.tc-catch b{color:#33231A}
.n3 .tc{padding:18px 20px}.n3 .tc-n{font-size:44px}.n3 .tc-tool,.n3 .tc-name,.n3 .tc-catch,.n3 .tc-l{font-size:16px}
.tc-steps p{font-size:21px;line-height:1.35;margin:6px 0}.tc-steps em{font:500 15px var(--mono);font-style:normal;text-transform:uppercase;color:#A84A1A;margin-right:8px}
.tc-reg{display:flex;align-items:center;gap:22px;font-size:18px;margin-top:8px}.tc-reg b{display:block;font:600 26px var(--mono)}.tc-reg .fail{color:#B3261E}.tc-reg .ok{color:#2F6B45}.tc-reg i{font-style:normal;font-size:26px}
.perf-method2{font-size:17px;line-height:1.35;margin:-6px 0 12px;color:#5E4D43}.perf-method2 b{color:#33231A}
.c1-legend{position:absolute;left:14px;bottom:14px;width:372px;z-index:5;background:rgba(255,255,255,.95);border:1px solid #E3D3C2;border-radius:16px;padding:12px 14px;
 box-shadow:0 12px 28px -18px rgba(120,60,20,.45)}
.lg-t{font:600 14px var(--sans);letter-spacing:1px;text-transform:uppercase;color:#5E4D43;margin-bottom:8px}
.lg-row{display:flex;gap:8px;margin-bottom:7px}.lg{font:700 14px var(--sans);padding:4px 9px;border-radius:6px;border:1.5px solid}
.lg.merge{background:#fff4ec;border-color:#d55e00;color:#7c2d00}.lg.deploy{background:#dbeafe;border-color:#2563eb;color:#1e3a8a}
.lg.push{background:#f1ebfa;border-color:#7e57c2;color:#4a2a8a}.lg.report{background:#f8fafc;border:1.5px dashed #64748b;color:#334155}
.lg-s{font-size:14px;line-height:1.35;color:#5E4D43}
'''


def cut_js(js):
    js = js.replace("else if(k==='n'||k==='N')",
                    "else if(k==='v'||k==='V'){var m=slides[cur].querySelector('.subref');if(m){var t=m.dataset.sub||m.dataset.parent;var f=slides.findIndex(function(x){return x.id===t});if(f>=0)go(f)}}\nelse if(k==='n'||k==='N')", 1)
    assert "k==='v'" in js
    return js
