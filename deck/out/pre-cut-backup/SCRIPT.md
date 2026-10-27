# Rewind · full spoken script

SWE5006 Team 14 · Gopal Guruprasath · 27 October 2026, 14:30 SGT.

## Timing table

| Section | Start | End | Budget |
|---|---:|---:|---:|
| 1 · Intro and project management | 00:00 | 03:30 | 3:30 |
| 2 · Analysis, design and patterns | 03:30 | 08:30 | 5:00 |
| 3 · Testing | 08:30 | 11:30 | 3:00 |
| 4 · CI/CD demonstration | 11:30 | 22:40 | 11:10 |
| 5 · System demo and quality attributes | 22:40 | 37:10 | 14:30 |
| **Talk total** | **00:00** | **37:10** | **37:10** |

Five minutes of Q&A follow. The remaining 2:50 in the forty-minute slot absorb interruptions. Feature timings include playback, pauses and narration; the CI/CD slides include about 15 s per live GitHub page on C10–C15 and C18; the recorded walkthrough is backup CB1.

## Presentation controls

Arrow keys / A / D: change frame. N: notes. O: overview. F: fullscreen. B: blackout. Space / P: play/pause current clip. M: sound. R: restart. C: command cards. Z: full-size figure. Digits + Enter: jump to physical page. Hashes accept physical page numbers or named anchors such as #F5 and #B7. Click a feature video to pause at a question.

## Spoken delivery

### 1 · A month of moments. One film

00:00–00:15 · Section 1 · 00:15

Good afternoon. I am Gopal Guruprasath, presenting Rewind for SWE5006 Team 14. Rewind turns a month of everyday contributions into one private film for a small group. I will connect the product to our design, tests and delivery pipeline, then show the complete journey.

Transition: First, the problem and the product boundary.

If asked: → B10

### 2 · Everyday moments need a shared reason to return

00:15–01:10 · Section 1 · 00:55

Our business problem is simple: people already capture moments, but the moments disappear inside busy chats and camera rolls. A group has no common point at which to look back together. Rewind adds that point. Two to ten members contribute photos or short videos, and the contributions remain sealed until a twenty-eight-day cycle closes. Each member has five moments and thirty seconds per week. The limit keeps the contribution small enough to become a habit. At the end, the group receives one film and a twenty-four-hour premiere before the film remains in Archive. Our scope is the real-account web and PWA journey: identity, private groups, invitations, capture, chat, reminders and films. That is the boundary used in the design and in the demonstration.

Transition: The four sprints show how we delivered this boundary.

If asked: → B1 · → B10

### 3 · Four sprints delivered the hosted private-group journey

01:10–03:30 · Section 1 · 02:20

We used four sprints with zero-based names. Sprint zero built the runnable foundation. Sprint one integrated capture, the cycle and Archive. Sprint two established the real-account product, private media and hosted integration. Sprint three concentrated on stability, recovery and behavioural regression tests. The velocity chart counts issues closed inside each sprint window: forty-four, one hundred, one hundred and forty-five, then thirty. It is a delivery-count view. The backup has the event-replayed burndowns, including scope changes. For example, Sprint two grew from nine issues in scope to one hundred and thirty-five, while Sprint three ended with five open in its milestone. We retained that scope movement in the records.

Our team is Nguyen Kim Long, Gopal Guruprasath, Jiang Jiayu, Phan Mai Tan Loi and Sang Haoxiang. Effort is split equally at twenty percent each. The agreed plan is ten person-days per member. I coordinated the product and integration work; the team responsibilities span requirements, server integration, client experience and quality support.

Our Definition of Done is outcome checked in the cheapest environment that exercises it, fast tests passing, a green aggregate Quality check, and merge to dev. Overnight batches also get a review pass with blocking findings fixed. Project planning, Sprint Planning and Sprint Review were held. The useful retrospective chain is visible in the implementation: Sprint one exposed integration gaps, so Sprint two exercised real adapters; Sprint two exposed stale state and incomplete downloads, so Sprint three added whole-interaction and pagination checks.

The remaining open issues cover focused runner selection, emoji and calendar labels, the hosted Safari/PWA integration check, and report assembly. The complete seven-item delivery register is in the backup. We now move from the product boundary to the analysis models.

Transition: The use cases now give that scope a formal boundary.

If asked: → B10

### 4 · Fourteen use cases follow one private-group journey

03:30–03:58 · Section 2 · 00:28

The use case view starts with user goals. Members join a private group, contribute, chat and watch; the owner also manages membership and settings. The boundary makes the secondary systems explicit: identity, object storage, web push and scheduled time. For detailed design I follow CU-B: close the cycle, compile the film and release it, which joins UC07 and UC08.

Transition: The logical view shows where those responsibilities live.

If asked: → B1 · → B3

### 5 · One Node application keeps rules close to transactions

03:58–04:30 · Section 2 · 00:32

