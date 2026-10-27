# Rewind · full spoken script

SWE5006 Team 14 · Gopal Guruprasath · 27 October 2026, 14:30 SGT.

## Timing table

| Section | Start | End | Budget |
|---|---:|---:|---:|
| 1 · Intro and project management | 00:00 | 03:30 | 3:30 |
| 2 · Analysis, design and patterns | 03:30 | 08:30 | 5:00 |
| 3 · Testing | 08:30 | 11:30 | 3:00 |
| 4 · CI/CD demonstration | 11:30 | 23:30 | 12:00 |
| 5 · System demo and quality attributes | 23:30 | 38:00 | 14:30 |
| **Talk total** | **00:00** | **38:00** | **38:00** |

Five minutes of Q&A follow. The remaining two minutes in the forty-minute slot absorb interruptions. Feature timings include playback, pauses and narration; the CI/CD frame includes the timed inspection actions.

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

03:30–04:03 · Section 2 · 00:33

The use case view starts with user goals rather than code. A member joins a private group, contributes, chats and watches; the owner also manages membership and settings. The boundary makes the secondary systems explicit: identity, object storage, web push and scheduled time. For detailed design I will follow CU-B: close the cycle, compile the film and release it. That path connects UC07 and UC08 and crosses persistence, background work and media processing.

Transition: The logical view shows where those responsibilities live.

If asked: → B1 · → B3

### 5 · One Node application keeps rules close to transactions

04:03–04:42 · Section 2 · 00:39

The principal architecture decision is a modular monolith. The application is small enough that splitting membership, contributions and cycles into separate services would add coordination without improving this workflow. Keeping the rules near a transaction makes acceptance and cycle transitions easier to reason about. Hosted PostgreSQL gives us durable relational state, while private S3 objects carry the media. Cognito supplies the web identity flow. Adapters keep those external protocols outside the domain decisions. This logical view shows responsibilities and dependencies; the deployment view later will show where these elements run.

Transition: Now map the analysis responsibilities onto that implementation.

If asked: → B4 · → B5 · → B9

### 6 · Analysis responsibilities become named implementation modules

04:42–05:27 · Section 2 · 00:45

The left side of this mapping is analysis. A boundary receives interaction, a control coordinates the use case, and entities represent the state the business needs to retain. Those are responsibilities. On the right, we refine them into implementation names. The scheduler finds work, lifecycle owns the cycle transition, compilation prepares and finalises the film, and the database retains cycles, jobs and frozen inputs. The analysis classes remain available in backup B1. In the design diagrams, a collection of functions is shown as a module. A class symbol is reserved for an actual class. That keeps the model traceable to the code a maintainer will open.

Transition: The hardest design problem is safely repeating this background work.

If asked: → B1 · → B2

### 7 · Durable claims keep repeated cycle work safe

05:27–06:21 · Section 2 · 00:54

A scheduler tick can repeat, and an old worker can finish after its lease expires. We compared polling alone, State or Command object hierarchies, and persisted state with a durable job. We chose the durable job with lease and generation checks: expensive rendering runs outside the transaction, then finalisation proves that this worker still owns the current claim. Storage creates a second design problem: duplicated backend branches would spread through the worker. Instead we inject the MediaStore Strategy. LocalMediaStore and PrivateS3MediaStore supply the implementations; the S3 transport Adapter translates the SDK operations. The pattern roles are labelled on the real design elements.

Transition: The sequence shows where those checks happen.

If asked: → B2 · → B7 · → B8 · → B9

### 8 · A repeated tick reuses work and fences stale completion

06:21–07:18 · Section 2 · 00:57

