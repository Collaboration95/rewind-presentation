# CI/CD demonstration shotlist

Total: 11:50 · 1920×1080 · 30 fps

| Shot | Time | Length | Frame / page | Narration line |
| --- | --- | --- | --- | --- |
| 01 · Pipeline decisions | 00:00–00:20 | 20 s | `frames/00-pipeline.png` | Follow one change through six decisions: the pull request, parallel verification, security findings, the verified bundle, hosted dev and promotion. I will connect each decision to the check or artifact that records its result. |
| 02 · PR #595 checks | 00:20–00:40 | 20 s | `frames/02-pr595-checks.png` | Pull request 595 contains the pipeline artifact changes. Its checks list shows static analysis, tests and the dependency audit feeding the aggregate Quality gate. The individual results remain visible alongside the required merge check. |
| 03 · PR #595 security checks | 00:40–00:56 | 16 s | `frames/02b-pr595-checks-security.png` | The same pull request also records CodeQL, image and IaC scans, and secret scanning. These results are visible for security review alongside Quality. |
| 04 · Protected dev | 00:56–01:20 | 24 s | `frames/03-protect-dev.png` | The dev branch requires a pull request, an up-to-date branch and the check named Format, lint, typecheck, and test. Conversation resolution and administrator enforcement are enabled. The required approving-review count is zero, which allows routine dev changes to proceed after the automated gate. |
| 05 · Protected main | 01:20–01:44 | 24 s | `frames/25-protect-main.png` | Main keeps the same required Quality context and adds one approving review, including approval of the last push. This is the promotion boundary: a change that has reached dev still passes through the main review rule. |
| 06 · Quality run graph | 01:44–02:12 | 28 s | `frames/04-quality-graph.png` | The Quality graph starts with change classification and fans out into parallel jobs. Tests, coverage, static checks and the production dependency audit feed the aggregate gate. Main-bound changes also run the web export and browser checks. |
| 07 · Quality artifacts | 02:12–02:32 | 20 s | `frames/06-quality-artifacts.png` | The run retains four artifact groups: root JUnit results, server coverage, frontend coverage and npm-audit JSON. They remain attached to the run and its commit, so a reviewer can inspect the machine-readable results behind the green check. |
| 08 · JUnit results | 02:32–02:52 | 20 s | `frames/05-quality-summaries.png` | The JUnit report records individual test cases and their outcomes. The job summary presents the totals, while the XML keeps the detail for inspection. This links the test result to the exact Quality run rather than relying on a copied test count. |
| 09 · Coverage summaries | 02:52–03:22 | 30 s | `frames/05b-quality-coverage-summaries.png` | These are the coverage reports retained by the same run. Frontend statement coverage is 89.64 percent, and server line coverage is 85.50 percent. The reports preserve the underlying counts and coverage dimensions alongside the test results. |
| 10 · Production dependency audit | 03:22–03:46 | 24 s | `frames/08-term-npm-audit.png` | The production dependency audit reports zero findings at every severity in this run. The command audits production dependencies and fails on High or Critical findings. Because this job feeds the required Quality gate, a failed audit prevents the normal merge path. |
| 11 · CodeQL security results | 03:46–04:08 | 22 s | `frames/09-codescan-alerts.png` | CodeQL publishes its analysis results to the Security area. The alert list records the rule, affected code and disposition. The captured dev results have no open alerts; closed alerts retain their review reasons so the decisions can be inspected. |
| 12 · PR #592 alert triage | 04:08–04:38 | 30 s | `frames/10-codescan-alert-56.png` | The load-test harness in pull request 592 raised CodeQL findings. Alert 56 concerns writing a report to an operator-selected path. Its recorded disposition is used in tests, with an explanation that this harness is operator-run and never shipped in the application image. |
| 13 · Gitleaks full-history scan | 04:38–05:02 | 24 s | `frames/13-gitleaks-summary.png` | The secret-scan workflow runs Gitleaks over the repository history and retains a redacted SARIF artifact. The run records the scan result. Historical exceptions are constrained to exact benign values and paths, so a new value in the same file still receives normal scanning. |
| 14 · Deploy dev run 40344230832 | 05:02–05:18 | 16 s | `frames/14-deploy-graph.png` | Deploy dev 40344230832 records the artifact-rich deployment. The graph orders change classification, the deploy job and the ZAP baseline against hosted dev. |
| 15 · Deploy job steps | 05:18–05:32 | 14 s | `frames/15-deploy-steps.png` | The steps wait for Quality on the same commit, build and scan the exact bundle, attest the artifacts, obtain temporary OIDC credentials and install the release. |
| 16 · Exact-bundle Trivy gate | 05:32–06:04 | 32 s | `frames/17-deploy-summaries.png` | This step scans the runtime and web images inside the bundle that will be uploaded. Both images have zero High and Critical findings in the manifest. The runtime image also records one Medium finding and two Unknown findings. The High and Critical gate runs before host upload. |
| 17 · CycloneDX SBOM | 06:04–06:28 | 24 s | `frames/18-term-trivy-sbom.png` | The CycloneDX files inventory components from the exact bundled runtime and web images. The SBOM and vulnerability reports describe the same image pair. Their hashes are recorded in the release manifest, connecting component inventory, scan results and the bundle identity. |
| 18 · Release manifest | 06:28–06:46 | 18 s | `frames/19-term-manifest.png` | The manifest records the commit, workflow run, successful Quality run, scanner and security-gate result. Its image entries and hashes connect the source verification to the retained deployment artifacts. |
| 19 · Retained deployment artifacts | 06:46–06:58 | 12 s | `frames/20-deploy-artifacts.png` | The run retains the deployable bundle, the security reports and manifest, and the ZAP reports as three downloadable artifact groups. |
| 20 · Manifest digests | 06:58–07:18 | 20 s | `frames/70-manifest-digests.png` | The SHA-256 entries bind the release tarball, both component inventories and both vulnerability reports. The second command computes the digest of the downloaded manifest itself. That exact digest is the subject checked by the attestation verification command. |
| 21 · GitHub build attestation | 07:18–07:42 | 24 s | `frames/21-attestation.png` | The deployment creates GitHub build attestations for the release bundle and security manifest. The provenance identifies the repository and deployment workflow that produced the subject. The next terminal command checks that signed provenance against the downloaded manifest bytes. |
| 22 · Verify the attestation | 07:42–08:12 | 30 s | `frames/22-term-attest-verify.png` | Here is the real gh attestation verify output for release-manifest.json. Verification succeeds against the repository policy, the SLSA provenance predicate and the GitHub Actions OIDC issuer. The matched signer workflow is deploy-dev.yml on the dev branch, and the command exits with status zero. |
| 23 · DAST job summary | 08:12–08:40 | 28 s | `frames/17-deploy-summaries.png` | After deployment, the ZAP baseline runs against hosted dev. Its summary records zero High, four Medium, seven Low and six Informational findings. The report is retained with the deploy run, and the baseline reports its findings without making them a deployment gate. |
| 24 · ZAP HTML report | 08:40–09:04 | 24 s | `frames/23-zap-report.png` | The retained HTML report makes the dynamic findings inspectable. Each entry names the rule, risk and affected requests. The Medium findings concern Content Security Policy. This connects the summary counts to concrete observations on the running hosted application. |
| 25 · Performance summary | 09:04–09:38 | 34 s | `frames/80-performance.png` | The full profile ran after deployment, with 1, 10, 25, 50 and 100 virtual users. At 100 VUs, the measured p95 is 1336 milliseconds and throughput is 17.84 requests per second, with 0 errors across 3212 requests. The retained summary records each steady stage. |
| 26 · Performance chart | 09:38–10:06 | 28 s | `frames/81-performance-chart.png` | The chart plots the clean run across the five load stages. The measured observations feed the response-time and throughput figures. The capacity table keeps the measured baseline alongside projected values for 250, 500 and 1,000 users. |
| 27 · Hosted dev health | 10:06–10:30 | 24 s | `frames/24-term-health.png` | The hosted dev health endpoint returns HTTP 200. The JSON reports PostgreSQL and a ready schema at migration 31. Deployment identity comes from the workflow and manifest; this endpoint provides a direct check that the hosted application and database are responding. |
| 28 · Environment controls | 10:30–10:54 | 24 s | `frames/28-environments.png` | The environment settings record which deployment paths run automatically and which require a reviewer. Dev has no environment approval gate. The promotion environment records its reviewer and branch policy. These controls are separate from the source-branch review rule. |
| 29 · Promotion PR #586 | 10:54–11:30 | 36 s | `frames/27-promotion-approval.png` | Pull request 586 carries dev into main. The captured pull request already has an approving review, and the main protection rule requires that review. Its checks and merge state remain visible separately. I am showing the promotion controls and leaving the pull request unchanged. |
| 30 · Decisions and retained artifacts | 11:30–11:50 | 20 s | `frames/99-decisions.png` | The chain is now visible: protected source changes, retained test and audit results, reviewed security findings, an exact-bundle scan, a signed manifest, hosted health, dynamic findings and a load-test result. Each artifact stays connected to the commit and run that produced it. |

