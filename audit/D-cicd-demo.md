# D · CI/CD demo: flow, real timings, storyboard (checked 26 Oct 2026, ~21:55 SGT)

Code read: worktree `rewind-present-audit` = origin/dev `f6cd896` (20 Oct). Repo is public, so run logs and settings pages are showable. Tags: [verified] = read from code, logs or API; [inferred] = reasoning. Read-only: I triggered, merged and changed nothing.

## 0. Read first: the pipeline is red for any NEW PR tonight

Two things changed after 20 Oct with no code change on dev. Both break a fresh run [verified]:

1. **`npm audit --omit=dev --audit-level=high` now fails** (job "Production dependency audit", inside the gate). Advisory GHSA-mrhx-c7xc-m3w5 (zod < 4.6.6, via expo > @expo/cli). Replaying `f6cd896`'s lockfile today fails; the same commit passed on 20 Oct (run 39443030843). Seen live on PR #589 run 40140117765 and PR #590 run 40140169768.
2. **The runtime image no longer builds**: `deploy/Dockerfile:25` pins `ffmpeg=8.1.2-r0`, Alpine v3.24 now ships only `8.1.3-r0` (I read the APKINDEX). "Scan runtime image" failed on PR #590 (run 40140169755, step "Build candidate image"). [inferred, high confidence] `release.py build` runs the same `docker build -f deploy/Dockerfile` (release.py:268-273), so the next code-changing merge to dev fails at Deploy dev "Build the verified release bundle". The host keeps its previous release.

Consequence: a green PR-to-live-on-dev run cannot be staged tonight until a fix PR lands (section 6, step 1). Lockfile-only test in /tmp: `overrides: {"zod": "4.6.6"}` gives `npm audit` 0 vulnerabilities; whether @expo/cli runs on zod 4 is untested, so run `npm run build:web` before merging. Do not weaken `--audit-level`.

The same red is a free, honest "blocked merge" exhibit (section 5, shot 5). Do not click "Update branch" on #589/#590 before the talk or the red runs stop being the latest.

## 1. Measured timings (400 runs, 8-26 Oct; wall clock = run startedAt to updatedAt)

| Workflow / event | n (ok) | Median | p90 | Range | Notes |
|---|---|---|---|---|---|
| Quality, PR, code change | 56 | 4.0 min | 4.7 | 2.5-11.6 | 20 Oct runs: 3.4-4.4. Slow tail = apt-get hang on 8 Oct |
| Quality, PR, docs-only | 24 | 0.3 min (~20 s) | 0.8 | 0.3-0.8 | e.g. run 38698434887 |
| Quality, PR to main | 1 shown | 3.9 min | | | run 39443030843; extra job "Web export and browser checks" 3.5 min is the critical path |
| Quality, push dev/main | 31 | 3.8 min | 4.0 | 1.9-4.2 | |
| CodeQL (PR or push) | 85/33 | 1.9 min | 2.3 | | jobs: js-ts ~105 s, python ~50 s, actions ~45 s, classify 8 s |
| Release security (PR, path-filtered) | 65 | 1.1 min | 1.2 | 1.0-1.7 | runtime image 56 s, web image 62 s, IaC 14 s |
| Deploy dev | 27 | 7.3 min | 7.7 | 6.1-8.0 | includes ~225 s waiting for Quality |
| Deploy release | 4 total | n/a | | | 3 of 4 never ran past approval (section 3) |
| database-operations | 0 runs | n/a | | | `workflow_dispatch` only, no runs in history; do not demo |

