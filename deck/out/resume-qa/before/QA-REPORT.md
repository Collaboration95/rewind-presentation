# Rewind presentation QA · 27 October 2026

**Result:** requirement content and visual checks pass, with the final CI/CD recording and refreshed performance evidence awaiting the parallel agent. Those two integrations are listed precisely below; the deck does not constitute their final acceptance.

**Talk:** Tue 27 Oct 2026, 14:30 SGT · SWE5006 · Team 14 · Gopal Guruprasath, sole presenter.

## Authority and scope

Read BRIEF-SHARED.md, including the full-width layout update; FIX-LIST.md; ../presentation-feedback-carryover.md; deck/OUTLINE.md; deck/SCRIPT.md; both UML READMEs and layout-check-SAD.json; records/TEAM.md, AGILE.md, FINDINGS.md, data and charts; PIPELINE-ARTIFACTS.md; and videos/SHOTLIST.md. Extracted the official presentation guidelines DOCX and the SWE5006 briefing PPTX, including briefing deliverables slides 5–6. Extraction is retained in out/qa/lecturer-requirements.txt.

G = official guidelines; B = briefing; E = lecturer outline in the shared brief; F = assessor feedback. The shared brief's current five-section timetable takes precedence over the older guideline's combined presentation/Q&A allocation. Owner-agreed effort is 20% and 10 person-days per member.

Application code was inspected read-only in ../rewind-present-audit at f6cd8969379ba720fc0508833f138e29475bc32a. Later workflow files and run metadata were read using authenticated gh only. No application repository edits, branch changes, pushes, merges, workflow dispatches or AWS actions were performed. No files under videos/cicd/ or load-test/ were modified. The deck builder reads existing chart PNGs; the parallel agent's production files and final results document were left alone. The performance frame's authored data and the CI/CD clip slot were retained.

## Requirement parity

A tick means the content is present in the actual deck or its attached speaker notes, with the stated source. PENDING identifies the explicitly reserved parallel-agent integration.

