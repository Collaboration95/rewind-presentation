# Rewind · final presentation outline

27 October 2026 · 14:30 SGT · Team 14 · Gopal Guruprasath

33:00 planned delivery + 2:00 interruptions = 35:00 hard limit. Q&A follows.

| Section | Clock | Budget | Main slides |
|---|---|---:|---:|
| Intro and project management | 00:00–03:00 | 3:00 | 4 |
| Analysis, design and patterns | 03:00–08:00 | 5:00 | 8 |
| Testing | 08:00–11:00 | 3:00 | 5 |
| CI/CD demonstration | 11:00–21:00 | 10:00 | 8 |
| System demo and quality attributes | 21:00–33:00 | 12:00 | 11 |

## Presentation sequence

28 narrative frames and 8 feature clips. Detail frames C5, C7, C15 and C11 follow their main frame (V opens, V returns); storyboards U1–U4 follow D2 (S). The arrow keys skip both. Everything else cut from the main path is a backup frame.

| Physical page | Anchor | Section | Clock | Content |
|---:|---|---:|---|---|
| 1 | s1 | 1 | 00:00–00:10 | A month of moments. One film |
| 2 | s2 | 1 | 00:10–01:00 | Everyday moments need a shared reason to return |
| 3 | s3 | 1 | 01:00–02:00 | Four sprints took Rewind from foundation to hosted real accounts |
| 4 | P1 | 1 | 02:00–03:00 | Sprint 1 burned down cleanly; effort was split equally |
| 5 | s4 | 2 | 03:00–03:30 | Fourteen use cases follow one private-group journey |
| 6 | s5 | 2 | 03:30–04:05 | One Node application keeps rules close to transactions |
| 7 | s6 | 2 | 04:05–04:40 | Analysis responsibilities become named implementation modules |
| 8 | s8 | 2 | 04:40–05:30 | Durable claims make a repeated tick safe: close, claim, render, fence |
| 9 | PAT | 2 | 05:30–06:15 | Each design problem has a named pattern in a named place |
| 10 | s9 | 2 | 06:15–06:55 | Keys preserve membership and the film’s exact input set |
| 11 | D1 | 2 | 06:55–07:20 | The cycle’s states were fixed before any screen |
| 12 | D2 | 2 | 07:20–08:00 | Each screen renders one state of the cycle |
| 17 | s10 | 3 | 08:00–08:40 | Twelve test types each catch a different failure |
| 18 | TU | 3 | 08:40–09:20 | Unit and component tests pin behaviour, like the “Try again” bug |
| 19 | TI | 3 | 09:20–09:55 | Integration tests call real routes, then rerun on PostgreSQL 17 |
| 20 | TE | 3 | 09:55–10:30 | End-to-end: a real browser, the installed PWA and WCAG 2.1 AA |
| 21 | T10 | 3 | 10:30–11:00 | Security is tested in the suites and scanned in the pipeline |
| 22 | C1 | 4 | 11:00–11:45 | One change passes four gates; colour says what a failure blocks |
| 23 | C3 | 4 | 11:45–12:30 | Protected branches carry source; every run leaves results we can inspect |
| 24 | C4 | 4 | 12:30–13:20 | Nine Quality jobs feed one required merge check; security reports beside it |
| 26 | C6 | 4 | 13:20–14:10 | Deploy scans and signs the exact bundle, then activates only if healthy |
| 28 | C8 | 4 | 14:10–14:55 | ZAP scans hosted dev after every deploy: 0 High, 4 Medium (CSP) |
| 30 | C10 | 4 | 14:55–15:45 | SAST findings are triaged with reasons; SCA blocked merges until fixed |
| 32 | C17 | 4 | 15:45–16:25 | The pipeline caught problems that source-level tests could not |
| 33 | C18 | 4 | 16:25–21:00 | Demo route: eight clicks from pull request to running site |
| 34 | s19 | 5 | 21:00–21:15 | A private-group journey runs from prompt to film |
| 35 | F3 | 5 | 21:15–22:00 | A shared prompt gives the group a common starting point |
| 36 | F4 | 5 | 22:00–23:00 | One accepted invitation creates one private membership |
| 37 | F5 | 5 | 23:00–24:00 | A submitted photo becomes a sealed moment |
| 38 | F6 | 5 | 24:00–25:10 | Video and photos share one enforced weekly allowance |
| 39 | F7 | 5 | 25:10–26:05 | Stored messages and live updates keep the group connected |
| 40 | F9 | 5 | 26:05–27:10 | The cycle closes, and the group watches its film |
| 41 | F11 | 5 | 27:10–28:15 | Archive keeps the film available after its premiere |
| 42 | F12 | 5 | 28:15–29:15 | A spent invitation gives an outsider no group access |
| 43 | PERF | 5 | 29:15–31:15 | A scripted load test: 100 users on hosted dev, p95 1.34 s, zero errors |
| 44 | s20 | 5 | 31:15–33:00 | The capacity model shows where to scale next |

