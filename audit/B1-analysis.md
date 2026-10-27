# B1 · Requirements and analysis models, critical use cases (as built at f6cd896, 20 Oct 2026)

Read-only audit of worktree `rewind-present-audit`. Paths are relative to it. Convention: a bare `file:line` was read at that line [verified]; `[inferred]` = my modelling choice or deduction; `[rendered]` = I rasterised the SVG and looked at the arrows.

## 0. Verdict
1. There is **no usable use-case/analysis/sequence set for slides today**. The SVG packages are stale and contain wrong arrows; the Mermaid set is mostly right but anchored to modules that were split on 15-20 Oct; one PlantUML use-case model exists but has no include/extend.
2. Pick the **UC01-UC14 labels** (site, owners page and report all use them) and add three real-but-unmodelled use cases (§2.2). Do not mix with the second numbering `UC-SIGN-IN…UC-INSPECT-OPERATIONS`.
3. Critical use cases: **CU-A "Contribute a photo within the weekly allowance" (UC05+UC06, shares acceptance with UC04)** and **CU-B "Close the cycle, compile, publish" (UC07+UC08)**. §4 and §5 hold the message lists for writing PlantUML; B2 already has statecharts `s1-cycle`/`s2-job`/`s3-intent` that match my reading.
4. Every existing sequence SVG I rasterised (5 of 44 pairs) has at least one mis-routed arrow or a missing S3 lifeline (§6). Treat all 88 as unverified.

## 1. Inventory of existing models
| Set | Where | Format | Baseline | State |
|---|---|---|---|---|
| Report packages ACCESS/CAPTURE/CYCLE/PARTICIPATION/ARCHIVE: 14 UC class pairs, 44 sequence pairs, 20 before/after pattern views | `doc/planning/report/packages/*/diagrams/*.svg` (137 + 4 overview SVGs = 141) | Generated/hand-built SVG cards. No PlantUML/Mermaid source anywhere. Not UML: no stereotypes, no typed attributes, no multiplicities, no message numbers, no alt/opt frames (alt is a text box) | `fc2b8c8` (3 Oct, `capture/use-cases.md:3`); README says assembly `25d5d83` | Stale. The site itself says "need a separate artwork refresh" (`docs/site/content/analysis-design.json`, section `class-model-register`) |
| Overall use-case model | `doc/planning/report/diagrams/use-cases-overall.svg` | SVG; only 4 association arrows (Owner/member→UC01, Invitee→UC03, Clock→UC07, Client platform→UC14); no include/extend/generalisation; no Cognito/S3/push actors; footer "Future OIDC provider and pre-upload retro remain required" [rendered] | n/a | Stale and incomplete |
| Newer models | `docs/design/{identity,capture,lifecycle,interactions,playback,client-installation,safety,operations}.md` | **Mermaid**: 87 blocks (28 class, 59 sequence), BCE-style analysis (A-*) and module/type design (D-*). Zero state diagrams | `40ebeb5` (15 Oct); commit `0c68955` (20 Oct) only re-pointed anchors | Best base. Real function names verified. Module attributions stale (§6.2) |
| UML use-case model | `doc/planning/current-product-baseline.md` ("UML use-case map") | **PlantUML**, 17 use cases, 9 actors, `Member --|> Account`, `Owner --|> Member`, no include/extend | `40ebeb5` | The only PlantUML in the repo; closest to the FlickPond look |
| ER | `docs/domain/database-design.md` (3 Mermaid ER) | Mermaid; honest about schema-vs-policy cardinality | `40ebeb5` | Accurate for CAPTURE/CYCLE (checked against `server/migrations/sqlite-baseline.sql`). B2 has `e1-er` |
| Site | `docs/site/content/{product,analysis-design,owners}.json` | JSON text + flow/hub visuals; links to the SVGs | 20 Oct | `product.json` use-case table is current and honest (UC01, UC10 "Changed"; two additions "not yet modelled") |

**Two competing numberings.** UC01-UC14 (report, site, owners) vs 17 semantic IDs (`UC-CONTRIBUTE`…, baseline doc) vs local IDs inside each `docs/design` file (UC-1..5, UC-01..05 collide). One slide, one scheme. Operator is an actor in the baseline PlantUML but "a stakeholder, not an in-app actor" in `product.json` (actors section): drop it from the main diagram.

