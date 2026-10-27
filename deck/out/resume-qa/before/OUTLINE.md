# Rewind · presentation outline

27 October 2026, 14:30 SGT · SWE5006 Team 14 · Gopal Guruprasath.

## Timing

| Section | Budget | Clock |
|---|---:|---:|
| 1 · Context and project management | 3:30 | 00:00–03:30 |
| 2 · Analysis, design and patterns | 5:00 | 03:30–08:30 |
| 3 · Testing | 3:00 | 08:30–11:30 |
| 4 · Source, artifacts and CI/CD demonstration | 12:00 | 11:30–23:30 |
| 5 · Feature demonstration, performance and scalability | 14:30 | 23:30–38:00 |
| Questions | 5:00 | after talk |

Twenty main narrative frames; twelve feature clip inserts follow frame 19. Twenty-five backup frames follow frame 20. Inserts retain their own feature labels and timing inside section 5. The overview and PDF contain all 57 frames. Figure pages use a 1280×688 image area beneath a thin claim headline.

## Main narrative

| Frame | Time | Claim / content | Figure or evidence |
|---|---:|---|---|
| 1 | 0:15 | Rewind turns a month of moments into one film | Cover, team, presenter |
| 2 | 0:55 | Small private groups give everyday moments a shared payoff | Problem, 28-day loop, scope |
| 3 | 2:20 | Four sprints moved the product from skeleton to hosted dev | Sprint milestones, dated status, equal team effort, DoD, ceremonies, retro action, burndown/velocity |
| 4 | 0:33 | Fourteen use cases follow one private group journey | uml/uc-model.svg |
| 5 | 0:39 | One Node application keeps the rules close to transactions | uml/arch-logical.svg, decision table |
| 6 | 0:45 | Analysis responsibilities become named implementation modules | uml/a2d-cycle.svg; analysis BCE in B1 |
| 7 | 0:54 | Durable claims keep repeated cycle work safe | uml/class-cycle.svg; problem → candidates → chosen |
| 8 | 0:57 | A repeated tick reuses work and fences stale completion | uml/seq-cycle.svg |
| 9 | 1:12 | Keys connect membership, contributions and durable film inputs | uml/er-core.svg |
| 10 | 1:36 | Test layers catch different failures before integration | Tools, CI jobs, gates and counts; coverage |
| 11 | 1:24 | A failed capture must return to a usable viewfinder | Red/green regression example, performance test type |
| 12 | 1:12 | A commit carries tests, inventory and deployment evidence | uml/artifact-flow.svg; artifact table |
| 13 | 1:36 | Pipeline decisions separate merge gates from deployment gates | uml/pipeline.svg |
| 14 | 1:42 | Security checks cover source, secrets, dependencies and running pages | CodeQL triage; ZAP 0/4/7/6; SCA; gitleaks; IaC |
| 15 | 1:30 | The manifest binds the deployed images to their scans | Real release-manifest.json excerpt; SBOM; Trivy; signed provenance |
| 16 | 1:12 | Hosted dev activates only after the candidate is healthy | uml/deploy-dev.svg; OIDC and rollback |
| 17 | 1:00 | Runtime boundaries exposed the most useful technical findings | FINDINGS: advisory, package pin, schema packaging, SSE, retry |
| 18 | 3:48 | Run 40344230832 connects green Quality to hosted dev | CLI/live steps and clip slot; run timestamps and artifacts |
| 19 | 0:18 | Follow one group from installation to a private film | Feature map; twelve inserts below |
| 20 | 3:12 | Load results guide the next scaling change | Method, measured table, capacity projection chart, maintainability |

## Feature inserts after frame 19

| ID | Time | Feature | Expected clip path |
|---|---:|---|---|
| F1 | 0:45 | Install Home Screen PWA | ../videos/clips/01-install-to-home-screen.mp4 |
| F2 | 0:45 | Account sign-in | ../videos/clips/02-sign-in.mp4 |
| F3 | 1:00 | Create group and prompt | ../videos/clips/03-create-group.mp4 |
| F4 | 1:00 | Invite and join | ../videos/clips/04-invite-and-join.mp4 |
| F5 | 0:55 | Photo with a look | ../videos/clips/05-photo-with-a-look.mp4 |
| F6 | 1:05 | Video and allowance | ../videos/clips/06-video-and-allowance.mp4 |
| F7 | 0:55 | Group chat | ../videos/clips/07-group-chat.mp4 |
| F8 | 0:50 | Weekly reminder | ../videos/clips/08-weekly-reminder.mp4 |
| F9 | 0:40 | Completed capsule and premiere | ../videos/clips/09-cycle-ends-film-ready.mp4 |
| F10 | 1:20 | Watch the film | ../videos/clips/10-watch-the-film.mp4 |
| F11 | 0:55 | Archive and save | ../videos/clips/11-archive-and-save.mp4 |
| F12 | 0:50 | Outsider denied | ../videos/clips/12-outsider-denied.mp4 |

## Q&A backup map

| Backup | Question | Figure / content |
|---|---|---|
| B1 | What did analysis identify? | bce-cycle |
| B2 | What are the cycle states? | state-cycle |
| B3 | How is capture accepted? | seq-capture |
| B4 | Show database detail / why relational? | er-core + PostgreSQL decision |
| B5 | Where is it deployed? | deploy-dev |
| B6 | What is covered and enforced? | Full testing/coverage table |
| B7 | Why Strategy and Adapter for storage? | pattern-storage |
| B8 | How does chat use Observer? | pattern-observer |
| B9 | How does persistence adapt SQLite-style calls? | pattern-persistence |
| B10 | Show agile records and equal effort | Burndowns, velocity, named team |
| B11 | Explain the capacity model | Measured/projected chart and parameters |
| B12 | Where are the scan and provenance outputs? | Security artifact inventory, verification commands |
| B13–B20 | Show full use-case and sequence continuations | seq-capture accept/commit/process; seq-cycle compile/release; use-case access/capture/cycle |
| B21–B23 | Show the other sprint burndowns | Sprint 0, Sprint 1, Sprint 2 |
| B24 | Show full sprint velocity | Issue closures and merged PRs |
| B25 | How do backlog, stories, sprint plans and reviews connect? | Saved backlog census, UC05 story trace, sprint goals and retro actions |

## Sources and integration

Use BRIEF-SHARED.md, audit A–G, records/TEAM.md, AGILE.md and FINDINGS.md, load-test/METHODOLOGY.md and RESULTS.md, PIPELINE-ARTIFACTS.md, and pipeline-run-40344230832/. Later run artifacts supersede older audit statements about missing DAST and pending deployment. Dated testing counts retain the 26 October audit baseline. No release-environment tour. Product cycle: 28 days.

All 23 supplied UML SVGs are embedded at full width. Eight use-case and sequence continuations each have a dedicated backup slide. Four additional backups print every sprint chart and velocity. Still imagery is embedded into the HTML; feature videos remain linked. Feature clips use the final clips directory; pipeline clip slot is clips/ci-cd-40344230832.mp4.

All 23 SVGs supplied by the UML agents are embedded. Detailed use-case and sequence variants are separate backup pages. The PDF prints every diagram and chart. Feature clip playback totals 11:00; section 5 includes 0:18 map and 3:12 performance/scalability.
