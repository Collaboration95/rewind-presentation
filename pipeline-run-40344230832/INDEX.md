# Presentation artifact index

Selected deployment: 40344230832, aea7478bce14131b821caaa99b1185077b4a9403; matching Quality 40344231052.

| Category | Retained file |
|---|---|
| SAST | `videos/cicd/evidence/codescan-alert-56.json` |
| SCA | `videos/cicd/evidence/artifacts/40343459119/quality-npm-audit/npm-audit.json` |
| Secrets | `videos/cicd/evidence/artifacts/40343459282/gitleaks-5860b188af0e988ab74a8bcdbf524891744d0620/gitleaks.sarif` |
| IaC | `pipeline-run-40344230832/iac/iac-full.json` |
| SBOM runtime | `pipeline-run-40344230832/security/sbom-runtime.cdx.json` |
| SBOM web | `pipeline-run-40344230832/security/sbom-web.cdx.json` |
| Trivy runtime | `pipeline-run-40344230832/security/trivy-runtime.json` |
| Trivy web | `pipeline-run-40344230832/security/trivy-web.json` |
| Provenance | `videos/cicd/evidence/attestation-verify.json` |
| Manifest | `pipeline-run-40344230832/security/release-manifest.json` |
| DAST | `pipeline-run-40344230832/zap/report_json.json` |
| Load test | `load-test/results/summary.json` |

IaC: same-commit Release security 40344231046; run identity in iac/source-run.json. Quality test/audit artifacts shown on film come from PR run 40343459119; Gitleaks comes from Secret scan 40343459282. The source/run distinctions are retained.

All four SBOM/Trivy file hashes match the selected deployment manifest. The filmed `gh attestation verify --repo Collaboration95/rewind-app release-manifest.json` succeeds; its retained text and structured JSON are under videos/cicd/evidence/.

The source video remains videos/cicd/cicd-demo.mp4. The stage video retains source intervals [0,630) and [654,710), totalling 686 seconds.