## 2. As-built use-case model
### 2.1 Actors
| Actor | Kind | Evidence |
|---|---|---|
| Account holder (signed in) | primary | `real_accounts`; `validateRealSession` `server/src/auth/index.ts:462` |
| Member --\|> Account holder | primary | `real_group_memberships` (account, group, profile, role) |
| Owner --\|> Member | primary | `role CHECK IN ('owner','member')` (baseline sql:244-253); owner-only `handleCreateInvite` `real-routes.ts:716` |
| Invitee | role of Account holder not yet in group | `handleAcceptInvite` `real-routes.ts:561`. Fold into Account holder (baseline does) |
| Cycle clock (timer, internal) | «system» | 1 s loop `scheduler.ts:8,114-163`, started in `cli.ts:671`; reminder loop 60 s `reminders/loop.ts:4` |
| Amazon Cognito | «system» external | `auth/cognito.ts`; sign-in `routes/auth-routes.ts:50,74`; account delete calls `cognito.deleteUser` (`auth-routes.ts:343-349`) |
| Amazon S3 | «system» external, hosted only | `media/s3-store.ts:55`; presigned PUT `media/runtime-store.ts:213`; disk locally |
| Web push service | «system» external | `reminders/providers.ts:194`; `public/sw.js:167` |
Do not draw: media worker/FFmpeg (internal, not an actor); Browser/OS (the camera is a boundary class `CameraPlatform`, not a use-case actor) [inferred]; Operator (no UI; `/admin` removed).

### 2.2 Use cases (all exist in code)
| UC | As-built name | Anchor (route / screen) | Change vs old models |
|---|---|---|---|
| UC01 | Sign in and out (Cognito Managed Login; Developer sign-in on local/dev) | `auth-routes.ts:50,74,160,215,280,395`; `App.tsx:484`; `src/auth/RealAccountProvider.tsx:123` | **Renamed/changed**: SVG/`access/use-cases.md` say "local password, OIDC = Sprint 3 target" |
| UC02 | Create and select a group | `createRealGroup` `groups/real.ts:43`; `real-routes.ts:405,412,635`; `GroupFlows.tsx:125` | same |
| UC03 | Issue, revoke, accept invitation | `groups/invites.ts:125,189,214`; `real-routes.ts:561,701,716`; `GroupFlows.tsx:34`; `settings/Invite.tsx:10` | same |
| UC04 | Record, trim, submit video | `VideoCaptureScreen.tsx`; `clip-uploader.ts:114` | looks now 4 retro looks + client grading (§6.1) |
| UC05 | Contribute a photo | `CameraCaptureScreen.tsx:92,337`; `groups/photo-submit.ts:33` | same |
| UC06 | Enforce allowance, one correction | `contributions/index.ts:146,225`; `ledger.ts:525` | same |
| UC07 | Close cycle, open successor | `cycles/lifecycle.ts:312,276` | same |
| UC08 | Compile, publish, premiere, archive | `jobs/compilation.ts:410,501,785`; `lifecycle.ts:216` | same |
| UC09 | Owner prompt and time zone | `real-routes.ts:291`; `groups/settings.ts:5`; `settings/PromptScreen.tsx:59` | same |
| UC10 | Reminder preference, web-push delivery | `settings/ReminderBlock.tsx:42`; `reminders/outbox.ts:443`; `loop.ts:12` | **Changed**: web push only (`createExpoReminderProvider` `providers.ts:122` still exists but paused); recurring loop now in server |
| UC11 | Private chat | `chat-routes.ts:514-529`; `chat/index.ts:347,498`; `RealAccountChatScreen.tsx:65` | same |
| UC12 | Premiere and Archive playback | `archive-routes.ts:83,144,30`; `Film.tsx:53`; `Archive.tsx:18` | same |
| UC13 | Download clip / film | `archive/archive-download.ts:260`; `/media/access` purpose `download` | same |
| UC14 | Install, update, open invite link | `public/sw.js`, `manifest.json`; `invites/deep-links.ts:51,107` | web/PWA only |
| **UC15 new** | Report, block, remove a moment (owner) | `real-routes.ts:434,500,469`; `groups/safety.ts:9,211,81` | not in any UC01-14 model |
| **UC16 new** | Delete own account | `auth-routes.ts:322`; `auth/deletion.ts:26` | not modelled |
| Dropped | synthetic Demo (code removed in `620c694`), `/admin`, Expo push expansion | | ACCESS "problem" SVGs still show a Demo adapter |

