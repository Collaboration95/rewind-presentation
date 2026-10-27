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

Arrow keys / A / D: change frame. N: notes. O: overview. F: fullscreen. B: blackout. P: play/pause current clip. C: command cards. Z: full-size figure. Digits + Enter: jump to physical page. Hashes accept physical page numbers or named anchors such as #F5 and #B7. Click a feature video to pause at a question.

## Spoken delivery

### 1 · A month of moments. One film.

00:00–00:15 · Section 1 · 00:15

Good afternoon. I am Gopal Guruprasath, presenting Rewind for SWE5006 Team 14. Rewind turns a month of everyday contributions into one private film for a small group. I will connect the product to our design, tests and delivery pipeline, then show the complete journey.

Transition: First, the problem and the product boundary.

If asked: → B10

### 2 · Everyday moments need a shared reason to return.

00:15–01:10 · Section 1 · 00:55

Our business problem is simple: people already capture moments, but the moments disappear inside busy chats and camera rolls. A group has no common point at which to look back together. Rewind adds that point. Two to ten members contribute photos or short videos, and the contributions remain sealed until a twenty-eight-day cycle closes. Each member has five moments and thirty seconds per week. The limit keeps the contribution small enough to become a habit. At the end, the group receives one film and a twenty-four-hour premiere before the film remains in Archive. Our scope is the real-account web and PWA journey: identity, private groups, invitations, capture, chat, reminders and films. That is the boundary used in the design and in the demonstration.

Transition: The four sprints show how we delivered this boundary.

If asked: → B1 · → B10

### 3 · Four sprints delivered the hosted private-group journey.

01:10–03:30 · Section 1 · 02:20

We used four sprints with zero-based names. Sprint zero built the runnable foundation. Sprint one integrated capture, the cycle and Archive. Sprint two established the real-account product, private media and hosted integration. Sprint three concentrated on stability, recovery and behavioural regression tests. The velocity chart counts issues closed inside each sprint window: forty-four, one hundred, one hundred and forty-five, then thirty. It is a delivery-count view. The backup has the event-replayed burndowns, including scope changes. For example, Sprint two grew from nine issues in scope to one hundred and thirty-five, while Sprint three ended with five open in its milestone. We retained that scope movement in the records.

Our team is Nguyen Kim Long, Gopal Guruprasath, Jiang Jiayu, Phan Mai Tan Loi and Sang Haoxiang. Effort is split equally at twenty percent each. The agreed plan is ten person-days per member. I coordinated the product and integration work; the team responsibilities span requirements, server integration, client experience and quality support.

Our Definition of Done is outcome checked in the cheapest environment that exercises it, fast tests passing, a green aggregate Quality check, and merge to dev. Overnight batches also get a review pass with blocking findings fixed. Project planning, Sprint Planning and Sprint Review were held. The useful retrospective chain is visible in the implementation: Sprint one exposed integration gaps, so Sprint two exercised real adapters; Sprint two exposed stale state and incomplete downloads, so Sprint three added whole-interaction and pagination checks.

This status is dated twenty-six October. The remaining presentation-relevant issues cover focused runner selection, emoji and calendar labels, the hosted Safari/PWA integration check, and report assembly. The complete seven-item delivery register is in the backup. We now move from the product boundary to the analysis models.

Transition: The use cases now give that scope a formal boundary.

If asked: → B10

### 4 · Fourteen use cases follow one private-group journey.

03:30–04:03 · Section 2 · 00:33

The use case view starts with user goals rather than code. A member joins a private group, contributes, chats and watches; the owner also manages membership and settings. The boundary makes the secondary systems explicit: identity, object storage, web push and scheduled time. For detailed design I will follow CU-B: close the cycle, compile the film and release it. That path connects UC07 and UC08 and crosses persistence, background work and media processing.

Transition: The logical view shows where those responsibilities live.

If asked: → B1 · → B3

### 5 · One Node application keeps rules close to transactions.

04:03–04:42 · Section 2 · 00:39

