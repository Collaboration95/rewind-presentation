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
    ('s10', 50), ('TT', 80), ('TS', 50),
    ('C1', 45), ('C3', 45), ('C4', 50), ('C6', 50), ('C8', 45), ('C10', 50), ('C17', 40), ('C18', 275),
    ('s19', 15), ('F3', 45), ('F4', 60), ('F5', 60), ('F6', 70), ('F7', 55), ('F9', 65), ('F11', 65), ('F12', 60),
    ('PERF', 120), ('s20', 105),
]
SUBS = {'C4': ('C5', 'security workflows beside Quality'), 'C6': ('C7', 'keyless upload and health-gated activation'),
        'C8': ('C15', 'the real ZAP results'), 'C10': ('C11', 'SCA: the zod advisory')}
TO_BACKUP = ['s7', 'T10', 'C2', 'C9', 'C12', 'C13', 'C14', 'C16', 'T1', 'T2', 's11', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8',
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
           'We held project planning, and Sprint Planning and Sprint Review every sprint. Done means the outcome checked in the cheapest real environment, fast tests, a green Quality check and a merge to dev.'),
    'P1': ('These are the four sprint burndowns and the velocity. Sprint one is the clean case: fifty issues in scope, thirty-seven open at the start and zero '
           'by the twenty-third of September. Sprint two is the counter-example: scope kept growing, to one hundred and thirty-five, as real accounts landed, '
           'and it closed with nine open. Velocity peaked in Sprint two with one hundred and forty-five issues closed and one hundred and thirty-two pull requests merged. '
           'Effort was not equal: I carried forty percent; Nguyen Kim Long, Jiang Jiayu and Phan Mai Tan Loi twenty percent each; Sang Haoxiang made a minimal contribution. '
           'Each retrospective changed the next sprint: integration gaps led to real adapters, stale state led to interaction tests.'),
    's8': ('This sequence is our hardest design problem: a scheduler tick can repeat, and an old worker can finish after its lease expires. '
           'Polling alone finds work but does not make repetition safe, so we compared State and Command object hierarchies with persisted state plus a durable job, '
           'and chose the durable job. One lifecycle transaction closes the cycle, freezes the inputs, queues the film job and opens the successor. '
           'The worker claims the job and renders outside the transaction. At finalisation it proves it still holds the current lease and generation, '
           'so a repeated tick reuses the job and a stale worker cannot publish.'),
    'PAT': ('Three more design problems, each solved with a named pattern; click a diagram to enlarge it. Top left, media storage: local disk in development and private S3 '
            'when hosted. MediaStore is the Strategy, with a local and a private-S3 implementation, and the S3 side adapts the AWS SDK, so the worker never branches. '
            'Top right, chat: every open screen needs each new message, so RealtimeHub is the Observer subject and each SSE connection subscribes. '
            'Bottom left, persistence: hosted PostgreSQL has a different API from local SQLite, so PostgresDatabase is an Adapter behind one data-access contract. '
            'Bottom right sums it up: problem, pattern, benefit.'
            '\n\n[Cite if asked] Repeated work: lifecycle.ts and jobs/compilation.ts (the durable job on slide 8). Storage: privateTransport adapts the AWS SDK commands. Chat: stored messages replay on reconnect.'),
    's9': ('This is the database schema for the same use case. Membership relates an account to a group and its role, and every access decision uses it. '
           'A group has cycles; a cycle has contributions; media jobs retain processing state. Compilation inputs freeze exactly which media belongs to a film, '
           'so a retry cannot reinterpret a changing collection. We chose PostgreSQL because this path depends on joins and transactions across related records. '
           'Before the screens, one more model: the cycle’s states.'),
    's10': ('Here is the whole test map: twelve types, each with its tool, count and when it runs. The tag says what a failure does. '
            'Blocks merge means the required Quality check turns red and the pull request cannot merge; reports means the result is recorded for review but never stops a merge. '
            'The top six block every pull request; browser, PWA and accessibility checks join for pull requests to main; the real-account journey and the load test run on demand. '
            'I will group them as unit, integration, end-to-end and security.'),
    'TT': ('Six layers, each with a real example. Unit and component tests: one thousand six hundred and seventy-four Jest tests check screens and state '
           'without a device, with node:test for server units. Integration: one thousand and six server tests call the real routes over HTTP, and the same suite '
           'runs again on PostgreSQL 17, so a dialect difference or migration drift fails the pull request. These block every merge. End to end, forty-one '
           'Playwright tests drive the exported app with an owner, an invited member and an outsider; the PWA build is checked as it will be installed; and axe '
           'with keyboard tests checks the main screens for WCAG 2.1 AA. Those three join for pull requests to main. Each card names one real test and the bug it catches.'),
    'TS': ('One real bug shows why we test behaviour. After a failed photo, Try again did nothing, because retry called capture from a state whose guard '
           'returned at once. The regression test fails the capture, taps Try again and expects the viewfinder and a fresh capture: it fails on the old code '
           'and passes with the fix. Security is also tested inside the suites: cross-group privacy denials, rate limits, our patched dependencies and the scan '
           'gates themselves. The pipeline scans come in the CI/CD section, and performance in the system demo.'
           '\n\n[Cite if asked] Regression test: camera-capture.characterisation.test.tsx. Rate limits: safety-rate-limits.test.mjs. Patched dependencies: braces and node-forge, where the original node-forge accepts a forged signature. Access tests cover account safety too; scan gates reject expired, wrong or incomplete scans.'),
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
    'PERF': ('Now the quality attributes. Performance was measured with a scripted load test against hosted dev: a Node HTTP runner drives the real API through '
             'CloudFront, Node and PostgreSQL, each user waits three to seven seconds between actions, and the mix is ninety-five percent reads. A stage passes with p95 '
             'under two seconds and errors under one percent. One to one hundred users all passed: at one hundred, p95 was 1.34 seconds, 17.8 requests per second, zero errors. '
             'This morning we pushed further. One hundred and fifty users still passed at 1.66 seconds. The breakpoint is two hundred users: p95 rose to 3.03 seconds, '
             'with still zero errors, and throughput saturated at twenty-nine requests per second, eighty percent of linear. At three hundred we stopped the ramp. '
             'The system fails by queueing, not by rejecting requests. The limiting factor is not the host CPU, which stayed under twenty-five percent, and not a rate limiter: '
             'every database call blocks the single Node event loop on one PostgreSQL client, so every request, even health, waits in the same queue.'
             '\n\n[Cite if asked] 1–100 users: 180 s steady stages (26 Oct); 150–300: 60 s stress stages (27 Oct). Every database call waits through Atomics.wait on a single pg client (server/src/postgres/database.ts, sync-worker.ts). Load-generator CPU peaked at 26% of one core, event-loop p99 ≤ 22 ms; zero 429s, 5xx, timeouts or socket errors.'),
    's20': ('Scalability: the capacity model fitted on the one-to-one-hundred run predicted a ceiling of about twenty-two requests per second and a knee near one hundred '
            'and sixteen users. The stress test confirms its shape and shows it is about 1.4 times conservative: the measured knee lies between one hundred and fifty and '
            'two hundred users, and saturation between twenty-nine and thirty-six requests per second. So the scale-out path follows the bottleneck. First, asynchronous '
            'persistence with a bounded connection pool, which removes the serialization. Second, a second API host behind a load balancer, which doubles the modelled '
            'ceiling; at two hundred and fifty users the mean drops from 6.4 to 1.1 seconds. Third, a separate media worker keeps film compilation off the API host. '
            'A larger instance alone would add little, because the CPU is not saturated. Maintainability is the pipeline we just walked through: those internal changes '
            'must pass the same behavioural tests, both database dialects, the exact-image scan and the health-gated deploy. Thank you; I am ready for questions.'),
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