### 2.3 Relationships to draw (keep ≤6 on the slide)
- Generalisation [verified]: Owner→Member→Account holder; "Sign in with Cognito" and "Developer sign-in" specialise UC01 (`SignInMethod = 'cognito'|'password'` `auth/index.ts:75`; routes `auth-routes.ts:419-423`); UC15 specialised into report / block / remove (3 routes).
- «include» Reserve allowance in UC04 and UC05: `reserveContributionAllowance` runs inside every acceptance transaction (`upload-intents.ts:703`, `media/clip-upload.ts:455`). Needs UC06 split into **UC06a Reserve allowance** (included) and **UC06b Correct one contribution** [inferred: current UC06 mixes both, so one bubble cannot be both included and extending].
- «extend» UC06b → UC05/UC04, extension point "replacement target": `replacesContributionId` → `linkContributionReplacement` in the same transaction (`upload-intents.ts:762-772`) [verified code, extend is a modelling choice].
- «extend» "Choose a video file" → UC04 (web fallback `pickVideoFile` `capture/contracts.ts`; `platform.ts:467`); «extend» "Append one archived clip" → UC08 (condition: exactly 1 current clip, `compilation.ts:37,305-328`).
- «include» "Obtain media access grant" in UC12 and UC13: `protectedAssetPath` `routes/media-access.ts:126` called from `handlePremiere` and `handleArchive`, consumed by `handleMediaAccess` `archive-routes.ts:30`.
- Associations: Cognito–UC01/UC16; S3–UC04/05/08/12/13; Web push–UC10; Clock–UC07 (+UC08 publish/archive steps, UC10 scan). Boundary label "Rewind (web/PWA client + Node server)". Authentication is a precondition, not an include (matches baseline doc).

## 3. Why these two
| Criterion | CU-A Contribute (UC05+06) | CU-B Release (UC07+08) |
|---|---|---|
| Carries the stated design tension (atomic quota, idempotent retries) | Yes: one writer transaction `upload-intents.ts:694-785` | Yes: transition + job + successor in one transaction `lifecycle.ts:324-403` |
| Secondary actors visible | S3 (direct PUT), camera | Clock, S3, FFmpeg |
| Demonstrable live | Yes on hosted dev (direct S3) or `make run-real` (staged path) | Only with 10-min cycles (`scripts/run-real-local.mjs:29`) |
| Statechart material | intent: open→pinned→completed; ledger states | cycle + film job (B2 `s1-cycle`, `s2-job`) |
Suggested split of the 5 minutes: ~3 min CU-A (BCE class + sequence), ~2 min CU-B (statechart + the three guard sentences). Video (UC04) is a variant of CU-A, not a second diagram.

## 4. CU-A · Contribute a photo within the weekly allowance
**Actors**: Member; S3 (secondary, hosted only). **Pre**: signed in, selected group, accepted membership, current cycle collecting (`cyclePhase` `cycles/engine.ts:65`), photo previewed (`StillImageCaptureSession` `still-image-session.ts:24`), allowance ≥1 item and ≥3 s (UI disables shutter below 3 s: `CameraCaptureScreen.tsx` `photoBlocked`). **Post**: one `contributions` row + one clip `media_jobs` row; quota window +1 item/+3 s; job reaches `ready` (client word "sealed", `ledger.ts:31-38`); no playable media is exposed.
**Main flow**: member taps submit → look applied in browser (web) → client asks server for an upload intent → PUT bytes straight to S3 → client completes the intent → server verifies bytes, then accepts in one transaction → client asks server to process → clip becomes `ready` → ledger shows sealed.
**Alternatives/exceptions** (all with codes in `routes/real-routes.ts:195-224`): A1 local/disk: no intent, `POST /contributions/upload/source` then `/contributions/upload` (`contribution-routes.ts:43,235` → `createClipUpload` `clip-upload.ts:293`); A2 quota used up → `quota_exceeded` 409, nothing written, rollback; A3 cycle ended mid-flow → `closed_cycle`; A4 PUT response lost → `reconcileUploadIntent` `upload-intents.ts:511` (list ≤8 versions, HEAD+hash each; exactly one match or fail closed, never "latest"); A5 completion response lost → complete/status replay returns the same receipt (`:629,:699`); A6 same key, different payload → `idempotency_conflict` (`:405`); A7 bytes differ from declared (type/size/probe) → `invalid_media` (`:668-691`); A8 processing fails → job `failed`, retry by client or worker tick (≤3 automatic attempts, `compilation.ts:332`); A9 correction: `DELETE /contributions/:id` (`contribution-routes.ts:453` → `deleteContribution` `contributions/index.ts:225`: one deletion per window `deletions_used < 1` `:308`, tombstone, quota restored), next submit carries `replacesContributionId`; A10 intent older than 15 min → `expired` (`UPLOAD_INTENT_TTL_MS` `:41`).