The principal architecture decision is a modular monolith. The application is small enough that splitting membership, contributions and cycles into separate services would add coordination without improving this workflow. Keeping the rules near a transaction makes acceptance and cycle transitions easier to reason about. Hosted PostgreSQL gives us durable relational state, while private S3 objects carry the media. Cognito supplies the web identity flow. Adapters keep those external protocols outside the domain decisions. This logical view shows responsibilities and dependencies; the deployment view later will show where these elements run.

Transition: Now map the analysis responsibilities onto that implementation.

If asked: → B4 · → B5 · → B9

### 6 · Analysis responsibilities become named implementation modules.

04:42–05:27 · Section 2 · 00:45

The left side of this mapping is analysis. A boundary receives interaction, a control coordinates the use case, and entities represent the state the business needs to retain. Those are responsibilities. On the right, we refine them into implementation names. The scheduler finds work, lifecycle owns the cycle transition, compilation prepares and finalises the film, and the database retains cycles, jobs and frozen inputs. The analysis classes remain available in backup B1. In the design diagrams, a collection of functions is shown as a module. A class symbol is reserved for an actual class. That keeps the model traceable to the code a maintainer will open.

Transition: The hardest design problem is safely repeating this background work.

If asked: → B1 · → B2

### 7 · Durable claims keep repeated cycle work safe.

05:27–06:21 · Section 2 · 00:54

The design problem is repeated execution. A scheduler tick can repeat, a process can stop, and an old worker can finish after another worker has claimed the same work. Polling alone only tells us that something needs attention. We considered a hierarchy of State objects, separate Command objects, and persistent state with a durable job. The chosen design uses persisted lifecycle state, a durable compilation job and a claim that includes lease and generation information. The MediaStore Strategy interface supplies PrivateS3MediaStore and LocalMediaStore without branching in the worker; their adapters isolate storage protocols. The class view makes those roles visible on real modules and stored entities. A worker can do expensive media work outside a long database transaction, then prove it still owns the claim before publishing. The result is a precise completion rule that survives retries and process restarts.

Transition: The sequence shows where those checks happen.

If asked: → B2 · → B7 · → B8 · → B9

### 8 · A repeated tick reuses work and fences stale completion.

06:21–07:18 · Section 2 · 00:57

Read the sequence from the numbered messages. Show closure here, then #B16 for compilation and #B17 for publication; return to #s9. The scheduler identifies the ended cycle and the lifecycle module performs the closing transition. That transaction also makes the next cycle available and stages the compilation work. The worker then claims the durable job and renders the frozen input set. Rendering happens outside the database transaction because it can take seconds. At finalisation, the code checks that the claim still belongs to this worker and generation. The alternative frames matter as much as the happy path: a repeated tick reuses existing work, and a stale worker cannot publish over the current result. The loop describes retry around the retained job. The arrows explain how the safety rule is enforced, while the schema explains what survives a restart.

Transition: The schema explains what makes those decisions durable.

If asked: → B16 · → B17

### 9 · Keys preserve membership and the film’s exact input set.

07:18–08:30 · Section 2 · 01:12

This is the database schema for the same use case, with the access relationships alongside it. Start at the group and membership relation. It answers who belongs to the group and in which role. A group has cycles; a cycle has contributions; the processing jobs retain what must happen to the media. The compilation-input relation is especially useful: it fixes the inputs associated with the film job, so later retry does not silently reinterpret a changing collection. Primary keys identify the durable records, foreign keys connect them, and uniqueness expresses rules such as one relevant membership or job identity.

We chose a relational store because this path depends on joins, consistency and transaction boundaries across related records. Hosted PostgreSQL also gives us managed backups. The code retains a local SQLite path, and the server suite runs across both dialects. For this explanation the important point is that privacy, lifecycle and recovery are stored relationships. The next section shows the tests that exercise those relationships through APIs and user actions.

Transition: Tests exercise those rules through their real boundaries.

If asked: → B4 · → B9

### 10 · Each test layer catches a different integration failure.

08:30–10:06 · Section 3 · 01:36

