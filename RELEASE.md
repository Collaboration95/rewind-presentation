# Release bring-up — 26 October 2026, 22:47 SGT

Presentation: **27 October 2026, 14:30 SGT**. Repository: `Collaboration95/rewind-app`.
Implementation worktree: `/Users/speedpowermac/Documents/projects/CODE_MAIN/NUS/SWE5006/rewind-release-up`, branch `guru/release-up`.

**Current result:** infrastructure is already provisioned and has no Terraform drift. The release application has never been activated and still returns HTTP 504. No release activation or PostgreSQL import is claimed. The remaining sequence is prepared below; only Andrew's final promotion review and one release environment approval require a person. The coordinator performs the merges, dispatch, receipt inspection and Terraform apply.

## Before and after

| Component | Verified before | Result of this run |
| --- | --- | --- |
| Release host | `rewind-release`, running, `micro_3_0`, static IP `18.143.9.66` | Already up; no replacement or power action needed. No application containers; no port 80 listener. About 33 GB free. |
| Host preparation | Pending bundle `f6e50ac9b848af9a85568c710caf4711616881bd` | Both bootstrap markers present. Retained inventory explicitly empty: no SQLite, files, schema or tables. Preserved archive SHA-256 `d5f8fd50a528317d36674bc78a5080657ed88f393749238032d2739841b81fb5`. |
| Release DB | `rewind-release-postgres`, available, `micro_2_0`, private, backup retention enabled | Reachable on TCP 5432 from the release host. Roles, import, activation and recovery still await the protected operation. |
| CloudFront | `E3PXNMFPBJBZEA`, Deployed, origin `ec2-18-143-9-66.ap-southeast-1.compute.amazonaws.com` | Origin and static IP agree. `https://d2r0xzy7vz590e.cloudfront.net/api/health` remains 504 until install. No distribution update needed. |
| Release media | `rewind-release-media-330599756236`, versioning enabled, all public-access blocks enabled | `_config/release.env` exists, AES256, original version `cpM7GoM27Xvip7pnHDAkSvXhO5DLlZtY`, last changed 15 October. No secrets copied by hand. |
| Cognito | Pool `ap-southeast-1_yeHksUpIs`, Essentials; client `3f00nk74h7m63u031bmgq9kv1j` | Managed Login page HTTP 200. Code flow with release callback `/api/auth/callback`, release logout `/`, `COGNITO` provider. Hosted settings have `REWIND_AUTH_PASSWORD=false`. |
| Terraform | One release root: `infra/terraform/release`, including `module.media`; 50 state addresses | Read-only plan: no changes. Applied that saved plan: **0 added, 0 changed, 0 destroyed**. Cutover remains false. |
| Dev | Host `rewind-demo`, CloudFront `d2m6kz76y4kuvm.cloudfront.net`, PostgreSQL healthy | No dev root applied, no dev settings written, no dev resources changed. The coordinator's 30-minute dev cycle setting was left alone. |
| Release workflows | Prepare run `39206079519` succeeded; install `39373300339` waited on old main | Stale install confirmed cancelled. New combined cutover operation prepared; current main must receive it before dispatch. |

The release root's backend is bucket `rewind-terraform-state-330599756236`, key `rewind/release/terraform.tfstate`, region `ap-southeast-1`. It needs no tfvars: its defaults select release. `media/` as a standalone root manages dev; its backend is ignored when used as the release module. `demo/` manages dev, and `bootstrap/` is shared account setup. None of those standalone roots should be applied for this bring-up. There is no separate `infra/terraform/environments/*` release root in this checkout. Backend files remain ignored and uncommitted.

Temporary SSH was used only to inspect release. AWS supplied short-lived keys and pinned host keys; local key material was automatically removed. The temporary operator `/32` was closed after both probes. No application or DB operation was performed over this inspection connection.

## Cost

Live regional bundle APIs report **US$7/month host + US$15/month DB = US$22/month** existing release capacity. It was already running, so this run adds **US$0/month recurring capacity**. The planned settings-only cutover also adds no capacity. There is no RDS resource to create; this is a Lightsail relational database, so the missing `rds:*` permission is irrelevant. No CloudFront update permission is needed for the matching existing origin.

