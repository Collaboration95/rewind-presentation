"""Speakable script (27 Oct, 14:10): short first-person blocks per main slide.
build_deck.py writes these to SCRIPT.md and to the speaker notes (N); the long
version stays in SCRIPT-detailed.md."""

CHEAT = [
    '**F** fullscreen · **→ / ←** next / back · **Space** play/pause a clip (M sound, R restart) · **N** notes · **O** overview',
    '**Z** or click enlarges a diagram (slide 9 patterns, any UML) · **Esc** closes it, and also leaves the embedded page on slide 12',
    '**S** opens the UI-flow storyboards · **V** on slides 18–21 opens the detail view, V again returns',
    '**Number + Enter** jumps to main slide n (badge bottom-right shows n / 34); backups come after 34',
    '**Fallback:** the PDF (deck/out/rewind-presentation.pdf); recorded CI/CD walkthrough = backup CB1; feature clips play from the deck',
]

S = {
 's1': ('Good afternoon. I am Gopal, and this is Rewind from Team 14. Rewind turns a month of small moments from a private group into one shared film.', 'intro'),
 's2': ('Our problem is simple: people take photos, but they get lost in busy group chats, and nobody looks back together. '
        'Rewind gives a small group a reason to come back: you add a few moments each week, they stay sealed, and at the end of the cycle everyone watches one film. '
        'Our scope was the real web and iPhone home-screen app, from sign-in to the film.', 'problem, scope'),
 's3': ('We worked in four sprints. Each one had a clear goal, from a working skeleton to real accounts and then stability. '
        'Today the whole journey runs on hosted dev. We planned each sprint and reviewed it at the end, and "done" meant checked in a real environment, tests green, and merged.', 'sprints, milestones, status, ceremonies, DoD'),
 's4': ('On the left are the four burndowns. Sprint 1 is the clean one; in Sprint 2 the scope kept growing as real accounts landed, and you can see that honestly. '
        'On the right is how the effort really split: I did forty percent, three teammates twenty each, and one member contributed very little. '
        'Each retro changed the next sprint, for example integration gaps led us to test with real adapters.', 'burndown, velocity, effort, retro'),
 's5': ('These are our use cases. Members join a private group, add moments, chat and watch; the owner also manages the group. '
        'I will follow one path in detail: the cycle closes, the film is built, and it is released.', 'use cases'),
 's6': ('Our main architecture decision was one Node application, a modular monolith, not microservices. '
        'The rules for groups and cycles need to change together in one transaction, so splitting them would only add problems. '
        'Outside services like S3 and Cognito sit behind adapters.', 'architecture decisions'),
 's7': ('This is the step from analysis to design. On the left are the analysis roles: boundary, control and entity. '
        'On the right is where each one lives in the real code, so the model and the code tell the same story.', 'analysis → design'),
 's8': ("When a cycle ends, a scheduler tick closes it — no user action. The risk is the tick running twice or the server restarting midway. So steps 4 to 10 are one transaction: the cycle moves to revealing, a film job is written to the database, and the next cycle is created only if it doesn't exist yet. Every step is an 'ensure', so a repeated tick finds the work already done. The worker then renders the film and only marks it ready if it still owns the job.", 'design model, design problem'),
 's9': ("Each pattern answers a problem we actually hit. Storage: local runs use disk, hosted uses private S3 — Strategy lets us pick one at startup behind one interface, and an Adapter wraps the AWS SDK, so tests never need the cloud. Chat: members should see messages instantly without the save code knowing who's connected — Observer: the hub notifies subscribers only after the message is committed, and stored history lets a reconnecting client catch up. Persistence: we moved from SQLite to PostgreSQL mid-project — an Adapter keeps one database contract, so the business logic didn't change and the same thousand server tests run on both. The common idea: put a stable interface where change was likely.", 'design patterns'),
 's10': ('This is the database schema for that same path. Membership decides who can see what. '
         'The key idea is that we freeze the exact list of moments that go into a film, so a retry always builds the same film.', 'database schema'),
 's11': ('We drew this state diagram before we designed any screen. A cycle collects moments, then it is revealed, then the film is published, and finally it is archived. '
         'Only the server moves it between states.', 'state diagram'),
 's12': ('Then each screen was designed for one of those states. This is our Home design: the countdown, the week and your allowance while the cycle is collecting. '
         'I can click through it live. Because every screen just shows the server state, a refresh or a second phone always agrees.', 'UI flow, analysis → design'),
 's13': ('This is our whole test map: twelve kinds of test, the tool, how many, and when each one runs. '
         '"Blocks merge" means a red result stops the pull request; "reports" means we record it and review it.', 'testing types'),
 's14': ('Here are six layers, each with one real bug it catches. The top row runs on every pull request: unit, API, and the same suite again on PostgreSQL. '
         'The bottom row runs before main: real browser, the installed app, and accessibility.', 'unit, integration, end-to-end, accessibility'),
 's15': ('One real bug: after a failed photo, "Try again" did nothing. We wrote a test that fails on the old code and passes with the fix. '
         'On the right, security is tested inside our suites too, and the pipeline scans come next.', 'regression test, security testing'),
 's16': ('This is the whole pipeline on one page. The colour tells you what a failure blocks: orange stops the merge, blue stops the deploy, grey only reports. '
         'I will zoom into each part.', 'CI/CD pipeline, procedures'),
 's17': ('Source code: every change goes through a pull request into a protected dev branch, and only one required check can let it merge. '
         'Artifacts: every run keeps its test results, scans, SBOMs and the release bundle, so we can always inspect what happened.', 'source code management, artifact management'),
 's18': ('A pull request fans out into parallel checks and they all join into one required check. '
         'Press V: beside it, the security workflows report but do not block the merge.', 'quality gate, SAST/secrets/IaC lanes'),
 's19': ('After merge, we build one bundle, scan the exact images inside it, and sign it before anything is uploaded. '
         'Press V: we log in to AWS without stored keys, and the new version only goes live if its health check passes.', 'SBOM, provenance, container scan, deploy'),
 's20': ('After every deploy, ZAP scans the running site. Press V for the real result: no High findings, and four Medium ones, all from one Content Security Policy gap we know how to fix.', 'DAST'),
 's21': ('SAST: CodeQL flagged three alerts and we closed each with a written reason. '
         'Press V for SCA: a new advisory blocked our merges for real until we fixed it.', 'SAST, SCA'),
 's22': ('These are problems the pipeline caught that normal tests would not. The lesson for us: check what you actually ship, not just the source code.', 'technical findings'),
 's23': ('Now I will show it live in GitHub. If the network fails, I will play the recording instead.', 'CI/CD live demo'),
 's24': ('Now the product. Two accounts are ready. We create a group, invite a friend, add a photo and a video, chat, watch the film, save it, and then try to break in as an outsider.', 'system demo overview'),
 's25': ('While it plays: the owner names the group and picks a shared prompt, which gives everyone a common theme. Press → when the new group appears.', 'UC02 create group'),
 's26': ('While it plays: the code works once and expires in a day, and the server decides who becomes a member. Press → when both accounts show the same group.', 'UC03 invite and join'),
 's27': ('While it plays: take a photo, pick a look and seal it; after that nobody can see it until the film. Press → when it shows Sealed.', 'UC05 photo'),
 's28': ('While it plays: video and photos share one weekly allowance, and the server enforces it, not just the app. Press → when the counts update.', 'UC04/UC06 video, allowance'),
 's29': ('While it plays: a message appears on the other phone without refreshing; that is the Observer pattern from earlier. Press → after the reply shows.', 'UC11 chat'),
 's30': ('While it plays: this capsule has closed, so the server built the film; now we watch it together. Press M only if you want sound, and → at the end screen.', 'UC07/UC08 cycle close, film'),
 's31': ('While it plays: after the premiere the film stays in Archive, and a member can save it as an MP4. Press → when the download opens.', 'UC12/UC13 archive and save'),
 's32': ('While it plays: an outsider tries the used invite code and is refused, and the group never appears for them. Press → after the refusal.', 'privacy, access control'),
 's33': ('Now quality. Performance: our scripted load test passed every stage up to a hundred users. '
         'Then we pushed it: it breaks at two hundred users, but it slows down rather than failing. '
         'The cause is not the CPU; it is that the server talks to the database through one connection.', 'performance, load test, stress test'),
 's34': ('Scalability: our model predicted this limit, and the stress test confirmed it. So the next steps are clear: an async database pool first, then a second server. '
         'Maintainability is the pipeline you just saw: every change has to pass the same tests and checks before it ships. Thank you, I am happy to take questions.', 'scalability, maintainability'),
}

LIVE = [
    'Pull request checks: the one required Quality check, with security workflows beside it.',
    'Quality run: the parallel jobs joining one result; open the artifacts list.',
    'CodeQL alert 56: the rule, the line, and our written reason for dismissing it.',
    'Deploy dev run: wait for Quality, build, scan, sign, install.',
    'Deploy steps: the scan of the exact images happens before upload.',
    'Attestation: the signature ties this manifest to this commit and workflow.',
    'ZAP report: zero High, four Medium, all Content Security Policy.',
    'Hosted health: the live version and the database are ready. Back to the slides.',
]
