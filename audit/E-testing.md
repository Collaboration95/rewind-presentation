# E. Testing inventory with dated numbers (Section 3, 3 min)

Commit: `f6cd896` (origin/dev, 20 Oct, merge of #585), worktree `rewind-present-audit`, clean (no tracked file edited).
Local runs: 26 Oct 2026, 21:42-21:58 SGT, Apple M5 (10 cores), Node 26.3.1 (CI uses `.nvmrc` 22.23.3), ffmpeg 9.0.2.
The Mac was shared with other agents (load average 5 to 95), so local timings are noisy and on the slow side.
CI numbers: run 39443030843 (Quality, PR #586 dev to main, 20 Oct 14:51 UTC) and run 39441043567 (Quality, push to dev, same SHA).

## 1. Headline numbers (all passed unless stated)

| What | Result | Source |
|---|---|---|
| `npm run test:fast` | root 122 (121 pass, 1 skip), server 1,006 (985 pass, 21 skip), Jest 1,674 pass; 0 fail; 2,802 tests in 40.9 s | local run, 26 Oct |
| Frontend coverage (`jest --coverage`) | statements 89.64%, branches 85.68%, functions 89.55%, lines 92.33%; 30.7 s | local; CI: 89.66 / 85.66 / 89.61 / 92.33 |
| Server coverage (`test:coverage:server`, SQLite) | lines 85.67%, branches 85.62%, functions 85.05%; 17 s | local; CI: 85.50 / 85.66 / 86.41 |
| Server suite on PostgreSQL 17 | 1,006 tests: 989 pass, 0 fail, 17 skip (SQLite-only); 38 s | local (own throwaway container), identical to CI (989/0/17, 137 s) |
| Playwright (41 tests, 9 files, incl. 6 Axe) | CI 20 Oct: 41 passed in 2.2 min. Local 26 Oct: first full run 40 passed, 1 FAILED; rerun of that spec file 4/4 passed | see 5 |
| Real-account E2E (Firefox, local HTTPS stack) | 2 consecutive runs, both passed, 153 s total. Not run in CI | local, 26 Oct |
| Deploy fixtures (`test:deploy`) | 11 scripts, all passed, 26 s (CI 20 s) | local |
| IaC gate unit tests (Python) | 6/6 passed | local |
| Static gates | format 6 s, lint 12 s, architecture under 1 s, typecheck 4 s, all exit 0 | local |
| Performance script | exit 0, 129.7 s, 1,200 requests, 0 errors, worst p95 6.47 ms (target 2,000); 3 films of 25 clips, 4.9 to 8.1 s (target 600 s) | local, 26 Oct, see 6 |
| Quality workflow wall time | 3 min 53 s (PR to main, with browser job); 3 min 23 s (push to dev, browser skipped) | CI |

Total automated test cases: about 2,850 = 1,674 Jest + 1,006 server + 122 root + 6 IaC unit + 41 Playwright + 1 real-account flow.
Test code is 66.2k lines (`tests/` + `server/tests/`) against 47.4k lines of source (`src/` + `server/src/`); 517 of 943 commits touch a test path.

## 2. Inventory by test type

| Type | Tool, location | Files | Cases | Catches | CI job | Blocks merge? | Time |
|---|---|---|---|---|---|---|---|
| Static gates | Prettier, ESLint, `tsc`, `scripts/check-architecture.mjs` | 4 checks | n/a (`architecture.test.mjs`: 2) | style, bug patterns, type errors, layer-boundary imports | "Static check (x)", 4-leg matrix | Yes, dev and main | 25-45 s each |
| Dependency audit | `npm audit --omit=dev --audit-level=high` | 1 | n/a | known-vulnerable production deps | "Production dependency audit" | Yes (inside aggregate) | 8 s |
| Frontend unit and component | Jest (jest-expo) + RN Testing Library, `tests/*.test.ts(x)` | 79 (45 .ts = 1,040 cases; 34 .tsx = 634) | 1,674 | screen logic, capture state, stores, uploader, playback, auth client | "Frontend tests and coverage" | Yes; 70% statement floor | 93 s CI, 40 s local |
| Server (API, auth, privacy, media, cycles) | `node --test`, `server/tests/*.test.mjs` | 66 | 1,006 | route behaviour, session/membership rules, media integrity, cycle engine, reminders | "Server tests and coverage" | Yes (no coverage threshold) | 118 s CI, 30 s local |
| Contract / API (my grouping) | same runner: `http-route-contract-{auth,media,real}` table-driven, plus 8 smaller contract, protocol and boundary-error files | 11 | 535 (507 in the three route-contract files) | route table drift; every `/real` route answers 401 for no, unknown and garbage session | same job | Yes | in server time |
| Security / authorisation (my grouping) | same runner: cross-group access, media tokens, media integrity, Cognito auth and callback failures, account safety, rate limits, HTTP limits, real-account auth, private media | 13 | 114 | outsider reads of group, chat, budget or media; tampered or sealed media; auth callback failures; brute force | same job | Yes | in server time |
| Migration / database (my grouping) | same runner: `migration-baseline`, `migration-chain`, `postgres`, `postgres-export`, `runtime-store`, `consistency-repair` and others; whole suite again on PostgreSQL 17 | 9 (plus full re-run) | 71 (plus 989 on PostgreSQL) | schema drift (fresh DB equals retired chain; PG schema equals migrated SQLite), dialect differences, repair of inconsistent data | "Server tests on PostgreSQL" | Yes | 198 s CI, 38 s local |
| Repo rules (root suite, 3 rows: 22 files, 122 cases in total) | `node --test`: `architecture`, `pwa`, `native-build`, `quality-classification`, `web-deployment`, `scaffold`, legal pages, runner and script tests, deploy `.mjs` | 17 | 90 | boundary violations (planted bad import is caught), PWA shell, change-scope classifier | "Root and IaC tests" | Yes | 59 s CI, 11 s local |
| Dependency-patch security | `braces-security`, `node-forge-security` (vendored patched tarballs) | 2 | 17 | regression of the patched `braces` and `node-forge` | same job | Yes | in root time |
| Terraform policy | `node --test`, `tests/terraform/` | 3 | 15 | IAM/deploy-role and web-distribution policy drift | same job | Yes | in root time |
| IaC scan gate | Python unittest, `tests/security/test_iac_scan.py` | 1 | 6 | expired, duplicate or unexpected scan exceptions pass the Trivy gate | same job | Yes | 0.1 s |
| Deploy fixtures | bash + Python + node, `tests/deploy/` and `deploy/tests/` | 11 .sh (+ `release-extraction.test.py`; the 2 deploy `.mjs` tests are in the root suite) | 16 named fixture groups, 5 injected-failure checks | backup, restore, release bundle, host lifecycle, failure injection (plan/apply/transfer/restore/health) | "Cloud-free deployment fixtures" | Yes | 20 s CI |
| Browser, responsive, a11y, PWA | Playwright + `@axe-core/playwright`, `tests/responsive/` | 9 | 41 (6 Axe/keyboard) | layout at several viewports, offline PWA shell, video capture and fallback, WCAG 2.x A/AA serious violations | "Web export and browser checks" | Main only (PR with base main, push to main); skipped for dev | 211 s job, 2.2 min tests |
| Real-account E2E | Playwright (Firefox) via `scripts/run-real-account-e2e.mjs`, `tests/e2e-real-account/` | 1 spec | 1 long flow | owner, invited member and outsider over strict local HTTPS, automatic next cycle | none | No (local only, in `test:slow`) | 1.2 min per run |
| Performance | `scripts/measure-real-group-performance.mjs` (+ 5 runner tests in root suite) | 1 | 1,200 requests, 3 films | p95 over 2 s, film not 720x1280/30 fps/audio, loudness outside -18..-14 LUFS, outsider privacy | none (not in workflow, package.json, Makefile or hooks) | No | 130 s |
| Hosted smoke | `deploy-dev.yml`: waits for Quality success on the SHA, `release-host.sh install` health checks (auto-restore), `curl /api/health` | n/a | 2 checks | broken release on the hosted host | "Deploy dev" (after merge) | No (post-merge; rolls back) | per deploy |
| Local gate | `.githooks/pre-push` mirrors the dev PR jobs; `pre-commit` runs the four static checks | n/a | n/a | failures before push | none | No (`--no-verify` skips) | minutes |

Reports only, not merge gates: CodeQL (`codeql.yml`) and Release security (Trivy images and IaC). Branch protection read on 26 Oct:
both `dev` and `main` require exactly one status context, "Format, lint, typecheck, and test" (strict, up to date), resolved conversations,
admins included; `main` also needs 1 approval. That aggregate needs 10 jobs green for dev (4 static legs, audit, root/IaC, server, PostgreSQL,
frontend, fixtures) and the browser job as the 11th for main. `gate` fails if any job is red or skipped unexpectedly.

## 3. Coverage cross-check (site, PR #581, today)

| Figure | quality.json | PR #581 body | CI f6cd896 | Local 26 Oct | Match? |
|---|---|---|---|---|---|
| Frontend statements | 89.6% | 89.6% | 89.66% | 89.64% | Yes |
| Frontend lines | 92.3% | 92.3% | 92.33% | 92.33% | Yes |
| Frontend tests | 1,674 | 1,674 | 1,674 | 1,674 | Yes |
| Server lines | "about 86%" | "about 86%" | 85.50% | 85.67% | Rounds up; say 85.5% |
| Server branches | 85.7% | 85.7% | 85.66% | 85.62% | Yes |
| PostgreSQL passed | 988 | 988 | 989 | 989 | Off by one (a test added after #581's run) |
| Server test files | 64 | n/a | n/a | 66 | No, 66 at f6cd896 |
| Frontend before #581 | 87% / 90% | 87% / 90% | n/a | n/a | PR #579 reports 87.05% / 89.66% after it; 77.38% / 80.70% before it |

The frontend coverage floor is 70% statements (`jest.config.cjs`), enforced in CI. Server coverage has no floor; it is uploaded as an artifact.

## 4. TDD and test-first evidence

- Site "TDD notes" (`quality.json`, section tdd-refactor) claims characterisation-first, "partly TDD". The history supports that, with timestamps (20 Oct, SGT):
  `5911086` 14:52 test pins media denials, then `49002de` removes legacy routes; `c3c240c` 14:57 pins HTTP route contract, then `354a6e1` splits `http.ts` (4k to 235 lines);
  `eb2e76a` 15:10 pins six client screens (4,516 lines of tests and doubles), then the VideoCapture, Settings and group-experience splits.
- Red then green across two PRs: #579 (`4ed732d`, 14:47, 23 `*.coverage.test.*` files) recorded two bugs as `it.skip` with `// BUG:` comments; #580 (`5d5cc72`, 15:27) fixed both and re-enabled the tests.
- Test-then-change in #584: `real-archive.test.mjs` pinned a null audit actor, then was intentionally changed with the fix (`9e2e022`); same for the stale session cookie (`c036e75`). Commit messages say "Tests first".
- Limits to say plainly: in #581 the "Try again" test and its fix are one commit (`1ebfc64`), so history alone cannot prove red-then-green. I proved it today (section 7). Day-to-day features are not strict TDD.
- Coverage-driven tests: 23 of 79 Jest files are `*.coverage.test.*` (829 of 1,674 cases, 50%), written in #579 to lift statements from 77.4% to 87.1%. They still found 2 bugs, but do not call them all behaviour specs.

## 5. Flakiness and known issues seen today

- Playwright `injected-recording.spec.ts:75` ("moving video") failed once in the first local full run (pixel-motion assertion, machine load about 14); rerun of the spec file passed 4/4. CI at 20 Oct was 41/41. The team's notes already list one flaky Chromium test.
- `npm audit --omit=dev --audit-level=high` FAILS today at f6cd896: 3 high findings, zod below 4.6.6 (GHSA-mrhx-c7xc-m3w5) under `expo`. It was green on 20 Oct; branches fix/587 and fix/588 (PRs #589 and #590, runs of 24 Oct) are red on "Production dependency audit", so a new PR to dev is blocked right now. Fix or accept before the CI/CD demo (Section 4), or the demo run will show red.
- First local PostgreSQL attempt was invalid: my own throwaway container was OOM-killed by the 1.9 GiB Docker VM (10 "not yet accepting connections" failures). Rerun on a fresh, memory-capped container: 989/0/17. Both containers removed; `rewind-pg-dev` and `dc2-v1-shortlane-local-postgres-1` untouched.
- `test:slow` is `build:web && check-pwa && playwright && real-account`; a Playwright failure skips the real-account step, so I ran `npm run test:real-account-e2e` separately.
- All 21 server skips on SQLite are PostgreSQL-only tests; all 17 on PostgreSQL are SQLite-only. Root skip: 1 nginx test (no nginx locally).

## 6. Performance results (the only measured numbers)

Script: `scripts/measure-real-group-performance.mjs` (692 lines; accepts no arguments or URLs; #353, #526). Not in CI.
Protocol: 3 repetitions; 5 members plus 1 outsider; 5 concurrent clients; 30 s warm-up; 100 samples per operation (group, prompt, budget, chat) per repetition; 25 generated 6-second clips compiled by real FFmpeg.
Environment: local SQLite, loopback HTTP, load generator and server in one Node process. It is not PostgreSQL, hosted, S3 or device performance (the doc says so).

| Run | Date, commit | API p95 (all four operations) | Errors | Film (25 clips, 150 s) | Loudness |
|---|---|---|---|---|---|
| 12 Oct (#526, doc) | `a1dc77e` + patch, Apple M5 | 4.3 to 9.7 ms | 0 | 5.0, 5.7, 9.0 s | -17.4 LUFS |
| 26 Oct (this audit) | `f6cd896`, clean tree, exit 0 | run 1 5.1 to 6.5 ms; run 2 4.0 to 4.3 ms; run 3 5.0 to 5.3 ms | 0 of 1,200 | 4.9, 8.1, 4.9 s; 720x1280, 30 fps, audio | -17.4 LUFS |

Targets: p95 at most 2,000 ms for non-media calls; film boundary-to-ready at most 600 s; loudness -18 to -14. Privacy checks inside the run: outsider group 404, budget 403, chat 403, prompt 403, non-owner prompt 403, sealed clip not advertised.
Also present, not run: `scripts/measure-database-calls.mjs` (PostgreSQL round trips per request, #261). No load test (k6/Artillery) and no hosted measurement exist.
Site wording to fix: "1,200 API requests and 25-clip film compilation per run" is really 3 repetitions, each with its own 25-clip film.

## 7. Verification of the example bug (done today)

- #581 "Try again does nothing after a failed photo capture" (`CameraCaptureScreen.tsx`): I reversed the `1ebfc64` source change on an untracked scratch copy of the current file and ran the new test. Pre-fix: FAIL ("Try again after a failed capture returns to the viewfinder for a fresh capture"). At `f6cd896`: PASS. Scratch copy deleted; worktree clean.
- #579/#580 `normalizeBaseUrl('/')`: replaying the old and new logic on `'/'` gives "rejected" and `"/"`. The old code stripped the slash before the same-origin check. (A logic replay, not the module itself.)

## 8. Proposed Section 3 (3 minutes, 3 slides)

Slide 1 (60 s), pyramid. Headline: "2,802 fast tests finish in 41 seconds on a laptop and run in CI on every PR; 42 slower browser and end-to-end tests guard what only a browser can show."
Layers, base to top, with real counts: static gates (4 checks + dependency audit) / Jest 1,674 / server 1,006 (run on SQLite, then 989 again on PostgreSQL 17) / root and policy 122 + IaC 6 + deploy fixtures 11 /
Playwright 41 (6 Axe) / real-account E2E 1 flow. Side box: "measured 26 Oct at f6cd896; coverage 89.6% statements frontend, 85.5% lines server". Footnote: performance script is separate (slide 2).

Slide 2 (70 s), table. Headline: "Ten checks must be green to merge to dev, eleven for main; scans and the performance run report but do not block."
Columns: type, tool, CI job, blocks merge?, number. Rows from section 2 (merge them into about 9 rows). Show the performance row last, with "p95 at most 6.5 ms over 1,200 requests; film of 25 clips in 4.9 to 8.1 s; local SQLite only, not in CI".
Say aloud: browser tests join only for main; real-account E2E and the performance script run by hand before a release; CodeQL and Trivy report but are not required checks.

Slide 3 (50 s), example. Headline: "Pinning tests before a refactor found a real bug: 'Try again' after a failed photo capture did nothing (PR #581)."
Show: the 18-line test, the fix (the retry called `captureImage` with `requireAccess`, which returns at once unless the screen is 'ready'), and "fails before, passes after (re-verified 26 Oct)".
Second case on the same slide: PR #579 recorded two bugs as skipped tests with `// BUG:` comments (14:47), PR #580 fixed them and re-enabled the tests (15:27, same day).
Closing line: "We call this characterisation-first, not strict TDD."

Likely Q&A (answers backed above): Why 70% floor when measured 89%? (safety net, not target). Are browser tests on every PR? (No, main only; why: cost and flake). Do tests touch AWS? (No; S3/Cognito/web push use protocol fixtures; deploy fixtures labelled cloud-free). Is half your Jest suite coverage padding? (829 of 1,674 are coverage-named; they found 2 bugs; behaviour tests cover privacy and cycles). Performance in production? (Not measured; local only). DAST? (None in any workflow.)

## 9. Reproduce

`npm ci && npm run test:fast`; `npm run test:coverage:frontend`; `npm run test:coverage:server`; `REWIND_TEST_POSTGRES_URL=... npm run server:test:postgres`;
`npx playwright test --list` (41 tests); `npm run test:real-account-e2e`; `node scripts/measure-real-group-performance.mjs`; `gh run view 39443030843 --log`.
