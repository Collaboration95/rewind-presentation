# Rewind presentation: handover

## Restyle and testing expansion · 27 Oct 2026, ~10:50 SGT

- **Style:** calm light-green palette (`#EEF4EF` background, `#15281F` ink, `#1F6B55` single accent, deep-green `#163A2F` cover), sans-serif section labels instead of mono kickers, no mono captions or table headers. UML and chart slides stay full-width on white. Overrides live in `deck/restyle.py`.
- **References removed:** every source/document footer, dated "checked on" strips, audit/file-path lines and the B25 "Source:" line. Footers now show only the slide counter. CI/CD slides (s18, B26–B31) only got the footer removal and palette.
- **Testing (Section 3) is now 14 slides in 3:00:** a 12-row matrix (type × tool × count × when it runs), then one slide each for static checks, Jest, the “Try again” regression, server/API, PostgreSQL, repository rules, deploy fixtures, Playwright, PWA, accessibility, security, load-test method and load-test results. Each has a real count, the tool, one example test (file and name) with the bug it catches, and a pipeline badge. Facts were checked against origin/dev 2390589. Code is in `deck/testing_slides.py`.
- **System demo s20** now covers only scalability (capacity projection, scale-out, maintainability), because the measured results moved to testing. The chart legend is now coloured. Section times are unchanged: 3:30 + 5:00 + 3:00 + 12:00 + 14:30 = 38:00.
- **Deck:** 26 main + 10 feature + 35 backup = **71 frames**; the PDF is re-exported (71 pages). The design jump is now **8 → 52 (B16) → 53 (B17) → 9**. You can also use the hashes #B16 and #B17.
- **QA:** all 71 frames captured at 1280×720. No overflow, no text under 14 px, no page errors. Backup of the pre-restyle files is in `deck/out/pre-restyle-backup/`.
- **Count notes:** root tests show **131**, which is the 124 from the last full run plus 7 tests added by #592/#594 (not re-run). Patched-dependency tests are named without a count.

## Final presentation handoff · 27 Oct 2026, 02:59 SGT

The remaining preparation is complete. **Talk: today, 27 Oct, 14:30 SGT. Gopal Guruprasath presents all five sections.**

- Integrated the final hosted load run and fresh charts: **100 VUs, p95 1,336 ms, 17.84 req/s; 6,038 steady requests, zero errors**. Updated the fitted projection to 22.0 req/s per-host ceiling and the 250/500/1000-user curves.
- Integrated the CI/CD recording as a **11:26 stage film inside its 12:00 slot**. Its 11:50 original remains in videos/cicd/. Supporting diagrams and detailed findings are B26–B31. The filmed PR Quality 40343459119 is distinguished from Deploy dev 40344230832 and its same-commit dev Quality 40344231052.
- Built **ten separate feature slides** in realistic iPhone frames: create → invite/join → photo → video/allowance → chat → reminder → film ready → watch → Archive/save → outsider denied. Main playback is 9:30. Installation/sign-in are B32/B33. Fresh hosted photo/video captures and the hosted reminder-settings cut are integrated.
- Added full spoken notes to every frame and tightened SCRIPT.md. Timing is **3:30 + 5:00 + 3:00 + 12:00 + 14:30 = 38:00**, with 2:00 for interruptions and a separate 5:00 Q&A.
- Checked lecturer DOCX/PPTX and assessor feedback; repaired pattern rationale, retained the real IaC findings JSON, aligned provenance verification with the demonstrated manifest, and corrected run attribution.
- Captured and inspected **all 59 frames at 1280×720**. Bounds, images, controls and page-error checks pass; all 23 UMLs are full width, minimum fitted text 14.055 px. Re-exported the **59-page PDF** and inspected its changed pages.

### Final files

