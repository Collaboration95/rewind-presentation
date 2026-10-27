# Pipeline artifacts

## Presentation artifact set · 27 October 2026

The selected deployment is **40344230832 at aea7478**, with same-commit dev Quality **40344231052**. The recording also shows PR Quality **40343459119 at 38593b2**. All retained artifact categories and their paths are listed in [pipeline-run-40344230832/INDEX.md](pipeline-run-40344230832/INDEX.md).

The final set includes the real **iac-full.json** from same-commit Release security **40344231046**, alongside both CycloneDX SBOMs, both Trivy reports, the deployment manifest, ZAP JSON/HTML, CodeQL records, npm-audit JSON, Gitleaks SARIF and successful manifest-attestation verification. The filmed command is `gh attestation verify --repo Collaboration95/rewind-app release-manifest.json`.

The implementation and dated CI snapshots follow.

Prepared 26 October 2026 for the 27 October, 14:30 SGT presentation.
Implementation branch: `guru/devsecops-artifacts`. PR: [#595](https://github.com/Collaboration95/rewind-app/pull/595) into `dev`; coordinator owns the merge.
Head: `38593b225cf636062f2b1578ccfcc033f86fbd64`. Includes `origin/dev` at `47ea5f0` after #591.

Open **Collaboration95/rewind-app → Actions → the workflow → the run for the commit**.
The run's **Artifacts** section contains downloadable files. Select a job to show its summary and individual gate steps.
A PR run proves PR checks only. Exact-bundle scans, attestations and ZAP need a successful deployment after merge to `dev`.

| Artifact | Workflow / job | Format | What it proves | Where to click in GitHub |
| --- | --- | --- | --- | --- |
| `quality-test-results-root` | Quality checks / Root and IaC tests (`static`) | `test-results-root.xml`, JUnit XML | Root/Terraform Node tests, including passed, failed and skipped cases | Actions → Quality checks → run → Artifacts; select Root and IaC tests for summary |
| `server-coverage` | Quality checks / Server tests and coverage (`server`) | `test-results-server.xml`, `coverage-summary.json`, `server-summary.txt`, raw `server-v8/*.json` | Server tests plus measured line, branch and function coverage | Actions → Quality checks → run → Artifacts → server-coverage; job summary shows counts and line coverage |
| `frontend-coverage` | Quality checks / Frontend tests and coverage (`frontend`) | `frontend-results.json`, `coverage-summary.json` | Jest counts and measured statement coverage; existing 70% statement gate still applies | Actions → Quality checks → run → Artifacts → frontend-coverage; frontend job summary |
| `quality-npm-audit` | Quality checks / Production dependency audit (`audit`) | `npm-audit.json` | Production dependency findings; HIGH+ fails the required aggregate Quality gate | Actions → Quality checks → run → audit job summary and Artifacts |
| `dev-release-security-<commit>` | Deploy dev / Deploy dev to the hosted host (`deploy`) | `sbom-runtime.cdx.json`, `sbom-web.cdx.json`, CycloneDX JSON | Component inventories from the exact verified runtime/web image archives in the release bundle | Actions → Deploy dev → post-merge run → Artifacts; expand Scan the exact bundled images |
| Same artifact | Deploy dev / `deploy` | `trivy-runtime.json`, `trivy-web.json`, Trivy JSON | Vulnerability findings for those exact bundled images; HIGH/CRITICAL stops host upload, with reports retained | Same run → deploy job summary severity table; download JSON from Artifacts |
| Same artifact | Deploy dev / `deploy` | `release-manifest.json` | Commit, run/attempt/workflow, successful Quality run ID, timestamp, image IDs and digests, severity counts; SHA-256 of bundle, both SBOMs and both scan reports | Same run → Artifacts → dev-release-security-commit → release-manifest.json |
| `dev-release-bundle-<commit>` | Deploy dev / `deploy` | `rewind-release.tar`, Sigstore attestation JSON bundle | Retained deployable image pair and GitHub-signed build provenance for the tarball and security manifest | Same run → Artifacts; deploy job summary links attestations; verify downloaded tarball with `gh attestation verify --repo Collaboration95/rewind-app rewind-release.tar` |
| `zap-baseline-<commit>` | Deploy dev / DAST (ZAP baseline on hosted dev) (`dast`) | `report_json.json`, `report_html.html`, `report_md.md` | Passive baseline and spider findings on hosted dev after deployment; unauthenticated and report-only | Same run → DAST job → summary; Artifacts → zap-baseline-commit → HTML for the presentation, JSON for raw findings |
| `gitleaks-<commit>` | Secret scan / Gitleaks full-history scan (`gitleaks`) | `gitleaks.sarif`, redacted SARIF | Default-rule full-history secrets scan with path-AND-exact-value allowlists for five historical generic-api-key false positives | Actions → Secret scan → run → Artifacts; Security → Code scanning → Gitleaks results (upload skipped for fork PR tokens) |
| `release-security-runtime-<commit>`, `release-security-web-<commit>` | Release security / Scan runtime/web image (`images`) | `<image>-sbom.cdx.json`, `<image>-vulnerabilities.txt`, `<image>-image-identity.txt` | Separate candidate image scan and inventory; this is independent of the exact deployed-bundle scan | Actions → Release security → run → Artifacts and each image job |
| `release-security-iac-<commit>` | Release security / Scan IaC configuration (`iac`) | `iac-full.json`, Trivy JSON | Terraform/Docker findings checked against exact exceptions and expiry dates | Actions → Release security → run → IaC job, Gate exact findings; download artifact |
| CodeQL analyses | CodeQL / CodeQL (JavaScript/TypeScript, Python, Actions) (`analyze`) | Code scanning results | SAST results and analysis completion for each language; findings are separate from required Quality | Actions → CodeQL → run → language job; Security → Code scanning → CodeQL alerts/analyses |

`jest-junit` is not installed, so frontend uses native Jest JSON without a new dependency.
The manifest is an Actions artifact only; the host installer is unchanged.
Locally built images may have no registry digest. The manifest explicitly records image config IDs, SHA-256 archive digests, available OCI manifest digests and any reported repository digests.
Artifacts last 30 days except existing server/frontend coverage artifacts (14 days). Docs-only Quality runs keep their existing skips and do not manufacture test or audit results.
Only **Format, lint, typecheck, and test** is required by branch protection. Other scans can fail their jobs; the new exact-bundle Trivy gate additionally prevents dev host upload. ZAP findings remain report-only.

## Validation and blockers

- Prettier check on all changed YAML: PASS.
- Actionlint on all four changed workflows: PASS (installed binary).
- `npm run test:root`, with JUnit enabled: PASS — 123 passed, 1 skipped, 0 failed; valid XML retained locally.
- Python security tests: PASS — 13 tests, including HIGH/CRITICAL, wrong-image, missing OS, language-only scan, empty inventory and scanner-error rejection.
- Gitleaks v8.30.1 Docker scan on full local history: PASS — 742 commits, no leaks, exit 0.
- `npm run test:fast`: PASS — root 123, server 985 and frontend 1,674 passed; 1 root and 21 server skips.
- Lint, architecture and typecheck: PASS; two pre-existing duplicate-import warnings in native-build tests.
- Cloud-free deployment fixtures: PASS.
- `npm audit --omit=dev --audit-level=high --json`: PASS — zero findings at every severity.
- Docker Trivy v0.70.0: JSON report and CycloneDX generation on an existing saved local image passed; ImageID and Alpine package inventory validated. This was a compatibility smoke check, not a scan of the current release.
- One GPT-6.1 Sol review pass completed. Fixed both findings: reject incomplete OS scans and narrow secret exceptions to exact benign values. Negative fixtures cover these boundaries.
- Post-merge dev deployment, signed provenance and hosted ZAP: pending coordinator merge; not claimed from local or PR checks.
- IaC exception decisions still expire on 31 October 2026; this batch does not renew them.
- Diagnosis limit: at most two attempts per problem. One reporter smoke command initially used a nonexistent test filename; the corrected existing Cognito test passed (17 cases) with valid JUnit and measured coverage JSON. No implementation blocker from that check.

- Gitleaks negative fixture: PASS — new random nonfunctional keys are detected in schema.ts, db.ts and the historical test path; exact historical exceptions remain clean.
- Reliability note: one later fast run returned 503 instead of 200 in `upload-intents-protocol.test.mjs:297`; the focused file passed all 3 tests, then the full fast rerun passed. No assertion or server code changed.
- Review findings are resolved; no known local implementation blocker remains. PR checks and post-merge deployment evidence are recorded separately below.

## PR CI snapshot at handoff

PR [#595](https://github.com/Collaboration95/rewind-app/pull/595), head `38593b225cf636062f2b1578ccfcc033f86fbd64`, targets `dev` and is mergeable. Read at 26 October, approximately 22:51 SGT.

- **Passed:** GitGuardian Security Checks; Quality Classify change scope; CodeQL Classify change scope.
- **Pending/running:** aggregate Quality and its test/static jobs; CodeQL language analyses; Release security image/IaC scans; Gitleaks full-history scan.
- **Expected skip:** Web export and browser checks on this dev PR.
- [Quality run 40343459119](https://github.com/Collaboration95/rewind-app/actions/runs/40343459119).
- [CodeQL run 40343459158](https://github.com/Collaboration95/rewind-app/actions/runs/40343459158).
- [Release security run 40343459113](https://github.com/Collaboration95/rewind-app/actions/runs/40343459113).
- [Secret scan run 40343459282](https://github.com/Collaboration95/rewind-app/actions/runs/40343459282).

This implementation subagent hands pending checks to the coordinator without polling them. The coordinator merges the single PR after required checks succeed, then records the Deploy dev run and opens its SBOMs, JSON reports, manifest, provenance and ZAP artifacts. No post-merge deployment or hosted scan success is claimed here.
