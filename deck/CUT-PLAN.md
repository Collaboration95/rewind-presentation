# Cut plan: 35-minute hard limit (owner approved, 27 Oct)

The total must fit in 35 minutes, demos included.
- **Target is 33:00 of content plus 2:00 for interruptions.**
- The main path is about 32 slides. Everything removed from it goes to **backup**, not deleted.
- Keep it technical and on topic.

| Section | Budget | Main slides |
|---|---|---|
| 1. Intro & project management | 3:00 | 3 |
| 2. Analysis & design + patterns | 5:00 | 7 |
| 3. Types of testing | 3:00 | 5 |
| 4. CI/CD demo | 10:00 (about 6:00 of slides, then about 4:00 live in GitHub) | 8 |
| 5. System demo + quality attributes | 12:00 | 9 |

## 1. Intro & project management (3:00)
- **s1:** cover with the iPhone, about 10 s.
- **s2:** business problem and scope.
- **s3:** sprints, milestones, status and outstanding issues.
- **New PM slide:** one burndown chart (move the best Sprint chart from B21–B23 here), equal effort split, DoD, and retro outcomes. The other burndowns stay in backup.

## 2. Analysis & design (5:00)
- **Keep:**
  - s4 use case diagram;
  - s5 architecture decisions;
  - s6 analysis→design;
  - s9 schema / keys (the database schema is required);
  - D1 state diagram and D2 UI flow page.
- **Merge s7 + s8** into one cycle-sequence slide (the more representative figure). Move the other to backup.
- **New main slide: "Design problems and patterns".** For each pattern, give the problem, the pattern chosen and where it lives:
  - Strategy + Adapter for media storage (disk/S3);
  - Observer for chat (RealtimeHub);
  - Adapter for persistence (PostgreSQL).

  Use small thumbnails or a table. The full pattern diagrams stay in B7–B9.
- **Drop the design jump** (8 → 69 → 70 → 9) and its notes.

## 3. Testing (3:00, 5 slides)
1. Overview matrix: type × tool × count × when it runs (blocks merge / main only / on demand). Add one spoken line explaining what "blocks" and "reports" mean.
2. Unit and component tests (Jest, node:test), with the "Try again" bug as the example (merges T2 + s11).
3. Integration: API routes on a running server, plus the same suite on PostgreSQL 17 (T3 + T4).
4. End-to-end: Playwright, plus the PWA build and accessibility with axe (T7 + T8 + T9).
5. Security testing (in the suites and in the pipeline), plus a one-line pointer: "performance is shown in the system demo" (T10).

- **To backup:** T1, T5, T6, T11, T12 and the old per-type slides.
- **Load test:** show it once only, in section 5.

## 4. CI/CD demo (10:00)
About 6:00 of slides:
1. **C1 + C2:** pipeline overview with the legend merged in (colour = what a failure blocks; shape = element type).
2. **C3:** source code and artifact management strategy (required).
3. **C4 + C5:** PR gates (the Quality fan-out into one required check, with security workflows alongside).
4. **C6 + C7:** deploy: scan and sign the exact bundle, keyless AWS (OIDC), health check, activation.
5. **C8 + C15:** DAST: ZAP after every deploy, with the real results (0 High / 4 Medium, all from the CSP gap).
6. **C10 + C11:** SAST triage (CodeQL alerts 54–56 with reasons), and SCA (the zod advisory blocked merges until #591 fixed it).
7. **C17:** technical findings (required).
8. **C18:** demo route.

Then about 4:00 of live GitHub clicks, with the recorded clip (CB1) as the fallback.

**To backup:** C9 catalogue, C12, C13, C14, C16.

## 5. System demo + quality attributes (12:00)
- **s19:** journey intro, short.
- **Feature clips (about 7:30 in total):**
  - F3 prompt (trimmed);
  - F4 invite / one membership;
  - F5 photo;
  - F6 video + allowance;
  - F7 chat;
  - F9 + F10 merged (film ready, then the reveal);
  - F11 archive;
  - F12 outsider denied.
- **F8 reminder:** to backup.
- **Performance:** a scripted load test against hosted dev; method plus results at 100 users (p95 1,336 ms, 17.84 req/s, 0 errors) on one slide. Use the T11/T12 content here.
- **Scalability:** the capacity model and the scale-out path (s20, trimmed to about 1:30).
- **Maintainability:** one spoken line pointing back to the pipeline just shown (it can sit on the scalability slide).

## Rules
- **SCRIPT.md:** rewrite to a strict 33:00, with a clock per slide.
- **OUTLINE.md and HANDOVER.md:** regenerate the outline and update the top section of the handover.
- **Slide counter:** visible on every slide, matching the physical page numbers.
- **Overview and jump links:** fix them.
- **Build source:** make all edits there so a rebuild keeps them.
- **Check:** screenshot every slide at 1280×720 and look at each. Text is 14 px or more, nothing overflows, and every video, iframe and figure loads.
- **Content rules:** no disclaimers, no 30-minute cycle, no document-reference footers.
- **PDF:** re-export it.
- **Backup:** first copy the current deck to `deck/out/pre-cut-backup/`.
