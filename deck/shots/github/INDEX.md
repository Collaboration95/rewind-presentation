# Rewind CI/CD screenshots

Captured 27 October 2026 using a 1600 × 1000 light-theme Chrome viewport. GitHub captures are public, signed-out views of the actual pages; the ZAP captures are from the saved run report. They show the historical run, not a fresh scan or a statement about current deployment state.

| File | Exact URL | What it shows | Suggested slide use |
| --- | --- | --- | --- |
| actions-workflows.png | https://github.com/Collaboration95/rewind-app/actions | Workflow list and recent runs; the Performance workflow is not visible in this capture. | Pipeline overview |
| deploy-graph.png | https://github.com/Collaboration95/rewind-app/actions/runs/40344230832 | Successful classify → deploy → DAST graph and three retained artifacts. | Dev deployment and dynamic security testing |
| quality-graph.png | https://github.com/Collaboration95/rewind-app/actions/runs/40344231052 | Quality workflow graph, job statuses and duration. | CI quality gates |
| quality-graph-artifacts.png | https://github.com/Collaboration95/rewind-app/actions/runs/40344231052 | Quality job list, two lint annotations, coverage, test and audit artifacts. | Quality evidence retained |
| pr-checks.png | https://github.com/Collaboration95/rewind-app/pull/595/checks | Merged PR checks sidebar and successful GitGuardian result. | PR checks and secret detection |
| codeql-run.png | https://github.com/Collaboration95/rewind-app/actions/runs/40344231062 | Successful CodeQL run with three language analyses in the job list. | Static security analysis |
| secret-scan-run.png | https://github.com/Collaboration95/rewind-app/actions/runs/40344231125 | Successful Gitleaks full-history job and artifact. | Secret scanning |
| release-security-run.png | https://github.com/Collaboration95/rewind-app/actions/runs/40344231046 | Successful image and IaC scan jobs with three artifacts. | Release security scans |
| attestations.png | https://github.com/Collaboration95/rewind-app/attestations/59963857 | Build provenance for commit aea7478 and deployment run 40344230832. | Supply-chain provenance |
| zap-summary.png | file:///Users/speedpowermac/Documents/projects/CODE_MAIN/NUS/SWE5006/presentation-prep/pipeline-run-40344230832/zap/report_html.html | Saved ZAP report summary: 0 high, 4 medium, 7 low and 6 informational alert types. | DAST results, with scan scope shown |
| zap-csp-detail.png | file:///Users/speedpowermac/Documents/projects/CODE_MAIN/NUS/SWE5006/presentation-prep/pipeline-run-40344230832/zap/report_html.html | Saved ZAP report medium-severity CSP wildcard finding and observed instances. | Example DAST finding |

## Exact reference URLs recorded using gh

- ZAP artifact archive endpoint (authentication required): https://api.github.com/repos/Collaboration95/rewind-app/actions/artifacts/12660614474/zip
- Code scanning alerts: https://github.com/Collaboration95/rewind-app/security/code-scanning
- Attestation created by this run: https://github.com/Collaboration95/rewind-app/attestations/59963857

## Not captured

- Deploy, DAST and Quality job summaries with their detailed tables and test counts: public browser requested sign-in; the collaborative screenshot tool timed out twice.
- Code scanning alert list and dismissed reasons: public browser returned 404; the owner's signed-in Brave session could display the list, but an authenticated screenshot could not be saved through the available capture workflow. The default main-branch view showed zero open alerts at the time of inspection. The authenticated `gh` query returned dismissed examples 49, 45, 32, 17 and 16; alerts 54–56 were not returned in that query.
- Branch/ruleset and release-environment protection: public browser returned 404; authenticated captures were not obtained. This is a capture limitation, not a claim that those settings do not exist.
- Repository attestations list was not captured separately; the exact run-specific attestation is captured above.