| Use | File |
|---|---|
| Present with embedded videos and full notes | [deck/deck.html](deck/deck.html) |
| Static slide backup | [deck/out/rewind-presentation.pdf](deck/out/rewind-presentation.pdf) |
| Word-for-word script and clip-clock cues | [deck/SCRIPT.md](deck/SCRIPT.md) |
| Sequence, timings and Q&A anchors | [deck/OUTLINE.md](deck/OUTLINE.md) |
| Final requirements and visual QA | [deck/QA-REPORT.md](deck/QA-REPORT.md) |
| Stage pipeline film | deck/clips/ci-cd-40344230832.mp4 |
| Stage feature films/posters | deck/clips/device/ and deck/clips/hosted-device/ |
| Original complete backup films | videos/demo.mp4 and videos/cicd/cicd-demo.mp4 |
| Raw artifact index | [pipeline-run-40344230832/INDEX.md](pipeline-run-40344230832/INDEX.md) |
| Capture, playback and artifact checks | deck/out/resume-qa/FINAL-CHECK.json and related reports |

### Before 14:30

1. Keep the presentation-prep folder together. Open **http://127.0.0.1:8778/deck/deck.html** in Chrome and press F for fullscreen; the existing server currently serves the final deck. If starting it again later, run `./deck/serve.sh` from presentation-prep. Use the HTML for video playback and keep the PDF ready as the static backup.
2. Put SCRIPT.md on a second screen or print it. Rehearse **Space/click** to play/pause, **Arrow** to advance, **M** for optional film sound, **R** to restart and **O** for the overview. Clips begin paused and muted. N displays notes during rehearsal.
3. Rehearse the design jump **8 → 40 → 41 → 9** (type a physical page number, then Enter) inside the same 57-second sequence explanation. Check projector legibility, speaker level and the pipeline/video transitions once.

The orchestrator nudge stopped after two attempts. The app was found as T3 Code (Beta); System Events blocked keystrokes: `osascript is not allowed to send keystrokes. (1002)`. Type Continue manually in that thread if needed. Presentation files are ready independently.

No application repository changes, pushes, merges, workflow dispatches or AWS operations were performed. The earlier sections below retain the overnight work record.

---

Written Mon 26 Oct 2026, about 22:10 SGT. **The talk is Tue 27 Oct at 14:30 SGT.** A fresh
agent or the owner should be able to pick up from this file alone. Detailed evidence is in
`audit/*.md` next to this file. Each audit file cites `file:line` and run IDs.






## 0f. Resume plan (27 Oct, 00:19 SGT): orchestrator out of usage

- A Sol xhigh agent (`rewind-resume-0229-20261027`) is already running. It waits until **02:29 SGT**, tries once to nudge this T3 thread (osascript: activate, then type "Continue" + Enter), then does everything in [RESUME-BRIEF.md](RESUME-BRIEF.md):
  - add the CI/CD video and the final load-test results to the deck;
  - rebuild the system demo as one feature per slide, each clip in an iPhone frame with presenter-controlled playback, and sign-in moved out of the main flow;
  - check the slides and script against the requirements;
  - run 1280×720 QA and re-export the PDF;
  - update this file.
- If the T3 nudge fails, just type "Continue" in the thread yourself.

## 0e. Freeze lifted (26 Oct, ~23:40): build phase

- **Merged tonight:** #591 (pipeline unblock), #595 (DevSecOps artifacts and DAST), #596 (CI FFmpeg/timeouts), #594 (release cutover option), #592 (load test and performance.yml). Release and main are parked: only Andrew's checkmark is needed, and the talk runs from dev.
- **Shared brief for all agents:** [BRIEF-SHARED.md](BRIEF-SHARED.md), including the diagram file contract that writes to `deck/uml/<id>.svg`.
- **Agents running (all GPT-6.1 Sol):**