## Source records

- BRIEF-SHARED.md; audit/D-cicd-demo.md §5
- https://github.com/Collaboration95/rewind-app/pull/595/checks
- https://github.com/Collaboration95/rewind-app/settings/branches
- https://github.com/Collaboration95/rewind-app/actions/runs/40343459119
- local command output
- https://github.com/Collaboration95/rewind-app/security/code-scanning?query=is%3Aclosed+branch%3Adev
- https://github.com/Collaboration95/rewind-app/security/code-scanning/56
- https://github.com/Collaboration95/rewind-app/actions/runs/40343459282
- https://github.com/Collaboration95/rewind-app/actions/runs/40344230832
- https://github.com/Collaboration95/rewind-app/actions/runs/40344230832/job/121646847180
- https://github.com/Collaboration95/rewind-app/attestations/59963857
- https://github.com/Collaboration95/rewind-app/actions/runs/40344230832/artifacts/12660614474
- ../../load-test/results/hosted.json
- https://github.com/Collaboration95/rewind-app/settings/environments
- https://github.com/Collaboration95/rewind-app/pull/586

## Production

Captured with Chromium at 1920×1080 and deviceScaleFactor 2. Gentle zoom and pan, highlighted cursor and section titles are composed from PNG overlays. The final edit is assembled with `presentation-prep/video-toolkit/render.py`. Narration cues are supplied above for the presenter.