### 4.1 BCE analysis classes → design element (draw only the right column's kinds)
| Analysis class | Stereotype | Real design element (kind) |
|---|---|---|
| CapturePage | «boundary» (Member) | `CameraCaptureScreen` `src/capture/CameraCaptureScreen.tsx:92` (React component), mounted by `GroupCaptureView` `src/groups/GroupCaptureView.tsx:11` |
| CameraInterface | «boundary» | `CameraPlatform` `capture/contracts.ts:101` (interface); sole implementor `ExpoCameraPlatform` `platform.ts:462` (class, has a web branch) |
| ObjectStorageInterface | «boundary» (S3) | `MediaStore` `server/src/media/store.ts:29` (interface) + `UploadIntentTransport` `upload-intents.ts:53` (interface, implemented as a closure at `runtime-store.ts:213`); class `PrivateS3MediaStore` `s3-store.ts:55` |
| SubmitContribution (client control) | «control» | `submitPhotoContribution` `groups/photo-submit.ts:33` and `createRealAccountVideoRuntimeClient` `capture/real-account-video-runtime.ts:46` and `createDirectTransferClient` `capture/direct-transfer.ts:296`: three **«module»** s, not classes. (Video: class `ClipUploadSession` `clip-uploader.ts:114`.) |
| AcceptContribution (server control, one per UC) | «control» | `completeUploadIntent` `upload-intents.ts:606` («module» function; local variant `createClipUpload` `clip-upload.ts:293`) |
| AllowancePolicy | «control» | `reserveContributionAllowance` `contributions/index.ts:146` («module» function) |
| ProcessClip | «control» | `processClipJob` `jobs/clip.ts:374` → `processStoredClip` `:649`; `ffmpeg.ts` «module» is the FFmpeg boundary (`processPhotoWithFfmpeg` `:308`) |
| Member / Cycle / Allowance / UploadIntent / Contribution / ClipJob | «entity» | tables below |

### 4.2 Entities (PostgreSQL baseline types; SQLite stores the same as TEXT/INTEGER/REAL; timestamps are ISO-8601 text)
- **Cycle** (`cycles`): id: text «PK»; group_id: text «FK»; starts_at, ends_at: iso; status: {collecting, revealing, archived}; max_count: int ≤5; max_seconds: int ≤30; count_used: int; seconds_used: real; release_status: {unpublished, published}; release_published_at: iso?; previous_cycle_id: text? (unique partial index `cycles_previous_cycle_idx`, baseline sql:431).
- **ContributionQuotaWindow** (`contribution_quota_windows`): id; cycle_id; member_id; window_start_at, window_end_at: iso; max_count ≤5; max_seconds ≤30; count_used ≥0; seconds_used: real ≥0; deletions_used: int 0..1; UNIQUE(cycle, member, window_start).
- **UploadIntent** (`upload_intents`): id; group_id; profile_id; cycle_id; idempotency_hash; request_hash; state: {open, pinned, completed, expired}; pinned_ref: text? (S3 version); reserved_seconds: real (0,15]; contribution_id: text? UNIQUE; job_id: text? UNIQUE; expires_at: iso; UNIQUE(environment, group, profile, idempotency_hash).
- **Contribution** (`contributions`): id; cycle_id; member_id; media_job_id; duration_seconds: real; created_at; quota_window_start_at; deleted_at: iso?; replaced_by_contribution_id: text? (self FK); removed_at: iso?.
- **MediaJob** (`media_jobs`): id; group_id; contribution_id: text? (clip); cycle_id: text? (film); kind: {clip, film, download}; status: pending|processing|ready|failed|deleted; media_type: {video, photo}; mode: text; attempt_count, claim_generation: int ≥0; source_path: text? (S3 ref); output_sha256: text?; output_bytes: int?; output_verified_at: iso?.
- Multiplicities (policy; schema permits wider, see `docs/domain/database-design.md`): Group 1—1..* Cycle; Cycle 0..1—0..1 Cycle (successor); Cycle 1—0..* Contribution; Member 1—0..* Contribution; Cycle 1—0..* Window; Member 1—0..* Window (≤4 per 28-day cycle); UploadIntent 0..1—0..1 Contribution; Contribution 1—1 clip MediaJob; Contribution 0..1—0..1 Contribution (replacement).

