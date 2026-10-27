# B2 · Design patterns, design classes, state, deployment, ER

Code read: worktree `rewind-present-audit` = `origin/dev` f6cd896 (20 Oct 2026). Read-only. [verified] = read in code at f6cd896; [inferred] = deduced, not observed.
Rendered drafts (PUML, SVG, PNG): `/tmp/rewind-b2/uml/` (d1-d4 class, s1-s3 state, p1 deployment, e1 ER, `_style.iuml`). They render, but layout needs one tidy pass before slides.

## 1. Pattern claim inventory (patterns.json, analysis-design.json, owners.json, report packages)

decisions.json, database.json, architecture.json, aws.json and cicd.json make no pattern claims [verified, grep]. The site pages are already honest about limits. The risk is in a few labels and in the old report packages.

| # | Claim (where) | Verdict | Evidence and gap |
|---|---|---|---|
| 1 | Adapter: `PostgresDatabase` adapts PostgreSQL to the node:sqlite surface (patterns other-patterns) | **Real** | `postgres/database.ts:106` PostgresStatement, `:139` PostgresDatabase (`prepare :235, exec :239, close :255`); `db.ts:48` `RewindDatabase = DatabaseSync`; `translate.ts:257`; pg client in worker thread `sync-worker.ts:5`. Gap: structural only (no `implements`); `db.ts:52` casts `as RewindDatabase`. |
| 2 | Strategy: storage selection disk/s3 (patterns other-patterns; report CAPTURE) | **Partial** | `MediaStore` `media/store.ts:29`, impls `local-store.ts:18` and `s3-store.ts:55`, chosen in `runtime-store.ts:347`. Missing: `disk` is `config.media === null` (`config.ts:340`), not a third strategy. Callers branch on the store or the ref: `isMediaRef` at `jobs/clip.ts:441,673`, `jobs/stored-output.ts:90,119`, `jobs/compilation.ts:957,1009`, `routes/media-access.ts:213`, `auth/deletion.ts:156`. `docs/architecture/current-system.md:116` says the same. |
| 3 | Adapter: S3 behind the store seam (report CAPTURE) | **Real** | `privateTransport(sdk)` `runtime-store.ts:143` maps AWS SDK commands to `PrivateS3Transport` `s3-store.ts:30`. |
| 4 | Adapter: `CognitoService` (ACCESS) | **Partial** | Port `auth/cognito.ts:22`, one production impl `createCognitoService :55`, test doubles `server/tests/cognito-auth.test.mjs`. Sign-in itself is two parallel route sets (`routes/auth-routes.ts:417-427`) switched by a flag (`:448`), so it is **not** a Strategy. The site already says so (patterns ACCESS qa[2]). |
| 5 | Adapter: `CameraPlatform` / `ExpoCameraPlatform` (CAPTURE) | **Real** | `src/capture/contracts.ts:101`, `platform.ts:462` ("No Expo or React Native types cross the capture port", `:461`). One production impl plus test fakes (`tests/CameraCaptureScreen.test.tsx:109`). |
| 6 | Observer/pub-sub `RealtimeHub` (PARTICIPATION) | **Real** | Real class `realtime/index.ts:9`, `subscribe :12` returns unsubscribe, `publish :22`; observers are the function type `RealtimeEventWriter :3` (no Observer interface); subscriber `routes/chat-routes.ts:244`; publish after commit `:394,:463`; created `http.ts:179`. Process-local (current-system.md). |
| 7 | Provider Adapter/Strategy + durable outbox (PARTICIPATION) | **Real** | `ReminderProvider` `reminders/outbox.ts:30`, registry type `:34`, web-push impl `providers.ts:194`, Expo impl `:122` (disabled scope), factory `:234`, pick by row `outbox.ts:499`, lease `:40`. |
| 8 | State machine (CYCLE; `server/src/cycles/lifecycle.ts`) | **Real** as persisted state + guarded functions | `lifecycle.ts:312-411`, `:216-273`. No per-state classes (site says so). **Broken citation:** `src/domain/cycles.ts` (patterns other-patterns, "State machine" row) does not exist [verified]. Use `server/src/cycles/engine.ts:65` (`cyclePhase`). |
| 9 | Command = durable job records (CYCLE) | **Partial** | `media_jobs` rows with `claim_generation` fence (`jobs/compilation.ts:501-574`). No command object or `execute()`. Call it "durable job queue with fenced claims". |
| 10 | Proxy: `MediaCapabilities` (ARCHIVE; report says "Strong") | **Weak** | `archive/capabilities.ts:22` issues and resolves tokens; `routes/archive-routes.ts:30-80` then serves. No shared interface with a real subject, so a lecturer can say "that is not a Proxy". Say "capability token + guard". |
| 11 | Facade: `createRealAccountArchiveClient` (ARCHIVE) | **Real, small** | `src/auth/real-account-client.ts:580`, interface `:417` (3 methods). |
| 12 | Adapter: download functions (ARCHIVE) | **Weak** | `src/archive/archive-download.ts:253` is a `Platform.OS === 'web'` branch inside functions. No interface. |
| 13 | "Repository-style functions" (patterns other-patterns) | **Not real** as Repository | `groups/real.ts` (13 `prepare`), `contributions/ledger.ts` (6), `chat/index.ts` (19) mix validation, transactions and SQL; routes still hold SQL (`routes/media-access.ts` 3, `contribution-routes.ts` 1, `real-routes.ts` 1). Do not draw a Repository. |
| 14 | Template Method "not evidenced"; `runAuditedJob` is a callback wrapper | **Correct** | `jobs/audited.ts:55`. |
| 15 | Report packages `doc/planning/report/packages/*/design-problem.md` | **Stale** | Pinned to fc2b8c8 (3 Oct) and 1128b6a (4 Oct). ACCESS cites `requireAuthorisedGroup` / `authorizeSessionMember`, which no longer exist (grep empty). Demo labels remain in `access/diagrams/problem-after-class.svg`. PARTICIPATION still says a one-shot `reminders --once` (now a 60 s loop, `cli.ts:635`). CYCLE says SQLite-only. The site (patterns.json intro) admits this. Do not reuse those SVGs as "as built". |