The main architecture decision is a modular monolith. Splitting membership, contributions and cycles into services would add coordination without helping this workflow; keeping the rules beside one transaction makes acceptance and cycle transitions easier to reason about. Hosted PostgreSQL holds durable relational state, private S3 holds media, and Cognito supplies web identity. Adapters keep those protocols out of the domain decisions.

Transition: Now map the analysis responsibilities onto that implementation.

If asked: → B4 · → B5 · → B9

### 6 · Analysis responsibilities become named implementation modules

04:30–05:08 · Section 2 · 00:38

The left side is analysis: a boundary receives interaction, a control coordinates the use case, and entities hold the state the business must retain. On the right we refine those responsibilities into real names. The scheduler finds work, lifecycle owns the cycle transition, compilation prepares and finalises the film, and the database keeps cycles, jobs and frozen inputs. A collection of functions is drawn as a module; a class symbol is reserved for a real class, so the model stays traceable to the code.

Transition: The hardest design problem is safely repeating this background work.

If asked: → B1 · → D1

### 7 · Durable claims keep repeated cycle work safe

05:08–05:56 · Section 2 · 00:48

A scheduler tick can repeat, and an old worker can finish after its lease expires. We compared polling alone, State or Command object hierarchies, and persisted state with a durable job. We chose the durable job with lease and generation checks: expensive rendering runs outside the transaction, then finalisation proves that this worker still owns the current claim. Storage creates a second design problem: duplicated backend branches would spread through the worker. Instead we inject the MediaStore Strategy. LocalMediaStore and PrivateS3MediaStore supply the implementations; the S3 transport Adapter translates the SDK operations. The pattern roles are labelled on the real design elements.

Transition: The sequence shows where those checks happen.

If asked: → D1 · → B7 · → B8 · → B9

### 8 · A repeated tick reuses work and fences stale completion

05:56–06:46 · Section 2 · 00:50

