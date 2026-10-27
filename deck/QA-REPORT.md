# Final presentation QA · 27 October 2026

**PASS.** All resume-brief integrations are complete. Final deck: **59 frames = 14 narrative + 10 feature inserts + 35 Q&A backups**. Presenter: Gopal Guruprasath, SWE5006 Team 14.

## Requirement parity

Read the official Presentation Guidelines DOCX directly, plus the official briefing PPTX slides 5–7, BRIEF-SHARED.md, RESUME-BRIEF.md, FIX-LIST.md and the carry-over assessor feedback. The current lecturer outline sets a 40-minute presentation slot and a separate five-minute Q&A.

| Requirement | Final coverage |
|---|---|
| Context, problem, scope | s1–s2 |
| Dated status, outstanding issues, milestones, sprint count | s3; current open mvp register rechecked with authenticated gh on 27 Oct |
| Named team and effort per member | s3; TEAM.md; five names, 20% and 10 person-days each, agreed split |
| DoD, ceremonies, retrospective changes | s3; B25; concrete S1→S2→S3 changes |
| Product backlog, stories and sprint plans | B25; UC05 issue trace |
| Every sprint burndown and velocity | B10, B21–B24; Sprints 0–3 |
| Architectural decisions and logical view | s5; real modules and adapter boundaries |
| Formal use cases, analysis→design and analysis classes | s4/s6; B1; B18–B20 |
| Critical design class, sequences and states | s7/s8; B2/B16/B17; CU-A B3/B13–B15 |
| Pattern problem, alternatives and choice | Spoken s7 and B7; Strategy plus S3 transport Adapter; Observer and persistence Adapter B8/B9 |
| Database schema | s9/B4; typed PK/FK/uniqueness and frozen film inputs |
| Testing types, tools, counts, enforcement and complex behaviour | s10/s11/B6; failing-before/passing-after capture recovery |
| Source and artifact management | s18 recording; B26; retained commit/run identities, inventories, hashes and provenance |
| SAST, DAST, SCA, secrets and IaC | s18 recording; B27/B28/B12; actual JSON/SARIF listed in out/resume-qa/artifacts.json |
| SBOM, exact-image scans and provenance | s18/B29/B12; both CycloneDX and Trivy JSONs; four report hashes match manifest |
| IaC raw findings | pipeline-run-40344230832/iac/iac-full.json; 15 findings; same-commit Release security 40344231046 identity retained |
| Technical findings | s18 narration and CodeQL/CSP footage; B31 advisory, package pin, packaging, SSE and retry findings |
| Significant use cases | F3–F12 in requested order, one clip and iPhone frame per slide |
| Main flow begins with create group | Installation/sign-in are B32/B33 |
| Scripted performance | s20/B34/B35; all quiet-host stages pass; 100 VUs p95 1,336 ms, 17.84 req/s; 6,038 steady requests, zero errors |
| Scalability | s20/B11; fitted means and projected one-/two-host curves; persistence/media/shared-state mechanism |
| Maintainability | s18 pipeline and s20 closing explanation |
| Recorded backups | videos/demo.mp4 and videos/cicd/cicd-demo.mp4 preserved; stage-specific MP4s linked locally |
| Single presenter, 28-day product cycle, hosted dev | Main slide/script content and video samples checked |

The first parity pass's three findings are fixed: storage-specific rationale is spoken; real IaC findings and run identity are retained; the demonstrated attestation command verifies release-manifest.json. The final parity pass found one attribution mismatch, now fixed in the visible s18 caption and full narration: filmed PR Quality **40343459119 at 38593b2** is distinct from deployed commit **aea7478**, Deploy dev **40344230832** and its same-commit dev Quality gate **40344231052**.

## Playback and timing

| Section | Budget | Elapsed clock |
|---|---:|---|
| Intro / PM | 3:30 | 00:00–03:30 |
| Analysis / design / patterns | 5:00 | 03:30–08:30 |
| Testing | 3:00 | 08:30–11:30 |
| CI/CD | 12:00 | 11:30–23:30 |
| System / quality attributes | 14:30 | 23:30–38:00 |

38:00 delivery plus 2:00 interruption reserve fills the 40:00 slot; Q&A follows for 5:00. The CI/CD stage film is 11:26 with 0:34 of introduction/closing; the 11:50 original is preserved. The stage edit retains [0,630) and [654,710), omitting the environment-settings shot. Supporting CI/CD slides are B26–B31. Main feature playback totals 9:30 with 1:30 of narration/holds, plus the 0:18 journey map and 3:12 performance discussion.

All 59 slides carry the full spoken script in their embedded notes, matching slides.json. Main clips load paused and muted. Space/P or click plays/pauses; M changes sound, R restarts, and leaving pauses the clip. Navigation, overview clicks, hashes, notes and command cards pass. The CU-B sequence visits physical pages 8 → 40 → 41 → 9 inside its existing 0:57 allocation.

Hosted photo/video footage was newly captured through the actual app and completed both uploads with HTTP 200. The reminder derivative retains the hosted settings sequence. Production receipts and edit manifests are in out/resume-qa/hosted-video/ and clips/hosted-device/. The collecting groups and completed The little things capsule are named correctly in the narration.

## Visual and export checks

Every frame was captured at **1280×720** and inspected in the contact sheets and focused original-size views. The completed replacements, pipeline caption, performance table and print views received final focused checks. Automated bounds: **zero overflow, zero broken images, zero browser page errors**. All 23 UML SVGs are included full width; the minimum fitted text is **14.055 px**. Final check data is out/resume-qa/FINAL-CHECK.json; per-slide measurements and controls are render-check.json; loaded video metadata is media-check.json.

T3 preview was attempted first. Both snapshot attempts returned `Preview automation snapshot timed out after 15000ms.` Captures used the existing documented Chrome/Playwright workflow. The PDF was rebuilt with Chrome headless, without headers/footers: **59 pages, 960×540 pt**, 3.84 MB. Every PDF page title matches the HTML sequence. Changed/demo/performance pages 12–24 and 57–59 were rasterised at 1280×720 and inspected. PDF text passes the stage-wording scan.

Original sources and backup films are preserved. No application repository changes, pushes, merges, workflow dispatches or AWS operations were performed.