This table separates the test types by the failure each can catch. Static checks enforce formatting, types and import boundaries. Jest and Testing Library exercise client logic and interaction state. The server suite drives API behaviour, privacy, media integrity and cycle rules using SQLite, and the full suite is exercised again on PostgreSQL seventeen. Repository and IaC tests cover architecture and policy rules. Cloud-free deployment fixtures inject failures around installation, transfer, health and recovery. Those lanes feed the aggregate Quality check.

Browser tests cover things that a unit test cannot demonstrate: responsive layout, PWA behaviour, keyboard use and accessibility. The baseline has forty-one Playwright tests, including six Axe checks. Those join the gate for main. The real-account Firefox flow and performance checks are separate runs. Performance is a test type here: the local script makes twelve hundred requests and compiles three films, while the hosted load study appears in the demonstration section.

The fast suite passed 1,674 frontend tests, 985 server tests with 21 skipped, and 123 root tests with one skipped. PostgreSQL and browser counts come from the twenty-six October audit. Client statement coverage is eighty-nine point six four percent against a seventy-percent floor; client line coverage is ninety-two point three three; server line coverage is eighty-five point six seven. I treat the coverage number as a way to find unexercised branches. The next example shows why the behavioural assertion matters.

Transition: A regression test is useful when it catches an actual interaction failure.

If asked: → B6

### 11 · “Try again” must return to a usable viewfinder.

10:06–11:30 · Section 3 · 01:24

A concrete bug makes the testing approach easier to assess. After a failed photo capture, the screen showed Try again. The retry path called capture while the screen was still in a state that made the access guard return immediately. The button existed, but the interaction went nowhere. The repair returned the user to the viewfinder for a fresh capture.

The regression test follows the user action: induce failure, select Try again, verify that the viewfinder returns, then capture again. The audit replayed the previous source against that new test. It failed before the repair and passed at f6cd896. That is the behaviour we want preserved through refactoring. Other characterisation tests pinned route contracts, media denials and screen behaviour before module extraction. The lesson is to assert the observable recovery path, especially after an error or context change. A coverage increase is useful when it exposes a branch like this. The delivery section now shows how the same source revision travels with its test output, security inventory and deployable images.

Transition: The pipeline retains these results alongside the source and deployment artifacts.

If asked: → B3 · → B6

### 12 · A commit carries tests, inventory and deployment evidence.

11:30–12:42 · Section 4 · 01:12

Source management starts with a focused issue branch and a pull request to protected dev. The required Quality result belongs to the exact commit. Once merged, that same source revision triggers dev deployment. The artifact flow matters because a passing test run and a deployed application must be connected by identity.

Quality retains root JUnit, server results and coverage, frontend Jest JSON and coverage, and the production dependency audit report. Deployment retains the runtime and web image inventories, the exact-image Trivy reports, the security manifest and the deployable tarball. Signed provenance binds the retained bundle and manifest to the workflow. After deployment, the ZAP reports describe the running hosted target. The host receives the built image pair in the verified bundle. It does not independently rebuild the application from a moving branch. These artifact families let us move from a source question to a test, package, scan or running-page result without treating those as interchangeable evidence.

Transition: The pipeline shows where each decision happens.

If asked: → B12

### 13 · Pipeline decisions separate merge gates from host activation.

12:42–14:18 · Section 4 · 01:36

There are several decisions inside this activity view. First, change classification decides whether the commit needs application checks or is documentation-only. A code change fans out across parallel static, client, server, PostgreSQL, root and deployment-fixture lanes. The aggregate fails on a failed or unexpectedly skipped required lane. Production dependency audit is part of that aggregate.

Second, deployment waits for a successful dev Quality run for the same commit. It builds and verifies the bundle, inventories the exact runtime and web images and scans those images. High or Critical findings at that exact-bundle gate stop host upload. This is a deployment gate even though the independent scan workflows are not branch-required checks.

Third, the host installs a candidate and checks it before activation. Failure takes the restoration path. Once the host is serving, the passive ZAP baseline spiders hosted dev and publishes its report. SAST and the other security reports remain visible as their own lanes. The distinction is operational: branch protection requires the aggregate Quality context; a deployment step can independently stop the upload; a reporting lane retains findings for triage. The words BLOCKS and REPORTS in the figure refer to those specific decisions.

