# Rewind · full spoken script

SWE5006 Team 14 · Gopal Guruprasath · 27 October 2026, 14:30 SGT.

## Timing table

| Section | Start | End | Budget |
|---|---:|---:|---:|
| 1 · Intro and project management | 00:00 | 03:00 | 3:00 |
| 2 · Analysis, design and patterns | 03:00 | 08:00 | 5:00 |
| 3 · Testing | 08:00 | 11:00 | 3:00 |
| 4 · CI/CD demonstration | 11:00 | 21:00 | 10:00 |
| 5 · System demo and quality attributes | 21:00 | 33:00 | 12:00 |
| **Talk total** | **00:00** | **33:00** | **33:00** |

Hard limit 35:00: 33:00 of content plus 2:00 for interruptions; Q&A follows. Each slide below has its own clock. Section 4 includes about 4:00 of live GitHub clicks on C18 (recorded fallback: backup CB1). Feature clips start on Space; press → as soon as the stated result shows.

## Presentation controls

Arrow keys / A / D: change frame; the main path ends at slide N, backups follow. V: open the detail frame of C4, C6, C8 or C10, and V again to return. S: UI-flow storyboards. N: notes. O: overview. F: fullscreen. B: blackout. Space / P: play/pause current clip. M: sound. R: restart. C: command cards. Z: full-size figure. Digits + Enter: jump to main slide n (the bottom-right badge shows n / N; backups show their label). Inside the UI-flow page (D2) click once, then → / 1–4 / S drive the page; Esc returns to the slides.

## Spoken delivery

### 1 · A month of moments. One film

00:00–00:10 · Section 1 · 00:10

Good afternoon. I am Gopal Guruprasath, presenting Rewind for Team 14: a month of everyday moments from a small private group, turned into one shared film.

Transition: First, the problem and the product boundary.

If asked: → P1

### 2 · Everyday moments need a shared reason to return

00:10–01:00 · Section 1 · 00:50

Our business problem is simple: people already capture moments, but the moments disappear inside busy chats and camera rolls. A group has no common point at which to look back together. Rewind adds that point. Two to ten members contribute photos or short videos, and the contributions remain sealed until a twenty-eight-day cycle closes. Each member has five moments and thirty seconds per week. The limit keeps the contribution small enough to become a habit. At the end, the group receives one film and a twenty-four-hour premiere before the film remains in Archive. Our scope is the real-account web and PWA journey: identity, private groups, invitations, capture, chat, reminders and films. That is the boundary used in the design and in the demonstration.

Transition: The four sprints show how we delivered this boundary.

If asked: → B1 · → P1

### 3 · Four sprints took Rewind from foundation to hosted real accounts

01:00–02:00 · Section 1 · 01:00

We used four sprints with zero-based names. Sprint zero built the runnable foundation; Sprint one integrated capture, the cycle and Archive; Sprint two delivered real accounts, private S3 media, PostgreSQL and Cognito; Sprint three concentrated on stability, recovery and regression tests. Velocity, as issues closed in each sprint window, was forty-four, one hundred, one hundred and forty-five and thirty. Today the real-account web and PWA journey runs end to end on hosted dev, and three hundred and nineteen of three hundred and twenty-nine backlog issues are closed. We held project planning, and Sprint Planning and Sprint Review every sprint. Done means the outcome checked in the cheapest real environment, fast tests, a green Quality check and a merge to dev.

Transition: The use cases now give that scope a formal boundary.

If asked: → P1

### 4 · Four burndowns, velocity and each member’s share of the effort

02:00–03:00 · Section 1 · 01:00

These are the four sprint burndowns and the velocity. Sprint one is the clean case: fifty issues in scope, thirty-seven open at the start and zero by the twenty-third of September. Sprint two is the counter-example: scope kept growing, to one hundred and thirty-five, as real accounts landed, and it closed with nine open. Velocity peaked in Sprint two with one hundred and forty-five issues closed and one hundred and thirty-two pull requests merged. Effort was not equal: I carried forty percent; Nguyen Kim Long, Jiang Jiayu and Phan Mai Tan Loi twenty percent each; Sang Haoxiang made a minimal contribution. Each retrospective changed the next sprint: integration gaps led to real adapters, stale state led to interaction tests.

Transition: 

If asked: → B25

### 5 · Fourteen use cases follow one private-group journey

03:00–03:30 · Section 2 · 00:30

The use case view starts with user goals. Members join a private group, contribute, chat and watch; the owner also manages membership and settings. The boundary makes the secondary systems explicit: identity, object storage, web push and scheduled time. For detailed design I follow CU-B: close the cycle, compile the film and release it, which joins UC07 and UC08.

Transition: The logical view shows where those responsibilities live.

If asked: → B1 · → B3

### 6 · One Node application keeps rules close to transactions

03:30–04:05 · Section 2 · 00:35

The main architecture decision is a modular monolith. Splitting membership, contributions and cycles into services would add coordination without helping this workflow; keeping the rules beside one transaction makes acceptance and cycle transitions easier to reason about. Hosted PostgreSQL holds durable relational state, private S3 holds media, and Cognito supplies web identity. Adapters keep those protocols out of the domain decisions.

Transition: Now map the analysis responsibilities onto that implementation.

If asked: → B4 · → B5 · → B9

### 7 · Analysis responsibilities become named implementation modules

04:05–04:40 · Section 2 · 00:35

The left side is analysis: a boundary receives interaction, a control coordinates the use case, and entities hold the state the business must retain. On the right we refine those responsibilities into real names. The scheduler finds work, lifecycle owns the cycle transition, compilation prepares and finalises the film, and the database keeps cycles, jobs and frozen inputs. A collection of functions is drawn as a module; a class symbol is reserved for a real class, so the model stays traceable to the code.

Transition: The hardest design problem is safely repeating this background work.

If asked: → B1 · → D1

### 8 · Durable claims make a repeated tick safe: close, claim, render, fence

04:40–05:30 · Section 2 · 00:50

This sequence is our hardest design problem: a scheduler tick can repeat, and an old worker can finish after its lease expires. Polling alone finds work but does not make repetition safe, so we compared State and Command object hierarchies with persisted state plus a durable job, and chose the durable job. One lifecycle transaction closes the cycle, freezes the inputs, queues the film job and opens the successor. The worker claims the job and renders outside the transaction. At finalisation it proves it still holds the current lease and generation, so a repeated tick reuses the job and a stale worker cannot publish.

Transition: The same reasoning gave three more named patterns.

If asked: → s7 · → B16 · → B17

