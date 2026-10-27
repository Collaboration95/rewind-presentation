# Fix list: bring the real system to parity before any slide or diagram work

Written 26 Oct 2026, 22:30 SGT. **Freeze rule:** no slides or diagrams until this list is done
and merged. The slides then describe a system that already does these things.

Requirement sources:
- **[G]** Presentation Guidelines docx (`~/Downloads/course_files_export 5/…Presentation Guidelines.docx`).
- **[B]** Briefing deck, deliverables slides 5–6.
- **[E]** Lecturer email (5-section outline).
- **[F]** FlickPond assessor feedback (`../presentation-feedback-carryover.md`).

## What the requirements actually ask for (checklist)

| Requirement | Source | Today | Gap |
|---|---|---|---|
| Strategy to manage **source code and artifacts** | G: DevSecOps | Code: protected dev/main, PR-only. Artifacts: images are rebuilt on the host from a tarball; the only uploaded artifacts are coverage and a PR-only SBOM | **No artifact story.** Nothing versioned, nothing tied to the deployed build |
| DevSecOps pipeline and procedures, with "minimal security considerations" | G, B | SAST (CodeQL), SCA (npm audit), Trivy image + IaC, SBOM, secret scanning + push protection, OIDC | DAST missing; scans don't gate deploys; the scanned image is not the deployed image |
| SAST **and DAST** visible inside the pipeline run | F, E | CodeQL only, no DAST | DAST missing |
| Technical findings and issues encountered | G | Many real ones (zod advisory, ffmpeg pin rot, apt-get hang flake, CodeQL dismissals) | Not written up anywhere |
| CI/CD pipeline demo, recorded backup | E | Pipeline red since 24 Oct | **Fix #591 in progress** |
| Demo quality attributes: **performance via scripted perf test** | G | Script exists, local SQLite only, not in CI | No hosted, repeatable run with a saved result |
| Demo quality attributes: **scalability (e.g. auto-scaling)** | G | One Lightsail host, no auto-scaling | Can't build tonight; answer honestly (plus measured headroom from the perf run) |
| Demo quality attributes: **maintainability (run the pipeline)** | G | Same as CI/CD demo | Covered once green |
| Significant use cases demonstrated on the real system | G, E | Hosted dev up; 28-day cycle; weekly push | Cycle now 30 min (applied); push can't be shown; copy says "four weeks" |
| Agile artifacts: backlog, user stories, sprint plans, **burndown charts**, reviews, retros | B | Issues, milestones, sprint plans, progress reports exist | No burndown chart file; effort table says "to fill" |
| Effort per member, DoD, sprints, retro and reflection | G | DoD, 4 sprints, progress reports | Effort: split equally (owner decision), labelled "agreed" |
| Unit tests for complex classes; analysis→design; patterns; DB schema | B, G | Tests strong; models stale | Diagram work is frozen until after the fixes |

## The fix list (one batch, overnight)

Effort is agent time. **P0** is required for parity. **P1** removes a known weakness an assessor is likely to probe.

### A. Pipeline and artifacts (the DevSecOps story)