### 4.3 Design sequence (numbered; hosted/direct path). Lifelines: Member · `:CameraCaptureScreen` «component» · `real-account-video-runtime.ts` «module» (+ `direct-transfer.ts`) · `real-routes.ts` «module» · `upload-intents.ts` «module» · `:RewindDatabase` · `S3` «system» · `jobs/clip.ts` «module» (+FFmpeg).
| # | From → To | Message | Source |
|---|---|---|---|
| 0 | UI → server (before capture opens) | `GET /real/media/config?uploadProtocol=2` → `directTransfer = backend==='s3'`; picks direct vs staged | `use-group-capture.ts:57-77`; `real-routes.ts:76-88` |
| 1 | Member → Screen | tap submit → `submitPhoto()` | `CameraCaptureScreen.tsx:337` |
| 2 | Screen → Screen | `retainForUpload()`; read bytes; web: `applyRetroLookToPhoto()` (`clientProcessed=true`) | `:358-392`; `retro-browser.ts:119` |
| 3 | Screen → runtime | `submitPhotoContribution(...)` via `GroupCaptureView` callback | `GroupCaptureView.tsx:46`; `photo-submit.ts:33` |
| 4 | runtime → runtime | `stagePhotoSource()` (direct: keeps bytes in memory, returns `direct-transfer://…`) | `real-account-video-runtime.ts:151,75-93` |
| 5 | runtime → direct-transfer | `uploadClip({mediaType:'photo', durationSeconds:3, mode, clientProcessed, replacesContributionId?})` → `transferContribution()` | `photo-submit.ts:55-70`; `runtime:166,174`; `direct-transfer.ts:340` |
| 6 | direct-transfer → local | SHA-256, save `Checkpoint` | `direct-transfer.ts:553-612` |
| 7 | direct-transfer → routes | `POST /real/groups/:g/upload-intents` | `:621`; route `real-routes.ts:767-771`, `handleUploadIntent:179` |
| 8 | routes → upload-intents | `requestUploadIntent()`: `normalize` → txn: `authorize`, existing-key lookup, `collecting`, `checkQuota` (held intents count), INSERT `upload_intents` state `open`, expiry = min(+15 min, cycle end, window end) | `real-routes.ts:277`; `upload-intents.ts:385,258,201,221,323,438` |
| 9 | upload-intents → S3-adapter | `transport.signPut()` → presigned PUT (tag `rewind-media-class=incoming`); re-authorize; return `{intent, upload}` | `:465-487`; `runtime-store.ts:213,231` |
| 10 | direct-transfer → local | persist `putStarted=true` **before** sending | `direct-transfer.ts:683-684` |
| 11 | direct-transfer → **S3** | `PUT` bytes (no app credentials) ← `x-amz-version-id`; persist `versionId`. **Bytes do not touch the API.** | `:688-716` |
| alt | lost PUT reply | `GET intent` then `POST …/reconcile`; server lists ≤8 versions, HEAD + hash each, exactly one match else fail closed | `direct-transfer.ts:501-521,720-738`; `upload-intents.ts:511-604` |
| 12 | direct-transfer → routes | `POST …/upload-intents/:id/complete {versionId}` | `direct-transfer.ts:752`; `real-routes.ts:268` |
| 13 | upload-intents → DB | txn 1: CAS `open→pinned` (`WHERE state='open' AND pinned_ref IS NULL`) | `upload-intents.ts:606,633-639` |
| 14 | upload-intents → S3, FFmpeg | `materializeStoredMedia` (read pinned version) → `probePhotoWithFfmpeg` → compare bytes/mime/type → `validateClipUpload` | `:645-691` |
| 15 | upload-intents → DB | **txn 2 (the atomic acceptance)**: re-`authorize`, `currentIntent`, `checkQuota`; `reserveContributionAllowance` = `UPDATE contribution_quota_windows SET count_used+1, seconds_used+? WHERE count_used<max_count AND seconds_used+?<=max_seconds`; INSERT `staged_sources`, `contributions`, `media_jobs` (clip, pending); `linkContributionReplacement` if replacing; UPDATE `cycles.count_used/seconds_used`; UPDATE intent `completed`; COMMIT. Any failure → ROLLBACK, no partial rows | `:694-785`; `contributions/index.ts:146-176`; `ledger.ts:525` |
| 16 | routes → direct-transfer | `200 {intent:{state:'completed', contributionId, jobId}}` | `:788`; `direct-transfer.ts:777-784` |
| 17 | runtime → routes | `GET /contributions?groupId` → `listContributionLedger` to build receipt (state queued) | `runtime:214-216`; `contribution-routes.ts:418`; `ledger.ts:396` |
| 18 | photo-submit → routes | `processClipJob()` → `POST /contributions/jobs/:jobId/process` → `processClipJob` | `photo-submit.ts:80`; `runtime:304-306`; `contribution-routes.ts:336`; `jobs/clip.ts:374,442` |
| 19 | clip.ts → S3, FFmpeg, DB | `claimClipJob` (generation+1) → read `incoming` version → `processPhotoWithFfmpeg` (3 s MP4; skips look if `client:`) → `probeClipWithFfmpeg` → `putProcessedFile` → `finalizeStoredClip`: verify output, delete raw version, UPDATE `status='ready'` under `storedClipFence` | `clip.ts:254,649-700,603-645`; `ffmpeg.ts:35,308` |
| 20 | routes → UI | `200 {job:{status:'ready'}}` → ledger state "sealed"; UI `onProgress`; alt `409 media_processing` → poll `GET /clips/:id` ≤8×1 s | `photo-submit.ts:12-30,80-86`; `runtime:307-327` |
Also a worker tick can pick up the same pending/failed clip job (`runWorkerTick` `jobs/worker.ts:266`), so retries do not need the client. Frames: `alt` on 8 (existing key same/different request), 11 (lost reply), 15 (quota/closed/replacement conflict); `opt` on 2 (web only); `ref` for processing (18-20). Local variant of 7-16: `POST /contributions/upload/source` (`handleUploadSource`) then `POST /contributions/upload` (`createClipUpload`, txn `clip-upload.ts:379`, reserve `:455`).