### 9 · Three design problems, three named patterns in the code

05:30–06:15 · Section 2 · 00:45

Three more design problems, each solved with a named pattern; click a diagram to enlarge it. Top left, media storage: local disk in development and private S3 when hosted. MediaStore is the Strategy, with a local and a private-S3 implementation, and the S3 side adapts the AWS SDK, so the worker never branches. Top right, chat: every open screen needs each new message, so RealtimeHub is the Observer subject and each SSE connection subscribes. Bottom left, persistence: hosted PostgreSQL has a different API from local SQLite, so PostgresDatabase is an Adapter behind one data-access contract. Bottom right sums it up: problem, pattern, benefit.

[Cite if asked] Repeated work: lifecycle.ts and jobs/compilation.ts (the durable job on slide 8). Storage: privateTransport adapts the AWS SDK commands. Chat: stored messages replay on reconnect.

Transition: 

If asked: → B7 · → B8 · → B9 · → s7

### 10 · Keys preserve membership and the film’s exact input set

06:15–06:55 · Section 2 · 00:40

This is the database schema for the same use case. Membership relates an account to a group and its role, and every access decision uses it. A group has cycles; a cycle has contributions; media jobs retain processing state. Compilation inputs freeze exactly which media belongs to a film, so a retry cannot reinterpret a changing collection. We chose PostgreSQL because this path depends on joins and transactions across related records. Before the screens, one more model: the cycle’s states.

Transition: The cycle statechart came before the screens.

If asked: → B4 · → B9

### 11 · The cycle’s states were fixed before any screen

06:55–07:20 · Section 2 · 00:25

Stored lifecycle state and durable jobs make work recoverable; a current lease and generation determine who may finalise.

Transition: Each screen then maps to one of these states.

If asked: → B16 · → B17

### 12 · Each screen renders one state of the cycle

07:20–08:00 · Section 2 · 00:40

[Click inside the page to step through a flow; Esc returns to the slides. If the page does not load, press S for the storyboards.]

The screens came second, and each one maps to a state. While the cycle is collecting, Home shows the countdown, the week and the member’s allowance, and capture is offered. When the cycle closes, Home shows the film developing. Once it is published, the premiere card opens the film for twenty-four hours, and after that the film lives in Archive. Every screen reads the server’s state instead of keeping its own, so a refresh or a second device always agrees.

Transition: Testing checks those states through their real boundaries.

If asked: → D1 · → U1 · → U2 · → U3 · → U4

### 13 · Twelve test types each catch a different failure

08:00–08:50 · Section 3 · 00:50

Here is the whole test map: twelve types, each with its tool, count and when it runs. The tag says what a failure does. Blocks merge means the required Quality check turns red and the pull request cannot merge; reports means the result is recorded for review but never stops a merge. The top six block every pull request; browser, PWA and accessibility checks join for pull requests to main; the real-account journey and the load test run on demand. I will group them as unit, integration, end-to-end and security.

Transition: Start at the bottom: static checks.

If asked: → B6

### 14 · Six test layers, each with a real example of what it catches

08:50–10:10 · Section 3 · 01:20

Six layers, each with a real example. Unit and component tests: one thousand six hundred and seventy-four Jest tests check screens and state without a device, with node:test for server units. Integration: one thousand and six server tests call the real routes over HTTP, and the same suite runs again on PostgreSQL 17, so a dialect difference or migration drift fails the pull request. These block every merge. End to end, forty-one Playwright tests drive the exported app with an owner, an invited member and an outsider; the PWA build is checked as it will be installed; and axe with keyboard tests checks the main screens for WCAG 2.1 AA. Those three join for pull requests to main. Each card names one real test and the bug it catches.

Transition: 

If asked: 

### 15 · A regression test for a real bug, and security inside the suites

10:10–11:00 · Section 3 · 00:50

One real bug shows why we test behaviour. After a failed photo, Try again did nothing, because retry called capture from a state whose guard returned at once. The regression test fails the capture, taps Try again and expects the viewfinder and a fresh capture: it fails on the old code and passes with the fix. Security is also tested inside the suites: cross-group privacy denials, rate limits, our patched dependencies and the scan gates themselves. The pipeline scans come in the CI/CD section, and performance in the system demo.

[Cite if asked] Regression test: camera-capture.characterisation.test.tsx. Rate limits: safety-rate-limits.test.mjs. Patched dependencies: braces and node-forge, where the original node-forge accepts a forged signature. Access tests cover account safety too; scan gates reject expired, wrong or incomplete scans.

Transition: 

If asked: → s11

### 16 · One change passes four gates; colour says what a failure blocks

11:00–11:45 · Section 4 · 00:45

This is the whole pipeline on one page. The legend in the corner reads every pipeline figure: colour says what a failure blocks, orange the merge, blue the deploy, purple a push or promotion rule, and dashed grey only reports; hexagons are decisions. Band one is the pull request into dev: Quality checks is the one required check, and CodeQL, Gitleaks, Trivy and GitGuardian report beside it. Band two starts on the same push to dev: wait for Quality on the merge commit, build one bundle, scan the exact images, sign, upload, and activate only if health passes. Band three is hosted dev, scanned by ZAP after every deploy; promotion to main needs one human approval.

Transition: Before the detail, a quick key to the shapes and colours.

If asked: → C2 legend · → C3 source and artifacts

### 17 · Protected branches carry source; every run leaves results we can inspect

11:45–12:30 · Section 4 · 00:45

Source management: work starts on an issue branch from the latest dev and enters dev only through a pull request. The dev rule requires the Format, lint, typecheck, and test check, an up-to-date branch and resolved conversations, applies to administrators, and forbids force-pushes and deletion. Main adds one approving review and the browser and PWA checks. Artifact management: Git keeps source, the lockfile, workflows, Terraform and Dockerfiles. Each run keeps its results as artifacts named with the commit SHA: JUnit, npm audit, SARIF, Trivy, SBOMs, the manifest and the release tar for thirty days, coverage for fourteen and ZAP for ninety. Provenance sits in GitHub attestations, and the host keeps the current, previous and pending releases for rollback.

Transition: Now zoom into the pull request band.

If asked: → CB2 branch protection settings

### 18 · Nine Quality jobs feed one required merge check; security reports beside it

12:30–13:20 · Section 4 · 00:50

This is quality.yml on a pull request. The first job classifies the change; a code change fans out into eight parallel lanes: four static checks, the production dependency audit, root and IaC tests, server tests on SQLite with coverage, the same suite on PostgreSQL 17, frontend Jest with a seventy percent statement floor, and the deployment fixtures. The last job, Format, lint, typecheck, and test, needs every lane green; it is the one check in branch protection, so a red lane disables the merge button.