EFFORT = [('Gopal Guruprasath', 40), ('Nguyen Kim Long', 20), ('Jiang Jiayu', 20), ('Phan Mai Tan Loi', 20), ('Sang Haoxiang', 0)]
EFFORT_ROWS = ''.join('<div class="eff"><span class="eff-n">' + n + '</span>' +
                      (f'<span class="eff-bar"><i style="width:{v*2.5}%"></i></span><b>{v}%</b>' if v else '<span class="eff-min">minimal contribution</span>') +
                      '</div>' for n, v in EFFORT)


def _mini(kind, p):
    return ('<div class="mc"><div class="mc-top"><span class="mc-kind">' + kind + '</span><span class="mc-n">' + p['count'] + '</span></div>'
            '<div class="mc-tool">' + p['label'] + ' · ' + p['tool'] + '</div><div class="mc-b">' + p['badges'] + '</div>'
            '<code>' + p['code'] + '</code><p class="mc-name">' + p['name'] + '</p><p class="mc-catch"><b>Catches:</b> ' + p['catch'] + '</p></div>')


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
             '<p><b>Done.</b> Outcome checked in the cheapest real environment + fast tests + green Quality + merge to dev.</p>')
    s3['body'] = re.sub(r'(<div class="pm-grid"><div>.*?</div>)<div>.*?</div></div>(<div class="status-strip">)',
                        lambda m: m.group(1) + '<div>' + right + '</div></div>' + m.group(2), s3['body'], count=1, flags=re.S)
    s3['body'] = re.sub(r'<div class="status-strip">.*?</div>\s*$', '', s3['body'], flags=re.S)
    s3['title'] = 'Four sprints took Rewind from foundation to hosted real accounts'
    from charts import burndown, velocity
    new['P1'] = _new('P1', 1, 'PM', 'Four burndowns, velocity and each member’s share of the effort',
                     '<div class="mgrid pm">' + ''.join('<div class="cell">' + burndown(i) + '</div>' for i in range(4)) +
                     '<div class="cell">' + velocity() + '</div><div class="cell text">'
                     '<div class="eff-t">Effort share · 100%</div>' + EFFORT_ROWS +
                     '<p class="eff-r"><b>Retro → next sprint.</b> S1 gaps → real adapters; S2 stale state → interaction tests.</p></div></div>',
                     SCRIPTS['P1'], refs=['B25'])
    # S2: patterns table replaces the separate class view (s7 moves to backup).
    rows = [('Repeated cycle work', 'A tick repeats; a stale worker finishes late', 'Persisted state + durable job, lease/generation fence', 'Lifecycle and compilation-job modules'),
            ('Media storage', 'Disk locally, private S3 when hosted; no branches in the worker', 'Strategy + Adapter', 'MediaStore → LocalMediaStore / PrivateS3MediaStore'),
            ('Live chat', 'Every open screen needs each new message', 'Observer', 'RealtimeHub subject · SSE subscribers'),
            ('Persistence', 'Hosted PostgreSQL differs from the local SQLite API', 'Adapter', 'PostgresDatabase behind one data-access contract')]
    def pcell(fig, name, problem):
        return ('<div class="pcell"><div class="pcell-h"><b>' + name + '</b> · ' + problem + '</div>'
                '<img class="pzoom" src="uml/' + fig + '.svg" alt="' + name + ' class view" title="Click or Z to enlarge"></div>')
    new['PAT'] = _new('PAT', 2, 'SDP', 'Three design problems, three named patterns in the code',
                      '<div class="pgrid">' + pcell('pattern-storage', 'Strategy + Adapter', 'media on disk or private S3') +
                      pcell('pattern-observer', 'Observer', 'live chat to every open screen') +
                      pcell('pattern-persistence', 'Adapter', 'PostgreSQL behind one data contract') +
                      '<div class="pcell sum"><div class="pcell-h"><b>Problem → pattern → benefit</b></div>'
                      '<div class="psum"><p><b>Two storage backends</b> → Strategy + Adapter → the worker never branches on disk vs S3</p>'
                      '<p><b>Many open screens</b> → Observer → one publish reaches every subscriber</p>'
                      '<p><b>Two SQL dialects</b> → Adapter → callers keep one data-access contract</p>'
                      '<p class="pnote">Click a diagram (or Z) to enlarge · full size in B7–B9</p></div></div></div>',
                      SCRIPTS['PAT'], refs=['B7', 'B8', 'B9', 's7'])
    # S3: five slides.
    t2, t3, t4, t7, t8, t9 = (_tt(by[k]['body']) for k in ('T2', 'T3', 'T4', 'T7', 'T8', 'T9'))
    bug = ('<div class="tc"><div class="tc-kind">Real regression · CU-A photo retry</div><div class="tc-head"><span class="tc-n">“Try again”</span></div>'
           '<div class="tc-steps"><p><em>Given</em> photo capture fails</p><p><em>When</em> the user taps “Try again”</p>'
           '<p><em>Then</em> the viewfinder returns and a fresh capture succeeds</p></div>'
           '<div class="tc-reg"><span>Old code <b class="fail">FAIL</b></span><i>→</i><span>Fixed <b class="ok">PASS</b></span></div>'
           '<p class="tc-fr"><b>Fault.</b> Retry called capture from a state where its guard returned at once.</p>'
           '<p class="tc-fr"><b>Repair.</b> Return to the viewfinder for a fresh capture.</p>'
           '<p class="tc-fr"><b>Test.</b> Asserts the viewfinder and a fresh capture, not just the button.</p>'
           '</div>')
    t10 = by['T10']['body']
    suites = ('<p><b>Access and privacy.</b> 13 server test files: cross-group reads, media tokens, Cognito callback failures.</p>'
              '<p><b>Rate limits.</b> Thirty chat messages pass; the next is refused.</p>'
              '<p><b>Patched dependencies.</b> Our node-forge fork rejects a forged signature.</p>'
              '<p><b>Scan gates.</b> 13 Python tests prove the IaC and image gates reject bad scans.</p>')
    lean = [('Unit + component', 'Jest', t2['count'], 'gate', 'a chat request that leaks the session token'),
            ('API', 'node:test', t3['count'], 'gate', 'another group’s member reading private content'),
            ('Database', 'PostgreSQL 17', t4['count'], 'gate', 'schema drift between fresh install and upgrade'),
            ('End-to-end', 'Playwright', t7['count'], 'main', 'an outsider opening the owner’s group'),
            ('PWA build', 'check-pwa', t8['count'], 'main', 'a service worker caching private media'),
            ('Accessibility', 'axe + keyboard', t9['count'], 'main', 'a dialog that lets keyboard focus escape')]
    chip = {'gate': '<span class="badge gate">Every PR · blocks merge</span>', 'main': '<span class="badge main">PRs to main · blocks merge</span>'}
    cite = '\n\n[Cite if asked] ' + ' · '.join(f"{k}: {re.sub('<[^>]+>', '', p['code'])} — {re.sub('<[^>]+>', '', p['name'])} ({re.sub('<[^>]+>', '', p['label'])}; {re.sub('<[^>]+>', '', p['tool'])})"
                                              for k, p in (('Unit', t2), ('API', t3), ('PostgreSQL', t4), ('E2E', t7), ('PWA', t8), ('A11y', t9)))
    new['TT'] = _new('TT', 3, 'TESTING', 'Six test layers, each with a real example of what it catches',
                     '<div class="dense lean">' + ''.join('<div class="mc"><div class="mc-kind">' + k + ' · ' + tool + '</div><div class="mc-n">' + n + '</div>'
                                                     + '<div class="mc-b">' + chip[c] + '</div><p class="mc-catch"><b>Catches:</b> ' + catch + '</p></div>'
                                                     for k, tool, n, c, catch in lean) + '</div>', SCRIPTS['TT'] + cite,
                     refs=['T2', 'T3', 'T4', 'T7', 'T8', 'T9'])
    new['TS'] = _new('TS', 3, 'TESTING', 'A regression test for a real bug, and security inside the suites',
                     '<div class="ts-grid">' + bug + '<div class="tc secbox"><div class="tc-kind">Security · in the test suites</div>' + suites +
                     '<div class="tc-kind sec-pipe">In the pipeline · Section 4</div>' + _g(r'(<table class="data secscan">.*?</table>)', t10) + '</div></div>', SCRIPTS['TS'], refs=['s11', 'T10'])
    # S5: performance on one slide from T11 method + T12 results.
    from charts import STRESS, stress_latency, stress_throughput
    rows = ''.join(f'<tr class="{"bp" if v == "BREAKPOINT" else "stop" if v == "STOPPED" else ""}"><td>{u:,}</td><td>{p95:,}</td><td>{rps:g}</td><td>{e:.0f}%</td>'
                   f'<td>{"PASS" if v == "PASS" else "Breakpoint" if v == "BREAKPOINT" else "Stopped (p95 &gt; 5 s)"}</td></tr>'
                   for u, p50, p95, p99, rps, e, v in STRESS)
    new['PERF'] = _new('PERF', 5, 'DEMO', 'Load and stress: 100 users pass; the breakpoint is 200, set by the database bridge',
                       '<div class="stress"><div class="st-left"><p class="perf-method2"><b>Method.</b> Scripted runner → hosted API · 3–7 s think time · 95% reads · pass: p95 &lt; 2 s, errors &lt; 1%</p>'
                       '<table class="data stresst"><thead><tr><th>Users</th><th>p95 ms</th><th>req/s</th><th>Errors</th><th>Verdict</th></tr></thead><tbody>' + rows + '</tbody></table>'
                       '<p class="st-p"><b>Breakpoint 200 users:</b> p95 3.03 s, still 0 errors. <b>Saturation:</b> 29 req/s at 200 (80% of linear). It fails by queueing; nothing is rejected.</p>'
                       '<p class="st-p"><b>Limiting factor:</b> one PostgreSQL client blocks the single Node event loop. Host CPU ≤ 25%; no 429s or 5xx.</p>'
                       '</div><div class="st-right"><div class="cell">' + stress_latency() + '</div><div class="cell">' + stress_throughput() + '</div></div></div>',
                       SCRIPTS['PERF'], refs=['T11', 'T12', 'B34', 'B11'])
    by['C17']['body'] = by['C17']['body'].replace('Read declared version from schema.ts (#583)', 'Read the declared schema version (#583)')
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
    s20 = by['s20']
    s20['body'] = re.sub(r'<p><b>Measured\.</b>.*?</p>', '<p><b>Measured.</b> Breakpoint 200 users (p95 3.03 s); saturation 29–36 req/s. The model is about 1.4× conservative.</p>', s20['body'], count=1)
    s20['body'] = re.sub(r'<p><b>Scale out\.</b>.*?</p>', '<p><b>Scale out.</b> Async persistence + connection pool first; then a second API host; a media worker keeps FFmpeg off the API host.</p>', s20['body'], count=1)
    s20['title'] = 'The capacity model, checked by the stress test, shows where to scale next'
    # Load charts: latency and throughput side by side in one backup.
    from charts import latency, throughput
    b34 = by['B34']
    b34.update(title='Measured latency and throughput by stage on hosted dev', extra='',
               body='<div class="mgrid two"><div class="cell">' + latency(540, 380) + '</div><div class="cell">' + throughput(540, 380) + '</div></div>',
               script='Latency p50, p95 and p99 per steady stage, beside throughput. Every p95 stays under two seconds; the 100-user p95 is 1,335.9 ms '
                      'and throughput 17.84 requests per second, with zero errors.')
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
    extra_frames = [x for x in slides if x['id'].startswith('U') and 'fallback' in x.get('extra', '')]
    extra_frames += [by[SUBS[k][0]] for k, _ in ORDER if k in SUBS]
    used = {id(x) for x in main + extra_frames}
    cut = []
    for k in TO_BACKUP:
        s = by[k]
        s.update(kind='back', secs=0)
        s['extra'] = s.get('extra', '').replace('device-slide', 'device-slide')
        cut.append(s)
    used |= {id(x) for x in cut}
    drop = {'B10', 'B21', 'B22', 'B23', 'B24', 'B35'}
    rest = [x for x in slides if id(x) not in used and x['id'] not in drop]
    for x in rest:
        if x['kind'] != 'back':
            raise SystemExit('unplaced main slide ' + x['id'])
    slides[:] = main + extra_frames + rest + cut
    for x in slides:
        x['refs'] = list(dict.fromkeys('P1' if r in drop - {'B35'} else 'B34' if r == 'B35' else r for r in x['refs']))
    for sec, budget in SECTION_SECS.items():
        got = sum(x['secs'] for x in main if x['sec'] == sec and x['kind'] != 'back')
        assert got == budget, (sec, got, budget)