[Show closure here; jump to #B16 for compilation, then #B17 for publication; return to #s9. All three views share this 57-second allocation.]

The scheduler finds the ended cycle. One lifecycle transaction closes it, records the frozen inputs and durable film job, and opens its successor. The worker claims that job and renders outside the transaction. At finalisation it checks the current lease, generation and ordered input set. The alternatives explain the safety rule: a repeated tick reuses the retained job, and a stale worker cannot publish. Publication verifies the stored bytes before exposing the film. After the premiere, archiving verifies them again. The next schema shows which records preserve these decisions across a restart.

Transition: The schema explains what makes those decisions durable.

If asked: → B16 · → B17

### 9 · Keys preserve membership and the film’s exact input set

07:18–08:30 · Section 2 · 01:12

This is the database schema for the same use case, with the access relationships alongside it. Start at the group and membership relation. It answers who belongs to the group and in which role. A group has cycles; a cycle has contributions; the processing jobs retain what must happen to the media. The compilation-input relation is especially useful: it fixes the inputs associated with the film job, so later retry does not silently reinterpret a changing collection. Primary keys identify the durable records, foreign keys connect them, and uniqueness expresses rules such as one relevant membership or job identity.

We chose a relational store because this path depends on joins, consistency and transaction boundaries across related records. Hosted PostgreSQL also gives us managed backups. The code retains a local SQLite path, and the server suite runs across both dialects. For this explanation the important point is that privacy, lifecycle and recovery are stored relationships. The next section shows the tests that exercise those relationships through APIs and user actions.

Transition: Tests exercise those rules through their real boundaries.

If asked: → B4 · → B9

### 10 · Twelve test types each catch a different failure

08:30–08:52 · Section 3 · 00:22

Here is the whole test map: twelve types, each catching a different kind of failure. The top six run on every pull request and block the merge. Browser, PWA and accessibility checks join for pull requests to main. The real-account journey and the load test run on demand. One slide on each.

Transition: Start at the bottom: static checks.

If asked: → B6

### 11 · Static checks reject style, type and layering errors

08:52–09:02 · Section 3 · 00:10

Static checks come first: Prettier, ESLint, TypeScript and our own layer rule. Domain code may not import a framework, and routes may not touch device APIs. They block every merge.

Transition: Next, the frontend unit tests.

If asked: → B6

### 12 · Component tests check screens and state without a device

09:02–09:16 · Section 3 · 00:14

The frontend has one thousand six hundred and seventy-four Jest tests. They render screens and drive state without a phone. Statement coverage is eighty-nine point six percent, with a seventy percent floor enforced in CI. This chat test fails if a session token ever appears in a request URL.

Transition: Here is one of those tests in detail.

If asked: → B6

### 13 · “Try again” must return to a usable viewfinder

09:16–09:34 · Section 3 · 00:18

One real bug shows why we test behaviour. After a failed photo, Try again did nothing: retry called capture from a state where its guard returned immediately. The test fails capture, taps Try again, and expects the viewfinder and a fresh capture. It fails on the old source and passes with the fix.

Transition: Next, the server and API tests.

If asked: → B3 · → B6

### 14 · API tests call real routes on a running server

09:34–09:48 · Section 3 · 00:14

The server suite has one thousand and six tests. Each starts the real HTTP server and calls real routes. This privacy test signs in as a member of another group and expects a 403 with no content for every protected resource.

Transition: The same suite then runs on PostgreSQL.

If asked: → B6

### 15 · The server suite runs again on PostgreSQL 17

09:48–09:58 · Section 3 · 00:10

The same suite runs again on PostgreSQL seventeen in a throwaway container: nine hundred and eighty-nine pass. That catches SQL that works on SQLite but not on the hosted database.

Transition: Repository rules guard the architecture itself.

If asked: → B9

### 16 · Repository tests stop the architecture and policies drifting

09:58–10:08 · Section 3 · 00:10

Repository tests check our own rules. The architecture guard is itself tested: we plant a bad import in each layer and expect two violations. Terraform and deploy policy, such as only deploying a commit that passed Quality, are tested the same way.

Transition: Deployment scripts get the same treatment.

If asked: → B6

### 17 · Deployment scripts are tested offline with injected failures

10:08–10:18 · Section 3 · 00:10

Deployment scripts are tested offline. Eleven fixtures replace tar, chown and the health check with fakes, then inject failures. A failed restore must leave the previous state intact.

Transition: Now the browser tests.

If asked: → B5

### 18 · Playwright drives the exported app in a real browser

10:18–10:32 · Section 3 · 00:14

Playwright drives the exported web app in Chromium at iPhone sizes: forty-one tests, required for pull requests to main. A longer Firefox journey uses real accounts: owner, invited member and outsider, through to the next cycle.

Transition: The exported PWA is checked as installed.

If asked: → B3

### 19 · The PWA build is checked the way it will be installed

10:32–10:42 · Section 3 · 00:10

The exported PWA is tested as it will be installed: manifest, service worker, offline page and icons. A service-worker rule test makes sure private media and API answers never enter the cache.

Transition: Accessibility uses the same browser run.

If asked: → B5

### 20 · Axe and keyboard tests check the main screens for WCAG 2.1 AA

10:42–10:52 · Section 3 · 00:10

Accessibility runs in the same browser job. Axe scans the main screens against WCAG 2.1 A and AA, and two keyboard tests check focus. Serious or critical violations fail the build.

Transition: Security is tested at two levels.

If asked: → B6

### 21 · Security is tested in the suites and scanned in the pipeline

10:52–11:04 · Section 3 · 00:12

Security is tested at two levels. Inside the suites: privacy denials, rate limits, our patched dependencies and the scan gates themselves. In the pipeline: SAST, SCA, secrets, IaC, image and DAST scans. I will show those in the CI/CD section.

Transition: Last, performance under load.

If asked: → B12

### 22 · A scripted load test drives the hosted API in five stages

11:04–11:18 · Section 3 · 00:14

Performance has its own test. A Node runner drives the hosted API through CloudFront in five stages, from one to one hundred concurrent users. Each user acts, then waits three to seven seconds. The mix is ninety-five percent reads. Every stage must keep p95 under two seconds and errors under one percent.

Transition: Here are the results.

If asked: → B11

### 23 · 100 concurrent users stay under the 2-second target, error-free

11:18–11:30 · Section 3 · 00:12

All five stages passed: six thousand and thirty-eight requests, zero errors. At one hundred users p95 was one point three four seconds, with seventeen point eight requests per second. I return to capacity in the system demo. Now, the pipeline that runs all of these tests.

Transition: Now the pipeline that runs these tests.

If asked: → B11 · → B34 · → B35

### 24 · The pipeline connects protected source to a verified deployment

11:30–23:30 · Section 4 · 12:00

[00:00–00:20 section clock: introduce the recording, then press Space. Narrate the following cues over the 11:26 film. Its clip clock starts at zero.]

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
Quality controls integration, the exact-image scan controls upload, and candidate health controls activation. CodeQL, IaC, secrets and ZAP retain their findings for review. Those retained artifacts make the next internal change inspectable. Now follow the product journey.

Transition: Start the group journey with accounts ready.

If asked: → B26 · → B27 · → B28 · → B29 · → B30 · → B31 · → B12

### 25 · A private-group journey runs from prompt to film

23:30–23:48 · Section 5 · 00:18

Our two members have their accounts ready. Start with the group and its shared prompt. Then invite, contribute, chat and choose a reminder. Finally open the completed film, save it, and test the outsider boundary. Each feature has its own controlled clip.

Transition: Create the group and choose its shared prompt.

If asked: → B1 · → B3

### F3 · A shared prompt gives the group a common starting point

23:48–24:57 · Section 5 · 01:09

[Press Space to start. Narrate over the clip; pause on the stated result. Playback begins muted. The allocated time includes nine seconds for the introduction and final hold.]

The owner creates a group and chooses a shared prompt. The prompt gives contributions a common theme without prescribing what each person must record. The group size is bounded, and its settings retain the prompt and time zone. Point to the new group name and the prompt on Home, then to the owner settings. We now need another member.

Transition: Invite a friend with a single-use code.

If asked: → B1

### F4 · One accepted invitation creates one private membership

24:57–26:06 · Section 5 · 01:09

[Press Space to start. Narrate over the clip; pause on the stated result. Playback begins muted. The allocated time includes nine seconds for the introduction and final hold.]

The owner creates an invitation and shares the code. It works once and expires after twenty-four hours. Our friend accepts it from the prepared account. Watch the member list change and the shared group appear for both accounts. Acceptance is a server decision: a valid code and authenticated account produce a durable membership. Reusing the code later will not add another member. Keep that rule in mind for the final outsider check.

Transition: The first contribution is a photo.

If asked: → B3

### F5 · A submitted photo becomes a sealed moment

26:06–27:10 · Section 5 · 01:04

[Press Space to start. Narrate over the clip; pause on the stated result. Playback begins muted. The allocated time includes nine seconds for the introduction and final hold.]

Take a photo and choose a look before submitting it. The user can review the contribution, but after acceptance it becomes sealed. Your moments retains the entry and allowance information without opening everyone’s submitted content early. A photo counts as one moment and becomes a three-second segment in the film. Watch the state change from capture to a retained sealed entry.

Transition: Video shares the same weekly allowance.

If asked: → B3

### F6 · Video and photos share one enforced weekly allowance

27:10–28:24 · Section 5 · 01:14

[Press Space to start. Narrate over the clip; pause on the stated result. Playback begins muted. The allocated time includes nine seconds for the introduction and final hold.]

Record a video, review the trim and submit it. A video can use up to fifteen seconds, and the total weekly allowance is shared with photos: five moments and thirty seconds per member. The visible ledger matters because the user needs to know what remains before trying another capture. The server checks the accepted contribution and media rather than trusting only the client display. Pause at the updated counts. The contribution is now part of the same sealed collection as the photo.

Transition: The group can talk while the moments stay sealed.

If asked: → B3

### F7 · Stored messages and live updates keep the group connected

28:24–29:28 · Section 5 · 01:04

[Press Space to start. Narrate over the clip; pause on the stated result. Playback begins muted. The allocated time includes nine seconds for the introduction and final hold.]

One member sends a message and the other sees it without refreshing. Replies and reactions remain in the shared conversation. The design combines stored messages with live SSE delivery and reconnect, so the live notification is not the only record of the message. This is where the Observer design in backup B8 becomes visible to a user.

Transition: Next, opt into the weekly reminder.

If asked: → B8

### F8 · Reminder permission leads to an explicit weekly choice

29:28–30:27 · Section 5 · 00:59

[Press Space to start. Narrate over the clip; pause on the stated result. Playback begins muted. The allocated time includes nine seconds for the introduction and final hold.]

Open settings and choose the weekly reminder. The switch makes the preference explicit, and snooze lasts seven days. The weekly schedule is Sunday at seven in the evening in the group’s time zone. On iPhone, add Rewind to the Home Screen for web push. Pause on the saved preference, then continue to a completed capsule and its premiere.

Transition: Now open the completed capsule and its premiere.

If asked: → B5

### F9 · The completed capsule is ready for its shared premiere

30:27–31:16 · Section 5 · 00:49

[Press Space to start. Narrate over the clip; pause on the stated result. Playback begins muted. The allocated time includes nine seconds for the introduction and final hold.]

Switch to The little things, a completed capsule from Maya and Jun. Its premiere card opens the shared film. Behind this result, the scheduler closes the ended cycle, queues durable compilation work and opens the successor. That is the CU-B path from the design section. Pause on the ready state, then continue to the film.

Transition: Open the group’s film.

If asked: → B2

### F10 · The reveal turns sealed contributions into one shared film

31:16–32:45 · Section 5 · 01:29

[Press Space to start. Narrate over the clip; pause on the stated result. Playback begins muted. The allocated time includes nine seconds for the introduction and final hold.]

The film is now available to the group. Open the premiere and watch the contributions together. The player exposes moment segments and lets the viewer move between them. The output is a portrait film at seven-twenty by twelve-eighty, thirty frames per second, with normalised audio. Press M only if you want the film sound. Pause at the end screen. The film connects the sealed contribution habit to the shared payoff we described at the start.

Transition: Archive keeps the film and offers saving.

If asked: → B2

### F11 · Archive keeps the film available after its premiere

32:45–33:49 · Section 5 · 01:04

[Press Space to start. Narrate over the clip; pause on the stated result. Playback begins muted. The allocated time includes nine seconds for the introduction and final hold.]

After the premiere, the film remains in Archive. Open the retained film, choose Save film and open the downloaded MP4. The end screen also lets a member save their own moments. This completes the journey from capture to a durable output the member can keep. Pause on the playable downloaded result. The final check uses a different account that has no membership.

Transition: Check the outsider boundary.

If asked: → B4

### F12 · A spent invitation gives an outsider no group access

33:49–34:48 · Section 5 · 00:59

[Press Space to start. Narrate over the clip; pause on the stated result. Playback begins muted. The allocated time includes nine seconds for the introduction and final hold.]

From the outsider’s prepared account, try the invitation already used by our friend. The app rejects it as already used. The group does not appear in the outsider’s list. This is the negative branch of the invitation rule shown earlier. The server tests also exercise direct group, budget, chat and media access with missing or wrong membership. The user demonstration and those API checks address the same privacy boundary at different layers. We have now completed the group journey.

Transition: Finish with the hosted load results and the scaling mechanism.

If asked: → B6

### 26 · The capacity model shows where to scale next

34:48–38:00 · Section 5 · 03:12

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
| B2 | Durable state survives interrupted compilation | Stored lifecycle state and durable jobs make work recoverable; a current lease and generation determine who may finalise. |
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
| B28 | Security checks cover code, packages, secrets and running pages | SAST is CodeQL across JavaScript and TypeScript, Python and Actions. Tonight the three load-script alerts were triaged as used in tests. That is a written disposition attached to those alerts. The DAST lane now runs a ZAP baseline against hosted dev. The saved report for this deployment has zero High, four Medium, seven Low and six Informational findings. The Medium findings concern Content Security Policy. The HTML report gives the alert, affected URL, evidence and remediation text.

SCA combines the production npm audit gate with Dependabot updates. High-severity production advisories fail Quality. Secret handling has both a full-history Gitleaks scan and repository push protection. The Gitleaks output is redacted SARIF; exceptions are narrow and match the intended historical values. IaC uses Trivy config on Terraform and Docker configuration, with exact findings and expiry dates checked by the gate.

Finally, deployment scans the exact runtime and web images extracted from its verified bundle. Those scans enforce the High/Critical threshold before uploading to the host. Each tool examines a different surface. In the walkthrough I will open the retained outputs rather than treating a green workflow badge as the complete security explanation. The retained IaC JSON contains fifteen findings. The successful scan workflow applies exact exceptions, with expiry on 31 October. That workflow result and the individual findings remain separately inspectable. |
| B29 | The manifest binds deployed images to their scans | This excerpt is from the actual release manifest, with the original field names and values. It identifies commit aea7478, deployment run 40344230832 and Quality run 40344231052. The security gate passed. The bundle hash identifies the retained tarball. The full file also records each image configuration ID, image-archive and OCI manifest digests, severity counts, and hashes for the two SBOMs and two Trivy reports.

Both bundled images have zero High and Critical findings. The runtime report also has one Medium and two Unknown entries; the web image has none at those severities. The CycloneDX inventories list what is present in each exact image. The Trivy reports describe vulnerabilities against that inventory. The manifest links those files by hash. GitHub-signed build provenance then binds the bundle and security manifest to the workflow execution.

The verification command is gh attestation verify, naming our repository and the downloaded release-manifest.json. A signature answers the build-origin and integrity question. The test and scan reports answer their own questions about behaviour and findings. Keeping those files together makes the deployment traceable without rebuilding an approximation later. |
| B30 | Hosted dev activates after candidate health succeeds | The deployment view puts the logical design onto hosted dev. GitHub Actions obtains temporary deploy credentials through OIDC. It ships the verified bundle to the Lightsail host, where nginx fronts the Node process. The application uses PostgreSQL, private S3 storage, Cognito and web push. CloudFront is the public edge.

Activation is a host decision. The installer prepares a candidate, verifies its health, then switches current. If the candidate is unhealthy, the installer restores the previous current. The deployment run then checks the public health endpoint. In our selected run, install completed at fifteen oh two forty-one UTC and the public check passed. The topology explains the runtime boundary, while the workflow and host installer explain who makes each decision. The following findings are examples of defects that escaped a narrower source-only view. |
| B31 | Packaging and runtime boundaries exposed useful defects | Five findings explain the checks we chose. A new zod advisory turned the production audit red even with a lockfile. The scoped dependency update restored a clean audit. Separately, Alpine removed the pinned FFmpeg package version, so the image failed before vulnerability scanning; the package pin had to move to the available version.

A schema refactor moved the registry while deployment packaging still read the old location. Updating the packaging consumer restored bundle verification. In the PWA, service-worker forwarding prevented SSE cancellation from reaching upstream; repeated group changes then exhausted stream limits. Keeping SSE browser-owned repaired that lifetime. Finally, the failed-capture retry needed a behavioural test of the recovery path. The common lesson is to exercise the real boundary: the package repository, the built image, the service worker, or the full interaction. We can now see how those concerns appear in one retained deployment run. |
| B32 | Installation keeps the app one tap away | We start in Safari and add Rewind to the Home Screen. The installed app then opens as its own window. This is the iPhone delivery surface used for the journey. Watch the transition from the browser to the standalone app. Once it opens, the next step is identity. |
| B33 | Sign-in returns the member to the private-group journey | Maya signs in and arrives in her private group space. The hosted development form gives us an authenticated account for this walkthrough. The web identity design also supports Cognito Managed Login using an authorization code with PKCE and a server-side exchange. The next decisions are about which group this account owns or belongs to. |
| B34 | Every steady load stage stays below the latency target | The measured p50, p95 and p99 curves cover one through one hundred virtual users. All p95 stages stay below two seconds; the 100-user p95 is 1,335.9 milliseconds. |
| B35 | Measured throughput rises with the active user count | The measured 100-user throughput is 17.84 requests per second, with zero errors. Each point uses its own three-minute steady window. |

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