| Agent | Output |
|---|---|
| UML-SAD (high) | ✅ **DONE (27 Oct ~00:20).** 16 figures (8 contract + 8 split parts), `.puml/.svg/.png`, verified vs dev 2390589, min text 14.33 px at 1280×720 when full width. Index: [deck/uml/README-SAD.md](deck/uml/README-SAD.md) |
| UML-ARCH (high) | ✅ **DONE.** 7 figures (pattern-storage/observer/persistence, er-core 9 tables, deploy-dev, pipeline, artifact-flow), verified vs dev 2390589, ≥14 px full width. Index: [deck/uml/README-ARCH.md](deck/uml/README-ARCH.md) |
| Deck (high) | ✅ **DONE.** [deck/deck.html](deck/deck.html), [PDF](deck/out/rewind-presentation.pdf), [OUTLINE](deck/OUTLINE.md), [SCRIPT](deck/SCRIPT.md) (timing + Q&A). 23 SVGs, 12 clips, notes on every slide. **Waiting on** `deck/clips/ci-cd-40344230832.mp4` from the CI/CD agent |
| CI/CD video + load re-run (high) | ✅ **DONE.** [videos/cicd/cicd-demo.mp4](videos/cicd/cicd-demo.mp4) (11:50), SHOTLIST (30 shots), 35 backup PNGs. Load re-run (local runner → hosted dev): 100 VUs, p95 1,336 ms, 17.84 req/s, 6,038 requests, 0 errors; RESULTS.md + 3 charts + 250/500/1000 projections. The `performance.yml` dispatch returns 404 until the workflow is on main. #586 now approved (release still parked) |
| Deck QA + fixes (xhigh) | ✅ **DONE.** Fixed UML sizing, charts, counts, wording; 57 slides + 17 PDF pages checked; script 38:00. Left for the resume agent: CI/CD video into `s18`, final load results into `s20` and `B11`, then re-export. See [deck/QA-REPORT.md](deck/QA-REPORT.md) |
| iPhone demo (xhigh) | ✅ **DONE.** [videos/demo.mp4](videos/demo.mp4) (11:12, 1080p30), 12 feature clips in `videos/clips/` (40–80 s each), narration in [videos/SHOTLIST.md](videos/SHOTLIST.md). iPhone 17 Pro simulator on hosted dev; real film with 5 moments; Archive download + outsider denial shown |

- **Next, after they finish:** coordinator QA pass (diagrams vs code, deck at 1280×720), owner rehearsal, freeze dev merges from 12:00.

## 0d. First full DevSecOps run (26 Oct, ~23:05). This is the run to demo.

- **#595 merged** (`aea7478`). Deploy dev run **40344230832**: deploy ✅, then DAST ✅.
  https://github.com/Collaboration95/rewind-app/actions/runs/40344230832
- **Artifacts** (copies in `pipeline-run-40344230832/`):
  - `release-manifest.json`: security_gate pass; commit, run, Quality run 40344231052, sha256 of the bundle, SBOMs and scans.
  - `sbom-runtime/web.cdx.json`, `trivy-runtime/web.json`.
  - The signed bundle `dev-release-bundle-*`.
  - The ZAP reports (HTML, JSON, MD).
- **ZAP findings:** 0 High, 4 Medium (all CSP: no-fallback directive, wildcard, script-src and style-src unsafe-inline), 7 Low, 6 Info. The CSP findings are a good "technical finding" to present.
- **#596 merged:** static FFmpeg plus longer timeouts for the apt-heavy jobs. **#594 merged** (`565e787`): `operation=cutover` is on dev.
- **#592 (load test):** CodeQL flagged 3 alerts (#54–56) in `scripts/load/hosted.mjs`. All were dismissed as 'used in tests' with a written reason (a real SAST triage example for the slides). The branch has been updated; merge once green.

## 0c. Load test (26 Oct, 23:15)

