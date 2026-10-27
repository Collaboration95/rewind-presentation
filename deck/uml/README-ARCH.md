# UML-ARCH figures

Verified against `origin/dev` **2390589dbf1d731fba9810ac410f5b31ac1c23c4**, checked out in a fresh detached `rewind-present-uml-arch` worktree. The remote `dev` ref was checked with authenticated `gh api`; no branch switch, push, merge, workflow dispatch or AWS operation was performed. Code citations below are relative to that checkout; preparation sources are relative to `presentation-prep/`.

- **pattern-storage** — Media jobs depend on `MediaStore`; concrete stores implement the Strategy, and the `privateTransport(sdk)` returned object adapts AWS SDK commands: `server/src/media/store.ts:29–35`, `server/src/media/local-store.ts:18`, `server/src/media/s3-store.ts:30–58`, `server/src/media/runtime-store.ts:143–167,347–389`, `server/src/jobs/stored-output.ts:17–49`, `server/src/config.ts:338–347`; cross-checked `audit/B2-design.md` §2 and reused `uml-drafts/d1-storage.puml`.
- **pattern-observer** — `RealtimeHub` delivers committed group events to SSE callback observers, while message replay uses database events: `server/src/realtime/index.ts:3–42`, `server/src/routes/chat-routes.ts:223–250,312,394,463`, `server/src/http.ts:179`, `server/src/chat/index.ts:221,347,498`; cross-checked `audit/B2-design.md` §2 and reused `uml-drafts/d4-observer.puml`.
- **pattern-persistence** — `PostgresDatabase` and `PostgresStatement` preserve the synchronous SQLite-shaped surface through SQL translation and a worker-thread `pg.Client`: `server/src/db.ts:48–84`, `server/src/postgres/database.ts:106–139,178–201,235–255`, `server/src/postgres/translate.ts:257`, `server/src/postgres/sync-worker.ts:95,355`; cross-checked `audit/B2-design.md` §2 and reused `uml-drafts/d2-persistence.puml`.
- **er-core** — Real-account memberships connect to real profiles and group metadata, profile triggers supply media actors, and compilation inputs identify film/clip job dependencies: `server/migrations/postgres/030-baseline.sql:56–61,83–159,279–304,493,543–580`, `server/migrations/postgres/031-cognito-accounts.sql:1–7`, `server/src/groups/real.ts:62–109`; cross-checked `audit/B2-design.md` §5 and reused the field/type conventions in `uml-drafts/e1-er.puml`.
- **deploy-dev** — Hosted dev uses CloudFront, nginx and Node on a Lightsail host, managed Lightsail PostgreSQL, S3, Cognito and browser push; Actions uses an environment/branch-scoped OIDC role and temporary SSH: `infra/terraform/demo/lightsail.tf:29–75`, `infra/terraform/demo/web-distribution.tf:1–70`, `infra/terraform/demo/deploy.tf:12–70`, `infra/terraform/media/database.tf:17–27,49–94`, `infra/terraform/media/main.tf:21–123,136–204,216–249`, `infra/terraform/media/cognito.tf:14–76`, `deploy/compose.yaml:1–125`, `deploy/nginx.conf:1–55`, `server/src/cli.ts:598–690`, `server/src/reminders/providers.ts:260–285`, `.github/workflows/deploy-dev.yml:186–240,289–335`; cross-checked `audit/B2-design.md` §4 and reused `uml-drafts/p1-deploy.puml`.
- **pipeline** — Aggregate Quality blocks merge, same-commit Quality and exact-bundle Trivy block deployment, host health gates activation, and independent security/ZAP/performance checks report: `.github/workflows/quality.yml:74–102,104–223,225–308,310–343`, `.github/workflows/codeql.yml:3–11,36–60`, `.github/workflows/release-security.yml:3–106`, `.github/workflows/secret-scan.yml:3–56`, `.github/workflows/deploy-dev.yml:28–35,104–184,269–335,351–402`, `.github/workflows/performance.yml:3–56`, `deploy/scan-release.py:13–35,51–111`, `deploy/release-host.sh:210–241,269–272`; checked against `PIPELINE-ARTIFACTS.md`, `audit/C-devsecops.md` §1–2, `audit/D-cicd-demo.md` §4, the supplied run manifest, and fresh `gh api` branch-protection/security settings; used FlickPond `W5-pipeline-main.puml` as the activity-partition reference.
- **artifact-flow** — Git preserves source and lockfiles; Actions retains test/audit/security evidence and the signed deployable tar; Security holds code-scanning results and Lightsail retains installed releases: `.github/workflows/quality.yml:95–102,143–150,178–189,214–223`, `.github/workflows/release-security.yml:46–77,99–106`, `.github/workflows/secret-scan.yml:33–47`, `.github/workflows/deploy-dev.yml:134–184,370–402`, `.github/workflows/performance.yml:35–56`, `deploy/release.py:22,236–289,300–334`, `deploy/scan-release.py:64–97`, `deploy/release-host.sh:13–27,224–241`, `PIPELINE-ARTIFACTS.md`, `pipeline-run-40344230832/security/release-manifest.json:1–70`; branch requirements checked through `gh api repos/Collaboration95/rewind-app/branches/{dev,main}/protection`.