Transition: Here are the security procedures inside those lanes.

If asked: → B5 · → B12

### 14 · Security checks cover code, packages, secrets and running pages.

14:18–16:00 · Section 4 · 01:42

SAST is CodeQL across JavaScript and TypeScript, Python and Actions. Tonight the three load-script alerts were triaged as used in tests. That is a written disposition attached to those alerts. The DAST lane now runs a ZAP baseline against hosted dev. The saved report for this deployment has zero High, four Medium, seven Low and six Informational findings. The Medium findings concern Content Security Policy. The HTML report gives the alert, affected URL, evidence and remediation text.

SCA combines the production npm audit gate with Dependabot updates. High-severity production advisories fail Quality. Secret handling has both a full-history Gitleaks scan and repository push protection. The Gitleaks output is redacted SARIF; exceptions are narrow and match the intended historical values. IaC uses Trivy config on Terraform and Docker configuration, with exact findings and expiry dates checked by the gate.

Finally, deployment scans the exact runtime and web images extracted from its verified bundle. Those scans enforce the High/Critical threshold before uploading to the host. Each tool examines a different surface. In the walkthrough I will open the retained outputs rather than treating a green workflow badge as the complete security explanation.

Transition: The manifest ties the image results to the bytes we deployed.

If asked: → B12

### 15 · The manifest binds deployed images to their scans.

16:00–17:30 · Section 4 · 01:30

This excerpt is from the actual release manifest, with the original field names and values. It identifies commit aea7478, deployment run 40344230832 and Quality run 40344231052. The security gate passed. The bundle hash identifies the retained tarball. The full file also records each image configuration ID, image-archive and OCI manifest digests, severity counts, and hashes for the two SBOMs and two Trivy reports.

Both bundled images have zero High and Critical findings. The runtime report also has one Medium and two Unknown entries; the web image has none at those severities. The CycloneDX inventories list what is present in each exact image. The Trivy reports describe vulnerabilities against that inventory. The manifest links those files by hash. GitHub-signed build provenance then binds the bundle and security manifest to the workflow execution.

The verification command is gh attestation verify, naming our repository and the downloaded rewind-release.tar. A signature answers the build-origin and integrity question. The test and scan reports answer their own questions about behaviour and findings. Keeping those files together makes the deployment traceable without rebuilding an approximation later.

Transition: Next, follow those verified bytes to the hosted application.

If asked: → B12

### 16 · Hosted dev activates after candidate health succeeds.

17:30–18:42 · Section 4 · 01:12

The deployment view puts the logical design onto hosted dev. GitHub Actions obtains temporary deploy credentials through OIDC. It ships the verified bundle to the Lightsail host, where nginx fronts the Node process. The application uses PostgreSQL, private S3 storage, Cognito and web push. CloudFront is the public edge.

Activation is a host decision. The installer prepares a candidate, verifies its health, then switches current. If the candidate is unhealthy, the installer restores the previous current. The deployment run then checks the public health endpoint. In our selected run, install completed at fifteen oh two forty-one UTC and the public check passed. The topology explains the runtime boundary, while the workflow and host installer explain who makes each decision. The following findings are examples of defects that escaped a narrower source-only view.

Transition: The technical findings show why those package and runtime checks matter.

If asked: → B5 · → B12

### 17 · Packaging and runtime boundaries exposed useful defects.

18:42–19:42 · Section 4 · 01:00

Five findings explain the checks we chose. A new zod advisory turned the production audit red even with a lockfile. The scoped dependency update restored a clean audit. Separately, Alpine removed the pinned FFmpeg package version, so the image failed before vulnerability scanning; the package pin had to move to the available version.

