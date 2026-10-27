# A · Deck structure, content sources and slide tooling (audit, 26 Oct 2026)

Read-only. Code = worktree `rewind-present-audit` (origin/dev `f6cd896`; `gh api compare f6cd896...dev` = identical today [verified]). Tags: [verified] = read/ran it; [inferred] = my reasoning. One presenter delivers all five sections (owner decision), so there are no hand-offs, no per-member dividers, and the plan below is timed for one voice.

## 0. The five things that matter most
1. **The current deck is `rewind.html` + `rewind-script.md`, and it is the wrong shape.** It follows the SWE5001-style outline (Overview / Conduct / Architecture / DevSecOps / Demo, 2+2+7+6+13 min). It has **no Testing section**, no pipeline demo, and **zero UML**. [verified]
2. **The "target look" PDF is not the dc2-rescue deck.** It is a separate 24-page "Flickpond — Architecture Presentation" (cream background, mono kicker, figure card + explanation column). The dc2-rescue repo holds a different, white-themed 147-slide HTML deck, and has no source for the PDF. [verified, §2a]
3. **We can fork the dc2 HTML deck tonight** (single file, ~40 lines of JS, no build step). PlantUML-to-SVG and Chrome-to-PDF both work on this Mac; I ran both. [verified, §2]
4. **The `npm audit` gate is red for any new PR.** New HIGH advisory GHSA-mrhx-c7xc-m3w5 (zod via expo, 3 high) failed Quality on PRs #589/#590 (runs 40140117765, 40140169768, 24 Oct). Deploy dev only deploys a commit that passed Quality. A live "merge, then deploy" demo would fail. [verified]
5. **Still missing for the talk:** effort per member is "to fill"; no DAST exists (draft PR #438 only); the demo has never been rehearsed or recorded (the script says PENDING); no formal UML exists for Rewind. [verified]

## 1. Audit of existing material

### 1a. `rewind.html` (1416 lines, 20 slides) and `rewind-script.md` (342 lines)
Untracked in the main checkout `rewind-app/doc/planning/report/presentation/`, dated 25 Oct. I rendered it with Chrome print to PDF (20 pages) and PNGs in `/tmp/rewind-a/` and viewed all of them.

| Check | Finding |
|---|---|
| Sections vs required outline | Overview (s1–2), Conduct (s3), Architecture (s4–9), DevSecOps (s10–11), Demo (s12–18), backups s19–20. Script budget is 30 min talk + 10 min Q&A in 2/2/7/6/13. Required: 3–4 / 5 / 3 / 10–12 / 12–15, 40 min plus 5 Q&A. [verified, script lines 17–27] |
| Testing (3 min) | Absent. Only s11 "Quality gates" (a DevSecOps slide) lists lanes: no tool/count/coverage table. Performance is in the demo (s17). |
| CI/CD (10–12 min) | Two static box-and-arrow slides (s10–11, 6 min) plus "saved records" (s17). No SAST/DAST in a pipeline picture, no live or recorded pipeline demo, no blocking-vs-reporting split. |
| Visual style | It reuses the dc2 palette and 1280×720 stage (same `.m .p .c .i .x` hex values). Every figure is a flexbox of rounded boxes and arrows. Headlines are topics ("Delivery status", "Summary"). There is no kicker, no explanation column, and no class, sequence or state diagram. Several captions are 21–23 px, below the 24 px rule. |
| Mechanics | Prev/Next buttons use clicks. No notes pane (`.source-note` is `display:none`, one line), no overview, no URL hash, no clip support, no progress bar. Print CSS works. |
| Facts: still true | Lightsail host (`infra/terraform/demo/lightsail.tf`), hosted dev on managed PostgreSQL (`infra/terraform/media/database.tf`: dev `enabled`, `cutover = true`), S3, Cognito, SQLite locally, `acceptRealGroupInvite` (`server/src/groups/invites.ts:214`), `claimCompilationJob` (`jobs/compilation.ts:501`), `RealtimeHub` (`realtime/index.ts:9`), `CameraPlatform` (`src/capture/contracts.ts:101`). Quality run 39443030843 and Deploy dev 39441043830 are both success at f6cd896 (20 Oct). [verified] |
| Facts: stale or risky | Slide 3 "Still open" omits #587/#588 (new 24 Oct); open `mvp` issues today are #588 #587 #527 #515 #504 #362 #230. s12/s16 say "rehearsal pending" and "No recording is assumed to exist". "Presenter A–D" labels are obsolete. Nothing says "no DAST". [verified via `gh`] |

**Salvageable from the script** (strip the A–D labels and per-presenter cues):
- Honesty discipline: "observed vs claimed", dated runs, local-vs-hosted labels. This is what the assessors asked for. Keep it.
- "Compared / Chosen" reasoning on s6–9 (Adapter vs Policy/Strategy, State vs polling, Observer plus stored replay). It is the seed of the pattern slide.
- The **Do / Expected / Fallback** triplets for the demo steps (s12–16) are good clip-recording shot lists.
- s17 numbers and wording: p95 ≤ 9.7 ms, film 9.0 s, 25 synthetic inputs, SQLite loopback, 12 Oct, base a1dc77e.
- Backups s19 (interrupted compile) and s20 (local/dev/release). The "private source map" at the end.
- Not reusable: the timing table, the section mapping, and every slide image (all box flows).

### 1b. Tracked in the worktree: `doc/planning/report/presentation/`
| Item | Verdict |
|---|---|
| `presentation-outline.md` | The 9-slide Sprint 2 plan pinned to e82dc42. Stale: SQLite/Node as current, PostgreSQL and Cognito as "future", ENOSPC deploy failures as latest. Discard. `submission.json#readiness` already says the 9-slide PPTX was deleted. [verified] |
| `demo-script.md` | A 5-minute narration of the headless-Firefox fixture runner (`npm run test:real-account-e2e`, exists at package.json:38), SQLite, e82dc42. Stale as a demo plan. The runner is still a useful rehearsal tool. |
| `build-presentation.mjs` (675 lines) | Needs the Codex-private `@oai/artifact-tool` runtime under `~/.cache/codex-runtimes/...` (this Mac has it) and a plugin skill path. It outputs an editable PPTX of stale content. Do not use. |
| `report/packages/*/diagrams` (137 SVG), `diagrams/*.svg` | Hand-built SVG boxes, not formal UML: no stereotypes, numbered messages or `alt`/`loop` frames. Pinned to fc2b8c8, which is **398 commits and 201 files in `server/src`+`src` behind** HEAD. UC07-F1 subtitle says "SQLite writer transaction"; `schema-current.svg` is titled "Current SQLite logical schema". Reuse the responsibilities and flows as text only. Redraw every figure. [verified] |

### 1c. `docs/site` (explainer: 14 pages, 106 sections, 261 "Questions to expect")
`python3 docs/site/build.py` reads `site.json` + `content/<slug>.json` and writes `html/`. I ran it on a copy in `/tmp`: 14 pages built, worktree untouched. [verified] It is a **study guide and Q&A bank, not slides**: its diagrams are sketch-style box flows (README says so). Use it as the content source.

| Page | Reusable and current | Stale or needs work |
|---|---|---|
| quality | Test pyramid, counts per layer, jobs per CI lane, coverage 89.64% stmts / 92.33% lines / 85.68% branches (matches `coverage/coverage-summary.json`), 70% floor `jest.config.cjs:17`, TDD/characterisation | "64 server test files": `ls server/tests/*.test.mjs` = **66**. The 1,674 FE and 988 PG test counts come from PR #581, not re-run [inferred]. No performance row in the pyramid. |
| cicd | Workflows, security table, OIDC, measured runs, promotion/rollback | No DAST. Does not mention the red audit gate (24 Oct). Runs are 20 Oct. |
| patterns, analysis-design | 5 problems → candidates → chosen; "pattern role × evidence × limit" table | Diagrams are informal. Pinned models predate the refactor (see 1b). |
| architecture, decisions, aws, database | Layers, ADR list, topology, entity groups (PostgreSQL hosted, SQLite local, private S3, Cognito are current) | Re-check module names after the 20 Oct refactor before drawing. |
| scrum | Sprint dates, DoD, tracking labels | **Effort table = "to fill"** (the only actual-effort record is ~1 h/day early in Sprint 0). Outstanding issues dated 20 Oct (7 `mvp` open today). "Sprint 3 in progress" ended 24 Oct. Sprint analytics HTML is from 6 Oct. |
| submission | Brief, deliverables, honesty rules | `presentation-plan` is the old 5-segment 3+3+9+8+17 plan (13+4 demo). It conflicts with the lecturer's format and says "40 including Q&A" where the brief says 40 + 5. **Owner to confirm.** |
| demo | Pre-demo checklist (accounts, rate limit 5/15 min, hosted health, tabs) | 13-minute two-device plan with the pipeline in the last 2 min. Must be split in two. |
| index, product, owners | Loop, scope, UC list | Status paragraph dated 20 Oct. `owners` is moot with one presenter, except as a table in backup. |

Gap list for Q&A prep: 261 model answers already exist. Turn the ones for the appendix topics into slide text.

## 2. FlickPond tooling (dc2-rescue `project-documentation/presentation/`)

**2a. The target PDF.** `pdfinfo`: 24 pages, 960×540 pt, "Flickpond — Architecture Presentation", authors Ibrahim Mammadov, Zhang Jizhang, Yang Dongwei, Jiang Yibai, Lu Jingxing, text layer "Glyphless" (OCR style). dc2's own `feedback-20261026/research/R1-old-deck-lessons.md` says the PDF's editor "does not establish" its source and treats it as a reference deck from a different codebase [verified]. Look, from viewing pages 1, 2, 6, 8, 11, 16: cream background `#F5F2E9`, cover `#14202B` with orange mono kicker, mono kicker per course (SAD purple, ARCHSS blue `#2C64A0`, PE orange `#B4501A`, DEVSECOPS teal), short title, a white rounded card with the UML at ~65% width, and a ~30% right column with bold lead-ins and one orange conclusion line. Fonts look like IBM Plex Sans/Mono [inferred]; Plex is not installed here (`fc-list` = 0).

**2b. How the dc2 deck is authored and built.**
- `site/deck.html` is one hand-edited, self-contained file (1151 lines, 424 KB, 147 slides = 60 main + 87 backup). Lines 1–~95 are CSS, then one `<section class="slide" id data-kind="main|back" data-num>` per slide, then ~55 lines of JS. **No generator.** `<h1>` is the claim; a kicker `<div style="font:600 15px Menlo…">` sits under it (e.g. "SAD · UML activity / execution admission and lease fence"); `.sec` is the top-right section label; `.foot` carries source links and a **hard-coded "n / 60"**; `aside.notes` holds notes with permalinks. [verified]
- Not part of the deck: `_template.html`, `_stitch.py`, `_check.py`, `assets/guide.css` (study-guide pages and the Pages link checker). `feedback-20261026/integrate.py` merges per-workstream fragments from a git base rev (`REPLACES sN` / `NEW after`). It is FlickPond-specific. `deck-presented-20261026.html` is the frozen 68-slide copy as presented.
- JS: scales the 1280×720 stage to the window. Keys: →/D, ←/A, **N** notes pane, **O** overview grid, **B** blackout, **F** fullscreen, **P** play/pause clip, digits+Enter jump; URL hash `#n`. A progress bar fills across main slides. Clicks never change slides (commit effc361).
- Clips: `<div class="clip" data-clip="clips/D1.mp4"><video preload="none">`. They load when the slide activates and show a dashed placeholder until `loadeddata`. Print shows the placeholder only. `clips/.gitignore` keeps mp4s out of git; they are 1920×1080 H.264 (D1 24 s). `PRESENTING.md` covers Zoom ("Optimize for video clip") and the clip table.
- PlantUML: `site/assets/uml/_style.iuml` (shared skinparams and the four accent colours) + 78 `.puml`, each starting `!include _style.iuml`, each with `title <View> · <use case> · as built at <sha>`. Slides embed `<img src="assets/uml/X.svg" style="max-width:1180px;max-height:440–560px">`. Slide-grade diagrams raise `defaultFontSize` to 16–25. Rule: ~20 boxes max, check at 1280×720.

**2c. Commands I ran (all succeeded, outputs in /tmp):**
```
# serve + present (hash links work)
cd <deck dir> && python3 -m http.server 8766      # open http://127.0.0.1:8766/deck.html, press F
# PDF: Chrome print stylesheet, 1.9 s, 147 pages, 960x540pt, 5.2 MB  (/tmp/a-deck-pdf/out/deck-flick.pdf)
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
  --user-data-dir=/tmp/<scratch> --no-pdf-header-footer --print-to-pdf=out.pdf "file://$PWD/deck.html"
# PNG check at 1280x720 (what DECK-QA.md did)
pdftoppm -r 96 -png out.pdf slide
# PlantUML -> SVG, 2 files in 2.0 s (needs java 17 + graphviz dot 16.1, both installed)
java -Djava.awt.headless=true -jar ~/dc2-tools/plantuml-1.2026.9.jar -tsvg X.puml   # keep _style.iuml beside it
# jar (30 MB, not in git) if missing:
gh release download v1.2026.9 --repo plantuml/plantuml --pattern plantuml-1.2026.9.jar --dir ~/dc2-tools
# optional raster preview of an SVG: Chrome --screenshot works (tested); npx @resvg/resvg-js-cli is untested here
# clip encode (ffmpeg present): ffmpeg -i in.mov -vf scale=1920:1080 -c:v libx264 -crf 23 -pix_fmt yuv420p D1.mp4
```
I also rendered `rewind.html` the same way (20 pages). I did not run anything against AWS, GitHub state or the worktree.

**2d. Can we fork tonight? Yes.** About 2–3 hours of setup, then slide authoring. Recommended:
- **Copy:** CSS + JS block of `deck.html` (verbatim), 6 exemplar slide patterns (title, claim + figure + explanation, table, big-number, clip, decision card), `assets/uml/_style.iuml` plus 3 starter `.puml` (class `W3-04`, activity `W5-pipeline-main`, a sequence), and trimmed `STYLE.md`/`PRESENTING.md`. **Skip:** `integrate.py`, `_stitch.py`, `_check.py`, `_template.html`, `guide.css`, `feedback-20261026/`, `research/`, the 147 slides.
- **Change:** (1) Theme: map accents to Rewind areas (ACCESS blue, CAPTURE green, CYCLE/ARCHIVE amber, PARTICIPATION purple, infra slate) in both CSS and `_style.iuml` (`$MEDIA`→…). (2) Add the PDF's layout: cream `#F5F2E9` stage, navy cover, a `.fig` white rounded card (65%) + `.expl` column (30%), ~20 lines of CSS. (3) Kickers become `SAD · 04a DESIGN SEQUENCE · UC08` using the tags PM / SAD / SDP / TESTING / DEVSECOPS / DEMO, with one colour per tag. (4) `.sec` labels become the five outline sections, and add a 5-segment progress strip in place of divider slides. (5) Replace the hard-coded "n / 60" with JS (`counter`). (6) Fonts: keep system sans + Menlo (zero install risk, same as dc2); only add Plex if you copy the font files locally. (7) Single-voice extras (~20 lines JS): a **T** key showing elapsed time vs the section budget, and each slide's notes ending with the *next slide's first sentence* instead of a hand-off.
- **Risk:** the dc2 deck's hard-coded footers, `data-num` and slide-count text must be regenerated. The only automated check is `pdftoppm`/eyeball at 1280×720.
- **Drawing effort:** formal UML is the bottleneck: ~9 new figures (§3) at ~30–45 min each including verifying names against code. Reuse dc2's `.puml` as syntax templates (autonumber, `alt`/`loop`, stereotypes, `<<module>>`).

## 3. Proposed Rewind deck — single presenter, 20 main slides, 35.5 min + 4.5 min buffer for interruptions + 5 min Q&A

Rules from the carryover apply: headline is a claim (≤10 words), figure titled with view, use case and "as built at f6cd896", draw only real names (`«module»` for function modules; real classes are `RealtimeHub`, `PostgresDatabase`, interface `MediaStore`/`CameraPlatform`), and every figure is dated. Status: **E** = exists (restyle), **T** = text/data exists, figure to make, **M** = must be made or recorded.

| # | Sec | Min | Kicker | Claim headline | Figure / content | Source of truth | St. |
|---|---|---|---|---|---|---|---|
| 1 | 1 | 0.3 | SWE5006 · TEAM PROJECT · 27 OCT 2026 | Rewind turns a month of moments into one film | Cover + Contribute→Seal→Compile→Watch strip | README.md; rewind.html s1 | E |
| 2 | 1 | 1.2 | PRODUCT · LOOP AND SCOPE | Contributions stay sealed until the cycle ends | 28-day loop, 24 h premiere, in/out chips (PWA yes, native iOS out) | product.json#scope; rewind.html s2 | E |
| 3 | 1 | 2.0 | PM · STATUS AS OF 26 OCT | Real accounts shipped; release isolation is still open | Sprint 0–3 strip with dates and closed counts (21/52/131/40); DoD one-liner; **effort table labelled "estimate" or "agreed split" on the slide**; today's `mvp` open list | scrum.json; `gh issue list --label mvp` | M (effort) |
| 4 | 2 | 0.5 | SAD · 02c USE CASE MODEL | Fourteen use cases serve three actors | UML use cases UC01–UC14, boundary, «include»/«extend», Cognito/S3/push as secondary actors | product.json#use-case-list | M |
| 5 | 2 | 0.7 | ARCHSS · ARCHITECTURE OVERVIEW | One Node monolith keeps every rule in one transaction | Component view ≤15 boxes: «module»s (HTTP policy, groups, contributions, cycles, jobs, realtime, archive) + Postgres/S3/Cognito | architecture.json#layers; docs/architecture/current-system.md | M |
| 6 | 2 | 0.8 | SAD · 03a ANALYSIS → 04a DESIGN · UC08 | Analysis responsibilities map onto real modules | Left: boundary/control/entity. Right: design names. Legend marks which is which | analysis-design.json#objects-to-code | M |
| 7 | 2 | 0.8 | SDP · DESIGN PROBLEM · CYCLE | Polling alone cannot keep a film job safe | Problem → candidates (polling, State classes, Command classes) → chosen (persisted state + durable job + lease/generation claim) | patterns.json#cycle; packages/cycle/design-problem.md | T |
| 8 | 2 | 1.0 | SAD · 04a DESIGN CLASSES · UC08 | A late worker cannot finalise under a stale claim | Class view with pattern role labels: `«module» scheduler` (`scheduler.ts:46`), `lifecycle` (`:419`), `compilation` (`:501`), `«entity»` tables | server/src/cycles, jobs | M |
| 9 | 2 | 1.2 | SAD · 04a DESIGN SEQUENCE · UC08 | A repeated tick reuses the same film job | Numbered sequence with `alt` (duplicate tick, stale claim) and `loop` (retry) | lifecycle.ts, compilation.ts, jobs/worker.ts | M |
| 10 | 3 | 1.4 | TESTING · TYPES, TOOLS, WHERE IN CI | Every test layer has a tool, a CI job and a count | Table: static, Jest FE, node:test server (SQLite and PG), root/IaC, deploy fixtures, Playwright + Axe, real-account e2e; names match `quality.yml` jobs | quality.json#layers, #ci-gate; quality.yml | T |
| 11 | 3 | 1.6 | TESTING · COVERAGE, PERFORMANCE, SECURITY | Measured numbers, each labelled with its environment | Big numbers 89.6% stmts (floor 70%), ~86% server lines, p95 ≤ 9.7 ms, film 9.0 s with date/env chips; names of access-control tests | coverage-summary.json; doc/planning/performance/353-local-measurement.md | T |
| 12 | 4 | 1.5 | DEVSECOPS · PIPELINE ACTIVITY VIEW | SAST and dependency audit run inside the pipeline | Swimlane activity: Quality (parallel jobs, **audit blocks**, `gate`), CodeQL (**reports**), Release security/Trivy (**reports**), GitGuardian; dashed "DAST: not implemented" | quality.yml:18/74/270; codeql.yml; release-security.yml | M |
| 13 | 4 | 1.5 | DEVSECOPS · DEPLOYMENT VIEW + DECISIONS | Deploy verifies the same commit and restores on failure | UML deployment: Actions → OIDC role → bundle → Lightsail (nginx + Node) → PostgreSQL/S3. Strip: scope classifier, required context, promotion (main needs 1 review), rollback = previous release restored on failed health check | deploy-dev.yml (header comment); deploy/README.md | M |
| 14 | 4 | 4.0 | CI/CD DEMO D1 · date · sha | The aggregate gate blocks a failing audit | Live or clip: PR → Quality jobs → protection settings (dev: strict, 0 approvals, conversation resolution) | gh run 40140169768 shows a real block | M |
| 15 | 4 | 4.0 | CI/CD DEMO D2 · date · sha | A passing merge reaches hosted dev unattended | Live or clip: run 39441043830 (f6cd896) → `/health` version | deploy-dev.yml | M |
| 16 | 5 | 0.7 | DEMO MAP | Five flows prove sealed, atomic and private | Flow → UC → attribute → env (hosted dev / local `make run-real`) → live or clip | rewind-script s12–16; demo.json | T |
| 17 | 5 | 4.0 | DEMO D3 · INVITE, CAPTURE, SEAL | Acceptance and sealing are server decisions | Do/Expected strip; limits 5 clips, 30 s, 15 s per video | rewind-script s13–14 | M |
| 18 | 5 | 3.5 | DEMO D4 · CHAT AND PRIVATE FILM | A stored message and a denied outsider | As above for s15–16 | rewind-script s15–16 | M |
| 19 | 5 | 3.0 | DEMO D5 · TEN-MINUTE ROLLOVER (LOCAL) | The cycle closes itself and a film appears | `make run-real` 10-min cycle; label "local, synthetic" | docs/site demo.json checklist | M |
| 20 | 5 | 1.8 | LIMITS AND NEXT · 26 OCT | Open: DAST, release isolation, device check, one host | 4 honest rows, each with next step | scrum.json#outstanding; §0 | T |

Cumulative clock: S1 3.5 → S2 8.5 → S3 11.5 → S4 22.5 → S5 35.5; keep 4.5 min spare for interruptions. If running late, cut slide 7 (fold into 8's notes) and slide 16.

**Single-voice rules.** One progress strip, no dividers. Each slide's notes: ≤3 lines of "say", the source path, and one lead-in sentence for the next slide. Slides 14–19 are the only ones where the presenter drives a browser *and* talks. Make the **recorded clip the primary** for 17–19 (voice-over live, on mute video), and live driving the fallback. [inferred: one person cannot drive two browser contexts and narrate reliably.] Label each clip with date and commit, and record all five today at real length.

## 4. Backup appendix (reachable by slide number; ≤1 sentence spoken answer each)
| ID | Question it answers | Content | Source | St. |
|---|---|---|---|---|
| B1 | "Where is your DAST?" | None in any workflow (grep `zap|dast|owasp` over `.github`, docs: no hits [verified]). Draft PR #438 "Vigolium DAST trials" (5 Oct, conflicting, never merged [verified]). Why: AGENTS.md scope guard bars new scanners without an `mvp` issue. Would add: ZAP baseline against a disposable local backend. | gh pr view 438 | M |
| B2 | "Show the schema" | ER subset with PK/FK/key columns: groups→cycles→media_jobs→compilation_job_inputs, contributions, memberships, real_accounts. Redraw as **PostgreSQL**. | server/migrations/postgres/030-baseline.sql; docs/domain/database-design.md | M |
| B3 | "Deployment / physical view" | Full diagram: CloudFront, Lightsail host, managed PG, private S3, Cognito, Terraform. | infra/terraform/demo, aws.json#topology | M |
| B4 | "Why PostgreSQL, not NoSQL?" | Requirement (managed backups, proposal §5.3) → choice (Lightsail PG 17, 7-day PITR, TLS) → rejected (SQLite + S3 snapshot; no HA #503). | docs/architecture/ADR-0003-postgresql.md | T |
| B5 | Coverage detail | Per-area table and the 70% floor rationale. | coverage-summary.json | T |
| B6 | "How does it scale?" | Single host by design, bounded concurrency and rate limits; scale-out needs shared state for media tokens and `RealtimeHub`. No auto-scaling claim. | submission.json#demo-evidence | T |
| B7 | "Effort per member" | Same table as slide 3, with method. | scrum.json#effort | M |
| B8 | "Threat model" | None exists (grep STRIDE/threat model: no hits [verified]). Build a 6-row STRIDE table with real controls (sessions, membership checks, 2-minute media capability `archive/capabilities.ts`, throttles). Verify each control in code first. | docs/design/safety.md | M |
| B9 | Second use case: capture | `CameraPlatform` + adapters class view; sequence reserve→upload→accept (`contributions/index.ts:146`). | src/capture/contracts.ts:101 | M |
| B10 | Chat replay | `RealtimeHub` class (Observer) + stored events cursor sequence. | realtime/index.ts:9 | M |
| B11 | Interrupted compile / recovery | Flow from rewind.html s19. | rewind.html s19 | E |
| B12 | Local vs dev vs release | Table from rewind.html s20. | rewind.html s20 | E |
| B13 | "What blocks a merge?" | dev: required context "Format, lint, typecheck, and test", strict, conversation resolution, 0 approvals; main: same + 1 approval [verified `gh api` 26 Oct]. CodeQL, Trivy, GitGuardian report independently. | gh api branches/*/protection | T |
| B14 | Sign-in and invite flows | Cognito PKCE sequence; `acceptRealGroupInvite` (`invites.ts:214`). | aws.json#identity | M |
| B15 | Restore drill | #508: RPO 334 s, RTO 1,022 s, from the site, not re-checked [inferred]. | demo-evidence | T |

## 5. Do tonight, in order
1. Fork the deck shell and render the 20 slides as placeholders. Check 1280×720 and the PDF export (~1 h).
2. Fill and date the effort table (owner only) and refresh the `mvp` list.
3. Decide how to handle the red audit gate before recording D1/D2 (fix the zod advisory via PR, or demo the block and use run 39441043830 for the deploy). I did not touch it.
4. Draw figures 4–9, 12 and 13 first (the only ones the main talk needs), then B1–B3.
5. Record all five clips with date and commit; keep the PDF as the third fallback.
