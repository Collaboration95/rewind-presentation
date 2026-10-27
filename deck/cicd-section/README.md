# CI/CD section (Section 4) · staging

Integrated 27 Oct ~11:00 via `deck/cicd_slides.py` (called from `build_deck.py`); physical pages 24–41 plus backups CB1–CB3 (87–89). `slides.html` remains the standalone staging fragment.

## Files

- `slides.html`: fragment with one `<style id="cicd-section-style">` block (all classes prefixed `cx-`) and 21 `<section>` slides in the deck's markup (kicker, h1, body, foot, `aside.notes` with `.spoken`). Ids are `C1`–`C18` (main) and `CB1`–`CB3` (backup).
- `build_slides.py`: regenerates `slides.html` (`python3 build_slides.py`). Edit text there rather than in the HTML.
- `cicd-*.puml/.svg/.png`: eight figures. `_cicd.iuml` includes `../uml/_style.iuml` and adds the enforcement-tag stereotypes. White background, so they sit on the light green slide. Render each from this folder with `-tsvg`, then a separate `-tpng` pass.
- `shots/`: `crop-*.png` are tight crops of `../shots/github/*.png` so text displays near 1:1. `15-deploy-steps.png` and `20-deploy-artifacts.png` are live public-page captures from `videos/cicd/frames`. Replica frames were not used.

## Paths in the fragment

Image paths are relative to `deck/`: `cicd-section/<figure>.svg`, `cicd-section/shots/…`, `assets/pipeline-poster.jpg` and `clips/ci-cd-40344230832.mp4`. The ZAP links point to `../pipeline-run-40344230832/zap/report_html.html#10055` and `#10038`, the same relative pattern as B12. If the deck inlines images as data URIs, inline these the same way. Every screenshot figure has the class `diagram`, so Z or a double-click zooms it.

## Order and timing (main path: 11:10)

| # | id | Slide | Kind | s |
|---|---|---|---|---:|
| 1 | C1 | Overview figure: one change passes four gates | figure | 55 |
| 2 | C2 | Legend: tags, shapes, frames, arrows | legend | 30 |
| 3 | C3 | Source and artifact management figure | figure | 50 |
| 4 | C4 | PR stage: Quality workflow figure | figure | 45 |
| 5 | C5 | PR stage: security workflows figure | figure | 35 |
| 6 | C6 | Deploy 1/2: build, exact-bundle scan, SBOM, manifest, attest | figure | 45 |
| 7 | C7 | Deploy 2/2: OIDC, upload, checksum, health, restore | figure | 35 |
| 8 | C8 | DAST stage figure | figure | 30 |
| 9 | C9 | Catalogue: nine checks with tool, trigger, failure effect, result, link | table | 40 |
| 10 | C10 | SAST: CodeQL, alerts 54–56 triage, alert-56 JSON | check | 35 |
| 11 | C11 | SCA: zod GHSA-mrhx-c7xc-m3w5 failure log, PR #591 fix, npm-audit.json | check | 40 |
| 12 | C12 | Secrets: push protection, GitGuardian, Gitleaks and allowlist | check | 30 |
| 13 | C13 | Containers + IaC: Trivy results, 15 IaC findings, exception JSON | check | 35 |
| 14 | C14 | SBOM + provenance: CycloneDX, manifest, `gh attestation verify` | check | 40 |
| 15 | C15 | DAST results: 0/4/7/6, CSP example with URL and evidence | check | 40 |
| 16 | C16 | Tests + coverage gates | check | 20 |
| 17 | C17 | Technical findings (six) | findings | 45 |
| 18 | C18 | Demo route: eight links in click order, with film timestamps | demo | 20 |
| | | **Total** | | **670 = 11:10** |

The live clicks happen on C10–C15 (each has its links) and on C18. Allow about 15 s per page; that fits inside the slide times. To trim to 10:00, move C16 and C12 to backup (−50 s) and shorten C3 (−20 s).

Backup slides: CB1 is the recorded film (11:26, timestamps in its notes). CB2 shows dev and main branch protection from the live branch-protection API. CB3 shows the deploy job steps and artifacts screenshots.

## Replaces in deck.html

