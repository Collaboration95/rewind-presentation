# Rewind · final presentation outline

27 October 2026 · 14:30 SGT · Team 14 · Gopal Guruprasath

38:00 planned delivery + 2:00 interruptions = 40:00 presentation slot. Q&A follows for 5:00.

| Section | Clock | Budget |
|---|---|---:|
| Intro and PM | 00:00–03:30 | 3:30 |
| Analysis, design and patterns | 03:30–08:30 | 5:00 |
| Testing | 08:30–11:30 | 3:00 |
| CI/CD demonstration | 11:30–23:30 | 12:00 |
| System demo and quality attributes | 23:30–38:00 | 14:30 |

## Presentation sequence

14 narrative frames and 10 feature inserts. Feature playback totals 9:30, with 1:30 for introductions and pauses. The CI/CD stage edit is 11:26, with 0:34 for introduction and closing.

| Physical page | Anchor | Section | Clock | Content |
|---:|---|---:|---|---|
| 1 | s1 | 1 | 00:00–00:15 | A month of moments. One film |
| 2 | s2 | 1 | 00:15–01:10 | Everyday moments need a shared reason to return |
| 3 | s3 | 1 | 01:10–03:30 | Four sprints delivered the hosted private-group journey |
| 4 | s4 | 2 | 03:30–04:03 | Fourteen use cases follow one private-group journey |
| 5 | s5 | 2 | 04:03–04:42 | One Node application keeps rules close to transactions |
| 6 | s6 | 2 | 04:42–05:27 | Analysis responsibilities become named implementation modules |
| 7 | s7 | 2 | 05:27–06:21 | Durable claims keep repeated cycle work safe |
| 8 | s8 | 2 | 06:21–07:18 | A repeated tick reuses work and fences stale completion |
| 9 | s9 | 2 | 07:18–08:30 | Keys preserve membership and the film’s exact input set |
| 10 | s10 | 3 | 08:30–10:06 | Each test layer catches a different integration failure |
| 11 | s11 | 3 | 10:06–11:30 | “Try again” must return to a usable viewfinder |
| 12 | s18 | 4 | 11:30–23:30 | The pipeline connects protected source to a verified deployment |
| 13 | s19 | 5 | 23:30–23:48 | A private-group journey runs from prompt to film |
| 14 | F3 | 5 | 23:48–24:57 | A shared prompt gives the group a common starting point |
| 15 | F4 | 5 | 24:57–26:06 | One accepted invitation creates one private membership |
| 16 | F5 | 5 | 26:06–27:10 | A submitted photo becomes a sealed moment |
| 17 | F6 | 5 | 27:10–28:24 | Video and photos share one enforced weekly allowance |
| 18 | F7 | 5 | 28:24–29:28 | Stored messages and live updates keep the group connected |
| 19 | F8 | 5 | 29:28–30:27 | Reminder permission leads to an explicit weekly choice |
| 20 | F9 | 5 | 30:27–31:16 | The completed capsule is ready for its shared premiere |
| 21 | F10 | 5 | 31:16–32:45 | The reveal turns sealed contributions into one shared film |
| 22 | F11 | 5 | 32:45–33:49 | Archive keeps the film available after its premiere |
| 23 | F12 | 5 | 33:49–34:48 | A spent invitation gives an outsider no group access |
| 24 | s20 | 5 | 34:48–38:00 | Load results identify the next scaling change |

The CU-B sequence uses s8 → B16 → B17 → s9 within the same 0:57 allocation. Installation and sign-in are B32/B33. Accounts are ready before the main demo. The reveal transition opens the completed capsule The little things.

## Q&A backups

| Anchor | Question / view |
|---|---|
| B1 | Analysis separates interaction, coordination and state |
| B2 | Durable state survives interrupted compilation |
| B3 | Capture acceptance checks identity, allowance and media |
| B4 | Relational keys make the private film traceable |
| B5 | The deployment view names each runtime boundary |
| B6 | Coverage and enforcement answer different questions |
| B7 | Storage changes behind Strategy and Adapter roles |
| B8 | Observer distributes chat updates alongside stored history |
| B9 | The persistence adapter preserves a common data-access contract |
| B10 | Agile records retain scope changes and equal effort |
| B11 | The capacity curve follows the closed-user workload |
| B12 | Retained artifacts make the deployment independently inspectable |
| B13 | Acceptance pins and probes the exact media version and replays an existing receipt |
| B14 | One transaction records quota, contribution, processing job and completion |
| B15 | Processing stores an MP4 and proves current ownership before marking ready |
| B16 | The worker claims settled inputs, materialises media and fences finalisation |
| B17 | Stored bytes and the current ready row are verified before publication and archiving |
| B18 | Account and group goals connect to Cognito, chat and web push |
| B19 | Photo and video acceptance include the shared allowance and optional correction |
| B20 | Cycle closure produces a film, premiere, Archive and authorised downloads |
| B21 | Sprint 0 records opening scope and daily delivery |
| B22 | Sprint 1 records opening scope and daily delivery |
| B23 | Sprint 2 records opening scope and daily delivery |
| B24 | Issue closures and merged PRs track sprint delivery |
| B25 | Backlog stories connect sprint goals to delivered use cases |
| B26 | A commit carries tests, inventory and deployment evidence |
| B27 | Pipeline decisions separate merge gates from host activation |
| B28 | Security checks cover code, packages, secrets and running pages |
| B29 | The manifest binds deployed images to their scans |
| B30 | Hosted dev activates after candidate health succeeds |
| B31 | Packaging and runtime boundaries exposed useful defects |
| B32 | Installation keeps the app one tap away |
| B33 | Sign-in returns the member to the private-group journey |
| B34 | Every steady load stage stays below the latency target |
| B35 | Measured throughput rises with the active user count |

## Playback and source files

- deck.html: every slide and full speaker notes; images and posters are embedded.
- SCRIPT.md: word-for-word delivery and clip-clock cues.
- clips/ci-cd-40344230832.mp4: 11:26 stage edit; ../videos/cicd/cicd-demo.mp4 is the 11:50 source backup.
- clips/device/ and clips/hosted-device/: portrait feature derivatives; ../videos/demo.mp4 is the complete system backup.
- ../load-test/results/summary.json: hosted run; 100 VUs, p95 1,336 ms, 17.84 req/s, 6,038 steady requests and zero errors.
- ../pipeline-run-40344230832/: manifest, SBOM, Trivy, ZAP and same-commit IaC JSON.
- ../records/: five named members, agreed effort, agile records and all four sprint charts.