[V shows the security workflows; V again returns.] Beside it, CodeQL, Gitleaks, release security and GitGuardian report into the Security tab without blocking the merge.

Transition: Beside Quality, the security workflows run and report.

If asked: → C16 tests and coverage numbers

### 19 · Deploy scans and signs the exact bundle, then activates only if healthy

13:20–14:10 · Section 4 · 00:50

The merge to dev starts Deploy dev. It first waits for the Quality run on this exact merge commit; if that fails, the host is untouched. release.py builds one tar with the runtime and web images. scan-release.py extracts those exact images, writes a CycloneDX SBOM and Trivy report for each, and stops on any High or Critical finding before upload. attest-build-provenance then signs the tar and the manifest.

[V shows the second half; V returns.] For upload, GitHub holds no AWS keys: OIDC gives a one-hour role session limited to this repository and dev. The host checks the tar’s SHA-256, starts the candidate and activates it only when health is ready; otherwise it restores the previous release.

Transition: Only then does the runner touch AWS.

If asked: → C14 SBOM and provenance

### 20 · ZAP scans hosted dev after every deploy: 0 High, 4 Medium (CSP)

14:10–14:55 · Section 4 · 00:45

After every deploy, a second job runs the OWASP ZAP baseline against the hosted site: a spider and an AJAX spider crawl it for two minutes and passive rules inspect every response, unauthenticated and without attacks, because hosted dev holds shared data. It is report-only.

[V shows the real results; V returns.] This deploy found zero High and four Medium alerts, all from one Content Security Policy gap: our full policy is served Report-Only, so directives such as form-action are effectively unrestricted. The fix is to enforce that policy once its reports are clean.

Transition: That completes the pipeline. Here is everything it checks for, in one table.

If asked: → C15 DAST results

### 21 · SAST findings are triaged with reasons; SCA blocked merges until fixed

14:55–15:45 · Section 4 · 00:50

SAST is CodeQL with the security-extended suite on TypeScript, Python and the workflow files, on every pull request, push and weekly. In pull request 592 it raised three medium alerts, 54 to 56, in the load-test script; we dismissed them as used in tests with a written reason, because that harness never ships in the image.

[V shows SCA; V returns.] SCA is the production dependency audit inside the required check. On 24 October a new advisory marked zod below 4.6.6 as high severity; Quality turned red and two pull requests could not merge until PR 591 added a scoped override. The retained audit now shows zero vulnerabilities across 674 production dependencies.

Transition: Next, dependencies, where a real advisory blocked us.

If asked: → alert 56 page live

### 22 · The pipeline caught problems that source-level tests could not

15:45–16:25 · Section 4 · 00:40

The technical findings. A new zod advisory blocked merges with no change from us until PR 591 fixed it. Alpine removed the FFmpeg version we pinned, so the image stopped building. An audit of our own pipeline found we scanned a rebuilt image rather than the deployed one; PR 595 moved the gate onto the exact bundle and added the manifest and attestation. Gitleaks reported twenty-seven historical false positives, so we allowlisted exact values. And Cognito code passed its tests while its runtime dependencies were missing from the image. The lesson: verify what ships, not just the source.

Transition: Now the live route through GitHub.

If asked: → B31 product findings

### 23 · Demo route: eight clicks from pull request to running site

16:25–21:00 · Section 4 · 04:35

This is the route for the live part: the pull request checks, the Quality run and its artifacts, a triaged CodeQL alert, the Deploy dev run and its steps, the attestation, the ZAP report and the hosted health endpoint.

[Live in GitHub, about thirty seconds per link. If the network fails, open backup CB1 and play the recorded walkthrough.]

1. Pull request checks: Quality is the required context; the security workflows sit beside it.
2. Quality run: the job graph fans out and joins the aggregate; open the artifacts list.
3. CodeQL alert 56: the rule, the line and the written dismissal reason.
4. Deploy dev 40344230832: wait for Quality, build, scan, attest, install.
5. Deploy steps: the exact-image scan and the upload order.
6. Attestation: the signed subject is the manifest for this commit.
7. ZAP report: 0 High, 4 Medium, all Content Security Policy.
8. Hosted health: the installed version and PostgreSQL readiness.

Return to the slides for the product journey.

Transition: Now the product journey on hosted dev.

If asked: → CB1 recorded film

### 24 · A private-group journey runs from prompt to film

21:00–21:15 · Section 5 · 00:15

Two members have their accounts ready. We create the group, invite, contribute a photo and a video, chat, then watch the film, save it, and test the outsider boundary.

Transition: Create the group and choose its shared prompt.

If asked: → B1 · → B3

### F3 · A shared prompt gives the group a common starting point

21:15–22:00 · Section 5 · 00:45

[Space to start. Narrate over the clip; press → as soon as the stated result shows. The clip need not finish.]

The owner names the group, picks a shared prompt and sets the size, two to ten members. The prompt gives contributions a common theme. Pause when the new group and its prompt appear in settings.

Transition: Invite a friend with a single-use code.

If asked: → B1

### F4 · One accepted invitation creates one private membership

22:00–23:00 · Section 5 · 01:00

[Space to start. Narrate over the clip; press → as soon as the stated result shows. The clip need not finish.]

The owner creates an invitation code; it works once and expires after twenty-four hours. Our friend accepts it from the prepared account, and both accounts now see the same group and member list. Acceptance is a server decision: a valid code and an authenticated account produce one durable membership. Reusing the code will not add anyone; we test that at the end.

Transition: The first contribution is a photo.

If asked: → B3

### F5 · A submitted photo becomes a sealed moment

23:00–24:00 · Section 5 · 01:00

[Space to start. Narrate over the clip; press → as soon as the stated result shows. The clip need not finish.]

Take a photo and choose a look before submitting it. The user can review the contribution, but after acceptance it becomes sealed. Your moments retains the entry and allowance information without opening everyone’s submitted content early. A photo counts as one moment and becomes a three-second segment in the film. Watch the state change from capture to a retained sealed entry.

Transition: Video shares the same weekly allowance.

If asked: → B3

### F6 · Video and photos share one enforced weekly allowance

24:00–25:10 · Section 5 · 01:10

[Space to start. Narrate over the clip; press → as soon as the stated result shows. The clip need not finish.]