A schema refactor moved the registry while deployment packaging still read the old location. Updating the packaging consumer restored bundle verification. In the PWA, service-worker forwarding prevented SSE cancellation from reaching upstream; repeated group changes then exhausted stream limits. Keeping SSE browser-owned repaired that lifetime. Finally, the failed-capture retry needed a behavioural test of the recovery path. The common lesson is to exercise the real boundary: the package repository, the built image, the service worker, or the full interaction. We can now see how those concerns appear in one retained deployment run.

Transition: Now follow one deployment run from Quality through artifacts and hosted health.

If asked: → B6 · → B12

### 18 · One run connects green Quality to hosted dev.

19:42–23:30 · Section 4 · 03:48

I will now walk through the retained run. First, here is Quality run 40344231052. The classifier sends a code change through the parallel lanes and the aggregate collects their results. The branch-required context is named Format, lint, typecheck, and test. This is where the production audit participates in the merge decision.

[00:00–00:45: show the Quality job graph and aggregate summary using the command cards.]

Next, look at the separate security outputs. CodeQL has its language analyses and written alert dispositions. Gitleaks has its full-history report. IaC has its exact-finding policy. These outputs remain separate from the aggregate requirement. The old failed audit example is useful because it shows a required lane actually stopping integration when a new advisory arrived.

[00:45–01:20: show saved scan inventory and the CodeQL triage record; open no repository page through a browser.]

Deployment run 40344230832 names the same source commit. The wait-for-Quality step took two minutes and three seconds. Building the verified bundle took fifty-three seconds. Scanning the exact image archives and writing the manifest took sixteen seconds. The run retained the SBOMs, Trivy JSON and manifest, then attested the release bundle and security manifest. Those steps all precede the upload.

[01:20–02:10: show the Deploy dev step table, then open the saved manifest and one SBOM. Point to the run ID, image identity and bundle hash.]

The host installation took one minute and sixteen seconds. The installer checked the candidate and the run passed its public health check. The subsequent ZAP scan took one minute and forty-four seconds and retained the report we saw: zero High, four Medium CSP, seven Low and six Informational findings. The sequence is important: exact-image security before upload, candidate health before activation, running-page DAST after deployment.

[02:10–03:10: open the saved ZAP report. Follow one CSP alert to its evidence and recommendation. Show the attestation verification command and its retained subject identity.]

Finally, hosted dev health reports the installed version and PostgreSQL readiness. This closes the trace from a specific source revision to the system we are about to use. A failing candidate follows the installer’s restoration path; we can inspect that source path or the deployment fixtures in questions.

[03:10–03:48: show the hosted health response and return to the deck. Leave the manifest and ZAP artifacts ready for questions.]

Transition: The same hosted system is the setting for the feature demonstration.

If asked: → B5 · → B12

### 19 · Follow one group from installation to a private film.

23:30–23:48 · Section 5 · 00:18

The system demonstration follows one group. First enter through installation, sign-in and invitation. Then contribute photos and video, chat and opt into reminders. Finally follow automatic closure into the film and Archive, and check the outsider boundary. Each feature has its own clip so we can pause at an interruption.

Transition: Start with installing the Home Screen app.

If asked: → B1 · → B3

### F1 · Installation keeps the app one tap away.

23:48–24:33 · Section 5 · 00:45

We start in Safari and add Rewind to the Home Screen. The installed app then opens as its own window. This is the iPhone delivery surface used for the journey. Watch the transition from the browser to the standalone app. Once it opens, the next step is identity.

Transition: Now sign in as Maya.

If asked: → B5

### F2 · Sign-in returns the member to the private-group journey.

24:33–25:18 · Section 5 · 00:45

Maya signs in and arrives in her private group space. The hosted development form gives us an authenticated account for this walkthrough. The web identity design also supports Cognito Managed Login using an authorization code with PKCE and a server-side exchange. The next decisions are about which group this account owns or belongs to.

Transition: Create the group and its shared prompt.

If asked: → B5

### F3 · A shared prompt gives the group a common starting point.

25:18–26:18 · Section 5 · 01:00

The owner creates a group and chooses a shared prompt. The prompt gives contributions a common theme without prescribing what each person must record. The group size is bounded, and its settings retain the prompt and time zone. Point to the new group name and the prompt on Home, then to the owner settings. We now need another member.