Unclaimed but real: route table `Route<C>` + `findRoute` (`routes/context.ts:31-54`), used by 4 route families (table-driven dispatch).

## 2. Recommended patterns (2-4)

Use 1 and 2 for the 5-minute slot; 3 and 4 as backup or for members who must each speak. Every figure carries "as built at f6cd896".

### P1 · Media storage: Strategy, with an S3 Adapter (lead pattern; drawn in d1-storage)
- **Problem:** capture, film compilation and Archive serving must read and write private media in two environments (local disk, hosted S3) without if-statements in each job.
- **Candidates:** (a) `if (s3)` branches in every job; (b) a `MediaStore` interface with one implementation per backend.
- **Chosen (b):** a new backend does not touch jobs, and tests inject the local store (`server/tests/configured-media-runtime.test.mjs`).
- **Say aloud:** local `make run` uses the legacy disk path, which is "no store"; hosted dev sets `REWIND_MEDIA_BACKEND=s3` (`infra/terraform/media/main.tf:216`).

| Element | Role | File:line |
|---|---|---|
| `interface MediaStore {put, head, read, delete}` | «strategy» | `media/store.ts:29` |
| `class LocalMediaStore implements MediaStore` | «concrete strategy» | `media/local-store.ts:18` (put :46, head :65, read :83, delete :95) |
| `class PrivateS3MediaStore implements MediaStore` (ctor: transport, options) | «concrete strategy» | `media/s3-store.ts:55` |
| `interface PrivateS3Transport {putObject, headObject, getObject, deleteObject}` | «target» | `media/s3-store.ts:30` |
| `privateTransport(sdk): PrivateS3Transport` | «adapter» (module function) | `media/runtime-store.ts:143` |
| AWS SDK `S3Client` + `*Command` (`S3RuntimeBindings`) | «adaptee» | `runtime-store.ts:41`, loaded `:91` |
| `createMediaRuntime(config): Promise<MediaRuntime>` | «factory» | `runtime-store.ts:347` (new Local `:355`, new S3 `:381`) |
| `parseMediaConfig(env, dataDir): MediaRuntimeConfig \| null` | «config» (null = disk) | `config.ts:338` |
| `interface StoredJobOptions {mediaStore?; mediaEnvironment?}` + `storedContext()` | «context» | `jobs/stored-output.ts:17,38` |

Relations: both stores realise `MediaStore`; `PrivateS3MediaStore --> PrivateS3Transport`; `createMediaRuntime` creates the stores; `StoredJobOptions o-- 0..1 MediaStore`.