## Notes for the presenter

Pattern problem/candidate/choice notes are comments in each pattern's `.puml` source. Storage compares repeated backend branches with an injected store/transport seam; persistence compares async rewrites with a synchronous adapter; chat compares polling with committed-event fan-out. The diagrams use real function/type names and explicitly label callback/object-literal roles. Local disk mode sets `config.media = null`; it is not a third `MediaStore` implementation. `PostgresDatabase` is structurally cast, not declared to inherit `DatabaseSync`.

The ER selects nine tables and selected columns. It follows the real-account membership path (`real_group_memberships`), rather than the retained baseline `memberships` table. `FK*` denotes its actual composite `(account_id, profile_id)` constraint. `profiles` is the media actor table and mirrors `real_profiles` by trigger. Annotated FK fields show some targets without an extra connector. `current_cycle_id` is not a database FK. There is no Archive table.

The pipeline uses UML activity partitions as responsibility swimlanes. The fork sends tokens into required Quality and independent reporting workflows; reporting results do not join the merge gate. `REPORTS` describes enforcement against merge/deploy, not whether a scan can turn its own job red. Candidate Trivy and IaC scans and Gitleaks can fail their jobs. Exact-bundle Trivy rejects HIGH/CRITICAL and invalid/incomplete image scans before upload. Attestation or bundle-retention failure also prevents subsequent upload through ordinary step failure. Push protection acts before the PR, separately from the three merge/deploy/report legend categories. Native secret scanning, push protection and Dependabot security updates were enabled in the repository settings read through `gh`.

Fresh workflow source supersedes the older C/D audit snapshots: Gitleaks, exact-bundle SBOM/Trivy/manifest/provenance and hosted ZAP now exist; Release security also runs on dev/main pushes. Only `Format, lint, typecheck, and test` is required on dev/main, with up-to-date checks; main additionally requires one approval and its Quality path includes browser checks. The main branch is shown only for source/promotion management; all deployment paths in these figures terminate at hosted dev.

The runtime communication paths in `deploy-dev` are numbered so protocol descriptions remain legible instead of overlapping connectors. Solid arrows show calls/transfer; dashed arrows show deployment transfer or push delivery. The map includes CloudFront's HTTP origin hop and does not imply HTTPS between CloudFront and nginx. Both images deploy on one host; Node owns the scheduler, media worker and reminder loops.

## Demo artifact verification

The supplied manifest identifies Deploy dev run **40344230832**, commit **aea7478bce14131b821caaa99b1185077b4a9403**, Quality run **40344231052** and `security_gate: pass`. The supplied `sbom-runtime.cdx.json`, `sbom-web.cdx.json`, `trivy-runtime.json` and `trivy-web.json` each match the manifest's SHA-256. Both image reports record zero HIGH and CRITICAL findings. These are the selected demo run's files; the diagram code verification pin is separately recorded above.

`release-manifest.json` is the security/provenance manifest retained by Actions. The tar's internal `manifest.json` is the release builder/installer manifest; they are different files. The release tar and Sigstore bundle are retained by the workflow, while the supplied local demo folder contains the security JSONs and ZAP reports. No checksum verification of an absent local tar or local Sigstore bundle is claimed.

## Rendering and slide placement

All seven `.puml` files include the shared `_style.iuml` supplied by UML-SAD. This agent left that shared file unchanged and used only local overrides. Every requested figure has `.puml`, `.svg` and `.png`; every PNG was opened and inspected, with dense layouts revised. Titles follow `<View> · <subject>` without dated/status disclaimers. Diagram generation requires no application/test-suite changes.

Use full-width figure slides. The following minima are computed from every SVG text element when fitted proportionally into a **1280×720 figure viewport**, including the figure title and legend. A 65%-width figure card will need a dedicated larger view to preserve 14 px text, particularly for the ER and pipeline.

| Figure | Native SVG / PNG size | Minimum fitted text |
| --- | --- | ---: |
| `pattern-storage` | 1398 × 821 | 15.79 px |
| `pattern-observer` | 1588 × 712 | 15.31 px |
| `pattern-persistence` | 1555 × 892 | 15.34 px |
| `er-core` | 1809 × 979 | 14.15 px |
| `deploy-dev` | 1322 × 911 | 15.02 px |
| `pipeline` | 1821 × 1013 | 15.46 px |
| `artifact-flow` | 1437 × 820 | 16.68 px |

Render formats separately from `presentation-prep/`:

```sh
java -Djava.awt.headless=true -jar plantuml.jar -tsvg deck/uml/{pattern-storage,pattern-observer,pattern-persistence,er-core,deploy-dev,pipeline,artifact-flow}.puml
java -Djava.awt.headless=true -jar plantuml.jar -tpng deck/uml/{pattern-storage,pattern-observer,pattern-persistence,er-core,deploy-dev,pipeline,artifact-flow}.puml
```