Design section: the statechart D1 (page 11) is followed by the full-bleed UI flow page D2 (page 12, opens on flow 3). There is no design jump any more; seq-cycle-compile and seq-cycle-release stay as backups B16 and B17. Installation and sign-in are B32/B33. Accounts are ready before the main demo. The reveal clip opens the completed capsule The little things.

## Q&A backups

| Anchor | Question / view |
|---|---|
| U1 | UI flow 1 · Join a private group |
| U2 | UI flow 2 · Contribute within the allowance |
| U3 | UI flow 3 · Cycle lifecycle to archive |
| U4 | UI flow 4 · Outsider is denied |
| C5 | Security workflows run beside Quality and keep their findings |
| C7 | Keyless AWS access and a health check decide activation |
| C15 | DAST: 0 High, 4 Medium, all from one Content Security Policy gap |
| C11 | SCA: a new zod advisory blocked merges until we fixed it |
| B1 | Analysis separates interaction, coordination and state |
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
| B30 | Hosted dev activates after candidate health succeeds |
| B31 | Packaging and runtime boundaries exposed useful defects |
| B32 | Installation keeps the app one tap away |
| B33 | Sign-in returns the member to the private-group journey |
| B34 | Every steady load stage stays below the latency target |
| B35 | Measured throughput rises with the active user count |
| CB1 | Recorded walkthrough · PR checks to hosted dev |
| CB2 | Branch protection: dev automates the gate; main adds a human review |
| CB3 | Deploy job steps in GitHub, in the order of the stage diagrams |
| s7 | Durable claims keep repeated cycle work safe |
| C2 | Colour says what a failure blocks; shape says what the element is |
| C9 | Nine kinds of check, each with a recorded result and a link |
| C12 | Secrets are checked at push, on the PR and across history |
| C13 | Trivy blocks risky images; IaC risks need dated exceptions |
| C14 | SBOM and provenance bind shipped bytes to scans and workflow |
| C16 | Tests and coverage gate the merge and are kept as artifacts |
| T1 | Static checks reject style, type and layering errors |
| T2 | Component tests check screens and state without a device |
| s11 | “Try again” must return to a usable viewfinder |
| T3 | API tests call real routes on a running server |
| T4 | The server suite runs again on PostgreSQL 17 |
| T5 | Repository tests stop the architecture and policies drifting |
| T6 | Deployment scripts are tested offline with injected failures |
| T7 | Playwright drives the exported app in a real browser |
| T8 | The PWA build is checked the way it will be installed |
| T9 | Axe and keyboard tests check the main screens for WCAG 2.1 AA |
| T11 | A scripted load test drives the hosted API in five stages |
| T12 | 100 concurrent users stay under the 2-second target, error-free |
| F8 | Reminder permission leads to an explicit weekly choice |
| F10 | The reveal turns sealed contributions into one shared film |

## Playback and source files

- deck.html: every slide and full speaker notes; images and posters are embedded.
- SCRIPT.md: word-for-word delivery and clip-clock cues.
- clips/ci-cd-40344230832.mp4: 11:26 stage edit (backup CB1); ../videos/cicd/cicd-demo.mp4 is the 11:50 source backup.
- cicd-section/: CI/CD figures (PlantUML), cropped GitHub screenshots and the staging README.
- clips/device/ and clips/hosted-device/: portrait feature derivatives; ../videos/demo.mp4 is the complete system backup.
- ../load-test/results/summary.json: hosted run; 100 VUs, p95 1,336 ms, 17.84 req/s, 6,038 steady requests and zero errors.
- ../pipeline-run-40344230832/: manifest, SBOM, Trivy, ZAP and same-commit IaC JSON.
- ../records/: five named members, agreed effort, agile records and all four sprint charts.