Record a video, review the trim and submit it. A video can use up to fifteen seconds, and the total weekly allowance is shared with photos: five moments and thirty seconds per member. The visible ledger matters because the user needs to know what remains before trying another capture. The server checks the accepted contribution and media rather than trusting only the client display. Pause at the updated counts. The contribution is now part of the same sealed collection as the photo.

Transition: The group can talk while the moments stay sealed.

If asked: → B3

### F7 · Stored messages and live updates keep the group connected

25:10–26:05 · Section 5 · 00:55

[Space to start. Narrate over the clip; press → as soon as the stated result shows. The clip need not finish.]

One member sends a message and the other sees it without refreshing. Replies and reactions remain in the shared conversation. The design combines stored messages with live SSE delivery and reconnect, so the live notification is not the only record of the message. This is where the Observer pattern from the design section becomes visible to a user.

Transition: Next, opt into the weekly reminder.

If asked: → B8

### F9 · The cycle closes, and the group watches its film

26:05–27:10 · Section 5 · 01:05

[Space to start. Narrate over the clip; press → as soon as the stated result shows. The clip need not finish.]

Switch to The little things, a completed capsule from Maya and Jun. The premiere card appears because the scheduler closed the cycle, compiled the film from the frozen inputs and opened the next cycle: the CU-B path from the design section. Open it: one portrait film, seven-twenty by twelve-eighty at thirty frames per second, built from everyone’s sealed moments. Press M only if you want sound. Pause at the end screen.

Transition: Open the group’s film.

If asked: → D1

### F11 · Archive keeps the film available after its premiere

27:10–28:15 · Section 5 · 01:05

[Space to start. Narrate over the clip; press → as soon as the stated result shows. The clip need not finish.]

After the premiere, the film remains in Archive. Open the retained film, choose Save film and open the downloaded MP4. The end screen also lets a member save their own moments. This completes the journey from capture to a durable output the member can keep. Pause on the playable downloaded result. The final check uses a different account that has no membership.

Transition: Check the outsider boundary.

If asked: → B4

### F12 · A spent invitation gives an outsider no group access

28:15–29:15 · Section 5 · 01:00

[Space to start. Narrate over the clip; press → as soon as the stated result shows. The clip need not finish.]

From the outsider’s prepared account, try the invitation already used by our friend. The app rejects it as already used. The group does not appear in the outsider’s list. This is the negative branch of the invitation rule shown earlier. The server tests also exercise direct group, budget, chat and media access with missing or wrong membership. The user demonstration and those API checks address the same privacy boundary at different layers. We have now completed the group journey.

Transition: Finish with the hosted load results and the scaling mechanism.

If asked: → B6

### 25 · Load and stress: 100 users pass; the breakpoint is 200, set by the database bridge

29:15–31:15 · Section 5 · 02:00

Now the quality attributes. Performance was measured with a scripted load test against hosted dev: a Node HTTP runner drives the real API through CloudFront, Node and PostgreSQL, each user waits three to seven seconds between actions, and the mix is ninety-five percent reads. A stage passes with p95 under two seconds and errors under one percent. One to one hundred users all passed: at one hundred, p95 was 1.34 seconds, 17.8 requests per second, zero errors. This morning we pushed further. One hundred and fifty users still passed at 1.66 seconds. The breakpoint is two hundred users: p95 rose to 3.03 seconds, with still zero errors, and throughput saturated at twenty-nine requests per second, eighty percent of linear. At three hundred we stopped the ramp. The system fails by queueing, not by rejecting requests. The limiting factor is not the host CPU, which stayed under twenty-five percent, and not a rate limiter: every database call blocks the single Node event loop on one PostgreSQL client, so every request, even health, waits in the same queue.

[Cite if asked] 1–100 users: 180 s steady stages (26 Oct); 150–300: 60 s stress stages (27 Oct). Every database call waits through Atomics.wait on a single pg client (server/src/postgres/database.ts, sync-worker.ts). Load-generator CPU peaked at 26% of one core, event-loop p99 ≤ 22 ms; zero 429s, 5xx, timeouts or socket errors.

Transition: 

If asked: → T12 · → B34 · → B11

### 26 · The capacity model, checked by the stress test, shows where to scale next

31:15–33:00 · Section 5 · 01:45

Scalability: the capacity model fitted on the one-to-one-hundred run predicted a ceiling of about twenty-two requests per second and a knee near one hundred and sixteen users. The stress test confirms its shape and shows it is about 1.4 times conservative: the measured knee lies between one hundred and fifty and two hundred users, and saturation between twenty-nine and thirty-six requests per second. So the scale-out path follows the bottleneck. First, asynchronous persistence with a bounded connection pool, which removes the serialization. Second, a second API host behind a load balancer, which doubles the modelled ceiling; at two hundred and fifty users the mean drops from 6.4 to 1.1 seconds. Third, a separate media worker keeps film compilation off the API host. A larger instance alone would add little, because the CPU is not saturated. Maintainability is the pipeline we just walked through: those internal changes must pass the same behavioural tests, both database dialects, the exact-image scan and the health-gated deploy. Thank you; I am ready for questions.

Transition: We can take questions using the backup map.

If asked: → B6 · → B11 · → B12

## Q&A backup map

| Backup | Question | Spoken answer |
|---|---|---|
| U0 | UI flow page · screens mapped to the cycle statechart | [Click inside the page to step through a flow; Esc returns to the slides. If the page does not load, press S for the storyboards.]

The screens came second, and each one maps to a state. While the cycle is collecting, Home shows the countdown, the week and the member’s allowance, and capture is offered. When the cycle closes, Home shows the film developing. Once it is published, the premiere card opens the film for twenty-four hours, and after that the film lives in Archive. Every screen reads the server’s state instead of keeping its own, so a refresh or a second device always agrees. |
| U1 | UI flow 1 · Join a private group | Storyboard for the Join a private group flow: each frame is labelled with the cycle state it renders. Use these if the interactive page is unavailable. |
| U2 | UI flow 2 · Contribute within the allowance | Storyboard for the Contribute within the allowance flow: each frame is labelled with the cycle state it renders. Use these if the interactive page is unavailable. |
| U3 | UI flow 3 · Cycle lifecycle to archive | Storyboard for the Cycle lifecycle to archive flow: each frame is labelled with the cycle state it renders. Use these if the interactive page is unavailable. |
| U4 | UI flow 4 · Outsider is denied | Storyboard for the Outsider is denied flow: each frame is labelled with the cycle state it renders. Use these if the interactive page is unavailable. |
| C5 | Security workflows run beside Quality and keep their findings | [Detail for C4: press V to return.] Five security procedures run on the same pull request. CodeQL is our SAST. Gitleaks scans the full git history for secrets. Release security builds both images, writes a CycloneDX SBOM and fails on High or Critical vulnerabilities, and scans Terraform and Dockerfiles. GitGuardian and Dependabot add secret and dependency alerts.