Transition: Invite a friend with a single-use code.

If asked: → B1

### F4 · One accepted invitation creates one private membership.

26:18–27:18 · Section 5 · 01:00

The owner creates an invitation and shares the code. It works once and expires after twenty-four hours. The friend signs in and accepts it. Watch the member list change and the shared group appear for both accounts. Acceptance is a server decision: a valid code and authenticated account produce a durable membership. Reusing the code later will not add another member. Keep that rule in mind for the final outsider check.

Transition: The first contribution is a photo.

If asked: → B3

### F5 · A submitted photo becomes a sealed moment.

27:18–28:13 · Section 5 · 00:55

Take a photo and choose a look before submitting it. The user can review the contribution, but after acceptance it becomes sealed. Your moments retains the entry and allowance information without opening everyone’s submitted content early. A photo counts as one moment and becomes a three-second segment in the film. Watch the state change from capture to a retained sealed entry.

Transition: Video shares the same weekly allowance.

If asked: → B3

### F6 · Video and photos share one enforced weekly allowance.

28:13–29:18 · Section 5 · 01:05

Record a video with sound, review the trim and submit it. A video can use up to fifteen seconds, and the total weekly allowance is shared with photos: five moments and thirty seconds per member. The visible ledger matters because the user needs to know what remains before trying another capture. The server checks the accepted contribution and media rather than trusting only the client display. Pause at the updated counts. The contribution is now part of the same sealed collection as the photo.

Transition: The group can talk while the moments stay sealed.

If asked: → B3

### F7 · Stored messages and live updates keep the group connected.

29:18–30:13 · Section 5 · 00:55

One member sends a message and the other sees it without refreshing. Replies and reactions remain in the shared conversation. The design combines stored messages with live SSE delivery and reconnect, so the live notification is not the only record of the message. This is where the Observer design in backup B8 becomes visible to a user.

Transition: Next, opt into the weekly reminder.

If asked: → B8

### F8 · Reminder permission leads to an explicit weekly choice.

30:13–31:03 · Section 5 · 00:50

Open reminders in the Home Screen app. The user chooses whether to receive the Sunday reminder and grants notification permission. The weekly schedule is Sunday at seven in the evening in the group’s time zone. A snooze lasts seven days. The useful interaction is the explicit permission and saved preference, with feedback tied to successful registration.

Transition: Now open the completed capsule and its premiere.

If asked: → B5

### F9 · The completed capsule is ready for its shared premiere.

31:03–31:43 · Section 5 · 00:40

Here is the completed capsule from Maya and Jun. Its premiere card opens the shared film. Behind this result, the scheduler closes the ended cycle, queues durable compilation work and opens the successor. That is the CU-B path from the design section. Pause on the ready state, then continue to the film.

Transition: Open the group’s film.

If asked: → B2

### F10 · The reveal turns sealed contributions into one shared film.

31:43–33:03 · Section 5 · 01:20

The film is now available to the group. Open the premiere and watch the contributions together. The player exposes moment segments and lets the viewer move between them. The output is a portrait film at seven-twenty by twelve-eighty, thirty frames per second, with normalised audio. Let a short section play with sound, then pause at the end screen. The film connects the sealed contribution habit to the shared payoff we described at the start.

Transition: Archive keeps the film and offers saving.

If asked: → B2

### F11 · Archive keeps the film available after its premiere.

33:03–33:58 · Section 5 · 00:55

After the premiere, the film remains in Archive. Open the retained film, choose Save film and open the downloaded MP4. The end screen also lets a member save their own moments. This completes the journey from capture to a durable output the member can keep. Pause on the playable downloaded result. The final check uses a different account that has no membership.

Transition: Check the outsider boundary.

If asked: → B4

### F12 · A spent invitation gives an outsider no group access.

33:58–34:48 · Section 5 · 00:50

