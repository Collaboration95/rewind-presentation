
### Slide 1 — A month of moments. One film (00:00–00:10)

Good afternoon. I am Gopal, and this is Rewind from Team 14. Rewind turns a month of small moments from a private group into one shared film. [covers: intro]

### Slide 2 — Everyday moments need a shared reason to return (00:10–01:00)

Our problem is simple: people take photos, but they get lost in busy group chats, and nobody looks back together. Rewind gives a small group a reason to come back: you add a few moments each week, they stay sealed, and at the end of the cycle everyone watches one film. Our scope was the real web and iPhone home-screen app, from sign-in to the film. [covers: problem, scope]

### Slide 3 — Four sprints took Rewind from foundation to hosted real accounts (01:00–02:00)

We worked in four sprints. Each one had a clear goal, from a working skeleton to real accounts and then stability. Today the whole journey runs on hosted dev. We planned each sprint and reviewed it at the end, and "done" meant checked in a real environment, tests green, and merged. [covers: sprints, milestones, status, ceremonies, DoD]

### Slide 4 — Four burndowns, velocity and each member’s share of the effort (02:00–03:00)

On the left are the four burndowns. Sprint 1 is the clean one; in Sprint 2 the scope kept growing as real accounts. On the right is how the effort really split: I did forty percent, three teammates twenty each, and one member contributed very little. Each retro changed the next sprint, for example integration gaps led us to test with real adapters. [covers: burndown, velocity, effort, retro]

### Slide 5 — Fourteen use cases follow one private-group journey (03:00–03:30)

These are our use cases. Members join a private group, add moments, chat and watch; the owner also manages the group. I will follow one path in detail: the cycle closes, the film is built, and it is released. [covers: use cases]

### Slide 6 — One Node application keeps rules close to transactions (03:30–04:05)

Our main architecture decision was one Node application, a modular monolith, not microservices. The rules for groups and cycles need to change together in one transaction, so splitting them would only add problems. Outside services like S3 and Cognito sit behind adapters. [covers: architecture decisions]

### Slide 7 — Analysis responsibilities become named implementation modules (04:05–04:40)

This is the step from analysis to design. On the left are the analysis roles: boundary, control and entity. On the right is where each one lives in the real code, so the model and the code tell the same story. [covers: analysis → design]

### Slide 8 — Durable claims make a repeated tick safe: close, claim, render, fence (04:40–05:30)

When a cycle ends, a scheduler tick closes it — no user action. The risk is the tick running twice or the server restarting midway. So steps 4 to 10 are one transaction: the cycle moves to revealing, a film job is written to the database, and the next cycle is created only if it doesn't exist yet. Every step is an 'ensure', so a repeated tick finds the work already done. The worker then renders the film and only marks it ready if it still owns the job. [covers: design model, design problem]

### Slide 9 — Three design problems, three named patterns in the code (05:30–06:15)

Each pattern answers a problem we actually hit. Storage: local runs use disk, hosted uses private S3 — Strategy lets us pick one at startup behind one interface, and an Adapter wraps the AWS SDK, so tests never need the cloud. Chat: members should see messages instantly without the save code knowing who's connected — Observer: the hub notifies subscribers only after the message is committed, and stored history lets a reconnecting client catch up. Persistence: we moved from SQLite to PostgreSQL mid-project — an Adapter keeps one database contract, so the business logic didn't change and the same thousand server tests run on both. The common idea: put a stable interface where change was likely. [covers: design patterns]

### Slide 10 — Keys preserve membership and the film’s exact input set (06:15–06:55)

This is the database schema for that same path. Membership decides who can see what. The key idea is that we freeze the exact list of moments that go into a film, so a retry always builds the same film. [covers: database schema]

### Slide 11 — The cycle’s states were fixed before any screen (06:55–07:20)

We drew this state diagram before we designed any screen. A cycle collects moments, then it is revealed, then the film is published, and finally it is archived. Only the server moves it between states. [covers: state diagram]

### Slide 12 — Each screen renders one state of the cycle (07:20–08:00)

Then each screen was designed for one of those states. This is our Home design: the countdown, the week and your allowance while the cycle is collecting. I can click through it live. Because every screen just shows the server state, a refresh or a second phone always agrees. [covers: UI flow, analysis → design]

### Slide 13 — Twelve test types each catch a different failure (08:00–08:50)

This is our whole test map: twelve kinds of test, the tool, how many, and when each one runs. "Blocks merge" means a red result stops the pull request; "reports" means we record it and review it. [covers: testing types]

### Slide 14 — Six test layers, each with a real example of what it catches (08:50–10:10)

Here are six layers, each with one real bug it catches. The top row runs on every pull request: unit, API, and the same suite again on PostgreSQL. The bottom row runs before main: real browser, the installed app, and accessibility. [covers: unit, integration, end-to-end, accessibility]

### Slide 15 — A regression test for a real bug, and security inside the suites (10:10–11:00)

One real bug: after a failed photo, "Try again" did nothing. We wrote a test that fails on the old code and passes with the fix. On the right, security is tested inside our suites too, and the pipeline scans come next. [covers: regression test, security testing]

### Slide 16 — One change passes four gates; colour says what a failure blocks (11:00–11:45)

This is the whole pipeline on one page. The colour tells you what a failure blocks: orange stops the merge, blue stops the deploy, grey only reports. I will zoom into each part. [covers: CI/CD pipeline, procedures]