These are reporting controls: they can turn their own job red, and the findings land in the Security tab or as artifacts, but they are not required checks. The vulnerability gate that does block is in the deployment, on the exact images we ship. That is the next page. |
| C7 | Keyless AWS access and a health check decide activation | [Detail for C6: press V to return.] GitHub has no AWS keys. The job exchanges its OIDC token for a one-hour role session, and the role trusts only this repository, the dev environment and refs/heads/dev. The runner checks the host is running, opens port 22 for its own address only with a short-lived key, ships the bundle and streams the hosted settings from a private S3 object.

On the host, the uploaded tar must match the built tar’s SHA-256. The installer starts the candidate images and activates them only when health is ready and the running image IDs match; otherwise it restores the previous release and the job turns red. Then the public health endpoint is checked, SSH is closed and the key deleted, and the DAST job starts. |
| C15 | DAST: 0 High, 4 Medium, all from one Content Security Policy gap | [Detail for C8: press V to return.] Here are the real ZAP results for the deployed commit: zero High, four Medium, seven Low and six informational alert types. All four Medium alerts are Content Security Policy findings.

Take the first one. ZAP sent a GET to the hosted home page, robots.txt and sitemap.xml, read the Content-Security-Policy header, and found only frame-ancestors none. Directives such as form-action do not fall back to default-src, so they are effectively unrestricted. The informational alert explains why: our full policy is served as Content-Security-Policy-Report-Only, so browsers report violations but do not enforce them. The fix is to promote that policy to enforced once its reports are clean. The Low findings are missing hardening headers and the nginx version string. |
| C11 | SCA: a new zod advisory blocked merges until we fixed it | [Detail for C10: press V to return.] SCA is the production dependency audit, inside the required check. On 24 October, with no code change from us, a new advisory, GHSA-mrhx-c7xc-m3w5, marked zod below 4.6.6 as high severity: oversized collections can exhaust memory. Our copy came in through Expo’s CLI. Three high findings turned Quality red and two small pull requests could not merge. That is the gate working as designed.

npm suggested a forced, breaking Expo upgrade. Instead PR 591 added a scoped override so only Expo’s CLI uses zod 4.6.6. The retained npm-audit.json for the deployed commit shows zero vulnerabilities at every severity across 674 production dependencies. Dependabot adds alerts and security update pull requests; the one open alert is a development-only package. |
| B1 | Analysis separates interaction, coordination and state | The analysis model separates the interaction boundary, use-case coordination and durable business state; main frame six maps those responsibilities to code. |
| B3 | Capture acceptance checks identity, allowance and media | The capture sequence follows reservation, media validation and acceptance, keeping membership and allowance decisions on the server. |
| B4 | Relational keys make the private film traceable | The relational choice follows transaction and consistency needs across membership, cycles, contributions and the frozen film input set. |
| B5 | The deployment view names each runtime boundary | CloudFront and nginx form the entry, Node runs the application, and PostgreSQL, S3 and Cognito provide the durable data and identity services. |
| B6 | Coverage and enforcement answer different questions | The statement floor is a regression safety net. Coverage reports identify branches to investigate, while behavioural tests assert the outcomes that matter. |
| B7 | Storage changes behind Strategy and Adapter roles | The problem is duplicated storage-specific branches in compilation and media code. We compared branching in each caller with an injected storage contract. We chose the MediaStore Strategy so the worker uses one interface. LocalMediaStore and PrivateS3MediaStore implement that contract, and privateTransport adapts AWS SDK commands. Hosted runtime selects PrivateS3MediaStore; disk mode has its separate filesystem path. |
| B8 | Observer distributes chat updates alongside stored history | RealtimeHub acts as the live update subject and subscribers receive events, while stored messages provide the durable history and reconnect path. |
| B9 | The persistence adapter preserves a common data-access contract | PostgresDatabase adapts the common call contract to PostgreSQL; centralising that translation also makes the synchronous bridge a clear target for performance work. |
| B11 | The capacity curve follows the closed-user workload | The quiet-host run fits S = 45.39 milliseconds per request, L = 377.9 milliseconds, and Z = 5 seconds. The model solves U = lambda S, R = L + S/(1-U), and lambda = N/(Z+R) together. Projected one-host throughput approaches 22.0 requests per second; the 90-percent-utilisation knee is about 116 users. At 250, 500 and 1,000 users, projected one-host means are 6.43, 17.75 and 40.44 seconds. The two-balanced-host means are 1.07, 6.43 and 17.75 seconds. The measured 100-user mean is 615.4 milliseconds, and its p95 is 1,335.9 milliseconds. |
| B12 | Retained artifacts make the deployment independently inspectable | Use the manifest for commit and image identity, SBOMs for inventory, scan JSON for findings, provenance for build origin and ZAP for the running hosted page. The demonstrated verification checks release-manifest.json and exits zero. The real IaC JSON is retained under pipeline-run-40344230832/iac/, from same-commit Release security run 40344231046. |
| B13 | Acceptance pins and probes the exact media version and replays an existing receipt | Acceptance pins and probes the exact media version and replays an existing receipt. |
| B14 | One transaction records quota, contribution, processing job and completion | One transaction records quota, contribution, processing job and completion. |
| B15 | Processing stores an MP4 and proves current ownership before marking ready | Processing stores an MP4 and proves current ownership before marking ready. |
| B16 | The worker claims settled inputs, materialises media and fences finalisation | The worker claims settled inputs, materialises media and fences finalisation. |
| B17 | Stored bytes and the current ready row are verified before publication and archiving | Stored bytes and the current ready row are verified before publication and archiving. |
| B18 | Account and group goals connect to Cognito, chat and web push | Account and group goals connect to Cognito, chat and web push. |
| B19 | Photo and video acceptance include the shared allowance and optional correction | Photo and video acceptance include the shared allowance and optional correction. |
| B20 | Cycle closure produces a film, premiere, Archive and authorised downloads | Cycle closure produces a film, premiere, Archive and authorised downloads. |
| B25 | Backlog stories connect sprint goals to delivered use cases | The saved backlog contains 329 issues, 319 closed and ten open. UC05 links the photo story to Sprint 2 issue 313 and Sprint 3 recovery and format issues 545 and 574. Sprint goals and retrospective actions retain that trace. |
| B26 | A commit carries tests, inventory and deployment evidence | Source management starts with a focused issue branch and a pull request to protected dev. The required Quality result belongs to the exact commit. Once merged, that same source revision triggers dev deployment. The artifact flow matters because a passing test run and a deployed application must be connected by identity.

