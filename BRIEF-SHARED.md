# Shared brief for every presentation agent (read first)

**Talk:** Tue 27 Oct 2026, 14:30 SGT. Presenter: Gopal Guruprasath, alone, all sections. Rewind is the SWE5006 project of Team 14.

## Required outline (lecturer email + official guidelines)

40 min, then 5 min Q&A, with interruptions.

| # | Section | Time |
|---|---|---|
| 1 | Intro & PM summary: context, business problem, scope, status and outstanding issues, milestones, effort per member, sprints, DoD, retros | 3–4 min |
| 2 | Analysis & design + patterns: architectural decisions, analysis→design transition, use case diagram, analysis and design models, design problems and patterns, **database schema** | 5 min |
| 3 | Types of testing | 3 min |
| 4 | CI/CD pipeline demo: strategy for managing **source code and artifacts**, the DevSecOps pipeline and procedures (**SAST, DAST, SCA, secrets, IaC, SBOM, provenance**), technical findings | 10–12 min |
| 5 | System demo: significant use cases plus quality attributes (performance via scripted load test, scalability, maintainability via the pipeline) | 12–15 min |

## Owner rules

- **No "simulated", "proposed", "not measured" or other disclaimers** on slides, figures or videos. The owner handles caveats himself.
- **Never show the demo cycle length** (30 min on dev). The product cycle is 28 days.
- **Team** (records/TEAM.md): Nguyen Kim Long, Gopal Guruprasath, Jiang Jiayu, Phan Mai Tan Loi, Sang Haoxiang. Effort (owner correction, 27 Oct): Gopal Guruprasath 40%, Nguyen Kim Long 20%, Jiang Jiayu 20%, Phan Mai Tan Loi 20%, Sang Haoxiang minimal contribution (0%). Ceremonies held: project planning, Sprint Planning and Sprint Review each sprint.
- **The release environment is out of scope for the talk.** Everything is shown on hosted dev, https://d2m6kz76y4kuvm.cloudfront.net.
- **Style (assessor feedback):** formal UML with real code names, claim headlines, about 20 main slides with the rest in backup, readable at 1280×720, every figure titled with its view and use case.

## Assessor feedback carried over

`../presentation-feedback-carryover.md`

## Facts and sources (`presentation-prep/`)

- **Audits:** `audit/` (A deck, B1 analysis models, B2 design/patterns/ER/deployment, C DevSecOps, D CI/CD demo, E testing, F1 system demo, G PM). Code facts are verified against `origin/dev`, file:line cited.
- **Records:** `records/` (TEAM, AGILE, FINDINGS, burndown and velocity charts).
- **Load test:** `load-test/` (METHODOLOGY, RESULTS, charts).
- **Pipeline:** `PIPELINE-ARTIFACTS.md`, and the run to demo: Deploy dev run 40344230832. Its artifacts are copied in `pipeline-run-40344230832/`. ZAP: 0 High / 4 Medium (CSP) / 7 Low / 6 Info.
- **Verified PlantUML drafts:** `uml-drafts/`, with `_style.iuml` holding the FlickPond skinparams.
- **Target look:** the FlickPond PDF at `/Users/speedpowermac/.t3/userdata/attachments/1efad8e5-737b-4def-bd5b-f1bae192cfde-0b42fcc8-1ba1-4f80-ae63-64a1137e5ee8-pdf.pdf`:
  - cream background `#F5F2E9` and a navy `#14202B` cover;
  - mono kicker per course (SAD purple, ARCHSS blue `#2C64A0`, DEVSECOPS teal);
  - claim headline, UML on a white rounded card (about 65% width) with a 30% explanation column.
- **Deck framework to fork:** `/Users/speedpowermac/Documents/projects/CODE_MAIN/NUS/dc2-rescue/project-documentation/presentation/site/deck.html`, a single file with keyboard navigation, notes (N), overview (O) and clip slides.

## Code