- Results are in `load-test/`.
- The mixed 100-VU run overlapped the #591 deploy and recorded 10.88% errors. The read-only re-run after the deploy passed: p95 625 ms, 18.4 req/s, 0 errors.
- **TODO:** once the deploys finish (#595, #594, #592), re-run the mixed profile on a quiet host, using the `performance.yml` workflow or `scripts/load/` from the `../rewind-loadtest` worktree, and refresh the charts.

## 0b. Release status (26 Oct, 22:55)

- **Infrastructure is up and drift-free.** Host `rewind-release` is running, release PostgreSQL is available, CloudFront `d2r0xzy7vz590e.cloudfront.net` is healthy, Cognito is configured, and Terraform shows 0 changes. Cost: US$22/month, already running.
- **The app was never installed**, so the release URL returns 504 until the first Deploy release.
- **PR #594 adds `operation=cutover`** to Deploy release (install, then import into PostgreSQL, in one approved run). The coordinator merges it when its checks pass.
- **Two ways to go live.** Full steps are in [RELEASE.md](RELEASE.md).
  - **Simple (works overnight, no coordinator needed mid-run):** Andrew approves #586 → merge → the push-triggered Deploy release runs `install` (SQLite) → Andrew approves the `release` environment → live.
  - **Full PostgreSQL cutover:** merge #586 → cancel the auto run → dispatch `operation=cutover` → Andrew approves → the coordinator must inspect the receipt and apply the #562 Terraform within 25 min. Do this in the morning, while the coordinator is active.
- **Promote only after tonight's PRs land on dev:** #594, the DevSecOps batch and the load test #592. Ask Andrew to approve #586 after that, ideally 08:00–09:00.

## 0a. Owner direction (26 Oct, 22:45): execute now

- **Release environment must be up.** Non-negotiable. Andrew (AndrewNguyenLKN) will approve the main promotion review and the `release` environment deployment. Demos still run from dev.
- **System demo:**
  - Short per-feature clips filmed in the iPhone Simulator; the starting and final features are enough.
  - Stock clips and 1:1 HTML mocks are allowed.
  - **No disclaimer or "simulated" text** in any footage, and the cycle length must never show.
- **Load test:** a real run on hosted dev plus a capacity-model projection ("measured" and "projected" columns, no other disclaimers).
- **Agents running:**

| Workstream | Agent | Output |
|---|---|---|
| Release bring-up | Codex Sol xhigh | `RELEASE.md`, worktree `../rewind-release-up` |
| Pipeline artifacts batch (A2–A8, DAST included) | Codex Sol xhigh | `PIPELINE-ARTIFACTS.md`, PR to dev |
| iPhone demo clips | Codex Sol xhigh | `videos/` (clips, demo.mp4, SHOTLIST.md) |
| Load test + capacity model + performance.yml | Codex Sol | `load-test/`, PR to dev |
| Burndown, team, agile records, findings | Codex Sol | `records/` |

- **#591 MERGED 26 Oct ~22:38 SGT** (`47ea5f0`). It also replaced the apt FFmpeg install in CI with a verified static build, because the Ubuntu mirror crawled. Deploy dev run 40341542790 succeeded at about 22:46 SGT: hosted dev runs 47ea5f0, and new groups get 30-minute cycles.
- Records done: `records/` (TEAM, AGILE, FINDINGS, burndown and velocity charts). The chart footers still carry disclaimer lines, and the Sprint 2 'opening scope' caption doesn't match the chart; fix both during slide styling.
- **Coordinator:** merges, then the agents' PRs. After that, freeze, and only then do slides and diagrams.

## 0. Earlier owner direction (26 Oct, 22:30)

- **Freeze:** no slides or diagrams until the fixes in [FIX-LIST.md](FIX-LIST.md) are done and merged. Build the deck from the frozen state.
- **Answers:**
  - No sign-up flow; use pre-made accounts.
  - Team: all five names. Sang Haoxiang is listed with minimal contribution; the others' contributions come from the progress reports.
  - Effort split equally, labelled "agreed". Meetings held: project planning, Sprint Planning, Review.
  - The main A&D use case is CU-B (cycle close → film).
  - Fork the FlickPond deck framework.
  - Simulation is allowed, e.g. scripted Friend and Outsider browsers, or an early-triggered push labelled as such.
  - Run everything off dev. Main promotion needs a teammate's approval.
- Still open: cycle length (30 min applied) and push approach. Both were explained to the owner.

## 1. The brief

Lecturer email: 40 min of presenting, then 5 min Q&A, and lecturers may interrupt. **The owner
(Gopal Guruprasath) presents all five sections alone.**

| # | Section | Time | Backup |
|---|---|---|---|
| 1 | Project intro + PM summary | 3–4 min | |
| 2 | Analysis & design + design patterns | 5 min | |
| 3 | Types of testing | 3 min | |
| 4 | CI/CD pipeline demo | 10–12 min | recorded video required |
| 5 | System demo | 12–15 min | recorded video required |

Assessor feedback from the owner's other talk (FlickPond, 26 Oct) carries over:
`../presentation-feedback-carryover.md`. In short:
- Formal UML with real class and function names: 1–2 critical use cases, each with a class diagram and a sequence diagram.
- Patterns shown on the class diagram with role stereotypes.
- SAST **and DAST** shown inside the pipeline picture, saying which checks block and which only report.
- Claim headlines, 15–20 main slides, every figure dated "as built".
- A wrong diagram costs more than a missing one.

Target look: the FlickPond PDF the owner attached, at
`~/.t3/userdata/attachments/1efad8e5-…-pdf.pdf` (24 pages). It has a cream background, a mono
kicker such as "SAD · 03a ANALYSIS MODEL", a claim headline, a PlantUML figure on a white card
and an explanation column.

## 2. Where we are (honest status)

| Area | Status | Detail |
|---|---|---|
| Deck | **Must be rebuilt.** The current `rewind.html` + `rewind-script.md` are untracked files in the main checkout. They follow the old outline (no testing section, no pipeline demo), have no UML, and use topic headlines. | audit/A-deck.md |
| UML | **None of the existing figures are presentable.** The 137 report SVGs are informal and 398 commits stale; some still say SQLite. Verified PlantUML drafts now exist for design classes, statecharts, deployment and ER (`uml-drafts/`). Still missing: use-case model, analysis BCE classes, design sequences. | audit/B1, B2 |
| Patterns | Real in code: media storage Strategy + S3 Adapter, PostgreSQL Adapter, `RealtimeHub` Observer, reminder provider + outbox. State is implemented as persisted states plus guarded functions, not GoF State classes. **Don't claim** a sign-in Strategy or a MediaCapabilities Proxy. `patterns.json` cites a file that doesn't exist (`src/domain/cycles.ts`). | audit/B2 |
| Testing | **Strong and measured.** `test:fast` 2,802 tests, 0 fail; frontend coverage 89.6% statements, server about 85.7% lines; PostgreSQL suite 989 pass; Playwright 41/41 in CI; perf script p95 6.5 ms. Only the aggregate gate blocks merges. | audit/E-testing.md |
| Pipeline | **Was red for every new PR since 24 Oct** (zod advisory in npm audit, and an ffmpeg pin Alpine no longer ships). **Fix PR #591 open, all checks green except 2 server jobs still running.** | audit/C, D |
| DevSecOps | Present: CodeQL (SAST, report-only), npm audit (SCA, **blocking**), Trivy image + IaC scans + CycloneDX SBOM (report-only, PR path-filtered), GitHub secret scanning + push protection, GitGuardian, OIDC to AWS, release approval gate. **Missing: DAST** (ZAP job written, not pushed yet), signing/provenance. | audit/C-devsecops.md |
| Hosted dev | Up: https://d2m6kz76y4kuvm.cloudfront.net, `/api/health` OK, PostgreSQL, serving `f6cd896`. **Release env is down** (504; never installed). Demo on dev only. | audit/D, F1 |
| System demo | **Not recorded, never rehearsed.** A film needs the cycle to close: the default cycle is 28 days. I already applied a 30-minute cycle on dev (see §3); it takes effect at the next deploy. Push reminders are weekly (Sunday 19:00) and **cannot fire before the talk**. Cognito inside the iPhone Home Screen app is **unverified**. | audit/F1-system-demo.md |
| PM | Team 14: Nguyen Kim Long, Gopal Guruprasath, Jiang Jiayu, Phan Mai Tan Loi, Sang Haoxiang. 329 issues (319 closed), 213 merged PRs, Sprints 0–3. **No measured effort exists** (scrum page says "to fill"). Sprint reports record that one member did no work: the team must decide the wording. 7 open `mvp` issues. | audit/G-pm.md |
| Video tooling | Built and tested on this Mac: `video-toolkit/` (render.py edit lists → 1080p, stamps, captions, phone frames). Real screen capture and iPhone footage are untested; do a 10 s check first. | audit/F2-video.md |

## 3. In flight right now (check these first)

1. **PR #591** `guru/presentation-pipeline-fixes` → dev
   (https://github.com/Collaboration95/rewind-app/pull/591):
   - Changes: a zod 4.6.6 override scoped to `@expo/cli`, and the ffmpeg pin changed to `8.1.3-r0`.
   - Locally: `npm audit` 0 high, `build:web` OK, `test:fast` all pass.
   - CI: everything passed except the "Server tests" and "Server tests on PostgreSQL" jobs, which were still running at 22:05.
   - **Next:** merge when green (Claude may merge per CLAUDE.md). The merge triggers Deploy dev (about 7 min).
2. **DAST branch** `guru/presentation-dast`, committed locally in worktree `../rewind-present-fix` (commit `59e8913` on top of the #591 commit), **not pushed**:
   - It adds a `dast` job to `.github/workflows/deploy-dev.yml`: a ZAP baseline against the hosted dev URL, after deploy, report-only, with results in the run summary and an artifact. It also adds `.zap/rules.tsv`. Root tests and prettier pass.
   - **Next, after #591 merges:** `git fetch && git merge origin/dev` (or rebase), push, open a PR to dev, merge. Its Deploy dev run then shows the DAST job: that is the run to demo.
3. **Terraform (already applied, 22:00):** `infra/terraform/media` with `extra_hosted_settings=["REWIND_REAL_CYCLE_MINUTES=30"]`.
   - The S3 object `_config/dev.env` now contains the key. It reaches the server at the **next Deploy dev**.
   - The setting only affects **groups created after that deploy**; existing groups keep 28 days.
   - The same apply also enforced two least-privilege IAM policy edits that were already merged on dev but never applied. Nothing else changed.
4. **Video toolkit is done:** `audit/F2-video.md`, scripts copied to `video-toolkit/`.
   - Run `render.py <edit-list.yaml>` for 1080p H.264 with a corner stamp, title cards, "wait trimmed" badges and phone frames. `templates.sh` holds the tested ffmpeg templates.
   - The installed ffmpeg 9.0.2 has no `drawtext` or `subtitles` filter, so text is rendered as PNG with ImageMagick and overlaid.
   - Estimated time: CI/CD video 2.5–3 h, system demo 3–4 h.
5. **#591 CI flake (22:15):** both server jobs hung at "Install FFmpeg" (the known apt-get hang). The run was cancelled and `gh run rerun 40335365737 --failed` re-ran them.

## 4. Decisions only the owner can make

1. **Demo cycle length:** 30 min is applied. The F1 agent suggested 60. Shorter allows more takes, longer means a calmer capture window. Keep 30 unless told otherwise.
2. **Second person or phone** for the "Friend" account tonight? If not, the Friend runs on the laptop (desktop browser or Playwright) and the outsider uses a third browser profile.
3. **Push reminder:** show the opt-in only and say delivery is weekly (recommended, honest), or stage a local push and label it as staged.
4. **Sign-in shot:** Cognito sign-up with the email code, or sign-in with a pre-made account (faster, recommended).
5. **Team slide:** all five names. Decide how to word Sang Haoxiang's non-contribution, or whether to say nothing on the slide.
6. **Effort split:** give percentages or hours, labelled "agreed" or "estimated" on the slide (nothing is measured).
7. **Roles and ceremonies:** who is PO and who is Scrum Master; whether Planning, Review and Retro were held with dates, and whether daily scrums were held. Otherwise the slide says "outputs recorded in GitHub, no minutes".
8. **A&D use cases:** recommended **CU-B "Close the cycle → compile → release the film" (UC07+UC08)** as the main one, and **CU-A "Contribute a photo within the weekly allowance" (UC05+UC06)** as the second or backup.
9. **Deck tooling:** recommended to fork the FlickPond HTML deck framework (`dc2-rescue/project-documentation/presentation/site/deck.html`, one file, keyboard navigation, notes, clip slides) and restyle it to the cream look of the PDF. PlantUML → SVG.

## 5. What needs to be done (priority order)

**P0, the talk fails without these:**
- A. Merge #591, then the DAST PR, so the pipeline is green and has DAST in a real run.
- B. Deck shell plus 20 main slides with speaker notes, timed to the five sections (slide table in audit/A-deck.md §3).
- C. CI/CD demo: the 10-shot, 12-min storyboard (audit/D-cicd-demo.md §5) uses existing run pages. Rehearse it live, and record the backup video.
- D. System demo: film the real app on hosted dev using the 14-scene storyboard (audit/F1-system-demo.md §4), edit it into a 12–15 min video, and narrate live over it.

**P1, the assessors explicitly asked for these:**
- E. Formal UML, verified against the code:
  - use-case model;
  - for CU-B: BCE analysis classes, design class diagram with pattern roles, numbered design sequence;
  - pipeline activity diagram with every scan tagged BLOCKS / REPORTS, including DAST;
  - deployment diagram.
  - Content for each figure is in B1 §3–5 and B2. Drafts are in `uml-drafts/`.
- F. Testing slides (3): pyramid with real counts, type → tool → CI job → blocks? table, and the "Try again" bug from #581 as the example (audit/E-testing.md §8).
- G. PM slides: Sprint strip with counts, effort labelled, open issues dated (audit/G-pm.md).

**P2, backup appendix:** ER subset, ADR PostgreSQL, STRIDE table (doesn't exist yet; verify each control in code), coverage detail, scaling answer, CU-A diagrams, "what blocks a merge".

## 6. Suggested timeline (SGT)

**Mon night:**
- 22:15 Merge #591 → deploy. Then push the DAST PR → merge → deploy with ZAP (about 20 min total).
- 22:30–23:00 **Owner, physical iPhone:**
  - Add to Home Screen, then Cognito sign-in inside the PWA. This is the go/no-go test.
  - Allow camera and mic.
  - Test capture into a rehearsal group created after the deploy, and check that Home shows about 30 min left.
- In parallel, agents: deck shell fork, UML figures, testing and PM slides.
- 23:00–00:30 Film the system demo: take group created at T0, scenes 3–8 in the first 20 min, then cycle close → film → Archive → outsider. Copy the footage to two places.
- 23:30–00:15 Record the CI/CD backup video (12 min, real length). Title card: date and dev SHA.

**Tue:**
- 07:30 Health check; the film still plays in the Archive (premiere lasts 24 h).
- 08:00–11:30 Edit the demo video (captions: date, `dev-<sha>`, "cycle compressed to 30 min"). Finish the deck, speaker notes and backups.
- 11:30–12:30 Export the videos and PDF fallback; keep copies on the laptop and USB.
- **12:00 Freeze merges to dev.** Any merge means a 7-min deploy and a server restart.
- 12:30–13:30 One full timed run-through, including a mid-video pause.
- 14:30 Talk.

## 7. Where things are

- **This folder:** `SWE5006/presentation-prep/`
  - `audit/` holds the 9 reports: A-deck, B1-analysis, B2-design, C-devsecops, D-cicd-demo, E-testing, F1-system-demo, F2-video (pending), G-pm.
  - `uml-drafts/` holds verified PlantUML drafts plus `_style.iuml` (FlickPond skinparams): d1 storage, d2 persistence, d3 reminders, d4 observer, s1 cycle, s2 job, s3 intent, p1 deploy, e1 ER.
  - `plantuml.jar`: render with `java -Djava.awt.headless=true -jar plantuml.jar -tsvg X.puml`, then run separately with `-tpng`, because running both formats in one pass writes only one.
- **Worktrees** (all under `SWE5006/`):
  - `rewind-present-audit`: detached at origin/dev `f6cd896`, node_modules installed, read-only reference.
  - `rewind-present-fix`: branch `guru/presentation-dast` (contains the #591 commit plus the DAST commit). `infra/terraform/media/.terraform` is initialised there (git-ignored).
  - `rewind-app`: the main checkout is **stale** (`a1dc77e`, 143 behind, 82 deletions not committed, already gone on origin/dev). Don't switch its branch. Its untracked `doc/planning/report/presentation/rewind.html` and `rewind-script.md` are the old deck and script. Salvage the script's Do/Expected/Fallback shot lists and its "observed vs claimed" wording.
- **FlickPond reference deck framework:** `NUS/dc2-rescue/project-documentation/presentation/site/deck.html` plus `assets/uml/*.puml` (78 examples), `STYLE.md` and `PRESENTING.md`.
- **Explainer site** (content source, 261 Q&As): `docs/site/content/*.json` → `python3 docs/site/build.py`.
- **AWS:** profile `rewind-terraform-apply`. Media/dev root `infra/terraform/media` uses the backend file `backend.hcl`; copy it from `rewind-app/infra/terraform/media/backend.hcl`, which is git-ignored.
- **PDF export of an HTML deck:** `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --user-data-dir=/tmp/x --no-pdf-header-footer --print-to-pdf=out.pdf "file://$PWD/deck.html"`

## 8. Gotchas

- **Owner media files:**
  - In-app capture uses the camera. A file picker appears only when the camera is denied or unavailable.
  - Files must be MP4 with audio, 15 s or less, 50 MiB or less; photos JPEG or PNG, 10 MiB or less. iPhone `.mov` and HEIC are rejected (convert with ffmpeg).
  - Limits per member per cycle: 5 contributions, 30 s of video in total.
- **On-screen copy says "four weeks" / "Week N of 4"**: caption the compressed cycle in the video.
- **Leave PRs #589 and #590 alone.** Their red runs (40140117765, 40140169768) show the gate blocking a merge.
- **Only one check is required by branch protection** ("Format, lint, typecheck, and test"). CodeQL, Trivy and GitGuardian report but don't block. Say exactly that.
- **Don't run an active or authenticated ZAP scan against hosted dev** (shared data). The baseline is passive only.
- Release needs reviewer `AndrewNguyenLKN` (`release` environment), and promotion PR #586 needs 1 review. Don't click "Review deployments" on stage.
- All 8 IaC scan exceptions expire **31 Oct**. After that, path-filtered PRs fail Release security until they are renewed (after the talk).
- `AGENTS.md` freezes `doc/planning/report/` unless the owner names it. The owner has asked for the presentation to be reworked, so reading the deck there is fine; put new deck work in this folder or a new path.
- Don't mention the post-nightly minor nits from 21–22 Oct (owner preference). Raise only what blocks the talk or the demo.

## 9. After the talk

1. Set the dev cycle back:
   ```
   terraform apply -var 'extra_hosted_settings=["REWIND_REAL_CYCLE_MINUTES=40320"]'
   ```
   Then run `gh workflow run deploy-dev.yml --ref dev`. `release-host.sh configure` never deletes keys, so set the value rather than removing it.
2. Close issues and PRs as appropriate. Renew the IaC exceptions before 31 Oct. Remove the worktrees `rewind-present-audit` and `rewind-present-fix` once merged.