Quality retains root JUnit, server results and coverage, frontend Jest JSON and coverage, and the production dependency audit report. Deployment retains the runtime and web image inventories, the exact-image Trivy reports, the security manifest and the deployable tarball. Signed provenance binds the retained bundle and manifest to the workflow. After deployment, the ZAP reports describe the running hosted target. The host receives the built image pair in the verified bundle. It does not independently rebuild the application from a moving branch. These artifact families let us move from a source question to a test, package, scan or running-page result without treating those as interchangeable evidence. |
| B27 | Pipeline decisions separate merge gates from host activation | There are several decisions inside this activity view. First, change classification decides whether the commit needs application checks or is documentation-only. A code change fans out across parallel static, client, server, PostgreSQL, root and deployment-fixture lanes. The aggregate fails on a failed or unexpectedly skipped required lane. Production dependency audit is part of that aggregate.

Second, deployment waits for a successful dev Quality run for the same commit. It builds and verifies the bundle, inventories the exact runtime and web images and scans those images. High or Critical findings at that exact-bundle gate stop host upload. This is a deployment gate even though the independent scan workflows are not branch-required checks.

Third, the host installs a candidate and checks it before activation. Failure takes the restoration path. Once the host is serving, the passive ZAP baseline spiders hosted dev and publishes its report. SAST and the other security reports remain visible as their own lanes. The distinction is operational: branch protection requires the aggregate Quality context; a deployment step can independently stop the upload; a reporting lane retains findings for triage. The words BLOCKS and REPORTS in the figure refer to those specific decisions. |
| B30 | Hosted dev activates after candidate health succeeds | The deployment view puts the logical design onto hosted dev. GitHub Actions obtains temporary deploy credentials through OIDC. It ships the verified bundle to the Lightsail host, where nginx fronts the Node process. The application uses PostgreSQL, private S3 storage, Cognito and web push. CloudFront is the public edge.

Activation is a host decision. The installer prepares a candidate, verifies its health, then switches current. If the candidate is unhealthy, the installer restores the previous current. The deployment run then checks the public health endpoint. In our selected run, install completed at fifteen oh two forty-one UTC and the public check passed. The topology explains the runtime boundary, while the workflow and host installer explain who makes each decision. The following findings are examples of defects that escaped a narrower source-only view. |
| B31 | Packaging and runtime boundaries exposed useful defects | Five findings explain the checks we chose. A new zod advisory turned the production audit red even with a lockfile. The scoped dependency update restored a clean audit. Separately, Alpine removed the pinned FFmpeg package version, so the image failed before vulnerability scanning; the package pin had to move to the available version.

A schema refactor moved the registry while deployment packaging still read the old location. Updating the packaging consumer restored bundle verification. In the PWA, service-worker forwarding prevented SSE cancellation from reaching upstream; repeated group changes then exhausted stream limits. Keeping SSE browser-owned repaired that lifetime. Finally, the failed-capture retry needed a behavioural test of the recovery path. The common lesson is to exercise the real boundary: the package repository, the built image, the service worker, or the full interaction. We can now see how those concerns appear in one retained deployment run. |
| B32 | Installation keeps the app one tap away | We start in Safari and add Rewind to the Home Screen. The installed app then opens as its own window. This is the iPhone delivery surface used for the journey. Watch the transition from the browser to the standalone app. Once it opens, the next step is identity. |
| B33 | Sign-in returns the member to the private-group journey | Maya signs in and arrives in her private group space. The hosted development form gives us an authenticated account for this walkthrough. The web identity design also supports Cognito Managed Login using an authorization code with PKCE and a server-side exchange. The next decisions are about which group this account owns or belongs to. |
| B34 | Measured latency and throughput by stage on hosted dev | Latency p50, p95 and p99 per steady stage, beside throughput. Every p95 stays under two seconds; the 100-user p95 is 1,335.9 ms and throughput 17.84 requests per second, with zero errors. |
| CB1 | Recorded walkthrough · PR checks to hosted dev | [00:00–00:20 section clock: introduce the recording, then press Space. Narrate the following cues over the 11:26 film. Its clip clock starts at zero.]

The recording starts with PR Quality 40343459119 at commit 38593b2. Deploy 40344230832 uses merged commit aea7478 and its separate dev Quality gate, 40344231052. Follow the actual artifacts and security findings; an advisory and FFmpeg pin explain why we verify built images.

[00:00–00:20 video · 01 · Pipeline decisions]
Follow one change through six decisions: the pull request, parallel verification, security findings, the verified bundle, hosted dev and promotion. I will connect each decision to the check or artifact that records its result.