| # | Fix | Why (source) | Artifact produced | Pri | Effort |
|---|---|---|---|---|---|
| A1 | Merge **#591** (zod override, ffmpeg pin) | Pipeline red (E) | none | P0 | in CI now |
| A2 | **DAST:** ZAP baseline job after deploy-dev, report-only. Already written on branch `guru/presentation-dast` | F, E | `zap-report.json`, `.html`, `.md` + run summary | P0 | 15 min |
| A3 | **Scan what we ship:** in deploy-dev, after "Build the verified release bundle", run Trivy on the *bundle's* images and generate CycloneDX SBOMs for them. **Fail the deploy on HIGH/CRITICAL** | Scanned ≠ deployed today; scans don't gate deploys | `sbom-runtime.cdx.json`, `sbom-web.cdx.json`, `trivy-runtime.json`, `trivy-web.json` | P0 | 45 min |
| A4 | **Signed provenance:** `actions/attest-build-provenance` on the release bundle tarball (free on public repos), checkable with `gh attestation verify` | Signing/provenance missing | Sigstore attestation linked to the run | P1 | 20 min |
| A5 | **Release manifest:** one `release-manifest.json` per deploy (commit, run ID, image IDs and digests, SBOM and scan hashes, Quality run ID, timestamp), uploaded as an artifact and kept on the host | "manage artifacts" (G) | `release-manifest.json` | P0 | 30 min |
| A6 | **Evidence bundle in Quality:** JUnit XML for server/root/frontend, `coverage-summary.json`, `npm-audit.json`, and a job summary table (counts, coverage, audit result) on every run | Show test and SCA artifacts (G, F) | `test-results-*.xml`, `coverage-summary.json`, `npm-audit.json` | P0 | 45 min |
| A7 | **Secret scan job (gitleaks)** with the allowlist that was verified clean locally | Visible secrets box in CI | `gitleaks.sarif` (also shown in the Security tab) | P1 | 20 min |
| A8 | **Run Release security on push to dev**, not only on path-filtered PRs, so every merged commit has image + IaC scans | Gap found in audit C | as A3 | P1 | 10 min |
| A9 | **Flake fix:** timeout plus one retry on "Install FFmpeg" / apt-get (it hung tonight on #591) | Live demo reliability; a real "technical issue encountered" | none | P1 | 20 min |
| A10 | **Performance workflow:** a manual-dispatch job runs the scripted load test against hosted dev (moderate, read-mostly, rate-limit aware) and saves the result | G demo: scripted perf test | `perf-results.json` + summary table | P0 | 1–1.5 h |
| A11 | Optional, after A1: merge **#589/#590** (open `mvp` bugs) once green. Their earlier red runs stay as "gate blocked a merge" evidence | Fewer outstanding issues | none | P1 | 15 min |

**Not doing, said honestly on a slide:**
- Required-check redesign (only the aggregate gate is required).
- Authenticated or active ZAP (shared data).
- Auto-scaling (single host by design).
- The release environment: it needs reviewer AndrewNguyenLKN, and the host is down by choice.

### B. App changes that make the real demo honest

| # | Fix | Why | Pri | Effort |
|---|---|---|---|---|
| B1 | Derive the "four weeks / Week N of 4" copy from the group's real cycle length (`GroupFlows.tsx:200`, `App.tsx:558`, `Home.tsx:90`) | A 30-min demo cycle currently shows wrong text on screen | P0 | 45 min |
| B2 | **Dev-only reminder trigger:** a setting so dev sends the real web-push reminder N minutes before a cycle ends (default stays Sunday 19:00) | Shows real push on the iPhone; owner allowed simulation | P1 | 1–1.5 h |
| B3 | Verify Cognito sign-in inside the iPhone Home Screen app | Never tested; blocks scene 2 | P0 | owner, 10 min |

### C. Records and docs (sources the slides will read from)

| # | Fix | Why | Pri | Effort |
|---|---|---|---|---|
| C1 | Burndown and velocity charts per Sprint, generated from GitHub issue events (data already rebuilt by audit G) | B: burndown charts | P0 | 45 min |
| C2 | Effort table: equal split, labelled "agreed split, not measured". Ceremonies: Sprint Planning, Review and project planning meetings held; outputs in GitHub and progress reports | Owner decision | P0 | 15 min |
| C3 | Team: five names. Sang Haoxiang listed with minimal contribution; the others' contributions taken from the progress reports | Owner decision | P0 | 20 min |
| C4 | Correct facts on the explainer site: `patterns.json` bad path, test-file counts, "Member A–D" placeholders, status dated 26 Oct, DAST and artifact sections updated after A | The site is the Q&A source | P1 | 30 min |
| C5 | "Technical findings and issues" log: zod advisory, ffmpeg pin rot, apt-get hang, CodeQL dismissals with reasons, IaC exceptions expiring 31 Oct, deploy-after-refactor break (#583) | G: findings | P0 | 30 min |

### D. Main promotion

- Promotion to `main` (PR #586 or a fresh one) **needs one approving review from a teammate**. Branch protection enforces this for admins too, so I cannot approve my own PR.
- Deploy release also needs **AndrewNguyenLKN**, and the release host is down.
- Plan: open a green promotion PR after the batch merges. A teammate approves if available, which gives the demo "the review gate in action". Everything else runs and is recorded off **dev**.

## Order overnight

1. A1 → A2. That merge plus deploy shows DAST in a real run.
2. One batch PR (per CLAUDE.md) with A3–A9, B1, B2, C4 and C5. Then merge, and deploy-dev runs the full pipeline with every artifact.
3. A10: perf run on hosted dev. C1–C3. A11.
4. Freeze. Then diagrams, slides and recordings, from the frozen state and its run IDs.