The outsider signs in with a different account and tries the invitation already used by our friend. The app rejects it as already used. The group does not appear in the outsider’s list. This is the negative branch of the invitation rule shown earlier. The server tests also exercise direct group, budget, chat and media access with missing or wrong membership. The user demonstration and those API checks address the same privacy boundary at different layers. We have now completed the group journey.

Transition: Finish with the hosted load results and the scaling mechanism.

If asked: → B6

### 20 · Load results identify the next scaling change.

34:48–38:00 · Section 5 · 03:12

The quality-attribute demonstration uses the hosted API through CloudFront, Node and PostgreSQL. A plain Node HTTP runner steps through one, ten, twenty-five, fifty and one hundred virtual users. Each steady stage lasts three minutes. Users wait three to seven seconds between requests, and the mixed journey is mostly reads with five percent chat sends. The acceptance rule is p95 below two seconds and fewer than one percent errors.

The measured table shows zero errors through fifty users. At that level, p95 was eight hundred and fifty-nine milliseconds and throughput was nine point one four requests per second. At one hundred users, p95 remained below the latency target, but the error rate was ten point eight eight percent, so that stage failed its combined acceptance rule. The short upstream-error interval overlapped a deployment installation. The errors remain in the mixed-run result.

A separate three-minute confirmation after deployment reused the same accounts and group with a read-only journey. It achieved six hundred and twenty-five milliseconds p95, eighteen point four two requests per second and zero errors at one hundred virtual users. That is a separate result with its own workload label.

The chart on the right is the capacity projection from the fitted operational scenario. It uses a serialized service demand of about fifty-one milliseconds per request, a fixed delay of about three hundred and forty-two milliseconds and five-second think time. The one-host model approaches nineteen point six requests per second. As user population rises, mean response time rises much faster than throughput. The two-host line divides arrival load between two service centers while holding the other assumptions fixed. Its values are model means; the measured table contains p95.

The mechanism behind the scaling work is visible in the code. The PostgreSQL bridge uses synchronous waiting and one client, which serializes parts of the request path. FFmpeg is a child process sharing the host CPU budget. Separating media work reserves API capacity, while asynchronous persistence and a bounded connection pool address request serialization. Multiple hosts also need coordinated media-capability state, local staging and job ownership; PostgreSQL and S3 remain shared.

For maintainability, return to the pipeline. A change to those internals should preserve the behavioural tests, database checks, verified image bundle, scan outputs and deployment health decision. That is how we can improve the mechanism while retaining the product behaviour demonstrated here. The backups contain the detailed model, coverage and diagrams for questions.

Transition: We can take questions using the backup map.

If asked: → B6 · → B11 · → B12

## Q&A backup map