[00:20–00:40 video · 02 · PR #595 checks]
Pull request 595 contains the pipeline artifact changes. Its checks list shows static analysis, tests and the dependency audit feeding the aggregate Quality gate. The individual results remain visible alongside the required merge check.

[00:40–00:56 video · 03 · PR #595 security checks]
The same pull request also records CodeQL, image and IaC scans, and secret scanning. These results are visible for security review alongside Quality.

[00:56–01:20 video · 04 · Protected dev]
The dev branch requires a pull request, an up-to-date branch and the check named Format, lint, typecheck, and test. Conversation resolution and administrator enforcement are enabled. The required approving-review count is zero, which allows routine dev changes to proceed after the automated gate.

[01:20–01:44 video · 05 · Protected main]
Main keeps the same required Quality context and adds one approving review, including approval of the last push. This is the promotion boundary: a change that has reached dev still passes through the main review rule.

[01:44–02:12 video · 06 · Quality run graph]
The Quality graph starts with change classification and fans out into parallel jobs. Tests, coverage, static checks and the production dependency audit feed the aggregate gate. Main-bound changes also run the web export and browser checks.

[02:12–02:32 video · 07 · Quality artifacts]
The run retains four artifact groups: root JUnit results, server coverage, frontend coverage and npm-audit JSON. They remain attached to the run and its commit, so a reviewer can inspect the machine-readable results behind the green check.

[02:32–02:52 video · 08 · JUnit results]
The JUnit report records individual test cases and their outcomes. The job summary presents the totals, while the XML keeps the detail for inspection. This links the test result to the exact Quality run rather than relying on a copied test count.

[02:52–03:22 video · 09 · Coverage summaries]
These are the coverage reports retained by the same run. Frontend statement coverage is 89.64 percent, and server line coverage is 85.50 percent. The reports preserve the underlying counts and coverage dimensions alongside the test results.

[03:22–03:46 video · 10 · Production dependency audit]
The production dependency audit reports zero findings at every severity in this run. The command audits production dependencies and fails on High or Critical findings. Because this job feeds the required Quality gate, a failed audit prevents the normal merge path.

[03:46–04:08 video · 11 · CodeQL security results]
CodeQL publishes its analysis results to the Security area. The alert list records the rule, affected code and disposition. The captured dev results have no open alerts; closed alerts retain their review reasons so the decisions can be inspected.

[04:08–04:38 video · 12 · PR #592 alert triage]
The load-test harness in pull request 592 raised CodeQL findings. Alert 56 concerns writing a report to an operator-selected path. Its recorded disposition is used in tests, with an explanation that this harness is operator-run and never shipped in the application image.

[04:38–05:02 video · 13 · Gitleaks full-history scan]
The secret-scan workflow runs Gitleaks over the repository history and retains a redacted SARIF artifact. The run records the scan result. Historical exceptions are constrained to exact benign values and paths, so a new value in the same file still receives normal scanning.

[05:02–05:18 video · 14 · Deploy dev run 40344230832]
Deploy dev 40344230832 records the artifact-rich deployment. The graph orders change classification, the deploy job and the ZAP baseline against hosted dev.

[05:18–05:32 video · 15 · Deploy job steps]
The steps wait for Quality on the same commit, build and scan the exact bundle, attest the artifacts, obtain temporary OIDC credentials and install the release.

[05:32–06:04 video · 16 · Exact-bundle Trivy gate]
This step scans the runtime and web images inside the bundle that will be uploaded. Both images have zero High and Critical findings in the manifest. The runtime image also records one Medium finding and two Unknown findings. The High and Critical gate runs before host upload.

[06:04–06:28 video · 17 · CycloneDX SBOM]
The CycloneDX files inventory components from the exact bundled runtime and web images. The SBOM and vulnerability reports describe the same image pair. Their hashes are recorded in the release manifest, connecting component inventory, scan results and the bundle identity.

[06:28–06:46 video · 18 · Release manifest]
The manifest records the commit, workflow run, successful Quality run, scanner and security-gate result. Its image entries and hashes connect the source verification to the retained deployment artifacts.

[06:46–06:58 video · 19 · Retained deployment artifacts]
The run retains the deployable bundle, the security reports and manifest, and the ZAP reports as three downloadable artifact groups.

[06:58–07:18 video · 20 · Manifest digests]
The SHA-256 entries bind the release tarball, both component inventories and both vulnerability reports. The second command computes the digest of the downloaded manifest itself. That exact digest is the subject checked by the attestation verification command.

[07:18–07:42 video · 21 · GitHub build attestation]
The deployment creates GitHub build attestations for the release bundle and security manifest. The provenance identifies the repository and deployment workflow that produced the subject. The next terminal command checks that signed provenance against the downloaded manifest bytes.

[07:42–08:12 video · 22 · Verify the attestation]
Here is the real gh attestation verify output for release-manifest.json. Verification succeeds against the repository policy, the SLSA provenance predicate and the GitHub Actions OIDC issuer. The matched signer workflow is deploy-dev.yml on the dev branch, and the command exits with status zero.

[08:12–08:40 video · 23 · DAST job summary]
After deployment, the ZAP baseline runs against hosted dev. Its summary records zero High, four Medium, seven Low and six Informational findings. The report is retained with the deploy run, and the baseline reports its findings without making them a deployment gate.

[08:40–09:04 video · 24 · ZAP HTML report]
The retained HTML report makes the dynamic findings inspectable. Each entry names the rule, risk and affected requests. The Medium findings concern Content Security Policy. This connects the summary counts to concrete observations on the running hosted application.

[09:04–09:38 video · 25 · Performance summary]
The full profile ran after deployment, with 1, 10, 25, 50 and 100 virtual users. At 100 VUs, the measured p95 is 1336 milliseconds and throughput is 17.84 requests per second, with 0 errors across 3212 requests. The retained summary records each steady stage.

[09:38–10:06 video · 26 · Performance chart]
The chart plots the clean run across the five load stages. The measured observations feed the response-time and throughput figures. The capacity table keeps the measured baseline alongside projected values for 250, 500 and 1,000 users.

[10:06–10:30 video · 27 · Hosted dev health]
The hosted dev health endpoint returns HTTP 200. The JSON reports PostgreSQL and a ready schema at migration 31. Deployment identity comes from the workflow and manifest; this endpoint provides a direct check that the hosted application and database are responding.

[10:30–11:06 video · 29 · Promotion PR #586]
Pull request 586 carries dev into main. The captured pull request already has an approving review, and the main protection rule requires that review. Its checks and merge state remain visible separately. I am showing the promotion controls and leaving the pull request unchanged.

[11:06–11:26 video · 30 · Decisions and retained artifacts]
The chain is now visible: protected source changes, retained test and audit results, reviewed security findings, an exact-bundle scan, a signed manifest, hosted health, dynamic findings and a load-test result. Each artifact stays connected to the commit and run that produced it.

[11:46–12:00 section clock: pause on the final decision chain.]
Quality controls integration, the exact-image scan controls upload, and candidate health controls activation. CodeQL, IaC, secrets and ZAP retain their findings for review. Those retained artifacts make the next internal change inspectable. Now follow the product journey. |
| CB2 | Branch protection: dev automates the gate; main adds a human review | Values read from the branch-protection API for dev and main on 27 October. Only one check is required on both branches; the other security workflows report. Main adds one approving review with last-push approval and the browser lane. |
| CB3 | Deploy job steps in GitHub, in the order of the stage diagrams | Real capture of the deploy job step list and its retained artifacts: dev-release-security, dev-release-bundle and zap-baseline, each named with the commit SHA. |
| s7 | Durable claims keep repeated cycle work safe | A scheduler tick can repeat, and an old worker can finish after its lease expires. We compared polling alone, State or Command object hierarchies, and persisted state with a durable job. We chose the durable job with lease and generation checks: expensive rendering runs outside the transaction, then finalisation proves that this worker still owns the current claim. Storage creates a second design problem: duplicated backend branches would spread through the worker. Instead we inject the MediaStore Strategy. LocalMediaStore and PrivateS3MediaStore supply the implementations; the S3 transport Adapter translates the SDK operations. The pattern roles are labelled on the real design elements. |
| C2 | Colour says what a failure blocks; shape says what the element is | Every pipeline page uses the same key. The colour and the first word of a box tell you what happens when it fails. Orange, BLOCKS MERGE: the required Quality check turns red and the pull request cannot merge. Blue, BLOCKS DEPLOY: the deploy stops before upload or before activation, and hosted dev keeps the release it already has. Purple: a platform rule or a human approval, such as push protection or the review on main. Dashed grey, REPORTS: the finding is recorded and visible, but it never stops a merge or a deployment.

Hexagons are decision points. A yes continues the flow; a no stops it. The yellow page shape is a retained artifact, a cylinder is a store, and a box with depth is a running host. |
| C9 | Nine kinds of check, each with a recorded result and a link | This is the catalogue of what we check for. Each row is a procedure the course asks for, with its tool, its trigger, what a failure blocks, the real result for the commit we deployed, aea7478, and a link to the GitHub page that holds it.

Two rows block merges: the dependency audit and the tests, because both are inside Quality. Three block the deployment: the exact-bundle Trivy scan, a failed attestation step, and the health check. SAST, IaC, Gitleaks and DAST report. The next slides take one row each and show the real artifact behind it. |
| C12 | Secrets are checked at push, on the PR and across history | Secrets are checked in three places. At push time, GitHub push protection rejects known provider key patterns before they reach the repository. On the pull request, GitGuardian scans the new commits. And the Secret scan workflow runs Gitleaks over the entire git history on every pull request and push, keeping a redacted SARIF report and sending it to the Security tab.

The default rules flagged migration identifiers and two test keys as generic API keys. Rather than silence the rule, the allowlist requires the exact file and the exact value, so a real key in the same file would still be found. The current result is zero findings. |
| C13 | Trivy blocks risky images; IaC risks need dated exceptions | Trivy scans our two container images twice. Release security scans candidate images on pull requests and pushes. The deployment then scans the images inside the exact bundle it will upload, and that second scan is the one that blocks: any High or Critical stops the upload. For this deployment both images had zero High and Critical. The runtime image has one Medium in zlib with a fix available, and two Unknown entries in musl.

For infrastructure as code, Trivy config scans Terraform and Dockerfiles. It found fifteen issues: seven Low and eight High. Every High must match exactly one exception with an owner, a reason and an expiry date. Most are about customer-managed KMS keys and a WAF that would add cost. The exceptions expire on 31 October, and after that the job fails until each risk is reviewed again. |
| C14 | SBOM and provenance bind shipped bytes to scans and workflow | The SBOM is a CycloneDX inventory of each exact bundled image: 187 components in the runtime image, including the FFmpeg package we had to re-pin, and 72 in the web image. The release manifest records the commit, the run, the Quality run that allowed it, both image IDs and digests, the severity counts, and the SHA-256 of the tar, both SBOMs and both reports. So inventory, findings and bytes are bound together.

Provenance: the deploy job signs the tar and the manifest with GitHub’s attest-build-provenance, using Sigstore and the job’s own OIDC identity. Anyone can check it: gh attestation verify on the downloaded manifest succeeds and names deploy-dev.yml on refs/heads/dev as the workflow that built it. |
| C16 | Tests and coverage gate the merge and are kept as artifacts | Tests are part of the same gate. On the filmed pull request run, root tests passed 123, the server suite passed 985 with 85.5 percent line coverage, and the frontend passed 1,674 with 89.6 percent statement coverage against a seventy percent threshold. The server suite also runs on PostgreSQL 17, the hosted engine. Every lane keeps JUnit, Jest JSON or coverage JSON as artifacts on the run. |
| s11 | “Try again” must return to a usable viewfinder | One real bug shows why we test behaviour. After a failed photo, Try again did nothing: retry called capture from a state where its guard returned immediately. The test fails capture, taps Try again, and expects the viewfinder and a fresh capture. It fails on the old source and passes with the fix. |
| T12 | 100 concurrent users stay under the 2-second target, error-free | All five stages passed: six thousand and thirty-eight requests, zero errors. At one hundred users p95 was one point three four seconds, with seventeen point eight requests per second. I return to capacity in the system demo. Now, the pipeline that runs all of these tests. |
| F8 | Reminder permission leads to an explicit weekly choice | [Press Space to start. Narrate over the clip; pause on the stated result. Playback begins muted. The allocated time includes nine seconds for the introduction and final hold.]

Open settings and choose the weekly reminder. The switch makes the preference explicit, and snooze lasts seven days. The weekly schedule is Sunday at seven in the evening in the group’s time zone. On iPhone, add Rewind to the Home Screen for web push. Pause on the saved preference, then continue to a completed capsule and its premiere. |
| F10 | The reveal turns sealed contributions into one shared film | [Press Space to start. Narrate over the clip; pause on the stated result. Playback begins muted. The allocated time includes nine seconds for the introduction and final hold.]

The film is now available to the group. Open the premiere and watch the contributions together. The player exposes moment segments and lets the viewer move between them. The output is a portrait film at seven-twenty by twelve-eighty, thirty frames per second, with normalised audio. Press M only if you want the film sound. Pause at the end screen. The film connects the sealed contribution habit to the shared payoff we described at the start. |

## CI/CD walk-through command cards

```sh
gh run view 40344231052 -R Collaboration95/rewind-app
gh api repos/Collaboration95/rewind-app/branches/dev/protection
gh run view 40344230832 -R Collaboration95/rewind-app
gh api repos/Collaboration95/rewind-app/actions/runs/40344230832/artifacts
gh attestation verify --repo Collaboration95/rewind-app release-manifest.json
```

Saved artifacts: `../pipeline-run-40344230832/security/` and `../pipeline-run-40344230832/zap/`. Hosted health: `https://d2m6kz76y4kuvm.cloudfront.net/api/health`.

## Source register

- Shared brief: scope, effort shares, delivery surface, five-section timing.
- Audits B1/B2: use cases, analysis, module mapping, design and patterns.
- Audit E: dated test inventory, coverage and red/green retry replay.
- records/TEAM.md and AGILE.md: team, effort, milestones, events and dated open register.
- records/FINDINGS.md: technical defects and repairs; later pipeline artifacts establish the delivered scan/deployment state.
- PIPELINE-ARTIFACTS.md and run 40344230832: exact-image inventory, manifest, scan and provenance flow.
- load-test/METHODOLOGY.md and RESULTS.md: hosted measurement, quiet-host run and fitted capacity projection.