### Slide 17 — Protected branches carry source; every run leaves results we can inspect (11:45–12:30)

Source code: every change goes through a pull request into a protected dev branch, and only one required check can let it merge. Artifacts: every run keeps its test results, scans, SBOMs and the release bundle, so we can always inspect what happened. [covers: source code management, artifact management]

### Slide 18 — Nine Quality jobs feed one required merge check; security reports beside it (12:30–13:20)

A pull request fans out into parallel checks and they all join into one required check. Press V: beside it, the security workflows report but do not block the merge. [covers: quality gate, SAST/secrets/IaC lanes]

### Slide 19 — Deploy scans and signs the exact bundle, then activates only if healthy (13:20–14:10)

After merge, we build one bundle, scan the exact images inside it, and sign it before anything is uploaded. Press V: we log in to AWS without stored keys, and the new version only goes live if its health check passes. [covers: SBOM, provenance, container scan, deploy]

### Slide 20 — ZAP scans hosted dev after every deploy: 0 High, 4 Medium (CSP) (14:10–14:55)

After every deploy, ZAP scans the running site. Press V for the real result: no High findings, and four Medium ones, all from one Content Security Policy gap we know how to fix. [covers: DAST]

### Slide 21 — SAST findings are triaged with reasons; SCA blocked merges until fixed (14:55–15:45)

SAST: CodeQL flagged three alerts and we closed each with a written reason. Press V for SCA: a new advisory blocked our merges for real until we fixed it. [covers: SAST, SCA]

### Slide 22 — The pipeline caught problems that source-level tests could not (15:45–16:25)

These are problems the pipeline caught that normal tests would not. The lesson for us: check what you actually ship, not just the source code. [covers: technical findings]

### Slide 23 — Demo route: eight clicks from pull request to running site (16:25–21:00)

Now I will show it live in GitHub. If the network fails, I will play the recording instead. [covers: CI/CD live demo]

Live in GitHub (about 30 s per click; links are on the slide):

1. Pull request checks: the one required Quality check, with security workflows beside it.
2. Quality run: the parallel jobs joining one result; open the artifacts list.
3. CodeQL alert 56: the rule, the line, and our written reason for dismissing it.
4. Deploy dev run: wait for Quality, build, scan, sign, install.
5. Deploy steps: the scan of the exact images happens before upload.
6. Attestation: the signature ties this manifest to this commit and workflow.
7. ZAP report: zero High, four Medium, all Content Security Policy.
8. Hosted health: the live version and the database are ready. Back to the slides.

### Slide 24 — A private-group journey runs from prompt to film (21:00–21:15)

Now the product. Two accounts are ready. We create a group, invite a friend, add a photo and a video, chat, watch the film, save it, and then try to break in as an outsider. [covers: system demo overview]

### Slide 25 — A shared prompt gives the group a common starting point (21:15–22:00)

While it plays: the owner names the group and picks a shared prompt, which gives everyone a common theme. Press → when the new group appears. [covers: UC02 create group]

### Slide 26 — One accepted invitation creates one private membership (22:00–23:00)

While it plays: the code works once and expires in a day, and the server decides who becomes a member. Press → when both accounts show the same group. [covers: UC03 invite and join]

### Slide 27 — A submitted photo becomes a sealed moment (23:00–24:00)

While it plays: take a photo, pick a look and seal it; after that nobody can see it until the film. Press → when it shows Sealed. [covers: UC05 photo]

### Slide 28 — Video and photos share one enforced weekly allowance (24:00–25:10)

While it plays: video and photos share one weekly allowance, and the server enforces it, not just the app. Press → when the counts update. [covers: UC04/UC06 video, allowance]

### Slide 29 — Stored messages and live updates keep the group connected (25:10–26:05)

While it plays: a message appears on the other phone without refreshing; that is the Observer pattern from earlier. Press → after the reply shows. [covers: UC11 chat]

### Slide 30 — The cycle closes, and the group watches its film (26:05–27:10)

While it plays: this capsule has closed, so the server built the film; now we watch it together. Press M only if you want sound, and → at the end screen. [covers: UC07/UC08 cycle close, film]

### Slide 31 — Archive keeps the film available after its premiere (27:10–28:15)

While it plays: after the premiere the film stays in Archive, and a member can save it as an MP4. Press → when the download opens. [covers: UC12/UC13 archive and save]

### Slide 32 — A spent invitation gives an outsider no group access (28:15–29:15)

While it plays: an outsider tries the used invite code and is refused, and the group never appears for them. Press → after the refusal. [covers: privacy, access control]

### Slide 33 — Load and stress: 100 users pass; the breakpoint is 200, set by the database bridge (29:15–31:15)

Now quality. Performance: our scripted load test passed every stage up to a hundred users. Then we pushed it: it breaks at two hundred users, but it slows down rather than failing. The cause is not the CPU; it is that the server talks to the database through one connection. [covers: performance, load test, stress test]

### Slide 34 — The capacity model, checked by the stress test, shows where to scale next (31:15–33:00)

Scalability: our model predicted this limit, and the stress test confirmed it. So the next steps are clear: an async database pool first, then a second server. Maintainability is the pipeline you just saw: every change has to pass the same tests and checks before it ships. Thank you, I am happy to take questions. [covers: scalability, maintainability]