S3, requests, transfer, Cognito usage and manual snapshots are additional. As a bounded storage example, 30 retained daily backups of 1 GB at US$0.025/GB-month are about US$0.75/month, putting that example at about US$22.75/month before requests/media/transfer/noncurrent versions. Thirty 40 GB backups are about US$30/month storage, or US$52/month including the existing capacity. A mistakenly retained rehearsal database would add another US$15/month. Actual cost is workload dependent; the existing US$10/US$15 alerts notify and do not cap spending. No Cost Explorer bill was obtained.

Pricing references: [Lightsail](https://aws.amazon.com/lightsail/pricing/), [S3](https://aws.amazon.com/s3/pricing/), [Cognito](https://aws.amazon.com/cognito/pricing/). Cognito's account-level free allowance must not be assumed to belong exclusively to release.

## Code and cutover plan

Bring-up PR: **[#594](https://github.com/Collaboration95/rewind-app/pull/594)**, head `900a067fd9f47fc5882da9be2d771e0977b06a8c`, targets `dev`. Required CI checks are pending; this sub-agent does not watch or merge PRs.

It adds `operation=cutover` to Deploy release. Under the same environment approval, it validates the release target/settings before changing the host, installs the qualified main bundle with SQLite authoritative, streams the Terraform-generated bootstrap object, stops every runtime writer, takes the exact final snapshot, imports and reconciles PostgreSQL, and uploads `release-cutover-receipt`. The next step waits at most 25 minutes for the coordinator's reviewed Terraform apply. It then streams the updated settings, activates through the existing receipt/hash guard, checks PostgreSQL status and a verified logical backup, and checks CloudFront HTTPS. A timeout leaves writers stopped. Normal `install` and preservation-only `prepare` remain available.

Fast tests passed: root 127 passed/1 skipped; server 985 passed/21 skipped; frontend 1674 passed. Six focused cutover cases passed. ShellCheck, actionlint, formatting and targeted ESLint passed. The normal pre-push hook also passed root/security/server tests, frontend coverage and cloud-free deployment fixtures. One GPT-6.1 Sol high-effort review identified settings-before-validation and deadline issues; both were repaired with regression coverage. Hosted activation, recovery rehearsal and real Cognito session behavior remain unverified until the protected deployment runs.

[PR #562](https://github.com/Collaboration95/rewind-app/pull/562) is still draft and behind dev. It contains only the release `cutover=false → true` change in `infra/terraform/media/database.tf`; dev's configuration is unchanged. Do not apply it before the new receipt succeeds. It can be updated/qualified now, then the coordinator merges it at the reconciled activation window. [Issue #504](https://github.com/Collaboration95/rewind-app/issues/504) still needs the real bootstrap/import/cutover, restart persistence, backup/restore and managed-recovery measurements; neither infrastructure existence nor this PR closes it.

An isolated release-only cutover configuration is staged at `/tmp/rewind-release-up-cutover/infra/terraform/release`. It is a copy of the release/media Terraform source with just that release cutover line changed. It includes the referenced cloud-init and Cognito icon. Its backend is the existing release state. It contains no dev root. Generate a fresh plan there only after receipt inspection. The expected change remains two in-place updates: `module.media.aws_s3_object.hosted_env` and `module.media.aws_iam_role_policy.deploy_reads_hosted_env`; no adds, deletes, replacements, database changes or dev objects are allowed. Inspect the actual fresh plan rather than relying on that expectation.

## Before Andrew's first click — coordinator

Merge the bring-up PR and other intended presentation fixes to `dev` after their required checks pass. Update/qualify #562 so it is ready for the short cutover window, but hold its apply until reconciliation. Finish the final dev→main promotion checks, including the required main-promotion slow/coverage/accessibility gates. Do not ask Andrew to approve a stale promotion head. This implementation agent has merged no PRs and pushed neither protected branch.

```sh
release_repo=Collaboration95/rewind-app
gh pr checks 586 --repo "$release_repo" --required
gh pr view 586 --repo "$release_repo" --json headRefOid,reviewDecision,url
# If #562 needs an update, do this ahead of the activation window:
gh pr update-branch 562 --repo "$release_repo"
gh pr checks 562 --repo "$release_repo" --required
```

## Andrew click 1 — approve final dev→main PR

Open [promotion PR #586](https://github.com/Collaboration95/rewind-app/pull/586/files), select **Review changes → Approve → Submit review** after all intended changes are present and checks are green.

The coordinator then merges the approved exact head and replaces the automatic install with the combined cutover run:

```sh
release_repo=Collaboration95/rewind-app
gh pr merge 586 --repo "$release_repo" --merge
release_main_sha=$(gh api "repos/$release_repo/git/ref/heads/main" --jq .object.sha)
gh run list --repo "$release_repo" --workflow deploy-release.yml --branch main --event push --limit 5 \
  --json databaseId,headSha,status,url
# Set this to the push-triggered run for release_main_sha, then cancel it:
release_auto_run=REPLACE_WITH_MATCHING_PUSH_RUN_ID
gh run cancel "$release_auto_run" --repo "$release_repo"
gh workflow run deploy-release.yml --repo "$release_repo" --ref main -f operation=cutover
gh run list --repo "$release_repo" --workflow deploy-release.yml --branch main --event workflow_dispatch --limit 5 \
  --json databaseId,headSha,status,url,createdAt
```

The coordinator selects the newly dispatched run matching `release_main_sha`, records its ID as `release_run`, and gives Andrew its exact returned `url`. That future URL cannot exist before the final main promotion. Check the run's title/input is **cutover**, not the cancelled automatic install or the old October run.

## Andrew click 2 — approve that release deployment

Open the **new run URL from the command above**, choose **Review deployments → release → Approve and deploy**. Runs are listed at [Deploy release](https://github.com/Collaboration95/rewind-app/actions/workflows/deploy-release.yml). The environment requires `AndrewNguyenLKN`, prevents self-review and allows `main` only. Do not bypass those controls. No separate prepare or Database operations approval is needed for the combined operation.

The coordinator follows the job state using `gh`, then downloads the receipt once **Upload the final reconciliation receipt** completes and **Wait for Terraform cutover and activate PostgreSQL** is running:

```sh
release_repo=Collaboration95/rewind-app
release_run=REPLACE_WITH_NEW_CUTOVER_RUN_ID
gh run view "$release_run" --repo "$release_repo" --json headSha,status,jobs,url
release_receipt_dir=$(mktemp -d /tmp/rewind-release-receipt.XXXXXX)
gh run download "$release_run" --repo "$release_repo" --name release-cutover-receipt --dir "$release_receipt_dir"
jq -e '.environment == "release" and .finalSnapshot == true and (.reconciliation.tables | length > 0)' \
  "$release_receipt_dir/release-cutover-receipt.json"
jq '{environment,manifest,manifestSha256,finalSnapshot,reconciliation}' \
  "$release_receipt_dir/release-cutover-receipt.json"
```

Validate the exact run/main SHA, release identity, fresh manifest, digest and all table reconciliations. The host separately rechecks manifest and PostgreSQL hashes before starting writers. Do not rely on `gh run view --log` for a running job: the downloadable artifact is the handoff mechanism.

During the 25-minute wait, the coordinator completes the code merge and fresh Terraform plan/apply:

```sh
gh pr ready 562 --repo "$release_repo"
gh pr checks 562 --repo "$release_repo" --required
gh pr merge 562 --repo "$release_repo" --merge

release_tf=/tmp/rewind-release-up-cutover/infra/terraform/release
AWS_PROFILE=rewind-terraform-apply terraform -chdir="$release_tf" init -input=false -reconfigure -backend-config=backend.hcl
AWS_PROFILE=rewind-terraform-apply terraform -chdir="$release_tf" plan -input=false \
  -out=/tmp/rewind-release-final-cutover.tfplan
chmod 600 /tmp/rewind-release-final-cutover.tfplan
# Inspect the full plan: only the two release in-place settings/policy updates.
AWS_PROFILE=rewind-terraform-apply terraform -chdir="$release_tf" show /tmp/rewind-release-final-cutover.tfplan
# Only after the receipt and exact plan are accepted by the coordinator:
AWS_PROFILE=rewind-terraform-apply terraform -chdir="$release_tf" apply -input=false /tmp/rewind-release-final-cutover.tfplan
```

This writes `_config/release.env` through Terraform. It never reads or writes `_config/dev.env`. The approved deployment notices the selected PostgreSQL URL, configures it from S3 and finishes activation and backup. Credentials are never placed in shell commands, chat or this file.

## Verify after the approved job finishes

```sh
gh run view "$release_run" --repo "$release_repo" --json status,conclusion,headSha,url
curl -fsS https://d2r0xzy7vz590e.cloudfront.net/api/health |
  jq -e '.ok == true and .ready == true and .checks.database == "postgresql" and .checks.schema.ready == true'
curl -fsS https://d2r0xzy7vz590e.cloudfront.net/ -o /dev/null
curl -fsS https://d2r0xzy7vz590e.cloudfront.net/api/auth/config |
  jq -e '.passwordSignIn == false and .cognito == true'
curl -fsS https://d2m6kz76y4kuvm.cloudfront.net/api/health |
  jq -e '.ok == true and .ready == true and .checks.database == "postgresql"'
```

Health and the deployment's image/revision comparison are the activation gates. Confirm Cognito is offered and developer password sign-in is absent/rejected. With an owned account, verify callback, sign-out, group/invitation and photo/video storage. Check the run's PostgreSQL status and backup result, the installed revision against `headSha`, and restart persistence through the normal protected operations if not already exercised. Do not infer a working user session from a 200 Managed Login page.

## Rollback and bounded blockers

- **Before the new protected run:** no release writers exist; cancel a wrong or stale run. Leave the host, database and retained archive intact. Use ordinary `install` for the fastest SQLite release if PostgreSQL activation is deferred; `prepare` alone never makes the public app run.
- **Bootstrap fails before quiesce:** the newly installed SQLite app remains authoritative. Fix the exact cause; do not select PostgreSQL.
- **Import fails or the apply wait expires:** writers remain stopped and retained SQLite/backups are preserved. Do not remove maintenance markers. If Terraform still selects SQLite, run the protected Database operations `target=release operation=resume` to abandon the import window. If cutover was already applied after a valid receipt, rerun qualified Deploy release `operation=install`; the existing activation guard revalidates reconciliation. A recovery workflow rerun may need a new environment approval; it is a failure contingency, not an extra approval in the successful two-click path.
- **After PostgreSQL accepts writes:** do not flip back to the old SQLite file. Use the documented quiesced reverse export/install with content reconciliation, or a verified PostgreSQL restore. Leave existing data, snapshots, tags and branches intact. Compatible image rollback uses `release-host.sh rollback`; it refuses newer-schema/config mismatches. The first-ever installation has no previous activated image to roll back to.
- **Host inspection:** first probe stopped on a permission-denied inventory read; the second used read-only sudo and succeeded. No further attempts needed.
- **Local tests:** first fast run timed out in two unchanged frontend tests; the latest-dev rerun and post-review rerun passed without changing tests or timeouts.
- **Isolated cutover-plan staging:** two initial plan attempts stopped on missing relative `cloud-init.sh`, then `assets/icon.png`. Both inputs have now been staged in the repository-relative layout. No cutover plan was saved or applied during this run. The unblock is the fresh `init/plan` above after receipt inspection; inspect it before applying. The live no-change release root plan/apply succeeded independently.
- **Permissions:** read-only profile cannot list CloudFront; the authorized Terraform profile successfully read it. Missing RDS/Cost Explorer/CloudFront-update permissions did not block any required resource action. Do not widen IAM merely for those unused services.

Limit any new focused blocker diagnosis to two attempts, record its exact error and unblock here, then continue independent work. Managed restore rehearsal, actual recovery timing, restart persistence and full real-account acceptance remain issue #504 follow-up evidence until performed; no successful deployment is claimed in advance.
