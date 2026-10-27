# C - DevSecOps gates and gaps (Rewind, audited 26 Oct 2026)

Code: worktree `rewind-present-audit` = origin/dev `f6cd896`. Read-only. Tags: **[V]** verified (file, API, log or local run), **[I]** inferred.
Everything below that says "run #N" is a workflow run number; the run ID is in section 7.

## 0. Read this first (five things that change the story)

1. **The pipeline is red on a fresh push to dev today [V].** Two things rotted after 20 Oct, the last green dev run (Quality #955, deploy-dev #119, both on `f6cd896`).
   - **npm audit.** `quality.yml:88` (`npm audit --omit=dev --audit-level=high`) fails on the `f6cd896` lockfile. I re-ran it on a copy on 26 Oct: 3 high, all from `zod 3.25.76` nested under `expo/@expo/cli` (GHSA-mrhx-c7xc-m3w5, fix only via `npm audit fix --force` to expo 54). Quality #957 and #958 (PRs #589, #590) failed on exactly this. Audit is inside the required gate, so **no PR can merge to dev until it is fixed or excepted.**
   - **ffmpeg pin.** `deploy/Dockerfile:25` pins `ffmpeg=8.1.2-r0`. Alpine 3.24 now only has `8.1.3-r0`. I confirmed this with `apk policy ffmpeg` in `node:24.21.0-alpine3.24` today, and Release security #462 failed with "ffmpeg-8.1.3-r0 breaks world[ffmpeg=8.1.2-r0]". `deploy-dev.yml` builds that Dockerfile via `deploy/release.py:272`, so **a live re-run or new push of Deploy dev also fails at "Build the verified release bundle".**
   - **Consequence.** Demo from the recorded/last-green runs (section 7), or fix both first (about 30-45 min including CI). Do not promise a live push-to-deploy unless both are fixed and one full run is rehearsed.
2. **Only one check is enforced by branch protection** [V]: `Format, lint, typecheck, and test` (the Quality gate job, `quality.yml:270`). CodeQL, Trivy images, Trivy IaC, GitGuardian, Dependabot and secret scanning are **not** required checks. Dev and main protection list the same single context. No rulesets exist.
3. **No DAST in any workflow on dev or main [V].** The only DAST attempt is draft PR #438 (Vigolium, unmerged, never run on dev). The carry-over note is right on that.
4. **The carry-over missed two things that exist [V]**: an **IaC scan** (Trivy config plus an exact-finding gate, `release-security.yml:78-105`) and **CycloneDX SBOMs** per image (`release-security.yml:49-56`). Both should appear on the pipeline picture.
5. **Release security does not run on push to dev/main** [V `release-security.yml:3-20`]. It runs only on PRs matching path filters, on `v*` tags and by manual dispatch. `deploy-dev.yml:104-128` waits only for the `quality.yml` push run, not for CodeQL or Release security.

## 1. Pipeline security table (workflow files at f6cd896)

"Fails job" = a failure turns that job red. "Required" = named in branch protection. Only the Quality gate is required.

| Stage | Job / step | Tool | Trigger | Blocks? | Required by protection? |
|---|---|---|---|---|---|
| Push | Secret scanning + push protection | GitHub native (repo setting) | every push | push protection blocks known-pattern secrets at push time; alerts otherwise report. 0 open, 0 resolved | n/a (setting) |
| PR | GitGuardian Security Checks | GitGuardian app | PR | report-only status (success on #586) | No |
| Local | `.githooks/pre-commit`, `pre-push` | prettier, eslint, tsc, tests | commit/push (set by `npm prepare`) | blocks locally; `--no-verify` skips. No security tool | No |
| Scope | `changes` "Classify change scope" (`quality.yml:18-46`) | `scripts/classify-quality-changes.mjs` | PR, push main/dev | decides `docs_only`; fails safe (runs everything) when base unavailable | via gate |
| Quality | Static check x4 (`:50-72`) | prettier, eslint, architecture, tsc | PR, push | fails job; counted by gate | via gate |
| Quality | **Production dependency audit** (`:74-88`) | `npm audit --audit-level=high` (SCA) | PR, push | **fails job at high+; counted by gate; currently red** | via gate |
| Quality | Root and IaC tests (`:90-123`) | node tests, `python -m unittest tests/security` (6 tests of the IaC gate logic) | PR, push | fails job | via gate |
| Quality | Server (+coverage), Server on PostgreSQL 17, Frontend (Jest, 70% statements), Fixtures | node:test, Jest | PR, push | fails job | via gate |
| Quality | Web export + browser/a11y (`:185-219`) | Playwright | only on `main` or PRs into main | fails job on main path; skipped on dev PRs | via gate (`:301-303`) |
| Quality | **gate** `Format, lint, typecheck, and test` (`:270-303`) | shell `test` on `needs.*.result` | PR, push | **fails unless every job succeeded** (docs-only: all skipped) | **Yes (dev and main, strict up-to-date)** |
| SAST | CodeQL `analyze` (`codeql.yml:36-60`) | CodeQL `security-extended`; js/ts, python, actions | PR, push main/dev, cron Mon 03:23 UTC | job fails only if analysis itself fails. Findings go to the Security tab; the "CodeQL" PR check is not required | **No** |
| Image scan | Release security `images` x2 (`release-security.yml:26-76`) | docker build, Trivy v0.70.0: SBOM, then vuln scan HIGH,CRITICAL `exit-code 1` | PR (path-filtered), tag `v*`, manual | fails job. **Not on push to dev/main.** Runtime image build is broken now (ffmpeg) | **No** |
| SBOM | same job, step "Generate CycloneDX image SBOM" | Trivy cyclonedx | same | generates only; artifact kept 30 days with image identity file | No |
| IaC | Release security `iac` (`:78-105`) | `trivy config .` then `scripts/check-iac-scan.py` | same | fails job on any unaccepted HIGH/CRITICAL or expired exception. 8 exceptions in `.github/iac-scan-exceptions.json`, **all expire 2026-10-31** | **No** |
| Supply chain | Dependabot (`.github/dependabot.yml`) | npm, github-actions, docker; monthly, grouped, target dev | schedule | report: PRs #569-571 open and unmerged. Security updates enabled | No |
| Deploy dev | "Wait for this commit's dev Quality checks" (`deploy-dev.yml:104-128`) | `gh api` poll of the `quality.yml` push run | push dev, manual | **blocks deploy** unless that run concluded `success` (25 min max) | n/a |
| Deploy dev | Build + verify bundle (`:130-141`) | `deploy/release.py build/verify` | same | fails job; image IDs and revision label verified | n/a |
| Deploy dev | OIDC to AWS (`:143-171`) | STS `assume-role-with-web-identity` | same | fails job | n/a |
| Deploy dev | Install + health + auto-restore (`:266-293`, `release-host.sh:262-271`) | health curl x2, restore prior release | same | fails job and restores prior release | n/a |
| Deploy dev | `environment: dev` (`:87`) | GitHub environment | same | **no reviewers, no branch policy** [V API] | n/a |
| Deploy release | `environment: release` (`deploy-release.yml:73`) | required reviewer + `main` only | push main, manual | **human approval gate** [V API] | n/a |
| Ops | Database operations | manual dispatch, branch check at `:49` | manual | environment-scoped | n/a |
| Not on dev | `terraform-environments.yml` | exists only on main (manual plan/apply) | manual | not part of the dev picture | n/a |
| Not on dev | `vigolium*.yml` | registered in Actions from the #438 branch only | none on dev | does not run on dev | n/a |

Other hygiene [V]: every `uses:` is SHA-pinned (though repo setting `sha_pinning_required` is false). No `pull_request_target`. Default token read-only. `persist-credentials: false` on checkouts. Repo has one Actions secret, `OPENAI_API_KEY`, left over from PR #438 and unused by any dev workflow.

## 2. Branch protection, rulesets, environments, alerts (live API, 26 Oct) [V]

| Item | dev | main |
|---|---|---|
| Required checks | `Format, lint, typecheck, and test` (strict, up-to-date) | same |
| Required reviews | **0** | **1**, last-push approval on |
| Enforce admins / force-push / deletion | on / blocked / blocked | same |
| Conversation resolution | required | required |
| Signed commits | not required | not required |
| Rulesets | none (`[]`) | none |

- PR #586 (dev to main promotion) currently shows `BLOCKED / REVIEW_REQUIRED`: a live demo of the main protection.
- Environments: `dev` (no rules), `release` (required reviewer `AndrewNguyenLKN`, prevent self-review, deployment branches = `main` only), `staging-demo` (stale, branch policy only). Env secrets: none.
- Alerts (counts): code scanning **0 open** (17 dismissed, 5 fixed); Dependabot **1 open** (medium, dev-scope `sprintf-js`, a *withdrawn* advisory); secret scanning **0 open**. Features on: secret scanning, push protection, Dependabot security updates.
- Say honestly: the 17 CodeQL dismissals include 2 high `js/xss-through-dom` (alerts #3, #45, `src/capture/platform.ts`) dismissed as false positives with a written rationale (blob-only guard, tested). The other 15 are in test files.

## 3. DevSecOps checklist

| Control | Status | Evidence |
|---|---|---|
| SAST | **Present, report-only** (not required) | CodeQL security-extended, 3 languages, 3 triggers |
| SCA / dependency audit | **Present, blocking** (via gate) | `npm audit` high+; plus Dependabot alerts/updates, Trivy image vulns. **Red now** |
| Secret scanning | **Present, partly blocking** | GitHub secret scanning + push protection (blocks at push), GitGuardian PR check (report). No gitleaks/CI scan, no pre-commit scan |
| Container image scan | **Present, job-blocking, not required** | Trivy HIGH/CRITICAL on runtime + web images; PR path-filter, tags, manual only |
| IaC scan | **Present, job-blocking, not required** | `trivy config .` plus exact-finding gate, expiring exceptions (expire 31 Oct); gate logic unit-tested inside Quality |
| DAST | **Missing** | none on dev/main. PR #438 draft only |
| SBOM | **Present, report-only** | CycloneDX per image, 30-day artifact; not published or attested |
| Signing / provenance | **Missing** (partial integrity only) | no cosign/attest; commits not required signed. Partial: revision label, `release.py verify` image-ID check, host sha256 check. **Scanned image is not the deployed image**: release-security builds its own, deploy rebuilds (`release.py:272`) |
| OIDC to AWS, least privilege | **Present** for CI | no AWS keys in repo secrets. Trust needs `aud`, `sub = environment:dev`, `ref = refs/heads/dev` (`infra/terraform/demo/deploy.tf:41-63`). Role: 3 Lightsail actions on one instance, `GetInstance`, `GetCallerIdentity` (+ S3 read of the env file, DB-ops policy in `media/`). Caveat: the **app host holds a static S3 IAM-user key** (`media/main.tf:135,201`), and the human Terraform-apply role is broad (exception AWS-0345) |
| Environment approval gates | **Release only** | release reviewer + main-only; dev deploys on merge by design (AGENTS.md) |
| Rollback | **Present, automatic + manual host command; no CI rollback** | `release-host.sh:262-271` restores prior release on failed health. `rollback` at `:286-296` needs SSH to the host. `deploy-release.yml:21-26` offers only install/prepare. Release host is down by choice, so Deploy release would stop at "Require a running host" |

## 4. DAST

**PR #438 "Add native and agentic Vigolium DAST trials" [V]**: draft by KaenBin, opened 5 Oct, last update 5 Oct, merge state **DIRTY** (conflicts), 32 files, +4079/-1. It adds `vigolium.yml` and `vigolium-agentic.yml`, which build a disposable Rewind backend in CI and run a niche scanner. The agentic variant sends synthetic HTTP traffic to OpenAI via `OPENAI_API_KEY` to generate probes. Coverage is only chat/groups SQLi and access scenarios. The PR says generation is nondeterministic and the proxy "is not a complete egress sandbox". The branch trial runs passed (5 Oct). **Not salvageable tonight**: conflicts, 4k lines, an external-AI data flow, and a live dependency on an OpenAI key. The one good idea to reuse is "scan a disposable backend inside CI".

**Cheapest credible DAST tonight: OWASP ZAP baseline vs hosted dev, after deploy, report-only first.**

Target `https://d2m6kz76y4kuvm.cloudfront.net` (README.md:16). One curl at 13:44 UTC: **HTTP 200**, 0.86 s, headers include `x-frame-options`, HSTS, enforced CSP `frame-ancestors 'none'`, the real CSP as report-only, `server: nginx/1.31.6` [V].

Put it in `deploy-dev.yml` as a job **after** `deploy`. A separate `workflow_run` workflow would not fire from dev, because `workflow_run`/`schedule` use the default branch (main) [I, GitHub behaviour].

```yaml
  dast:
    needs: deploy
    name: DAST (ZAP baseline on hosted dev)
    runs-on: ubuntu-24.04
    timeout-minutes: 15
    permissions:
      contents: read # job-level override: no id-token, no issues:write
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          ref: ${{ github.sha }}
          persist-credentials: false
      - name: ZAP baseline scan (passive plus spider, unauthenticated)
        uses: zaproxy/action-baseline@de8ad967d3548d44ef623df22cf95c3b0baf8b25 # v0.15.0
        with:
          target: https://d2m6kz76y4kuvm.cloudfront.net
          rules_file_name: .zap/rules.tsv
          cmd_options: '-j -m 2' # -j adds the AJAX spider (Expo web is a SPA); -m = spider minutes
          allow_issue_writing: false # default is true and needs issues:write
          fail_action: false # report-only. true = fail on ANY alert incl. WARN
          artifact_name: zap-baseline-${{ github.sha }}
```
The SHA is the commit behind tag v0.15.0, resolved through the GitHub API on 26 Oct [V]. Action inputs checked against its `action.yml` [V].

- **Runtime [I]**: image pull about 1 min, spider 2 min, report about 1 min; **about 4-6 min** total. It extends the `deploy-demo-dev` concurrency hold by the same time, because concurrency is per run.
- **Auth**: unauthenticated, so it only sees the SPA shell, static assets, `/api/health`, `/api/auth/config` and the legal pages. It is **not** an authenticated API scan like FlickPond's. Rewind has no OpenAPI file, so `action-api-scan` is out. An authenticated step is feasible later: `POST /api/auth/login` with `clientType: 'native'` returns a `token` (`auth-routes.ts:220-275`), and the action passes `ZAP_AUTH_HEADER_VALUE='Bearer <token>'`. That needs a dedicated dev user. Do not run an active scan against hosted dev (shared data, registration endpoint, rate limits).
- **Report-only vs fail**: `fail_action: true` fails on any alert, so it cannot be "High only". For a "fail on listed rules only" gate, call `zap-baseline.py -c .zap/rules.tsv -I` through `docker run ghcr.io/zaproxy/zaproxy:stable` (`-I` = do not fail on WARN, so only rules set to FAIL exit 1). Passive baseline rarely emits High, so the gate would be symbolic. Ship report-only and say so.
- **`.zap/rules.tsv`** (tab-separated; verify IDs on the first report [I]):
  ```
  10096	IGNORE	(Timestamp Disclosure in minified JS bundle)
  10109	IGNORE	(Modern Web Application, informational)
  ```
- **Likely noise [I, from the headers above]**: 10036 server version leak (nginx via CloudFront), 10063 Permissions-Policy not set, 90004 Spectre site-isolation headers (COOP/COEP/CORP), 10055 CSP "no fallback" because the enforced CSP is only `frame-ancestors` and the full policy is report-only (a true, presentable finding), plus a few informational JS items. Expect about 3-8 WARN-NEW, 0 FAIL, nothing that blocks.
- **Repo gotchas [V]**: `tests/scaffold.test.mjs:78-98` and `tests/quality-classification.test.mjs:101-110` parse `deploy-dev.yml`. Append the job *after* `deploy:` and run `npm run test:root` locally. `format:check` runs prettier on the YAML, so run `npx prettier --write` on it.
- **Better, not tonight**: build the web export + server in CI and scan localhost, so the PR's code is scanned before merge (shift-left). It needs `build:web` (about 2 min), server env wiring and a second job.
- **Do not run it against the live site from a laptop to "test" it**; I did not. First real run should be the pipeline run.

**IaC scan: already present, add nothing.** Optional: renew the 8 exceptions that expire 31 Oct (`.github/iac-scan-exceptions.json`), or after that date every PR matching the path filter fails with "expired exception" [V `scripts/check-iac-scan.py:37`].

**Secret scanning: native scanning and push protection exist; gitleaks is missing.** If a visible CI box is wanted, add a standalone `secret-scan.yml` (not inside `quality.yml`: the gate's `needs` list and its docs-only skip assertions are tested):

```yaml
jobs:
  gitleaks:
    runs-on: ubuntu-24.04
    timeout-minutes: 5
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          fetch-depth: 0
          persist-credentials: false
      - run: docker run --rm -v "$PWD:/repo" ghcr.io/gitleaks/gitleaks:v8.30.1 git /repo --redact --no-banner --exit-code 1 --config /repo/.gitleaks.toml
```
`.gitleaks.toml`: `[extend] useDefault = true` plus `[[allowlists]] targetRules = ["generic-api-key"] paths = ['''server/src/(schema|db)\.ts''', '''tests/.*''']`.
I ran gitleaks v8.30.1 locally against a clone of `f6cd896` [V]: **default rules give 27 findings** (history), all `generic-api-key` false positives (`key: '...'` in `schema.ts`/`db.ts`, `idempotencyKey` in tests). **With the allowlist: "no leaks found", 736 commits in 2.95 s, exit 0.** Without the config the job would be red from day one. This is job-blocking but not a required check unless added to protection.

## 5. Ranked list

**Add tonight (under 1 h each)**
1. **Fix the two rotted gates first** (prerequisite, 30-45 min with CI): bump or drop the ffmpeg pin (`deploy/Dockerfile:25`) and resolve the zod audit failure (a `package.json` override is a breaking-risk guess; test `npm run build:web`, or record a dated, explained exception). Without this, any live push, the DAST job and Deploy dev all fail.
2. **ZAP baseline job in `deploy-dev.yml`**, report-only, about 40 min: it answers "where is your DAST" with a box in the same run you demo.
3. **Redraw the pipeline picture with every real scan and its enforcement tag** (no code, 20 min): secret scanning/push protection, GitGuardian, npm audit, CodeQL, Trivy image + SBOM, Trivy IaC, ZAP. Tag each BLOCKS-MERGE / FAILS-JOB-NOT-REQUIRED / REPORT-ONLY.
4. **gitleaks standalone workflow + allowlist** (20 min, optional): verified clean locally; gives secrets a visible CI box.

**State honestly on a slide**
- Only the Quality gate blocks merges, and the audit is inside it. CodeQL, Trivy, IaC and GitGuardian are not required checks: "the workflow requires it" is not "branch protection enforces it".
- Release security runs on PRs (path-filtered), tags and manual runs, not on every push to dev.
- DAST: unauthenticated ZAP baseline, report-only; no authenticated API scan, no OpenAPI spec; Vigolium trial (PR #438) abandoned as a draft.
- No artifact signing or provenance; SBOM generated, not published; scanned image is rebuilt before deploy.
- Dev deploys have no approval gate by design; release has a human reviewer.
- Rollback is automatic on failed health plus a manual host command; there is no CI rollback button.
- CI uses OIDC, but the app host holds a static scoped S3 key. CodeQL is "0 open, 17 dismissed with rationale".
- State of the audit/ffmpeg rot, if shown live, and that IaC exceptions expire 31 Oct.

**Skip**
- Authenticated ZAP full/API scan: no OpenAPI, needs a seeded user, active attacks on shared dev data.
- Reviving PR #438: conflicts, 4k lines, OpenAI data flow, nondeterministic.
- checkov/tfsec: Trivy config already covers Terraform and Dockerfiles.
- cosign/attestations: images ship as tarballs, not through a registry, so it is more than an hour.
- Making CodeQL/Release security required: path filters would leave checks pending on docs PRs. It needs a gate redesign; do it after the talk.
- SonarCloud: needs an account and token.

## 6. Questions an assessor may ask, and the true answers
- "Does a failed Trivy scan stop a deploy?" No. Deploy dev waits only for Quality (`deploy-dev.yml:104-128`).
- "Does CodeQL block a merge?" No; it is not a required check.
- "Who approves production?" `AndrewNguyenLKN` via the release environment, and one PR review on main (self-review prevented).
- "Where are keys?" CI: none (OIDC). Host: one scoped S3 IAM-user key delivered via a private S3 object.

## 7. Evidence (run IDs; `gh run view <id> --repo Collaboration95/rewind-app`)
- Last green dev push, f6cd896: Quality #955 `39441043567` (3m23s), Deploy dev #119 `39441043830` (6m45s incl. Quality wait), CodeQL #744 `39441043794` (js/ts 116 s).
- Promotion PR #586 on f6cd896: Quality #956 `39443030843` (browser job ran, 211 s), Release security #461 `39443030856` (images 58-64 s, IaC 14 s; artifacts `release-security-{runtime,web,iac}-f4bd293d...` expire about 19 Nov).
- Failures: Quality #957 `40140117765`, #958 `40140169768` (audit); Release security #462 `40140169755` (ffmpeg).
- PR #438 DAST trial: draft, DIRTY. Trial runs `37277466740` and `37277472772`, 5 Oct.
- Not checked: live AWS IAM state (Terraform read only), and the ZAP YAML has not been executed anywhere.