### P2 · Persistence: Adapter (PostgreSQL behind the node:sqlite surface; d2-persistence)
- **Problem:** local runs and most tests use SQLite; hosted dev uses PostgreSQL 17; 37 server files call `database.prepare(sql).get(...)` synchronously.
- **Candidates:** (a) rewrite every module on async `pg`; (b) an adapter exposing the same synchronous method names, with SQL translation.
- **Chosen (b):** domain code unchanged; the suite can run on PostgreSQL (`REWIND_TEST_DATABASE_URL`, `postgres/runtime.ts:63`); ADR-0003 holds the decision.

| Element | Role | File:line |
|---|---|---|
| `DatabaseSync`, `StatementSync` (built-in `node:sqlite`) and `type RewindDatabase = DatabaseSync` | «target» | `db.ts:3,48` |
| `class PostgresDatabase` (`prepare`, `exec`, `query`, `close`, `call_`) | «adapter» | `postgres/database.ts:139` |
| `class PostgresStatement` (`run`, `get`, `all`, `iterate`) | «adapter» | `postgres/database.ts:106` |
| `translate(sql): TranslatedStatement` | «module» | `postgres/translate.ts:257` |
| worker thread with `pg.Client`, `port.on('message')` | «adaptee» | `postgres/sync-worker.ts:5,355` |
| `openDatabase(config)` / `asRewindDatabase` | «factory» | `db.ts:68`, `:52` |

Relations: `PostgresDatabase *-- PostgresStatement`; `PostgresDatabase ..> translate`; `PostgresDatabase ..> sync-worker` (postMessage + `Atomics.wait`, `database.ts:178-201`); `openDatabase` creates either side.

### P3 · Reminders: provider Strategy + durable outbox (d3-reminders)
- **Problem:** a weekly reminder must survive crashes, opt-outs and provider errors. A direct push call from the settings handler loses all three.
- **Candidates:** (a) call the push provider inline; (b) `ReminderProvider` strategies behind a leased `reminder_outbox` table.
- **Chosen (b):** the row, its lease and its state make a send durable, bounded (3 attempts) and cancellable.

| Element | Role | File:line |
|---|---|---|
| `interface ReminderProvider {send, receipt?}`; `ReminderProviders = Partial<Record<name, ReminderProvider>>` | «strategy» | `reminders/outbox.ts:30,34` |
| `createWebPushReminderProvider(config, binding)` | «concrete strategy» | `reminders/providers.ts:194` |
| `createExpoReminderProvider` | «concrete strategy», disabled scope | `providers.ts:122` |
| `interface WebPushBinding` + object literal using `web-push` | «target» / «adapter» | `providers.ts:18`, `:250-285` |
| `createConfiguredReminderProviders(config)` | «factory» | `providers.ts:234` |
| `scanDueReminderJobs`, `runReminderOutboxTick(db, providers)` | «context» | `outbox.ts:306,443` (`providers[destination.provider]` `:499`) |
| `startReminderLoop` (60 s, only if a provider exists) | «module» | `loop.ts:12`; `cli.ts:635` |
| table `reminder_outbox` (7 states, lease, `UNIQUE(group_id, account_id, local_sunday)`) | «table» | `030-baseline.sql:378` |

### P4 · Chat: Observer (RealtimeHub; d4-observer)
- **Problem:** members in a group must see a message at once, without polling.
- **Candidates:** (a) client polling; (b) a subject that fans out committed events.
- **Chosen (b):** SSE writers subscribe per group; persisted `realtime_events` give replay after a reconnect.

| Element | Role | File:line |
|---|---|---|
| `class RealtimeHub` (`subscribers`, `subscribe`, `publish`, `subscriberCount`) | «subject» | `realtime/index.ts:9-42` |
| `type RealtimeEventWriter = (event) => void` | «observer» | `realtime/index.ts:3` |
| SSE handler closure (`writeEvent`, `writeReaction`, `subscribeToGroup`) | «concrete observer» | `routes/chat-routes.ts:223-250` |
| POST handlers call `publish` after `createChatMessage` | «publisher» | `chat-routes.ts:394,463`; `chat/index.ts:347,498` |
| `listChatEvents` replay; table `realtime_events` | persistence | `chat/index.ts:221`; `chat-routes.ts:312` |