Per-job medians in a PR Quality run (8-run sample, all parallel after a ~8 s classify): Server tests on PostgreSQL 202 s (critical path), Server tests (SQLite) 124 s, Frontend+coverage 94 s, Root and IaC tests 70 s, lint 51 s, format 38 s, typecheck 36 s, architecture 25 s, fixtures 20 s, npm audit 10 s, gate 3 s. Queue delay about 4 s.
Deploy dev steps (median): wait for Quality 225 s, build bundle 56 s, OIDC 5 s, ship bundle 52 s, apply settings 5 s, install + health 66 s, cleanup 2 s.
Merge to live on hosted dev: PR #585 merged 14:38:12Z, GitHub Deployment `success` 14:45:01Z = 6 min 49 s [verified].
Whole loop (open PR, 4 min checks, merge, 7 min deploy) is about 11-12 min of machine time: it cannot run live inside a 10-12 min slot.

## 2. Health now

| Item | State [verified] |
|---|---|
| dev `f6cd896` (20 Oct) | Quality 39441043567, CodeQL 39441043794, Deploy dev 39441043830 all success |
| main `f6e50ac` (19 Oct) | Quality push 39205848927 success; weekly CodeQL schedule success today 09:06 UTC (run 40297081627) |
| Open PRs | #586 dev to main: all checks green on 20 Oct, `REVIEW_REQUIRED`, 0 reviews, diverged (63 ahead, 1 behind). #589 and #590: red (section 0) |
| Failures in 18 days | PR Quality 18 of 100 failed: 11 browser job on main-promotion PRs (12-15 Oct, since green), 4 "Cloud-free deployment fixtures" (3 PR + dev push 52b8e01), 2 npm audit (today's issue), 1 deps, 1 server tests. Deploy dev 5 of 40 failed (2 refused because Quality failed, 2 real tooling bug after #581 fixed by #583, 1 install on 8 Oct) |
| Intermittent | "Cloud-free deployment fixtures" is the one to watch (log of 52b8e01 shows a test assertion, not infra). Notes from 8 Oct also list apt-get hangs; none seen in the last 14 days |
| CodeQL results | 0 open alerts, 17 dismissed (each with a written false-positive reason), 5 fixed. 1 open Dependabot alert (sprintf-js, medium) |

## 3. Environments, secrets, rollback

**Hosted dev: up.** https://d2m6kz76y4kuvm.cloudfront.net (README.md:16, deploy/README.md:19): `/api/health` HTTP 200, 0.9 s, PostgreSQL, schema ready, migration 31.
- Health `version` is the constant `0.1.0` (`server/src/config.ts:6`), so it cannot show the commit. Commit evidence instead: GitHub Deployments for environment `dev` newest = `f6cd896` success 14:45:01Z (equals origin/dev); deploy log line "Activated release f6cd8969... after runtime and web health checks"; `index.html` Last-Modified 14:42:25 GMT sits inside that run. Page: https://github.com/Collaboration95/rewind-app/deployments
- Unknown paths such as `/version.json` also return 200 (nginx SPA fallback), so a 200 proves nothing except for `/api/health`.

**Release: down.** Not in the repo (Terraform output `web_url`); the URL in my notes, https://d2r0xzy7vz590e.cloudfront.net/api/health, returned **504** (CloudFront cannot reach the origin). Why [verified]: the 19 Oct dispatch run 39206079519 was `prepare` (health step skipped), approved after ~23 h; the later run 39373300339 (20 Oct 05:08) is still `waiting`; the only app-installing runs were never approved. Per owner notes release is down by choice: say "release is deliberately not promoted yet", not "broken".

**Approvals** [verified via API]: environment `dev` has no protection rules. Environment `release` needs reviewer `AndrewNguyenLKN`, self-review prevented, deploys from `main` only; Collaboration95 shows `current_user_can_approve: false` on the pending run, so the waiting page is safe to show.

**Credentials**: no AWS keys in GitHub. Job has `id-token: write`, step "Assume the deploy role with GitHub OIDC" calls `sts assume-role-with-web-identity` (3600 s session, values masked). Role ARN is a repo *variable* (`AWS_DEMO_DEPLOY_ROLE_ARN`). IAM trust (`infra/terraform/demo/deploy.tf:25-62`) accepts only `environment:dev` and ref `refs/heads/dev`; release role only `environment:release`. Host access is a Lightsail temporary SSH key, port 22 opened to the runner's /32 and closed in an `always()` step. App settings are not in GitHub: Terraform writes a private S3 `_config/` object, the step streams it over SSH to `release-host.sh configure`. No SSM. The only repo secret is `OPENAI_API_KEY`, used by no workflow.

**Rollback** [verified, deploy/release-host.sh:266-296]:
- Automatic, inside the deploy: `install` starts the new images, `health_ready` polls 30 x 2 s on `127.0.0.1:8787/health` and `127.0.0.1/api/health`, then `running_images_match` checks image ID and revision label. On failure `restore_current` reloads the previous release and the step goes red ("upgrade health failed; prior release restored").
- Manual: `./deploy/release-host.sh rollback` on the host over SSH. It refuses if the database schema is newer than the target.
- Nothing triggers rollback after activation (no alarm-driven or CI-button rollback). Say this plainly.
- Real evidence of the guards: Deploy dev 39381789166 refused to deploy because the push Quality run failed; 39432025788 failed at "Build the verified release bundle" ("no declared schema migration versions") before touching the host.

## 4. The real path and who decides what

`commit` > PR to `dev` > Quality (+ CodeQL + Release security + GitGuardian) > merge > push Quality on the merge commit and Deploy dev (same push, deploy waits) > hosted dev. Then PR `dev` to `main` > Quality + browser job > 1 review > merge > Deploy release > approval > release host.

| Decision | Made by (file or setting) | Blocks or reports |
|---|---|---|
| Which jobs run | job "Classify change scope" = `scripts/classify-quality-changes.mjs`, output `docs_only` feeds every `if:` (quality.yml:18-46). Log line `{"docsOnly":false,"reason":"runnable-change"}`. Only `.md` under root, docs/, doc/, skills/ counts as docs. Unknown base commit: runs everything. Same job copied into codeql.yml, deploy-dev.yml, deploy-release.yml | decides |
| Browser/PWA/a11y job | `if: ref == main \|\| base_ref == main` (quality.yml:189) | main-bound only |
| May the PR merge | job `gate` "Format, lint, typecheck, and test" (`needs` all, `if: always()`, quality.yml:270) is the **only** required context (dev and main protection, app_id 15368). Dev: up-to-date required, 0 approvals, conversation resolution, enforce_admins. Main: also 1 approval with last-push approval | **blocks** |
| SCA | "Production dependency audit", `npm audit --omit=dev --audit-level=high`, inside the gate | **blocks** (high+) |
| SAST | CodeQL js-ts, python, actions, `security-extended`; PR, push dev/main, Monday cron | **reports** (not required) |
| Image + IaC scan | Trivy in release-security.yml: HIGH/CRITICAL `exit-code 1`, SBOM kept 30 days; PR (path filter), `v*` tags | **reports**: red on the PR but not required, and no deploy workflow consults it |
| Secrets | GitGuardian app check (not required) + GitHub secret scanning with push protection (enabled) | push protection blocks the push; GitGuardian reports |
| DAST | none in any workflow | say so |
| Deploy to dev | step "Wait for this commit's dev Quality checks" (polls push run for the SHA, 1500 s max, refuses on failure) | **blocks** |
| Promote to main | PR review rule above, plus Quality must be up to date with main | **blocks** (human) |
| Deploy to release | environment `release` reviewer approval | **blocks** (human) |
| Rollback | section 3 | automatic at install only |

## 5. Storyboard (12:00 total; 11:30 plus 30 s slack)

URLs are the existing runs, so every shot works today. After staging, swap in the new run IDs. All pages need a logged-in Collaboration95 browser (settings pages need admin).

| # | Time | Page | Point at | Say (one sentence) | Mode | Fallback |
|---|---|---|---|---|---|---|
| 1 | 0:00-0:50 | Slide: one pipeline picture with the scans inside it, 6 numbered decision points, "blocks" vs "reports" in two colours, plus a deployment strip (dev host, release host) | the numbers | "Six decisions are made in this picture, and four security scans sit inside it; I will show where each one lives." | slide | n/a |
| 2 | 0:50-2:10 | PR checks box: staged PR (after staging) or `/pull/586` (all checks green at 20 Oct) | "Classify change scope", 4 x "Static check", "Production dependency audit", 3 x "CodeQL (...)", "Scan runtime/web image", "Scan IaC configuration", "GitGuardian", last "Format, lint, typecheck, and test" | "These are the checks on one PR: dependency audit is SCA, CodeQL is SAST, Trivy scans images and Terraform, GitGuardian watches secrets." | live | screenshot of #586 |
| 3 | 2:10-3:10 | `/settings/branches` > rule for `dev`, then `main` | "Require status checks": exactly one name; "Require branches up to date"; main "1 approval" | "Only the gate check blocks a merge; CodeQL, Trivy and GitGuardian show on the PR but do not block, so I will call them reporting, not enforcing." | live | screenshot |
| 4 | 3:10-4:30 | Actions run 39443030843 (graph), open step log of "Classify change scope"; then docs-only run 38698434887 | graph fan-out from classify; `docsOnly:false` line; the docs-only run: 8 jobs skipped, gate green in ~20 s | "This one job decides scope: a code change fans out into parallel lanes, a markdown-only change finishes in 20 seconds and says no application tests ran." | live; optional live: open a pre-pushed docs-only branch as a PR and watch ~25 s | both runs exist |
| 5 | 4:30-5:45 | `/pull/590`, then run 40140117765 log "Production dependency audit", then 40140169755 "Scan runtime image" | red audit lines "3 high severity vulnerabilities"; red Trivy build; disabled "Merge" with "Required statuses must pass" | "Nobody changed code: on 24 October a new advisory and an Alpine package bump turned both PRs red, and the gate blocked the merge until we fixed it." (use only if the fix PR is done; else say "this is what blocks us now") | live | screenshots; throwaway failing-test PR if #590 was touched |
| 6 | 5:45-6:45 | `/security/code-scanning`, then "Closed" tab; run page artifact `release-security-runtime-<sha>` | "0 open", 17 dismissed with comments, 5 fixed; SBOM artifact | "CodeQL reports go to Security; we triage each finding with a written reason, and we have no DAST today: a ZAP baseline against hosted dev is the first thing we would add, as a non-blocking step after deploy." | live | screenshot |
| 7 | 6:45-8:45 | Deploy dev run 39441043830 (or staged), expand steps; then https://d2m6kz76y4kuvm.cloudfront.net and `/api/health`; then `/deployments` | step "Wait for this commit's dev Quality checks" 3m45; "Assume the deploy role with GitHub OIDC" 5 s; "Install the release" 66 s; Deployment `f6cd896` success; staged visible UI change | "Deploy waits for the same commit's Quality run, gets 1-hour AWS credentials through OIDC instead of stored keys, and the host only switches after its own health check passes; here is the change on hosted dev." | live | recording / screenshots; local `make run` per demo.json fallback |
| 8 | 8:45-10:15 | `/pull/586` (63 commits, "Review required"); then run 39373300339 "Waiting"; then `/settings/environments` > release | Quality incl. "Web export and browser checks"; reviewer name; "prevent self-review"; branch policy main | "Promotion to main needs a green gate that also includes the browser job, one approving review, and a second human approval on the release environment; release is deliberately not deployed yet." Do not click "Review deployments" | live | screenshots |
| 9 | 10:15-11:30 | GitHub file view `deploy/release-host.sh` lines 266-296; then runs 39381789166 and 39432025788 | `candidate_ready`, `restore_current`; two red Deploy dev runs | "Rollback is decided on the host: bad health restores the previous release automatically, a manual rollback command exists, and nothing rolls back after activation." | live | screenshot |
| 10 | 11:30-12:00 | Closing slide: block/report table + DAST stance | | "Blocks: gate, audit, review, approval. Reports: CodeQL, Trivy, GitGuardian. Missing: DAST." | slide | n/a |

Cut order if over time: shot 9 to 30 s, then shot 6, then 4's docs-only half. Never cut 2, 3 or 8 (the three assessor asks). Rule from demo.json: never merge, push or deploy on stage; at most open the docs-only PR in shot 4.

## 6. Prerequisites to stage tonight, in order (times SGT, now ~21:55)

1. **Fix the two red items (about 25 min work, 6 min CI).** One PR to dev: ffmpeg pin to `8.1.3-r0` (`deploy/Dockerfile:25`) and a zod fix that makes `npm audit --omit=dev --audit-level=high` pass. Check locally first: `npm audit --omit=dev --audit-level=high`, `docker build -f deploy/Dockerfile .`, `npm run build:web`, `npm run test:fast`. Open ~22:25. Expected: Quality ~4-5 min, Release security ~1 min (touches deploy/**), CodeQL ~2 min, all done ~22:31. If either fix cannot be made safe, jump to plan B below.
2. **Merge it (~22:32).** Push Quality ~3.8 min and Deploy dev ~7.3 min run together, hosted dev updated ~22:40. Verify: Deployments page shows the new SHA `success`, `/api/health` 200. PR #586 re-runs on its own (its head is `dev`): confirm it goes green again incl. the browser job (~4 min), and leave it unapproved and unmerged.
3. **Demo UI PR (~22:42).** Branch from the new dev tip (strict mode: an older branch is BEHIND). One visible, reversible copy change on the welcome screen, e.g. the "Developer sign-in" link text, `App.tsx:484` (no test greps that text; testID is used) [inferred, confirm with `grep -rn` first]. Expect checks done ~22:48 (Quality 4 min, CodeQL 2, Release security 1 as `src/**`/`App.tsx` match). Merge ~22:49, hosted dev shows it ~22:57. Keep the merged PR and its Deploy dev run IDs for shots 2, 7.
4. **Throwaway failing PR (optional, ~22:50).** Break one frontend assertion on a `demo/blocked-test` branch; "Frontend tests and coverage" red in ~1.5 min, gate red at ~4 min. Only needed if #590 gets updated or fixed.
5. **Freeze and capture (~23:00).** Do not touch #589/#590. Screenshot every shot page (fallbacks). Note final SHAs and run IDs in the shot list.
6. **Record the backup video at real length (~23:15 to 00:00).** All 10 shots, 12 min, one take plus retake. Title card: "Recorded 26 Oct 2026, dev `<sha>`". Say "recording" aloud on it.
7. **Tomorrow.** 09:00 re-open tabs, check hosted dev health and Actions status page. Freeze merges to dev from 12:00: any merge starts a 7-minute deploy and moves "latest". 14:00 recheck login, tab order, zoom 125%.

**Plan B (fix not ready by ~23:30):** keep everything on existing artifacts, which are all valid today (runs listed in section 5). Present shot 5 as "this is the current state; the gate blocks us", say hosted dev runs the 20 Oct commit, and skip the "new change appears" half of shot 7. No claim is lost, only freshness.

## 7. Other facts and caveats

- Two Quality runs per change: PR head (gates the merge) and merge commit (gates the deploy). Do not add the two durations (docs/site cicd.json already says this).
- Release security only fires on path matches (`src/**`, `server/**`, `deploy/**`, `infra/**`, `.github/workflows/**`, package files, App.tsx); a docs-only PR skips it, which is why #589 has no Trivy run.
- CodeQL on PRs has its own classify job; a docs-only PR skips CodeQL too.
- Deploy logs (public) print the dev host IP; acceptable, but zoom past it.
- Existing site pages (`cicd.json`, `demo.json`) already state block vs report correctly; `demo.json` step 8a/8b is only ~3.5 min and must be replaced by this storyboard.
