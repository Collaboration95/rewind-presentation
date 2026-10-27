# Deck verification · 27 October 2026

The current detailed report is QA-REPORT.md.

- 20 main narrative slides, 12 timed feature inserts, 25 backup pages: 57 HTML/PDF frames.
- Timing: 3:30 + 5:00 + 3:00 + 12:00 + 14:30 = 38:00.
- All 23 UML SVGs have full-width views; every split view and agile chart prints to PDF.
- All still images are embedded in deck.html. Twelve final feature MP4s remain linked; total playback 11:00. videos/demo.mp4 is 11:12.
- All 57 slides captured at 1280×720 and visually reviewed. Smallest UML text: 14.055 px. No overflow, broken images or browser page errors.
- Arrow/hash navigation, notes, overview and overview clicks, clip playback/pause-on-leave, and command cards passed.
- Chrome PDF export: 57 pages, 960×540 pt; 17 sample pages visually reviewed.
- CI/CD video integration remains at s18: videos/cicd/cicd-demo.mp4 → deck/clips/ci-cd-40344230832.mp4.
- Final load-results integration remains at s20 and B11, including model consistency and the re-export.

See out/qa/render-check.json for browser checks and QA-REPORT.md for full requirement parity, factual evidence and exact integration paths.