Not recommended: Repository (#13), Proxy (#10), sign-in Strategy (#4), Template Method, Command.

## 3. Statecharts (a)

**Cycle** (`cycles.status`, `cycles.release_status`; s1-cycle). Initial: `createRealGroup()` inserts `collecting` (`groups/real.ts:94-99`). Trigger for all: `runCycleSchedulerTick` (`cycles/scheduler.ts:46`, 1 s loop `:114`). Each runs in one `BEGIN IMMEDIATE` transaction.

| From | Event [guard] / action | To | Code |
|---|---|---|---|
| collecting | advance [now < ends_at] / waiting_for_boundary | collecting | `lifecycle.ts:333-339` |
| collecting | advance [now >= ends_at] / status='revealing'; event `collecting_to_revealing`; `ensureCompilationJob` (film job pending); `ensureSuccessor` (new collecting cycle, move `groups.current_cycle_id`) | revealing/unpublished | `:344-364`, `:276-310` |
| revealing/unpublished | advance / waiting_for_release | same | `:368-372` |
| revealing/unpublished | `publishCycleRelease` [status='revealing' and now >= ends_at and film job `ready` with verified sha256 and size] / release_status='published', release_published_at=now | revealing/published | `:216-273`; called `scheduler.ts:77` |
| revealing/published | advance [now < published_at + 24 h] / premiere | same | `:373-377`; `PREMIERE_DURATION_MS :38` |
| revealing/published | advance [now >= published_at + 24 h and output re-verified] / status='archived'; event `revealing_to_archived` | archived | `:378-395` |
| archived | advance / already_archived | archived | `:367` |

"Premiere" is a time window, not a stored state. `lock_state` is always `'locked'` (vestigial); leave it off the chart. Replays are safe via `UNIQUE (cycle_id, transition)` on `cycle_lifecycle_events` and the conditional `UPDATE groups ... AND current_cycle_id = ?` (`:306`).

**Media job** (`media_jobs.status`, clip and film; s2-job). Create: `completeUploadIntent` (clip) or `ensureCompilationJob` (film, `compilation.ts:410`).
- pending → processing: claim [film: all clip inputs settled] / `claim_generation+1`, `attempt_count+1`, `processing_started_at` (`compilation.ts:501-574`; `clip.ts:254-325`).
- processing → processing: claim [now − started ≥ 15 min, `jobs/shared.ts:6`] / `claim_generation+1`, same attempt.
- processing → ready: finalise [claim_generation current; output verified] / `output_path`, `output_sha256`, `output_bytes`, `output_verified_at` (`compilation.ts:785-850`; `clip.ts:603`).
- processing → failed: error [claim_generation current] / `error_code`, `failed_at` (`compilation.ts:762-783`).
- failed → processing: claim [attempt_count < 3] (`MAX_COMPILATION_ATTEMPTS`, `compilation.ts:34`; worker cap `worker.ts:165`). failed → end: `retry_exhausted` (a clip stays retryable by request, `worker.ts:63`).

**Upload intent** (`upload_intents.state`; s3-intent; capture): `[*]→open` (`requestUploadIntent` [member, cycle collecting, quota], `upload-intents.ts:442`) → `pinned` (`completeUploadIntent`, `:635`) → `completed` (probe ok, `checkQuota`, insert `contributions` + clip job + `staged_sources`, `cycles.count_used+1`, `:780`); `open|pinned → expired` (`cleanupUploadIntents`, `:826`). Reminder outbox has its own 7-state machine (`outbox.ts:443-557`); skip unless asked.

## 4. Deployment (b): hosted dev as declared (p1-deploy)

Nodes [verified from Terraform and compose; the live account was not queried]:
- **Member device:** browser or installed PWA; `public/sw.js` handles `push` (`:167`).
- **CloudFront** (`demo/web-distribution.tf:1-70`): viewer HTTPS, caching disabled, origin = `ec2-<static-ip>.ap-southeast-1.compute.amazonaws.com` over **http-only :80**, injects `X-Rewind-Origin-Auth` and `X-Forwarded-Proto: https`. The default is `real_auth_https_distribution_enabled = false` (`demo/variables.tf:76`); hosted dev uses it, per README ("single public entry point `d2m6kz76y4kuvm`") and `nginx.conf` redirects [inferred: the tfvars are private].
- **Lightsail instance `rewind-demo`** (`demo/lightsail.tf:36-81`): `micro_3_0`, Ubuntu 24.04, static IP, firewall 80 open, 22 limited to the operator CIDR. Docker Compose project (`deploy/compose.yaml`):
  - `rewind-demo-web`: nginx, container :8080 published on host :80, serves the Expo web export and proxies `/api/` (`nginx.conf`).
  - `rewind-demo-runtime`: Node `server/src/cli.ts start`, :8787 bound to 127.0.0.1, read-only root, tmpfs `/tmp`, volumes `/srv/rewind/data|media`. One process holds the HTTP app, `RealtimeHub`, the cycle scheduler with the media worker tick, the reminder loop and ffmpeg children (`cli.ts:598-690`, current-system.md). **There is no separate worker or queue service.**
  - systemd timer `rewind-backup`, 03:15 UTC (`deploy/rewind-backup.timer`), uploads to an S3 backup bucket.
- **Lightsail managed PostgreSQL 17** `rewind-dev-postgres`, `micro_2_0`, single AZ, public with TLS and generated role logins, daily backup with 7-day restore (`media/database.tf:14-60`). It is **not RDS**, and not Aurora.
- **S3 media bucket** `rewind-dev-media-<acct>` (`media/main.tf`): private, versioned, SSE-S3, TLS-only policy, CORS PUT from the CloudFront origin, lifecycle (abandoned `incoming` 7 d, old versions 30 d), plus `_config/dev.env` read by the deploy role. Runtime uses a static IAM user key (Lightsail has no instance roles).
- **Cognito** pool `rewind-dev`, Managed Login, code + PKCE, self sign-up, no MFA (`media/cognito.tf`). **Web push**: the runtime POSTs to the endpoint inside each subscription (browser vendor push service) with VAPID (`providers.ts:260-285`).
- **GitHub Actions `Deploy dev`** (`.github/workflows/deploy-dev.yml:143-330`): OIDC → role `rewind-demo-deploy` → opens SSH for the runner IP only → scp bundle → `release-host.sh configure|install` → health check → closes SSH. No Terraform in the pipeline.
- Edges: PWA→CloudFront HTTPS; CloudFront→nginx HTTP :80; nginx→runtime :8787; runtime→PostgreSQL TLS (5432 default [inferred]); runtime→S3 HTTPS; PWA→S3 presigned PUT; runtime→Cognito token endpoint; runtime→push service.
- Absent (useful for Q&A): load balancer, NAT, ECS/Fargate, ECR, SQS, RDS, separate worker.

**Dev vs release** (`infra/terraform/release/main.tf`): release is a second, independent stack, declared `rewind-release` (own Lightsail host, static IP, CloudFront, deploy role limited to GitHub environment `release` on `main`, backup bucket, own media bucket and Cognito pool via the `media` module). It sets `auth_password=false` (no password form). Its database is enabled but private with `cutover=false` (`media/database.tf:16-18`; README says "configuration is not proof of a live apply"). Deploy: `deploy-release.yml` from `main` after review, versus dev on every merge to `dev`. Whether release runs today was **not verified**; an earlier project note says it was stopped on purpose (8 Oct). Dev keeps the password form ("Developer sign-in") next to Cognito.

## 5. ER subset (c): capture, cycle, Archive (e1-er; PostgreSQL baseline 030 + 031)

Types: IDs and timestamps are `TEXT COLLATE "C"` (ISO-8601 strings), counters `BIGINT`, seconds `DOUBLE PRECISION` (`030-baseline.sql:1-14`). Archive has **no table**: it is published cycles plus their film job and clip jobs.

| Table | PK | FKs and key columns |
|---|---|---|
| groups | id | `current_cycle_id` (logical, no FK) |
| real_group_metadata | group_id | → groups; `owner_account_id` → real_accounts; `max_members` 2..10; `time_zone` |
| cycles | id | `group_id` → groups; `previous_cycle_id` → cycles (partial unique, so ≤ 1 successor); `status` collecting/revealing/archived; `release_status`; `release_published_at`; `max_count`, `max_seconds`, `count_used`, `seconds_used` |
| cycle_lifecycle_events | id | `cycle_id` → cycles; `transition` (3 values); UNIQUE(cycle_id, transition) |
| contribution_quota_windows | id | `cycle_id` → cycles; `member_id` → profiles; UNIQUE(cycle_id, member_id, window_start_at) |
| profiles / real_profiles | id / id | `profiles` mirrors `real_profiles` by trigger (same id; `030-baseline.sql:543-580`); `real_profiles.account_id` → real_accounts, unique |
| contributions | id | `cycle_id` → cycles; `member_id` → **profiles** (not real_profiles); `media_job_id` logical, no FK; `duration_seconds`; `deleted_at`; `replaced_by_contribution_id` → contributions |
| upload_intents | id | `group_id` → real_group_metadata; `profile_id` → real_profiles; `cycle_id` → cycles; `contribution_id` unique → contributions; `job_id` unique → media_jobs; `state`; `pinned_ref`; UNIQUE(environment, group_id, profile_id, idempotency_hash) |
| media_jobs | id | `group_id` → groups; `cycle_id` → cycles (film); `contribution_id` → contributions (clip); `kind`; `status`; `claim_generation`; `attempt_count`; `output_path`, `output_sha256`, `output_bytes`; partial unique (cycle_id) WHERE kind='film' |
| compilation_job_inputs | (job_id, clip_job_id) | both → media_jobs; `contribution_id` → contributions; `position`; UNIQUE(job_id, contribution_id) |
| film_segments | (film_job_id, position) | `film_job_id` → media_jobs; `contribution_id` → contributions (SET NULL); `start_seconds`, `duration_seconds` |

12 boxes is dense; for a slide split into "capture + cycle" and "Archive". Cardinalities are in the PUML.

## 6. PlantUML

Works here. The jar is `/tmp/rewind-b2/plantuml.jar` (v1.2026.9, 30 MB, from github.com/plantuml/plantuml/releases/latest). **Run format flags separately**: `-tsvg -tpng` together writes only one format.
```sh
cd /tmp/rewind-b2/uml   # _style.iuml must sit next to the .puml
for f in svg png; do java -Djava.awt.headless=true -jar /tmp/rewind-b2/plantuml.jar -t$f *.puml; done
```
Smoke test passed for class and sequence (`/tmp/rewind-b2/t-class.*`, `t-seq.*`, SVG and PNG). `dot` is used for class, state, deployment and ER; sequence needs none. Docker not needed.

FlickPond look (`.../presentation/site/assets/uml/_style.iuml`): Helvetica 15, white shapes, 1.4 slate arrows (#475569), class header #F1F5F9, notes #fffbe6, transparent background, blue interface boxes, green implementation/entity boxes, amber external boxes, legend at the bottom ("as built at <sha>" in every title). Useful block (also saved as `/tmp/rewind-b2/uml/_style.iuml`):
```
skinparam dpi 110
skinparam shadowing false
skinparam roundCorner 6
skinparam defaultFontName "Helvetica"
skinparam defaultFontSize 15
skinparam defaultFontColor #0f172a
skinparam ArrowColor #475569
skinparam ArrowThickness 1.4
skinparam ArrowFontSize 13
skinparam BackgroundColor transparent
skinparam NoteBackgroundColor #fffbe6
skinparam NoteBorderColor #d6c27a
skinparam LegendBackgroundColor #ffffff
skinparam LegendBorderColor #94a3b8
skinparam ClassBackgroundColor #ffffff
skinparam ClassBorderColor #334155
skinparam ClassHeaderBackgroundColor #F1F5F9
skinparam classAttributeIconSize 0
skinparam StateBackgroundColor #ffffff
skinparam StateBorderColor #334155
hide circle
hide empty members
```
Role boxes: `interface X <<strategy>> #DBEAFE`, `class Y <<adapter>> #ECFDF5`, `<<adaptee>> #FEF3C7`, modules as `class "file.ts" as M <<module>>`.

## 7. Problems that would hurt the presentation

1. **Disk is not a Strategy.** Do not draw "Disk / S3 / Local" as three strategies. Draw `LocalMediaStore` and `PrivateS3MediaStore`, and state that local runs use the legacy path (#2).
2. **Sign-in "Strategy" (Cognito vs password) is not in the code** (#4). Pitch Cognito as a port with an injected test double, and the password form as a dev-only route set.
3. **Proxy and Repository labels will be challenged** (#10, #13). Drop both, or hedge in one phrase.
4. **Broken citation** `src/domain/cycles.ts` in patterns.json (#8). Fix to `server/src/cycles/engine.ts` / `lifecycle.ts`.
5. **Do not reuse the old report SVGs** as "as built" (#15). They still show Demo functions that no longer exist.
6. **Database is Lightsail managed PostgreSQL, not RDS** (the brief said RDS). Only the CA-bundle comment mentions RDS. The deck must say Lightsail.
7. **Deployment has no worker container, queue or load balancer**: the pipeline and system-demo narration must not imply one. Statechart events come from one in-process scheduler tick.
8. **Release status is unverified.** Show it only as "declared in Terraform", with a dated check by someone who can query AWS.
9. **PUML layout is draft**: d3 is wide (2105 px, check 1280×720), p1 places GitHub Actions at the cloud edge, and e1 should be split in two. Content is checked against code; layout is not final.