- **Current code:** origin/dev. Create a worktree from `/Users/speedpowermac/Documents/projects/CODE_MAIN/NUS/SWE5006/rewind-app` with `git worktree add <path> origin/dev --detach`.
- **Read-only copy:** `/Users/speedpowermac/Documents/projects/CODE_MAIN/NUS/SWE5006/rewind-present-audit` (f6cd896; app code is unchanged since then, only CI changed).
- **Never** switch the main checkout's branch, merge PRs, push to dev or main, or change AWS.

## Rendering

- **PlantUML:** `java -Djava.awt.headless=true -jar presentation-prep/plantuml.jar -tsvg X.puml`, then run it again with `-tpng`. Run the two separately; one pass writes only one format.
- **Chrome PDF:** `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --user-data-dir=/tmp/x --no-pdf-header-footer --print-to-pdf=out.pdf "file://$PWD/deck.html"`

## Diagram file contract

Output goes to `presentation-prep/deck/uml/`, as `<id>.puml`, `<id>.svg` and `<id>.png`. The deck embeds these SVGs.

| id | Figure | Owner |
|---|---|---|
| `uc-model` | Use case model UC01–UC14, actors, include/extend, secondary actors (Cognito, S3, web push, scheduler) | UML-SAD |
| `arch-logical` | Logical architecture: layers and modules, ≤15 boxes | UML-SAD |
| `bce-cycle` | Analysis classes (boundary/control/entity) for CU-B "close cycle → compile → release film" (UC07+UC08) | UML-SAD |
| `a2d-cycle` | Analysis → design mapping for CU-B (BCE names → real modules, files, tables) | UML-SAD |
| `class-cycle` | Design class diagram for CU-B with pattern role stereotypes | UML-SAD |
| `seq-cycle` | Design sequence for CU-B: numbered messages, alt/loop, real function names | UML-SAD |
| `state-cycle` | Cycle statechart | UML-SAD |
| `seq-capture` | Design sequence for CU-A "contribute photo within allowance" (backup) | UML-SAD |
| `pattern-storage` | Strategy + Adapter: MediaStore, S3 (problem/candidates in notes) | UML-ARCH |
| `pattern-observer` | Observer: RealtimeHub chat | UML-ARCH |
| `pattern-persistence` | Adapter: PostgresDatabase | UML-ARCH |
| `er-core` | ER schema subset: groups, memberships, cycles, contributions, media_jobs, compilation inputs, profiles; PK/FK/types (split into two if over 20 boxes) | UML-ARCH |
| `deploy-dev` | UML deployment: GitHub Actions → OIDC → Lightsail host (nginx + Node) → PostgreSQL, S3, CloudFront, Cognito, web push | UML-ARCH |
| `pipeline` | DevSecOps activity diagram with swimlanes (Developer, GitHub PR checks, Deploy dev, Hosted dev). Show every scan tagged BLOCKS or REPORTS, and every artifact produced | UML-ARCH |
| `artifact-flow` | Source and artifact management: branches, PR, protected dev/main, artifacts (JUnit, coverage, npm-audit, SBOM, Trivy, manifest, attestation, ZAP) and where they live | UML-ARCH |

## Update (26 Oct, ~23:55): split figures

- UML-SAD split `seq-cycle` into compile and release parts, and `seq-capture` into pin, commit and process backups, to keep fonts at 14 px or more.
- Split files keep the contract id as a prefix, e.g. `seq-cycle-*.svg`. **Deck:** glob `uml/<id>*.svg`, and give each part its own slide or backup slide.
- `deck/uml/README-SAD.md` and `README-ARCH.md` list every final file.

## Update (27 Oct, ~00:10): figure layout rule from UML-SAD

- There are 16 SAD figures. The `uc-model` overview has abbreviated labels; `uc-model-access`, `uc-model-capture` and `uc-model-cycle` give full names and links.
- `seq-cycle` covers closure, and `seq-cycle-compile` / `seq-cycle-release` continue UC08. `seq-capture` continues in `-accept`, `-commit` and `-process`.
- **Deck: render large UML figures FULL WIDTH (fit about 1248×688), not in the 65% card.** A narrow card drops text below 14 px.
  - Put the explanation in a thin strip or the speaker notes, or use a build pair: figure slide, then explanation slide.
  - See `deck/uml/layout-check-SAD.json`.