[Show closure here; jump to #B16 for compilation, then #B17 for publication; return to #s9. All three views share this 50-second allocation.]

The scheduler finds the ended cycle. One lifecycle transaction closes it, records the frozen inputs and durable film job, and opens its successor. The worker claims that job and renders outside the transaction. At finalisation it checks the current lease, generation and ordered input set. The alternatives explain the safety rule: a repeated tick reuses the retained job, and a stale worker cannot publish. Publication verifies the stored bytes before exposing the film. After the premiere, archiving verifies them again. The next schema shows which records preserve these decisions across a restart.

Transition: The schema explains what makes those decisions durable.

If asked: → B16 · → B17

### 9 · Keys preserve membership and the film’s exact input set

06:46–07:30 · Section 2 · 00:44

This is the database schema for the same use case. Membership relates an account to a group and its role, and every access decision uses it. A group has cycles; a cycle has contributions; media jobs retain processing state. Compilation inputs freeze exactly which media belongs to a film, so a retry cannot reinterpret a changing collection. Primary keys, foreign keys and uniqueness enforce those rules. We chose PostgreSQL because this path depends on joins and transactions across related records; the server suite runs on both SQLite and PostgreSQL. Before the screens, one more model: the cycle’s states.

Transition: The cycle statechart came before the screens.

If asked: → B4 · → B9

### 10 · The cycle’s states were fixed before any screen

07:30–07:55 · Section 2 · 00:25

Stored lifecycle state and durable jobs make work recoverable; a current lease and generation determine who may finalise.

Transition: Each screen then maps to one of these states.

If asked: → B16 · → B17

### 11 · Each screen renders one state of the cycle

07:55–08:30 · Section 2 · 00:35

[Click inside the page to step through a flow; Esc returns to the slides. If the page does not load, press S for the storyboards.]

The screens came second, and each one maps to a state. While the cycle is collecting, Home shows the countdown, the week and the member’s allowance, and capture is offered. When the cycle closes, Home shows the film developing. Once it is published, the premiere card opens the film for twenty-four hours, and after that the film lives in Archive. Every screen reads the server’s state instead of keeping its own, so a refresh or a second device always agrees.

Transition: Testing checks those states through their real boundaries.

If asked: → D1

### 12 · Twelve test types each catch a different failure

08:30–08:52 · Section 3 · 00:22

Here is the whole test map: twelve types, each catching a different kind of failure. The top six run on every pull request and block the merge. Browser, PWA and accessibility checks join for pull requests to main. The real-account journey and the load test run on demand. One slide on each.

Transition: Start at the bottom: static checks.

If asked: → B6

### 13 · Static checks reject style, type and layering errors

08:52–09:02 · Section 3 · 00:10

Static checks come first: Prettier, ESLint, TypeScript and our own layer rule. Domain code may not import a framework, and routes may not touch device APIs. They block every merge.

Transition: Next, the frontend unit tests.

If asked: → B6

### 14 · Component tests check screens and state without a device

09:02–09:16 · Section 3 · 00:14

The frontend has one thousand six hundred and seventy-four Jest tests. They render screens and drive state without a phone. Statement coverage is eighty-nine point six percent, with a seventy percent floor enforced in CI. This chat test fails if a session token ever appears in a request URL.

Transition: Here is one of those tests in detail.

If asked: → B6

### 15 · “Try again” must return to a usable viewfinder

09:16–09:34 · Section 3 · 00:18

One real bug shows why we test behaviour. After a failed photo, Try again did nothing: retry called capture from a state where its guard returned immediately. The test fails capture, taps Try again, and expects the viewfinder and a fresh capture. It fails on the old source and passes with the fix.

Transition: Next, the server and API tests.

If asked: → B3 · → B6

### 16 · API tests call real routes on a running server

09:34–09:48 · Section 3 · 00:14

The server suite has one thousand and six tests. Each starts the real HTTP server and calls real routes. This privacy test signs in as a member of another group and expects a 403 with no content for every protected resource.

Transition: The same suite then runs on PostgreSQL.

If asked: → B6

### 17 · The server suite runs again on PostgreSQL 17

09:48–09:58 · Section 3 · 00:10

The same suite runs again on PostgreSQL seventeen in a throwaway container: nine hundred and eighty-nine pass. That catches SQL that works on SQLite but not on the hosted database.

Transition: Repository rules guard the architecture itself.

If asked: → B9

### 18 · Repository tests stop the architecture and policies drifting

09:58–10:08 · Section 3 · 00:10

Repository tests check our own rules. The architecture guard is itself tested: we plant a bad import in each layer and expect two violations. Terraform and deploy policy, such as only deploying a commit that passed Quality, are tested the same way.

Transition: Deployment scripts get the same treatment.

If asked: → B6

### 19 · Deployment scripts are tested offline with injected failures

10:08–10:18 · Section 3 · 00:10

Deployment scripts are tested offline. Eleven fixtures replace tar, chown and the health check with fakes, then inject failures. A failed restore must leave the previous state intact.

Transition: Now the browser tests.

If asked: → B5

### 20 · Playwright drives the exported app in a real browser

10:18–10:32 · Section 3 · 00:14

Playwright drives the exported web app in Chromium at iPhone sizes: forty-one tests, required for pull requests to main. A longer Firefox journey uses real accounts: owner, invited member and outsider, through to the next cycle.

Transition: The exported PWA is checked as installed.

If asked: → B3

### 21 · The PWA build is checked the way it will be installed

10:32–10:42 · Section 3 · 00:10

The exported PWA is tested as it will be installed: manifest, service worker, offline page and icons. A service-worker rule test makes sure private media and API answers never enter the cache.

Transition: Accessibility uses the same browser run.

If asked: → B5

### 22 · Axe and keyboard tests check the main screens for WCAG 2.1 AA

10:42–10:52 · Section 3 · 00:10

Accessibility runs in the same browser job. Axe scans the main screens against WCAG 2.1 A and AA, and two keyboard tests check focus. Serious or critical violations fail the build.

Transition: Security is tested at two levels.

If asked: → B6

### 23 · Security is tested in the suites and scanned in the pipeline

10:52–11:04 · Section 3 · 00:12

Security is tested at two levels. Inside the suites: privacy denials, rate limits, our patched dependencies and the scan gates themselves. In the pipeline: SAST, SCA, secrets, IaC, image and DAST scans. I will show those in the CI/CD section.

Transition: Last, performance under load.

If asked: → B12

### 24 · A scripted load test drives the hosted API in five stages

11:04–11:18 · Section 3 · 00:14

Performance has its own test. A Node runner drives the hosted API through CloudFront in five stages, from one to one hundred concurrent users. Each user acts, then waits three to seven seconds. The mix is ninety-five percent reads. Every stage must keep p95 under two seconds and errors under one percent.

Transition: Here are the results.

If asked: → B11

### 25 · 100 concurrent users stay under the 2-second target, error-free

11:18–11:30 · Section 3 · 00:12

All five stages passed: six thousand and thirty-eight requests, zero errors. At one hundred users p95 was one point three four seconds, with seventeen point eight requests per second. I return to capacity in the system demo. Now, the pipeline that runs all of these tests.

Transition: Now the pipeline that runs these tests.

If asked: → B11 · → B34 · → B35

### 26 · One change passes four gates before it reaches hosted dev

11:30–12:25 · Section 4 · 00:55

This is the whole pipeline on one page; the next pages zoom into each band. A developer commits on an issue branch. Local git hooks run format, lint, architecture and typecheck, and GitHub push protection rejects known secret patterns at push time.

Band one is the pull request into dev. Quality checks is the only required check, so it is the merge gate. CodeQL, Gitleaks, Trivy and GitGuardian run beside it and report; their results are visible on the PR but do not block the merge.

Band two starts on the same push to dev. Deploy dev first waits for the Quality run on the merge commit, builds one release bundle, scans the exact images inside it, writes the SBOMs and manifest, signs provenance, and only then uploads. The host activates the release only if its health check passes; otherwise it restores the previous release.

Band three is hosted dev. After every deployment, OWASP ZAP scans the running site and reports. Promotion to main is a separate pull request with one human approval.

Transition: Before the detail, a quick key to the shapes and colours.

If asked: → C2 legend · → C3 source and artifacts

### 27 · Colour says what a failure blocks; shape says what the element is

12:25–12:55 · Section 4 · 00:30

Every pipeline page uses the same key. The colour and the first word of a box tell you what happens when it fails. Orange, BLOCKS MERGE: the required Quality check turns red and the pull request cannot merge. Blue, BLOCKS DEPLOY: the deploy stops before upload or before activation, and hosted dev keeps the release it already has. Purple: a platform rule or a human approval, such as push protection or the review on main. Dashed grey, REPORTS: the finding is recorded and visible, but it never stops a merge or a deployment.

Hexagons are decision points. A yes continues the flow; a no stops it. The yellow page shape is a retained artifact, a cylinder is a store, and a box with depth is a running host.

Transition: With that key, start with how source and results are managed.

If asked: → C3

### 28 · Protected branches carry source; every run leaves results we can inspect

12:55–13:45 · Section 4 · 00:50

Source management: work starts on an issue branch from the latest dev and enters dev only through a pull request. The dev rule requires the check named Format, lint, typecheck, and test, requires the branch to be up to date, requires conversations to be resolved, applies to administrators, and forbids force-pushes and deletion. Main has the same rule plus one approving review, including approval of the last push, and its Quality run adds the browser and PWA checks.

Artifact management: Git keeps source, the lockfile, workflows, Terraform and Dockerfiles permanently. Each workflow run keeps its machine-readable results as Actions artifacts named with the commit SHA: thirty days for JUnit, npm audit, SARIF, Trivy, IaC, SBOMs, the manifest and the release tar; fourteen days for coverage; ninety days for the ZAP reports. CodeQL and Gitleaks results go to the Security tab. Signed provenance sits in GitHub attestations. The host keeps only the current, previous and pending releases, so rollback always has a target.

Transition: Now zoom into the pull request band.

If asked: → CB2 branch protection settings

### 29 · The Quality workflow fans out nine jobs into one required merge check

13:45–14:30 · Section 4 · 00:45

This is quality.yml on a pull request. The first job classifies the change. If only Markdown documentation changed, every job is skipped and the gate passes in about twenty seconds. Otherwise eight lanes run in parallel: four static checks, the production dependency audit, root and IaC tests, server tests on SQLite with coverage, the same server suite on PostgreSQL 17, frontend Jest with a seventy percent statement threshold, and the deployment fixtures. Main-bound pull requests also run the web export, PWA and accessibility checks.

The last job, Format, lint, typecheck, and test, requires every lane to succeed. It is the one check named in branch protection, so a red lane means the merge button stays disabled.

Transition: Beside Quality, the security workflows run and report.

If asked: → C16 tests and coverage numbers

### 30 · Security workflows run beside Quality and keep their findings

14:30–15:05 · Section 4 · 00:35

Five security procedures run on the same pull request. CodeQL is our SAST. Gitleaks scans the full git history for secrets. Release security builds both images, writes a CycloneDX SBOM and fails on High or Critical vulnerabilities, and scans Terraform and Dockerfiles. GitGuardian and Dependabot add secret and dependency alerts.

These are reporting controls: they can turn their own job red, and the findings land in the Security tab or as artifacts, but they are not required checks. The vulnerability gate that does block is in the deployment, on the exact images we ship. That is the next page.

Transition: After merge, the same push starts Deploy dev.

If asked: → C9 catalogue

### 31 · Deploy scans and signs the exact bundle before anything is uploaded

15:05–15:50 · Section 4 · 00:45

The merge to dev starts Deploy dev. Its first gate polls the Quality run for this exact merge commit; if that run fails, the deploy refuses and the host is untouched. Then release.py builds one tar containing the runtime and web images and verifies it.

scan-release.py does not rebuild anything. It extracts the two image archives from that tar, runs Trivy to produce a CycloneDX SBOM and a JSON report for each, and checks that Trivy saw the same image IDs and a non-empty Alpine package list. Any High or Critical finding stops the job before upload. The SBOMs, reports and release manifest are kept even when the gate fails.

Finally attest-build-provenance signs the tar and the manifest, and the bundle is kept with its Sigstore attestation.

Transition: Only then does the runner touch AWS.

If asked: → C14 SBOM and provenance

### 32 · Keyless AWS access and a health check decide activation

15:50–16:25 · Section 4 · 00:35

GitHub has no AWS keys. The job exchanges its OIDC token for a one-hour role session, and the role trusts only this repository, the dev environment and refs/heads/dev. The runner checks the host is running, opens port 22 for its own address only with a short-lived key, ships the bundle and streams the hosted settings from a private S3 object.

On the host, the uploaded tar must match the built tar’s SHA-256. The installer starts the candidate images and activates them only when health is ready and the running image IDs match; otherwise it restores the previous release and the job turns red. Then the public health endpoint is checked, SSH is closed and the key deleted, and the DAST job starts.

Transition: The DAST job is the last stage.

If asked: → CB3 deploy job steps screenshot

### 33 · ZAP scans the running hosted site after every deploy

16:25–16:55 · Section 4 · 00:30

DAST runs as a second job that needs the deploy. It uses the OWASP ZAP baseline action: a spider and an AJAX spider crawl the single-page app for two minutes, and passive rules inspect every response. It is unauthenticated and sends no attacks, because hosted dev holds shared data. The rules file only ignores two noise rules, timestamps in the minified bundle and the “modern web application” note.

The job is report-only: fail_action is false, so findings never fail the run. It publishes a risk table in the run summary and keeps JSON, HTML and Markdown reports for ninety days. This run found zero High and four Medium findings, all about Content Security Policy.

Transition: That completes the pipeline. Here is everything it checks for, in one table.

If asked: → C15 DAST results

### 34 · Nine kinds of check, each with a recorded result and a link

16:55–17:35 · Section 4 · 00:40

This is the catalogue of what we check for. Each row is a procedure the course asks for, with its tool, its trigger, what a failure blocks, the real result for the commit we deployed, aea7478, and a link to the GitHub page that holds it.

Two rows block merges: the dependency audit and the tests, because both are inside Quality. Three block the deployment: the exact-bundle Trivy scan, a failed attestation step, and the health check. SAST, IaC, Gitleaks and DAST report. The next slides take one row each and show the real artifact behind it.

Transition: First row: SAST.

If asked: → C10–C16

### 35 · SAST: CodeQL findings are triaged with a written reason

17:35–18:10 · Section 4 · 00:35

SAST is CodeQL with the security-extended query suite on three languages: our TypeScript and JavaScript, the Python deployment scripts, and the workflow files themselves. It runs on every pull request, every push to dev and main, and weekly.

A real example: the load-test pull request, 592, raised three medium alerts in scripts/load/hosted.mjs, because the script sends fixture files over the network and writes the results to a path the operator chooses. We reviewed them and dismissed them as used in tests, with a written reason: it is an operator-run harness that never ships in the application image. The alert, the rule, the line and the reason stay on record. Today there are no open alerts.

Transition: Next, dependencies, where a real advisory blocked us.

If asked: → alert 56 page live

### 36 · SCA: a new zod advisory blocked merges until we fixed it

18:10–18:50 · Section 4 · 00:40

SCA is the production dependency audit, inside the required check. On 24 October, with no code change from us, a new advisory, GHSA-mrhx-c7xc-m3w5, marked zod below 4.6.6 as high severity: oversized collections can exhaust memory. Our copy came in through Expo’s CLI. Three high findings turned Quality red and two small pull requests could not merge. That is the gate working as designed.

npm suggested a forced, breaking Expo upgrade. Instead PR 591 added a scoped override so only Expo’s CLI uses zod 4.6.6. The retained npm-audit.json for the deployed commit shows zero vulnerabilities at every severity across 674 production dependencies. Dependabot adds alerts and security update pull requests; the one open alert is a development-only package.

Transition: Secrets next.

If asked: → C17 findings row 1

### 37 · Secrets are checked at push, on the PR and across history

18:50–19:20 · Section 4 · 00:30

Secrets are checked in three places. At push time, GitHub push protection rejects known provider key patterns before they reach the repository. On the pull request, GitGuardian scans the new commits. And the Secret scan workflow runs Gitleaks over the entire git history on every pull request and push, keeping a redacted SARIF report and sending it to the Security tab.

The default rules flagged migration identifiers and two test keys as generic API keys. Rather than silence the rule, the allowlist requires the exact file and the exact value, so a real key in the same file would still be found. The current result is zero findings.

Transition: Containers and infrastructure.

If asked: → C17 findings

### 38 · Trivy blocks risky images; IaC risks need dated exceptions

19:20–19:55 · Section 4 · 00:35

Trivy scans our two container images twice. Release security scans candidate images on pull requests and pushes. The deployment then scans the images inside the exact bundle it will upload, and that second scan is the one that blocks: any High or Critical stops the upload. For this deployment both images had zero High and Critical. The runtime image has one Medium in zlib with a fix available, and two Unknown entries in musl.

For infrastructure as code, Trivy config scans Terraform and Dockerfiles. It found fifteen issues: seven Low and eight High. Every High must match exactly one exception with an owner, a reason and an expiry date. Most are about customer-managed KMS keys and a WAF that would add cost. The exceptions expire on 31 October, and after that the job fails until each risk is reviewed again.

Transition: The image scan feeds the SBOM and provenance.

If asked: → C14

### 39 · SBOM and provenance bind shipped bytes to scans and workflow

19:55–20:35 · Section 4 · 00:40

The SBOM is a CycloneDX inventory of each exact bundled image: 187 components in the runtime image, including the FFmpeg package we had to re-pin, and 72 in the web image. The release manifest records the commit, the run, the Quality run that allowed it, both image IDs and digests, the severity counts, and the SHA-256 of the tar, both SBOMs and both reports. So inventory, findings and bytes are bound together.

Provenance: the deploy job signs the tar and the manifest with GitHub’s attest-build-provenance, using Sigstore and the job’s own OIDC identity. Anyone can check it: gh attestation verify on the downloaded manifest succeeds and names deploy-dev.yml on refs/heads/dev as the workflow that built it.

Transition: The last security procedure looks at the running site.

If asked: → C6

### 40 · DAST: 0 High, 4 Medium, all from one Content Security Policy gap

20:35–21:15 · Section 4 · 00:40

Here are the real ZAP results for the deployed commit: zero High, four Medium, seven Low and six informational alert types. All four Medium alerts are Content Security Policy findings.

Take the first one. ZAP sent a GET to the hosted home page, robots.txt and sitemap.xml, read the Content-Security-Policy header, and found only frame-ancestors none. Directives such as form-action do not fall back to default-src, so they are effectively unrestricted. The informational alert explains why: our full policy is served as Content-Security-Policy-Report-Only, so browsers report violations but do not enforce them. The fix is to promote that policy to enforced once its reports are clean. The Low findings are missing hardening headers and the nginx version string.

Transition: Tests and coverage complete the catalogue.

If asked: → open the HTML report

### 41 · Tests and coverage gate the merge and are kept as artifacts

21:15–21:35 · Section 4 · 00:20

Tests are part of the same gate. On the filmed pull request run, root tests passed 123, the server suite passed 985 with 85.5 percent line coverage, and the frontend passed 1,674 with 89.6 percent statement coverage against a seventy percent threshold. The server suite also runs on PostgreSQL 17, the hosted engine. Every lane keeps JUnit, Jest JSON or coverage JSON as artifacts on the run.

Transition: What did the pipeline teach us?

If asked: → C4

### 42 · The pipeline caught problems that source-level tests could not

21:35–22:20 · Section 4 · 00:45

Six technical findings. First, on 24 October a new zod advisory turned the audit red with no change from us, and the gate blocked two pull requests until PR 591 fixed it. Second, the same week Alpine removed the FFmpeg version we pinned, so the runtime image stopped building; we re-pinned to the available version.

Third, an audit of our own pipeline found that the image we scanned was not the image we deployed, because deployment rebuilt it. PR 595 moved the gate onto the exact bundle and added the manifest and attestation. Fourth, Gitleaks’ default rules reported twenty-seven false positives in history; we allowlisted exact values, not whole files.

Fifth, a refactor moved the schema registry while packaging still read the old path; bundle verification caught it before the host was touched. Sixth, Cognito code passed its tests but its runtime dependencies were missing from the built image. The lesson is to verify what ships, not just the source.

Transition: Now the live route through GitHub.

If asked: → B31 product findings

### 43 · Demo route: eight clicks from pull request to running site

22:20–22:40 · Section 4 · 00:20

This is the click route for the live part. Each link opens the real page; the Film column gives the timestamp in the recorded walkthrough if the network fails. The order follows the pipeline: pull request checks, the Quality run and its artifacts, a triaged CodeQL alert, the Deploy dev run, its steps, the attestation, the ZAP report, and finally the hosted health endpoint. Keep each page to about fifteen seconds.

Transition: Close the CI/CD section and move to the system demonstration.

If asked: → CB1 recorded film

### 44 · A private-group journey runs from prompt to film

22:40–22:58 · Section 5 · 00:18

Our two members have their accounts ready. Start with the group and its shared prompt. Then invite, contribute, chat and choose a reminder. Finally open the completed film, save it, and test the outsider boundary. Each feature has its own controlled clip.

Transition: Create the group and choose its shared prompt.

If asked: → B1 · → B3

### F3 · A shared prompt gives the group a common starting point

22:58–24:07 · Section 5 · 01:09

[Press Space to start. Narrate over the clip; pause on the stated result. Playback begins muted. The allocated time includes nine seconds for the introduction and final hold.]

The owner creates a group and chooses a shared prompt. The prompt gives contributions a common theme without prescribing what each person must record. The group size is bounded, and its settings retain the prompt and time zone. Point to the new group name and the prompt on Home, then to the owner settings. We now need another member.

Transition: Invite a friend with a single-use code.

If asked: → B1

### F4 · One accepted invitation creates one private membership

24:07–25:16 · Section 5 · 01:09

[Press Space to start. Narrate over the clip; pause on the stated result. Playback begins muted. The allocated time includes nine seconds for the introduction and final hold.]

The owner creates an invitation and shares the code. It works once and expires after twenty-four hours. Our friend accepts it from the prepared account. Watch the member list change and the shared group appear for both accounts. Acceptance is a server decision: a valid code and authenticated account produce a durable membership. Reusing the code later will not add another member. Keep that rule in mind for the final outsider check.

Transition: The first contribution is a photo.

If asked: → B3

### F5 · A submitted photo becomes a sealed moment

25:16–26:20 · Section 5 · 01:04

[Press Space to start. Narrate over the clip; pause on the stated result. Playback begins muted. The allocated time includes nine seconds for the introduction and final hold.]

Take a photo and choose a look before submitting it. The user can review the contribution, but after acceptance it becomes sealed. Your moments retains the entry and allowance information without opening everyone’s submitted content early. A photo counts as one moment and becomes a three-second segment in the film. Watch the state change from capture to a retained sealed entry.

Transition: Video shares the same weekly allowance.

If asked: → B3

### F6 · Video and photos share one enforced weekly allowance

26:20–27:34 · Section 5 · 01:14

[Press Space to start. Narrate over the clip; pause on the stated result. Playback begins muted. The allocated time includes nine seconds for the introduction and final hold.]

Record a video, review the trim and submit it. A video can use up to fifteen seconds, and the total weekly allowance is shared with photos: five moments and thirty seconds per member. The visible ledger matters because the user needs to know what remains before trying another capture. The server checks the accepted contribution and media rather than trusting only the client display. Pause at the updated counts. The contribution is now part of the same sealed collection as the photo.

Transition: The group can talk while the moments stay sealed.

If asked: → B3

### F7 · Stored messages and live updates keep the group connected

27:34–28:38 · Section 5 · 01:04

[Press Space to start. Narrate over the clip; pause on the stated result. Playback begins muted. The allocated time includes nine seconds for the introduction and final hold.]

One member sends a message and the other sees it without refreshing. Replies and reactions remain in the shared conversation. The design combines stored messages with live SSE delivery and reconnect, so the live notification is not the only record of the message. This is where the Observer design in backup B8 becomes visible to a user.

Transition: Next, opt into the weekly reminder.

If asked: → B8

### F8 · Reminder permission leads to an explicit weekly choice

28:38–29:37 · Section 5 · 00:59

[Press Space to start. Narrate over the clip; pause on the stated result. Playback begins muted. The allocated time includes nine seconds for the introduction and final hold.]

Open settings and choose the weekly reminder. The switch makes the preference explicit, and snooze lasts seven days. The weekly schedule is Sunday at seven in the evening in the group’s time zone. On iPhone, add Rewind to the Home Screen for web push. Pause on the saved preference, then continue to a completed capsule and its premiere.

Transition: Now open the completed capsule and its premiere.

If asked: → B5

### F9 · The completed capsule is ready for its shared premiere

29:37–30:26 · Section 5 · 00:49

[Press Space to start. Narrate over the clip; pause on the stated result. Playback begins muted. The allocated time includes nine seconds for the introduction and final hold.]

Switch to The little things, a completed capsule from Maya and Jun. Its premiere card opens the shared film. Behind this result, the scheduler closes the ended cycle, queues durable compilation work and opens the successor. That is the CU-B path from the design section. Pause on the ready state, then continue to the film.

Transition: Open the group’s film.

If asked: → D1

### F10 · The reveal turns sealed contributions into one shared film

30:26–31:55 · Section 5 · 01:29

[Press Space to start. Narrate over the clip; pause on the stated result. Playback begins muted. The allocated time includes nine seconds for the introduction and final hold.]

The film is now available to the group. Open the premiere and watch the contributions together. The player exposes moment segments and lets the viewer move between them. The output is a portrait film at seven-twenty by twelve-eighty, thirty frames per second, with normalised audio. Press M only if you want the film sound. Pause at the end screen. The film connects the sealed contribution habit to the shared payoff we described at the start.

Transition: Archive keeps the film and offers saving.

If asked: → D1

### F11 · Archive keeps the film available after its premiere

31:55–32:59 · Section 5 · 01:04

[Press Space to start. Narrate over the clip; pause on the stated result. Playback begins muted. The allocated time includes nine seconds for the introduction and final hold.]

After the premiere, the film remains in Archive. Open the retained film, choose Save film and open the downloaded MP4. The end screen also lets a member save their own moments. This completes the journey from capture to a durable output the member can keep. Pause on the playable downloaded result. The final check uses a different account that has no membership.

Transition: Check the outsider boundary.

If asked: → B4

### F12 · A spent invitation gives an outsider no group access

32:59–33:58 · Section 5 · 00:59

[Press Space to start. Narrate over the clip; pause on the stated result. Playback begins muted. The allocated time includes nine seconds for the introduction and final hold.]

From the outsider’s prepared account, try the invitation already used by our friend. The app rejects it as already used. The group does not appear in the outsider’s list. This is the negative branch of the invitation rule shown earlier. The server tests also exercise direct group, budget, chat and media access with missing or wrong membership. The user demonstration and those API checks address the same privacy boundary at different layers. We have now completed the group journey.

Transition: Finish with the hosted load results and the scaling mechanism.

If asked: → B6

### 45 · The capacity model shows where to scale next

33:58–37:10 · Section 5 · 03:12

[00:00–00:30: recall the measured result from the testing section.]
In testing we saw the measured result on hosted dev: one hundred concurrent users, p95 one point three four seconds, seventeen point eight four requests per second and zero errors across six thousand and thirty-eight requests. That is the performance quality attribute. Scalability asks what happens beyond that.

[00:30–01:30: follow the one-host and two-host projected curves.]
The curves fit a closed-user model to the measured means at ten through one hundred users. The fitted serialized service demand is forty-five point four milliseconds per request, with a fixed delay of three hundred and seventy-eight milliseconds and five seconds of think time. One API host approaches about twenty-two requests per second, with a knee near one hundred and sixteen active users. At two hundred and fifty users the projected mean is six point four seconds on one host and one point one seconds with two balanced hosts. The curves are means; the measured table in testing gave p95.

[01:30–02:30: explain the mechanism behind the scale-out choices.]
The PostgreSQL adapter waits synchronously around one client, so part of the API path serializes. The media worker also shares host CPU with requests. Separate media processing first, then make persistence asynchronous with a bounded connection pool. A second API host also needs coordinated capability state, staged media and scheduler ownership. Sessions already live in PostgreSQL, and PostgreSQL and S3 stay shared. The shared writer lock means adding a host improves read concurrency more than shared write throughput.

[02:30–03:12: connect maintainability to the pipeline, then invite questions.]
The pipeline we followed checks those changes through behavioural tests, both database dialects, built-image verification, exact-image security, signed provenance and candidate health. That is the maintainability strategy: improve the internal mechanism while preserving the observed product behaviour. We have connected the group journey to its design, checks and delivery evidence. Thank you; I am ready for questions.

Transition: We can take questions using the backup map.

If asked: → B6 · → B11 · → B12

## Q&A backup map

| Backup | Question | Spoken answer |
|---|---|---|
| B1 | Analysis separates interaction, coordination and state | The analysis model separates the interaction boundary, use-case coordination and durable business state; main frame six maps those responsibilities to code. |
| B3 | Capture acceptance checks identity, allowance and media | The capture sequence follows reservation, media validation and acceptance, keeping membership and allowance decisions on the server. |
| B4 | Relational keys make the private film traceable | The relational choice follows transaction and consistency needs across membership, cycles, contributions and the frozen film input set. |
| B5 | The deployment view names each runtime boundary | CloudFront and nginx form the entry, Node runs the application, and PostgreSQL, S3 and Cognito provide the durable data and identity services. |
| B6 | Coverage and enforcement answer different questions | The statement floor is a regression safety net. Coverage reports identify branches to investigate, while behavioural tests assert the outcomes that matter. |
| B7 | Storage changes behind Strategy and Adapter roles | The problem is duplicated storage-specific branches in compilation and media code. We compared branching in each caller with an injected storage contract. We chose the MediaStore Strategy so the worker uses one interface. LocalMediaStore and PrivateS3MediaStore implement that contract, and privateTransport adapts AWS SDK commands. Hosted runtime selects PrivateS3MediaStore; disk mode has its separate filesystem path. |
| B8 | Observer distributes chat updates alongside stored history | RealtimeHub acts as the live update subject and subscribers receive events, while stored messages provide the durable history and reconnect path. |
| B9 | The persistence adapter preserves a common data-access contract | PostgresDatabase adapts the common call contract to PostgreSQL; centralising that translation also makes the synchronous bridge a clear target for performance work. |
| B10 | Agile records retain scope changes and equal effort | The burndowns retain scope change and reopen events. Effort is the agreed twenty-percent split: ten person-days each. The open delivery register is #230, #362, #504, #515, #527, #587 and #588. |
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
| B21 | Sprint 0 records opening scope and daily delivery | Use the opening snapshot and daily boundaries to follow scope and remaining issues in Sprint 0. |
| B22 | Sprint 1 records opening scope and daily delivery | Use the opening snapshot and daily boundaries to follow scope and remaining issues in Sprint 1. |
| B23 | Sprint 2 records opening scope and daily delivery | Use the opening snapshot and daily boundaries to follow scope and remaining issues in Sprint 2. |
| B24 | Issue closures and merged PRs track sprint delivery | The chart counts issue closures and merged PRs within each SGT sprint window. |
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
| B34 | Every steady load stage stays below the latency target | The measured p50, p95 and p99 curves cover one through one hundred virtual users. All p95 stages stay below two seconds; the 100-user p95 is 1,335.9 milliseconds. |
| B35 | Measured throughput rises with the active user count | The measured 100-user throughput is 17.84 requests per second, with zero errors. Each point uses its own three-minute steady window. |
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

- Shared brief: scope, equal effort, delivery surface, five-section timing.
- Audits B1/B2: use cases, analysis, module mapping, design and patterns.
- Audit E: dated test inventory, coverage and red/green retry replay.
- records/TEAM.md and AGILE.md: team, effort, milestones, events and dated open register.
- records/FINDINGS.md: technical defects and repairs; later pipeline artifacts establish the delivered scan/deployment state.
- PIPELINE-ARTIFACTS.md and run 40344230832: exact-image inventory, manifest, scan and provenance flow.
- load-test/METHODOLOGY.md and RESULTS.md: hosted measurement, quiet-host run and fitted capacity projection.