| Check | Requirement | Source | Actual slides / artifacts | Result |
|---|---|---|---|---|
| ✓ | Introduction, team and presenter | G/E | s1; sole presenter named | Present |
| ✓ | Context and business problem | G/E | s2: scattered moments, private shared film | Present |
| ✓ | Product scope and limits | G/E | s2; s4; F1–F12; 28-day product cycle | Present |
| ✓ | Current status and outstanding issues | G/E | s3 dated 26 Oct; B10 notes retain seven-item register | Present |
| ✓ | Actual milestones and sprint dates | G/E | s3: Sprint 0–3, zero-based names and dates | Present |
| ✓ | Effort per named team member | G/E | s3: all five names, 20% and 10 person-days each, agreed split; TEAM.md | Present per owner decision |
| ✓ | Sprint count, goals and plans | G/B/E | s3; B25; AGILE.md sprint-plan register | Present |
| ✓ | Definition of Done | G/E | s3 and spoken script: outcome, fast tests, green Quality, batch review, dev merge | Present |
| ✓ | Sprint reviews and retrospective changes | G/B/E | s3; B25; S1 integration → S2 adapters → S3 interaction checks | Present |
| ✓ | Product backlog and user stories | B | B25: backlog census; UC05 story → #313 / #545 / #574; AGILE.md | Added explicit backup |
| ✓ | Burndown charts | B/E | B10: Sprint 3; B21–B23: Sprints 0–2 | Every sprint printed |
| ✓ | Velocity / delivery counts | B/E | s3 summary; B24 full chart; 44/100/145/30 closed issues | Present |
| ✓ | Architectural decisions and logical architecture | G/B/F | s5: modular monolith, transactions, PostgreSQL, S3, Cognito, interfaces | Present |
| ✓ | Analysis → design transition | G/B/F | s6: conceptual BCE responsibilities mapped to real modules, functions and tables | Present |
| ✓ | Formal use-case diagram | G/B/F | s4 overview; B18 access; B19 capture; B20 cycle | All four views printed |
| ✓ | Analysis model | G/B/F | s6 bridge; B1 boundary/control/entity classes | Present |
| ✓ | Detailed design class model | G/B/F | s7 CU-B; real modules, type alias, Strategy roles, multiplicities | Present |
| ✓ | Detailed design sequence and state model | B/F | s8 closure; B16 compile; B17 publish/archive; B2 states | Dedicated continuation pages |
| ✓ | Second significant use-case design | B/F | B3 and B13–B15: photo upload, exact version, acceptance transaction, processing | Present |
| ✓ | Design problems, candidates and patterns | G/B/F | s7 repeated execution and Strategy seam; B7 Strategy/Adapter; B8 Observer; B9 persistence Adapter; script explanations | Present |
| ✓ | DATABASE SCHEMA with keys and types | G/B/F | s9 and B4: real memberships, group metadata, profiles, cycles, contributions, jobs, inputs | Full width; minimum text 14.055 px |
| ✓ | Testing types, tools and enforcement | E/B | s10; B6: static, client, server, PostgreSQL, root/IaC, deploy fixtures, browser/Axe, real-account, performance | Counts repaired |
| ✓ | Unit / behavioural tests for complex behaviour | B/F | s11 capture retry before/after; s7–s8 durable compilation; audit/E-testing.md trace | Present |
| ✓ | Source-code management strategy | G/E | s12: issue branch → PR → protected dev; protected main promotion and review | Present |
| ✓ | Artifact-management strategy | G/E | s12; s15; B12: tests, coverage, inventories, reports, bundle, hashes, retention, provenance | Present |
| ✓ | DevSecOps pipeline design and procedures | G/B/E/F | s13 UML activity partitions, classification and merge/deploy/report decisions | Full width |
| ✓ | SAST | E/F | s14; CodeQL JavaScript/TypeScript, Python, Actions; findings triage | Present |
| ✓ | DAST | E/F | s14 and s18; pipeline-run-40344230832/zap/report_json.json and report_html.html | 0 High / 4 Medium CSP / 7 Low / 6 Info |
| ✓ | SCA | E/F | s13–s14: production npm audit HIGH+ gate and Dependabot | Present |
| ✓ | Secrets | E/F | s13–s14: Gitleaks full-history SARIF and push protection | Present |
| ✓ | IaC security | E/F | s13–s14: Trivy config, exact exceptions and expiry gate | Present |
| ✓ | SBOM and exact-image scanning | E/F | s15; two real CycloneDX JSONs and two Trivy JSONs in pipeline-run-40344230832/security/ | Four report hashes match manifest |
| ✓ | Manifest and signed provenance | E/F | s15; real release-manifest.json excerpt; attestation workflow step and gh verification command; B12 | Original JSON keys/values preserved |
| ✓ | Technical findings and issues | G/E | s17; s11; FINDINGS.md: advisory, FFmpeg pin, schema packaging, SSE lifetime, retry | Stale #591 / DAST records corrected |
| ✓ | CI/CD demonstration / maintainability | G/E | s18 command-card walkthrough; successful same-commit Quality/Deploy dev metadata; s20 maintainability link | Walkthrough present |
| PENDING | CI/CD recorded backup | E | s18 data-clip="clips/ci-cd-40344230832.mp4" | Await final video; preserve this slot |
| ✓ | Significant system use cases | G/E | s19 and F1–F12: install, sign-in, create, invite, photo, video/allowance, chat, reminder, close, watch, Archive/save, outsider denial | Twelve linked feature clips |
| ✓ | System-demo backup | E | videos/demo.mp4 and videos/clips/*.mp4 | Complete film 672.021 s; clip schedule 660 s |
| PENDING | Scripted performance and scalability evidence | G/E | s20 measured table and projection; B11 capacity chart and notes | Existing content retained; integrate final results together |
| ✓ | Readability, claim headlines, view/use-case titles | B/F | All 57 frames; figure-native titles plus thin claim strip | Visual checks pass |
| ✓ | About 20 main slides; detail in backup | F/E | 20 main + 12 timed feature inserts + 25 backup pages | 57 physical pages |

## Fixes completed

- Large UMLs now use a 1280×688 image area beneath an 18 px claim strip. Prose is in the spoken script/notes. The smallest fitted UML text is 14.055 px; all 23 supplied SVGs are included.
- Eight hidden use-case/sequence variants became their own backups (B13–B20). The PDF now includes every split view. B21–B24 print the remaining burndowns and full velocity; B25 explicitly shows backlog, user-story and sprint-plan traceability.
- Removed the two disclaimer footer lines from burndowns and velocity in records/build_records.py and regenerated all five PNGs. Burndowns now plot the 00:00 opening snapshot before daily close points. Sprint 2 visibly starts at scope/open 9/3 and closes at 135/9, matching AGILE.md. Date locators/formatters explicitly use SGT.
- Corrected fast-suite counts in s10, B6 and SCRIPT.md: frontend 1,674 passed; server 985 passed / 21 skipped; root 123 passed / 1 skipped. Python security-gate tests are 13. Older dated coverage and PostgreSQL/browser results remain separately labelled.
- Corrected the storage implementation name to PrivateS3MediaStore and explained LocalMediaStore, MediaStore, privateTransport and the separate disk runtime path accurately.
- Updated records' #591 merge and DAST status from the later successful selected runs. Effort wording uses the agreed split; removed prohibited stage wording from the target records and generator source.
- Fixed overlapping overview rows, which intercepted thumbnail clicks. Repaired crowded CI/CD and performance layouts. No performance values were changed.
- Embedded SVGs, chart PNGs and poster JPEGs directly into deck.html. Feature videos stay at their expected linked paths. Rebuild changes are retained in build_deck.py so they survive export.

## Fact checks

| Claim | Verification | Outcome |
|---|---|---|
| Selected deployment | gh run view 40344230832; out/qa/deploy-run.json | Deploy dev succeeded at aea7478bce14131b821caaa99b1185077b4a9403; DAST job succeeded |
| Selected Quality | gh run view 40344231052; out/qa/quality-run.json | Quality checks succeeded at the same commit; browser job skipped on dev |
| Workflow names | Selected-commit YAML retrieved through gh into out/qa/*-selected.yml | Quality checks, Deploy dev, CodeQL, Release security, Secret scan |
| Performance workflow | Current diagram pin 2390589; out/qa/performance-current.yml | Scripted hosted performance; performance.yml is later than selected deploy commit |
| ZAP alert groups | Parsed site[].alerts[].riskcode in report_json.json | 4 Medium CSP, 7 Low, 6 Info; no High alerts |
| Manifest identity | Original JSON; s15 preformatted excerpt | commit, run_id, quality_run_id, security_gate and sha256 preserved |
| Report integrity | SHA-256 of both SBOMs and both Trivy reports | All four match; out/qa/artifact-hash-check.json |
| Image severity counts | Manifest images.runtime/web.counts | Both 0 HIGH / 0 CRITICAL; runtime 1 MEDIUM / 2 UNKNOWN |
| Cycle / worker names | server/src/cycles/{scheduler,lifecycle}.ts; jobs/{worker,compilation}.ts | runCycleSchedulerTick, advanceCycleLifecycleWithStore, publishCycleReleaseWithStore, runWorkerTick, claimCompilationJob, processCompilationJobForWorker exist |
| Pattern names | media/{store,local-store,s3-store,runtime-store}.ts; realtime/index.ts; postgres/database.ts | MediaStore, LocalMediaStore, PrivateS3MediaStore, privateTransport, RealtimeHub, PostgresDatabase exist |
| Scaling mechanism | postgres/database.ts:183,194; postgres/sync-worker.ts:80–107 | Atomics.wait bridge and retained pg.Client match the described mechanism |
| #591 status | gh pr view 591, read only | Merged 26 Oct 14:38:48 UTC at 47ea5f0 |

The selected workflow reports successful attestation steps. The local supplied folder contains the security and ZAP JSONs; this QA did not execute gh attestation verify on a local release tarball.

## Visual, interaction and export checks

- Final viewport: 1280×720, device scale 1, local HTTP server, Chrome through Playwright. T3 preview inspection worked, but two screenshot attempts returned `Preview automation snapshot timed out after 15000ms.` Screenshots then used the requested headless workflow.
- Every slide was captured: out/qa/slides/01-s1.png through 57-B25.png. All frames were opened through original-resolution four-frame contact sheets and focused follow-up/PDF views. out/qa/render-check.json retains per-frame metadata, bounds, image checks and fitted font measurements.
- Final checks: zero stage overflow, zero text overflow into the footer, zero broken images, zero sub-14 px UML text, zero browser page errors. s18, s20, B11 and the added B25 were rechecked after their layout repairs.
- Arrow navigation, named hashes, N notes, O overview, overview click, P playback, pause on leaving a clip, and C command cards passed. Overview contains 57 frames.
- Raw deck text, SCRIPT.md, OUTLINE.md, top-level records Markdown, and records/build_records.py were scanned for the prohibited disclaimer terms and hidden cycle-duration patterns. No matches remain in stage text; the product cycle stays 28 days.
- Re-exported with the shared brief's Chrome headless PDF command and no headers/footers. Final PDF: out/rewind-presentation.pdf, 57 pages, 960×540 pt (1280×720 CSS stage). Opened samples: pages 1, 3, 4, 7, 9, 10, 13, 15, 18, 20, 32, 39, 43, 48, 55, 56, 57. Rasterisations: out/qa/pdf/.

## Timing

| Section | Budget | Clock | Check |
|---|---:|---|---|
| 1 · Introduction and project management | 3:30 | 00:00–03:30 | Within 3–4 min |
| 2 · Analysis, design and patterns | 5:00 | 03:30–08:30 | Meets 5 min |
| 3 · Testing | 3:00 | 08:30–11:30 | Meets 3 min |
| 4 · CI/CD demonstration | 12:00 | 11:30–23:30 | Within 10–12 min |
| 5 · System demo and quality attributes | 14:30 | 23:30–38:00 | Within 12–15 min |
| Total | **38:00** | | **≤40 min; 2 min interruption allowance** |

Feature playback totals 11:00 inside section 5, followed by 3:12 for performance/scalability and 0:18 for the journey map. The complete system film adds twelve one-second cards and runs 11:12. The CI/CD recording must replace its allotted walkthrough time, not add to it. Sequence continuations B16/B17 are cued inside s8's existing 0:57 budget.

## Exact integration handoff after parallel-agent finalisation

Do not change videos/cicd/ or load-test/ from this QA pass. Integrate only after that agent declares the two deliverables final.

| Slide ID / physical page | Final source | Destination / required integration |
|---|---|---|
| **s18 / 18** | **videos/cicd/cicd-demo.mp4** | Copy the completed video to **deck/clips/ci-cd-40344230832.mp4**. Keep s18's existing data-clip path. Verify duration, playback, closing the overlay and pausing on slide exit. The frame currently budgets 3:48 for walkthrough actions; reconcile the final clip with the whole 12:00 CI/CD section. |
| **s20 / 32** | **load-test/RESULTS.md**, final measured JSON/CSV and charts cited by it | Update **deck/build_deck.py** perfrows, confirmation values, thresholds/method text, projection points, notes and full spoken script from one final result set. Rebuild **deck/deck.html** and **deck/SCRIPT.md**; update **deck/OUTLINE.md** only if timing or source labels change. Preserve measured/projected labels. |
| **B11 / 43** | **load-test/charts/measured-vs-projected.png**, **load-test/results/capacity-model.json**, as confirmed by final RESULTS.md | Refresh **deck/assets/measured-vs-projected.png** and its embedded HTML image. Update B11's model parameters, ceilings and notes/script to the same fit. Current retained notes say S=51.039 ms and L=341.8 ms, while the chart refreshed by the parallel producer says 45.4 ms and 378 ms: reconcile these together, not separately. |
| **s20 / 32 and B11 / 43** | Same final capacity model | Use one consistent one-host/two-host curve and workload definition in both frames. Check the measured table, confirmation run and projection are aligned with the final labels. |
| **s18, s20, B11; final deck and PDF** | Integrated video and results above | Rebuild once with **python3 deck/build_deck.py**, rerun the 1280×720 visual/control checks for those frames, then re-export **deck/out/rewind-presentation.pdf**. Recheck total ≤40 min and replace this report's two PENDING rows only after validation. |

**Remaining parity gaps:** final CI/CD recorded backup; refreshed and internally consistent performance/scalability results. No other requirement-content gap was found in this pass.