## 5. CU-B · Close the cycle, compile the film, release it
**Actors**: Cycle clock (primary, internal); Member (consumer); S3 and FFmpeg (secondary). **Pre**: group has a collecting cycle. **Post**: old cycle `revealing`, successor `collecting` and current, one film job; later `release_status='published'`, then `archived` 24 h after `release_published_at` (`PREMIERE_DURATION_MS` `lifecycle.ts:38`). **Intake closes at `ends_at` even before the tick persists `revealing`** (`cyclePhase` returns `ended`; every intake path requires `collecting`, e.g. `upload-intents.ts:221`).
**Alternatives**: before boundary → `waiting_for_boundary` (`lifecycle.ts:333-339`); duplicate tick/restart → same successor, job and event (unique `previous_cycle_id`, `(cycle,transition)`, one film per cycle `media_jobs_one_film_per_cycle_idx` sql:440); clips still pending → `waiting_for_inputs`, no attempt spent (`compilation.ts:516-521`); input digest mismatch → fail (`:727`); FFmpeg error → `failed`, retry while attempts < 3 (`:34,544`), then "delayed" (`media-access.ts:164`); stale worker (lease 15 min `jobs/shared.ts:6`) → new generation, old one cannot publish (`:785-841`); too early/not ready publish (`lifecycle.ts:246-257`); output bytes changed before archive → stay `waiting_for_release` (`:378`).
**BCE**: «boundary» `startCycleSchedulerLoop` `scheduler.ts:114` (Clock), `FilmScreen` `Film.tsx:53` / `ArchiveScreen` `Archive.tsx:18` (Member), `MediaStore` (S3), `ffmpeg.ts` «module»; «control» `advanceCycleLifecycleWithStore` `lifecycle.ts:435` (UC07), `processCompilationJobForWorker` `compilation.ts:858` + `publishCycleReleaseWithStore` `lifecycle.ts:426` (UC08), `handlePremiere` `archive-routes.ts:83`; `MediaCapabilities` `archive/capabilities.ts:22` is a real class (`issue:25`, `resolve:43`, TTL 2 min); «entity» Cycle, Contribution, MediaJob(clip/film), `compilation_job_inputs` (job_id, clip_job_id, contribution_id, position: int; PK(job_id, clip_job_id)), `cycle_lifecycle_events` (transition: {collecting_to_revealing, revealing_to_archived, next_cycle_created}), `film_segments` (film_job_id, position, contribution_id?, start_seconds, duration_seconds: real). Film 1—0..* Input; Cycle 1—0..1 film job; Cycle 1—0..* Event.
**Design sequence** (lifelines: Clock · `scheduler.ts` · `lifecycle.ts` · `compilation.ts`/`worker.ts` · `:RewindDatabase` · S3 · `ffmpeg.ts` · later: Member · `archive-routes.ts`):
| # | Message | Source |
|---|---|---|
| 1 | every 1 s: `runCycleSchedulerTick()`; SELECT due cycles (`collecting ∧ ends_at<=now` ∨ `revealing` ∨ current `archived`) cursor-paged, limit 16 | `scheduler.ts:46-65` |
| 2 | per candidate `advanceCycleLifecycleWithStore()`; if revealing+published+24 h elapsed, verify output bytes first (outside txn) | `scheduler.ts:70`; `lifecycle.ts:435-455` |
| 3 | `advanceCycleLifecycleVerified()`: `BEGIN IMMEDIATE` (PostgreSQL emulates with one advisory lock, `ADR-0003:38`); alt not yet `ends_at` → COMMIT `waiting_for_boundary` | `lifecycle.ts:312-339` |
| 4 | UPDATE `status='revealing'`; `addEvent(collecting_to_revealing)` ON CONFLICT DO NOTHING | `:344-352,200-214` |
| 5 | `ensureCompilationJob()`: insert film job `pending` + provisional inputs (unless exists) | `:353-363`; `compilation.ts:410-455` |
| 6 | `ensureSuccessor()`: lookup by `previous_cycle_id`, else INSERT successor at old `ends_at`, same duration/quota; `UPDATE groups SET current_cycle_id … WHERE current_cycle_id = old`; COMMIT | `:276-310,364,403` |
| 7 | same tick: `publishCycleReleaseWithStore()` → `not_ready` (film not built yet) | `scheduler.ts:76-79` |
| 8 | round-robin `runWorkerTick(groupId)` → `listWorkerCandidates` → `processCompilationJobForWorker` | `scheduler.ts:84-96`; `worker.ts:153,266-290` |
| 9 | `claimCompilationJob(requireSettledInputs)`: alt clips pending → `waiting_for_inputs`; first claim `freezeSettledCompilationInputsLocked`; UPDATE `processing`, generation+1, attempt+1 (only from pending/failed); COMMIT | `compilation.ts:866-876,501-573,381` |
| 10 | materialize inputs (from S3), verify each SHA-256/size (`firstFailingInput`) | `:954-989` |
| 11 | `compileFilmWithFfmpeg()` (720×1280, loudnorm −16 LUFS, optional labelled archive filler) → `probeClipWithFfmpeg()` | `:1003-1008`; `ffmpeg.ts:469,516` |
| 12 | `putProcessedFile(…,'films')` to S3 | `:1011-1016` |
| 13 | `publishCompilationOutput()`: hash; `BEGIN IMMEDIATE`; require same `claim_generation` and same ordered input ids; UPDATE `ready` + sha256/bytes/verified_at; alt fence fails → ROLLBACK, `markCompilationFailed` | `:785-841,1036-1054` |
| 14 | later tick: `publishCycleReleaseWithStore()` → `verifyCompilationOutput` → `verifyReadyJobOutput` (hash) → txn: `revealing`, `now>=ends_at`, ready proof → UPDATE `release_status='published'`, `release_published_at=now` | `lifecycle.ts:426-434,216-263`; `stored-output.ts:111` |
| 15 | ≥24 h later: `advanceCycleLifecycleWithStore()` re-verifies → UPDATE `archived`, event `revealing_to_archived` | `:373-396` |
| 16 | Member: `GET /cycles/:id/premiere` → `requireAuthorisedMediaGroup`, `getPremiereFilm`, `premiereState`, `protectedAssetPath` → `MediaCapabilities.issue()` returns `/media/access/<token>` | `real-account-client.ts:596`; `archive-routes.ts:83-142`; `db.ts:749`; `media-access.ts:41,162,126` |
| 17 | Member: `GET /media/access/:token` → `resolve()` (session, selection) → `openVerifiedServingFile()` (hash) → `streamMp4()` | `archive-routes.ts:30-81`; `capabilities.ts:43`; `media-access.ts:199,326` |
No separate worker process is drawn: in the running server the scheduler tick calls `runWorkerTick`; `startWorkerLoop` is only the `worker` CLI command (`cli.ts:561`).