CUT_CSS = r'''
.pgrid{display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:14px;height:100%}
.pcell{background:#fff;border:1px solid #EADBCB;border-radius:20px;padding:10px 14px;display:flex;flex-direction:column;min-height:0;overflow:hidden;
 box-shadow:0 14px 30px -20px rgba(160,90,40,.35)}
.pcell-h{font-size:16px;color:#5E4D43;margin-bottom:6px;flex:none}.pcell-h b{color:#A84A1A}
.pcell img{flex:1;min-height:0;width:100%;object-fit:contain;cursor:zoom-in}
.pcell.sum{background:rgba(255,255,255,.75)}.psum p{font-size:17px;line-height:1.35;margin:0 0 12px;color:#5E4D43}.psum b{color:#33231A}
.psum .pnote{font-size:14px;color:#A84A1A;margin-top:4px}
#PAT>.body{margin-bottom:44px}

.dense.lean .mc{padding:18px 22px;gap:10px;justify-content:center}
.dense.lean .mc-kind{font-size:17px;letter-spacing:.6px}
.dense.lean .mc-n{font-size:58px;line-height:1}
.dense.lean .mc-b .badge{font-size:15px;padding:4px 11px}
.dense.lean .mc-catch{font-size:19px;line-height:1.32}

.eff-t{font:650 14px var(--sans);letter-spacing:1px;text-transform:uppercase;color:#A84A1A;margin-bottom:6px}
.eff{display:grid;grid-template-columns:142px 1fr 40px;align-items:center;gap:8px;font-size:15px;line-height:1.2;margin:0 0 7px;color:#33231A}
.eff-bar{height:12px;background:#F1E4D6;border-radius:6px;overflow:hidden}.eff-bar i{display:block;height:100%;background:linear-gradient(90deg,#ffb27e,#e0703a);border-radius:6px}
.eff b{font:600 15px var(--mono);text-align:right}.eff-min{grid-column:2 / 4;font-size:15px;font-style:italic;color:#5E4D43}
.mgrid .cell.text .eff-r{font-size:15px;margin-top:10px}

.stress{display:grid;grid-template-columns:1fr 560px;gap:18px;height:100%}
.st-left .perf-method2{font-size:15px;margin:0 0 6px}
.data.stresst{font-size:16px}.data.stresst th{font-size:14px;padding:4px 8px}.data.stresst td{padding:4px 8px;text-align:right}.data.stresst td:last-child,.data.stresst th:last-child{text-align:left}
.data.stresst td:first-child{font-weight:650}.data.stresst tr.bp td{background:#FBE6D4;color:#7A3512;font-weight:700}.data.stresst tr.stop td{color:#5E4D43}
.st-p{font-size:15px;line-height:1.35;margin:7px 0 0;color:#5E4D43}.st-p b{color:#33231A}.st-p code{font-size:14px}
.st-right{display:grid;grid-template-rows:1fr 1fr;gap:10px;min-height:0}
.st-right .cell{background:rgba(255,255,255,.72);border-radius:16px;display:flex;align-items:center;justify-content:center;overflow:hidden;box-shadow:inset 0 1px 1px #fff,0 14px 30px -20px rgba(160,90,40,.35)}
#PERF>.body{margin-bottom:40px}#PERF>h1{font-size:32px}

.dense{display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:1fr 1fr;gap:14px;height:100%}
.mc{background:rgba(255,255,255,.74);border:1px solid rgba(255,255,255,.9);border-radius:18px;padding:12px 16px;display:flex;flex-direction:column;gap:5px;
 box-shadow:inset 0 1px 1px #fff,0 14px 30px -20px rgba(160,90,40,.35);min-height:0;overflow:hidden}
.mc-top{display:flex;justify-content:space-between;align-items:baseline;gap:8px}
.mc-kind{font:650 14px var(--sans);letter-spacing:.8px;text-transform:uppercase;color:#A84A1A}
.mc-n{font-family:var(--serif);font-variation-settings:'SOFT' 100;font-weight:560;font-size:26px;line-height:1;color:#33231A;white-space:nowrap}
.mc-tool{font-size:14px;line-height:1.3;color:#5E4D43}.mc-b .badge{font-size:14px;padding:3px 9px}
.mc code{font-size:14px;color:#4A3326;overflow-wrap:anywhere;margin-top:2px}
.mc-name{font-size:14px;line-height:1.3;font-style:italic;margin:0;color:#33231A}.mc-catch{font-size:14px;line-height:1.3;margin:0;color:#5E4D43}.mc-catch b{color:#33231A}
#TT>.body,#P1>.body,#TS>.body{margin-bottom:46px}
.ts-grid{display:grid;grid-template-columns:1fr 1.15fr;gap:22px;height:100%}
.tc.secbox p{font-size:17px;line-height:1.38;margin:0 0 9px;color:#5E4D43}.tc.secbox p b{color:#33231A}.tc.secbox code{font-size:15px}
.tc.secbox .sec-pipe{margin-top:6px;padding-top:10px;border-top:1px solid #EADBCB}.tc.secbox p{font-size:16px;margin:0 0 6px}
.tc.secbox .data.secscan{font-size:15px;background:transparent}.tc.secbox .data.secscan td,.tc.secbox .data.secscan th{padding:3px 8px}.tc.secbox .badge{font-size:14px;padding:2px 9px}
#TS .tc{padding:16px 22px;gap:6px}#TS .tc-n{font-size:40px}#TS .tc-steps p{font-size:18px;margin:3px 0}#TS .tc-reg b{font-size:22px}
.tc-fr{font-size:16px;line-height:1.35;margin:4px 0;color:#5E4D43}.tc-fr b{color:#33231A}.ts-grid .tc-ex{margin-top:8px}

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
    js = js.replace("var cur=-1,buf='',hudT=0;", "var cur=-1,buf='',hudT=0;document.addEventListener('click',function(e){if(e.target.matches&&e.target.matches('img.pzoom'))toggleFigureZoom(e.target)});", 1)
    js = js.replace("var im=src||slides[cur].querySelector('.alternate-view:not([hidden]) img,.diagram img');", "var im=src||slides[cur].querySelector('.alternate-view:not([hidden]) img,.diagram img,img.pzoom');", 1)
    return js