| Backup | Question | Spoken answer |
|---|---|---|
| B1 | Analysis separates interaction, coordination and state. | The analysis model separates the interaction boundary, use-case coordination and durable business state; main frame six maps those responsibilities to code. |
| B2 | Durable state survives interrupted compilation. | Stored lifecycle state and durable jobs make work recoverable; a current lease and generation determine who may finalise. |
| B3 | Capture acceptance checks identity, allowance and media. | The capture sequence follows reservation, media validation and acceptance, keeping membership and allowance decisions on the server. |
| B4 | Relational keys make the private film traceable. | The relational choice follows transaction and consistency needs across membership, cycles, contributions and the frozen film input set. |
| B5 | The deployment view names each runtime boundary. | CloudFront and nginx form the entry, Node runs the application, and PostgreSQL, S3 and Cognito provide the durable data and identity services. |
| B6 | Coverage and enforcement answer different questions. | The statement floor is a regression safety net. Coverage reports identify branches to investigate, while behavioural tests assert the outcomes that matter. |
| B7 | Storage changes behind Strategy and Adapter roles. | MediaStore supplies the Strategy contract. LocalMediaStore and PrivateS3MediaStore implement it; privateTransport adapts AWS SDK commands. Hosted runtime selects PrivateS3MediaStore, while disk mode takes its separate filesystem path. |
| B8 | Observer distributes chat updates alongside stored history. | RealtimeHub acts as the live update subject and subscribers receive events, while stored messages provide the durable history and reconnect path. |
| B9 | The persistence adapter preserves a common data-access contract. | PostgresDatabase adapts the common call contract to PostgreSQL; centralising that translation also makes the synchronous bridge a clear target for performance work. |
| B10 | Agile records retain scope changes and equal effort. | The burndowns retain scope change and reopen events. Effort is the agreed twenty-percent split: ten person-days each. The dated delivery register is #230, #362, #504, #515, #527, #587 and #588. |
| B11 | The capacity curve follows the closed-user workload. | The closed-user model includes think time, so slower responses reduce offered throughput. Its fitted scenario includes the initial run’s deployment-overlap interval. |
| B12 | Retained artifacts make the deployment independently inspectable. | Use the manifest for commit and image identity, SBOMs for inventory, scan JSON for findings, provenance for build origin and ZAP for the running hosted page. |
| B13 | Acceptance pins and probes the exact media version and replays an existing receipt. | Acceptance pins and probes the exact media version and replays an existing receipt. |
| B14 | One transaction records quota, contribution, processing job and completion. | One transaction records quota, contribution, processing job and completion. |
| B15 | Processing stores an MP4 and proves current ownership before marking ready. | Processing stores an MP4 and proves current ownership before marking ready. |
| B16 | The worker claims settled inputs, materialises media and fences finalisation. | The worker claims settled inputs, materialises media and fences finalisation. |
| B17 | Stored bytes and the current ready row are verified before publication and archiving. | Stored bytes and the current ready row are verified before publication and archiving. |
| B18 | Account and group goals connect to Cognito, chat and web push. | Account and group goals connect to Cognito, chat and web push. |
| B19 | Photo and video acceptance include the shared allowance and optional correction. | Photo and video acceptance include the shared allowance and optional correction. |
| B20 | Cycle closure produces a film, premiere, Archive and authorised downloads. | Cycle closure produces a film, premiere, Archive and authorised downloads. |
| B21 | Sprint 0 records opening scope and daily delivery. | Use the opening snapshot and daily boundaries to follow scope and remaining issues in Sprint 0. |
| B22 | Sprint 1 records opening scope and daily delivery. | Use the opening snapshot and daily boundaries to follow scope and remaining issues in Sprint 1. |
| B23 | Sprint 2 records opening scope and daily delivery. | Use the opening snapshot and daily boundaries to follow scope and remaining issues in Sprint 2. |
| B24 | Issue closures and merged PRs track sprint delivery. | The chart counts issue closures and merged PRs within each SGT sprint window. |
| B25 | Backlog stories connect sprint goals to delivered use cases. | The saved backlog contains 329 issues, 319 closed and ten open. UC05 links the photo story to Sprint 2 issue 313 and Sprint 3 recovery and format issues 545 and 574. Sprint goals and retrospective actions retain that trace. |

## CI/CD walk-through command cards

```sh
gh run view 40344231052 -R Collaboration95/rewind-app
gh api repos/Collaboration95/rewind-app/branches/dev/protection
gh run view 40344230832 -R Collaboration95/rewind-app
gh api repos/Collaboration95/rewind-app/actions/runs/40344230832/artifacts
gh attestation verify --repo Collaboration95/rewind-app rewind-release.tar
```

Saved artifacts: `../pipeline-run-40344230832/security/` and `../pipeline-run-40344230832/zap/`. Hosted health: `https://d2m6kz76y4kuvm.cloudfront.net/api/health`.

## Source register

- Shared brief: scope, equal effort, delivery surface, five-section timing.
- Audits B1/B2: use cases, analysis, module mapping, design and patterns.
- Audit E: dated test inventory, coverage and red/green retry replay.
- records/TEAM.md and AGILE.md: team, effort, milestones, events and dated open register.
- records/FINDINGS.md: technical defects and repairs; later pipeline artifacts establish the delivered scan/deployment state.
- PIPELINE-ARTIFACTS.md and run 40344230832: exact-image inventory, manifest, scan and provenance flow.
- load-test/METHODOLOGY.md and RESULTS.md: hosted measurement, separate confirmation and capacity projection.