## 6. Do not show
### 6.1 Wrong or stale in the SVG packages [rendered unless noted]
- `capture/uc06-f1-design-sequence.svg`: "show allowance and queued state" is drawn from Ledger → **FFmpeg**; "process job after acceptance" is drawn **FFmpeg → UI**. Processing is requested by the client (`POST …/process`) or the worker tick, never worker → client.
- `capture/uc04-f3-design-sequence.svg`: "request intent…" arrow points back to the runtime; "PUT bytes pin version" goes to the app's contribution lifeline (bytes go to S3); "process accepted video" and "ready/failed" are reversed; **no S3 lifeline**.
- `capture/uc05-f2-design-sequence.svg`: bytes sent to the app's HTTP boundary (false in direct mode); `processPhotoWithFfmpeg()` drawn from the acceptance transaction (it runs later in `processStoredClip`); probe drawn inside the reservation step (probe runs between txn 1 and txn 2).
- `cycle/uc07-f1-design-sequence.svg`: "UPDATE current cycle id" drawn to *lifecycle events* (it is `groups.current_cycle_id`); subtitle "SQLite writer transaction" (hosted dev is PostgreSQL). `uc08-f1` arrows are acceptable but lifelines are concepts ("worker tick", "ready proof"), not functions.
- `capture/design-problem.md` and UC04/UC05 SVG: "two modes `soft-focus`/`high-contrast`, pre-upload retro is future (#365-367)". Code: four looks `disposable-flash|ccd|8mm|vhs` (`ffmpeg.ts:19`), `soft-focus`/`high-contrast` only legacy (`:21`), web grades before upload (`CameraCaptureScreen.tsx:364`).
- "CameraPlatform — browser / Expo adapters": one implementor, `ExpoCameraPlatform` (`platform.ts:462`).
- ACCESS problem SVGs: `requireSessionIdentity`, `requireAuthorisedGroup`, `authorizeSessionMember`, `authorizeMember`, `authorizeOwner`, "Demo session adapter / Shared Demo policy": none exist (grep of `src`, `server/src`, tests: 0 hits); Demo removed. ARCHIVE UC13: `BrowserDownloadAdapter`, `NativeDownloadAdapter`, `RealAccountArchiveScreen`, "Archive Facade + Media Proxy": invented (real: functions in `archive-download.ts`, `ArchiveScreen`). UC10: `PrivateReminderSubscription` not found.
- UC01 SVGs/`access/use-cases.md`: local password only, `server/src/http.ts` route, "OIDC target". `use-cases-overall.svg` footer: "OIDC and pre-upload retro remain required".
- Any "SQLite …" lifeline label for hosted flows (PostgreSQL on hosted dev); label "Database (SQLite local, PostgreSQL hosted)".
### 6.2 Mermaid set (`docs/design`): fix names before porting
- `capture.md:224` and `:286`: `RealAccountGroupExperience → CameraCaptureScreen : onSubmitPhoto` is now `GroupCaptureView.tsx:46` → `photo-submit.ts`. Participants `http.ts` (`:292,:323,:383`), `media/index.ts` (`:293,:385`), `jobs/index.ts` (`:294,:391`) are now `routes/contribution-routes.ts` / `routes/real-routes.ts` / `routes/body.ts`, `media/clip-upload.ts` + `staged-source.ts`, `jobs/clip.ts`. `http.ts` is a 235-line dispatcher.
- `lifecycle.md:238-244` (`Http` module with `premiereState`, `filterServableArchive`, `protectedAssetPath`, `openVerifiedServingFile`) → `routes/media-access.ts`; `:272,:299` `jobs/index.ts` → `jobs/compilation.ts`, `stored-output.ts`; `:371` `http.ts` → `routes/archive-routes.ts`. `jobs/index.ts` is a 7-line barrel, so 18 of 164 `#L` anchors in `docs/design` are past end of file (e.g. `lifecycle.md:407-410,486`); `src/domain/cycles.ts` no longer exists.
- Do not draw a caller for `cleanupUploadIntents` (`upload-intents.ts:798`, referenced in `capture.md` traceability): no runtime code calls it; abandoned objects expire by S3 lifecycle rule `expire-abandoned-incoming` (`infra/terraform/media/main.tf:76`) [inferred as the actual cleanup].
- `docs/design/README.md` and old Mermaid use `<<functional_module>>`; use «module».
### 6.3 Wording traps for Q&A
- "Reservation": `requestUploadIntent` only **holds** (state `open`, counted by `checkQuota`, 15 min); the counter is incremented once, in `completeUploadIntent` txn 2. `product.json` main-flows says the intent "records an expiring upload reservation", say "hold".
- "Atomic" on PostgreSQL rests on serialised writers (one advisory lock per write transaction), not row-level concurrency (`ADR-0003:38,113`).
- `contributions.duration_seconds` is `INTEGER` in the SQLite baseline but fractional values are stored (`upload-intents.ts:692`); PostgreSQL uses double precision. Draw `real`.
- Schema allows several clip jobs per contribution; policy says one (`database-design.md` note after the ERD). Draw 1—1 with "policy" in the legend.
- Stale deck: `doc/planning/report/presentation/*` (nine-slide draft at `e82dc42`, Demo route, "future OIDC/PostgreSQL") must not be reused.
