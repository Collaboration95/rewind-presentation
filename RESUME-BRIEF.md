# Resume brief: wakes at 02:29 SGT, 27 Oct 2026

Written 00:19 SGT. The orchestrator ran out of usage, so the Sol agent that reads this owns the remaining prep work. The talk is **today at 14:30 SGT**.

## Read first (all in `presentation-prep/`)
- `BRIEF-SHARED.md`: owner rules, the required outline, sources, and the layout rules.
- `HANDOVER.md`: overall status and the agents table.
- `FIX-LIST.md`: the requirements checklist.
- `../presentation-feedback-carryover.md`: assessor feedback.
- `deck/` (deck.html, OUTLINE.md, SCRIPT.md, QA-REPORT.md, uml/README-SAD.md, uml/README-ARCH.md).
- `videos/SHOTLIST.md` and the clips in `videos/clips/`.
- `load-test/` (RESULTS.md, status.json, charts).
- `PIPELINE-ARTIFACTS.md`.
- Official guidelines: the docx and the briefing pptx in `~/Downloads/course_files_export 5/SWE5006 - Practice Project Presentation Guidelines/`.

## Work that may still be in progress when you wake
Check the files, not the agents:

| Agent | Done when |
|---|---|
| Deck QA | `deck/QA-REPORT.md` exists |
| CI/CD video and load-test re-run | `videos/cicd/cicd-demo.mp4` exists and `load-test/RESULTS.md` holds the re-run |

If an output is missing, wait in 10-minute steps (up to about 60 minutes) before doing the dependent step. Do everything else in the meantime.

## Your jobs, in order
1. **Integrate.** Apply the pending integration list from `deck/QA-REPORT.md`:
   - final load-test numbers and charts on the performance slide;
   - the CI/CD video in place of the placeholder `deck/clips/ci-cd-40344230832.mp4`.
2. **Separate videos, one per slide** (owner request):
   - The system demo is a sequence of slides, one feature per slide, each playing its own clip.
   - The presenter controls playback: click or Space to play and pause, and the clip doesn't autoplay with audio. That way he can talk over each slide.
   - Show each clip inside a realistic **iPhone device frame**: a CSS or SVG frame around a `<video>`, sized so the UI stays legible at 1280×720.
   - **Drop the sign-up, sign-in and onboarding flow from the main demo slides.** `01-install-to-home-screen` and `02-sign-in` go to backup at most.
   - Main demo order follows the use cases: create group, invite and join, photo, video and allowance, chat, reminder, cycle ends and film ready, watch film, archive and save, outsider denied.
   - The demo slides plus the quality-attribute slides (load test, scalability, maintainability via the pipeline) must fit in 12–15 min.
   - Keep `videos/demo.mp4` as the full backup.
   - You may re-cut clips with ffmpeg from `videos/clips/` or the raw takes in `videos/raw/`. Don't re-film unless a clip is unusable.
3. **Check for exact parity with what the lecturers want.** Recheck the deck and the script against:
   - the lecturer email's five sections and times: intro and PM 3–4 min; analysis and design with patterns 5 min; testing 3 min; CI/CD demo 10–12 min; system demo 12–15 min. Total 40 min, plus 5 min of Q&A.
   - the guidelines docx and the briefing deliverables. These include the database schema; the strategy for source code and artifacts; SAST, DAST, SCA, secrets, IaC, SBOM and provenance with real JSON artifacts; technical findings; burndown charts; effort per member; DoD; retros; and the quality attributes.

   Tighten the script so every slide's notes say exactly what to say, with the timings adding up.
4. **Visual QA.** Screenshot every slide at 1280×720 and look at each one. Large UML is full width, text is 14 px or more, and nothing overflows. Then re-export the PDF.
5. **Update `HANDOVER.md`.** Add a new top section with what changed, the final file list, and anything the owner must do before 14:30.

## Owner rules (non-negotiable)
- **No disclaimers anywhere.** No "simulated", "mock", "proposed", "not measured" and so on. The load test may use "measured" and "projected" columns.
- **Never show the demo cycle length** (30 min); the product cycle is 28 days.
- **One presenter**, Gopal Guruprasath. The team of five is in `records/TEAM.md`, with effort as an equal "agreed split".
- **All demos come from hosted dev** (https://d2m6kz76y4kuvm.cloudfront.net). The release environment is out of scope.
- **Never** modify the `rewind-app` repo, push, merge PRs, or touch AWS.