| Existing | Action |
|---|---|
| `s18` (main, 12:00 film slide) | Replace with C1–C18. The film moves to backup CB1 |
| `B27` (pipeline activity figure) | Superseded by C1 + C4–C8. Keep as backup or drop |
| `B26` (artifact-flow figure) | Superseded by C3. Keep as backup or drop |
| `B28` (security table) | Superseded by C9–C15. Drop |
| `B29` (manifest excerpt) | Superseded by C14. Drop |
| `B12` (artifact table) | Superseded by C3 + C9. Keep as backup if wanted |
| `B31` (findings) | Keep as backup: product/runtime findings. C17 is the pipeline set; C17's notes point to B31 |
| `B5` (deployment view) | Keep as is |

Renumber `data-num` / `data-main` on integration. The fragment numbers C1 = 12 onward, as if `s18` were removed. Check the "If asked" pointers: they cite C/CB ids and B31/B12.

## Figure legibility (fitted into 1280 × 688)

| Figure | Native | Min text |
|---|---|---:|
| `cicd-0-legend.svg` | 1279 × 537 | 20.0 px (≈15.6 px in the C2 card) |
| `cicd-1-overview.svg` | 1690 × 853 | 15.1 px |
| `cicd-2-pr-quality.svg` | 1662 × 859 | 15.4 px |
| `cicd-3-pr-security.svg` | 1300 × 599 | 17.7 px |
| `cicd-4-deploy-build.svg` | 1329 × 770 | 17.9 px |
| `cicd-5-deploy-ship.svg` | 1370 × 769 | 17.9 px |
| `cicd-6-dast.svg` | 1662 × 637 | 15.4 px |
| `cicd-7-source-artifacts.svg` | 1401 × 575 | 18.3 px |

All 21 slides were rendered at 1280 × 720 with the current deck CSS (restyled green background). No body overflow, and no text node is below 14 px.

## Screenshot slots

| Slot | Used on | Source |
|---|---|---|
| CodeQL run, three languages | C10 | `shots/github/codeql-run.png` (cropped) |
| Secret scan run + SARIF artifact | C12 | `shots/github/secret-scan-run.png` (cropped) |
| Release security run (images + IaC) | C13 | `shots/github/release-security-run.png` (cropped) |
| Attestation 59963857 | C14 | `shots/github/attestations.png` (cropped) |
| ZAP summary + CSP detail | C15 | `shots/github/zap-summary.png`, `zap-csp-detail.png` (cropped) |
| Quality artifacts | C16 | `shots/github/quality-graph-artifacts.png` (cropped) |
| Deploy job steps, deploy artifacts | CB3 | `videos/cicd/frames/15-deploy-steps.png`, `20-deploy-artifacts.png` (live captures) |
| Unused but available | — | `actions-workflows.png`, `deploy-graph.png`, `quality-graph.png`, `pr-checks.png` |

**Missing (no real capture exists):**

- Branch protection rules for dev and main. CB2 shows the same values as a table from the API.
- Code-scanning alert list and alert 56 detail. C10 shows the alert JSON and links to the alert.
- Deploy and Quality job summaries (Trivy gate table, coverage table). C13 and C16 give the values; the video frames for these are replicas.
- Environments settings page and the PR #586 approval.

Any of these can drop into the left card of its slide: `shot('<path>', '<caption>', '<alt>')` in `build_slides.py`.

## Facts used (all read on 27 Oct)

- **Workflows:** from `origin/dev` 2390589 (worktree `/tmp/rewind-cicd`): quality, codeql, secret-scan, release-security, deploy-dev, `.zap/rules.tsv`, `.gitleaks.toml`, `.github/iac-scan-exceptions.json`, `deploy/scan-release.py`, `jest.config.cjs`.
- **Runs, jobs and artifact IDs** (read-only `gh`): Deploy dev 40344230832, dev Quality 40344231052, PR Quality 40343459119, Release security 40344231046, Secret scan 40344231125, CodeQL 40344231062, failed audit 40140117765, failed image build 40140169755.
- **Code-scanning alerts 54–56** (dismissed "used in tests", 26 Oct 15:26 UTC): 0 open, 17 dismissed and 5 fixed overall.
- **Branch protection** for dev and main, and the repository's security settings.
- **Advisory GHSA-mrhx-c7xc-m3w5:** zod < 4.6.6, high.
- **Retention:** coverage 14 days; ZAP artifact 90 days (expires 24 Jan 2027); everything else 30 days.
