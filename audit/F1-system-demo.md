# F1 · System demo: what the app does, environment readiness, storyboard, prep timeline

Audited Mon 26 Oct 2026 ~21:50 SGT, worktree `rewind-present-audit` = origin/dev `f6cd896` (still dev HEAD per `git ls-remote`).
Read-only: code reading and `curl` only. Tags: [verified] = seen in code or a live response; [inferred] = reasoned, not run.
Paths below are relative to the worktree. Line numbers are at `f6cd896`.

## 0. Verdict

- A real, recorded demo is feasible. Hosted dev is healthy and runs `f6cd896`.
- **Blocker 1:** a hosted film needs a short cycle. Default is 28 days; the setting exists but must be applied by Terraform plus a deploy (section 2).
- **Blocker 2:** the web-push reminder cannot be made to fire tonight (section 3, item 2). Show the opt-in only, or stage it and say so.
- **Biggest unknown:** Cognito sign-in inside the iPhone Home Screen app has never been checked on a device. Test it first.

## 1. Feature inventory (what the code really does)

| Area | What exists | Best shown on |
|---|---|---|
| Sign-in | Web/PWA: primary button "Continue with Cognito" (Managed Login, code+PKCE) and a small "Developer sign-in" link when the server allows both (`App.tsx:466-486`). Developer form = username (3-32 chars) + password (12+), register rate limit 5 per 15 min per source (`server/src/routes/limits.ts:53-55`). First Cognito login asks "What should we call you?" (`App.tsx:221`). Sessions: 7 days idle, 30 absolute (`server/src/auth/index.ts:29-30`). | iPhone PWA for Cognito (real redirect); laptop for Developer sign-in |
| Which env uses which | Hosted dev: both [verified `GET /api/auth/config` = `{"passwordSignIn":true,"cognito":true}`]. Local `make run`: Developer only [inferred: no `REWIND_COGNITO_*` in `scripts/run-real-local.mjs`]. Release: Cognito only, server refuses to start with password on (`server/src/config.ts:277`), but release is down (section 2). Native Expo: password only (`App.tsx:465`). | n/a |
| Groups | Create: name <=80, prompt <=160, 2-10 members, 5 creations per account per 24 h (`limits.ts:47`), 20 owned max (`real-routes.ts:662`). Switch-group menu, owner edits prompt and time zone while the cycle is collecting (`server/src/groups/settings.ts:20-30`). | either |
| Invitations | Six-letter code, "Works once · expires in 24 hours" (`src/real/settings/Invite.tsx:43`), share/copy/revoke, 10 wrong guesses per 15 min throttled (`server/src/groups/invites.ts:11-12`). Reusing a code shows "This invitation has already been used." (`real-routes.ts:606`). `/invite` web link survives sign-in (`App.tsx:712`). | phone for Share sheet; laptop to enter code |
| Capture: photo | 4 looks: Disposable Flash, Compact Digital (default), 8mm, VHS (`src/domain/video.ts:18-30`). A photo = 1 moment and a 3 s film segment (`camera-ui.tsx:35`). JPEG/PNG <=10 MiB (`CameraCaptureScreen.tsx:340-346`). | **iPhone** |
| Capture: video | <=15 s, sound required, trim, same 4 looks. Look is re-encoded **on the device in real time**, so a 10 s clip takes about 10 s to submit (`src/capture/retro-browser.ts:14,23`). Server re-probes (<=50 MiB, `server/src/media/clip-policy.ts:6-7`). | **iPhone** |
| File instead of camera | Only offered when the camera is unsupported, denied or unavailable (`CameraCaptureScreen.tsx:552-620`, `VideoAccessCard.tsx:35-86`). Accepts JPEG/PNG and **MP4 with audio** (`src/capture/platform.ts:842-900`); labelled "Chosen from a file". | laptop with camera blocked |
| Allowance and ledger | 5 moments and 30 s per 7-day window; one delete-and-retake per window; "Your moments" shows sealed entries (when, length, never content) (`src/real/Moments.tsx`, `home-model.ts:48`). On a short cycle the whole cycle is one window (`home-model.ts:48-60`). | either |
| Cycles | Server default 28 days (`server/src/config.ts:14`, `groups/real.ts:11`). Scheduler scans every 1 s (`cycles/scheduler.ts:8`); at the end it closes the cycle, queues the film job and opens a successor of the same length (`cycles/lifecycle.ts:276-290`). | laptop (countdown flip) |
| Film | ffmpeg: 720x1280, letterboxed, loudnorm -16 LUFS (`server/src/ffmpeg.ts:492,516`). Waits for all clips to finish processing. One clip -> borrows an older clip as filler; zero clips -> `inputPaths.length === 0` throws (`jobs/compilation.ts:305-329`, `ffmpeg.ts:475`). | n/a |
| Premiere and Archive | Home card "Your film is here · Premiere · N h left" for 24 h (`lifecycle.ts:38`), then "Earlier films". Player: segment bar, tap left/right to skip moments. End screen: Talk about it in Chat, Replay, **Save film**, **Save your own moments**, Report, Remove my moment (`src/real/Film.tsx:458-525`). | iPhone to watch; **laptop to Save** (browser download) |
| Chat | Messages <=2000 chars, one-level replies, one reaction (sparkle), live over SSE with reconnect, unread badges, report/block (`src/chat/RealAccountChatScreen.tsx`). | two devices side by side |
| Reminders | Opt-in toggle, **web push only**, one weekly push, Sunday 19:00 group time zone, snooze 7 days. On iPhone only the Home Screen app can subscribe (`src/reminders/push-platform.ts:46-47`, `ReminderBlock.tsx`). | iPhone PWA, hosted HTTPS |
| PWA | `public/manifest.json`, `sw.js`, `offline.html`, apple startup images; max column width 520 so a desktop window looks like a phone (`src/ui/tokens.ts:93`). | iPhone |
| Safety/legal | Report and block (members, messages, moments), privacy/support/terms pages (`/privacy.html` = 200). | laptop |
| Account deletion | Cognito account: type DELETE, deletes the Cognito user too; Developer account: password. Owned groups pass to the next-joined member (`DeleteAccount.tsx`, `server/src/routes/auth-routes.ts:335-370`). | laptop, throwaway account only |
| Version label | Footer shows `dev-f6cd896` on hosted dev and local (`App.tsx:845`). Use it for the "date and commit" label the feedback asks for. | any |

## 2. Environment readiness

| Check (26 Oct ~21:50 SGT) | Result |
|---|---|
| Hosted dev `https://d2m6kz76y4kuvm.cloudfront.net/` (`README.md:16`) | 200 [verified] |
| `/api/health` | `ok:true, ready:true, database:"postgresql", ffmpegConfigured:true, migration 31, missingMigrationKeys:[]` [verified] |
| Deployed build | JS bundle contains `dev-f6cd896` [verified], so hosted dev = current dev HEAD |
| Cognito Managed Login | `/api/auth/cognito/start` -> 302 to `rewind-dev-330599756236.auth.ap-southeast-1.amazoncognito.com`, login page 200 [verified]. Self sign-up is on (`infra/terraform/media/cognito.tf:24`, email code via Cognito's default sender). |
| `/manifest.json`, `/sw.js`, `/privacy.html` | 200 each [verified] |
| Release (CloudFront `d2r0xzy7vz590e`, from memory notes; the repo does not record it) | 504 on `/` and `/api/health` [verified]. Do not plan on release. |

**Cycle length on hosted dev.** I could not read the live setting (it lives in a secret S3 object). Code says 28 days unless `REWIND_REAL_CYCLE_MINUTES` is set [verified `config.ts:204-210`]. Allowed 1 to 40320 minutes. Applied at group creation only (`real-routes.ts:682`); successor cycles copy the previous length (`lifecycle.ts:280`), so an old 28-day group never shrinks.

**How to get a film within an hour tonight (supported route, no code change):**
1. `infra/terraform/media` (the dev root) takes `extra_hosted_settings` (`variables.tf:33`, written into `_config/dev.env` at `main.tf:210-231`). Apply with `rewind-terraform-apply`: `-var 'extra_hosted_settings=["REWIND_REAL_CYCLE_MINUTES=60"]'`. A `backend.hcl` already exists in the stale `rewind-app/infra/terraform/media`; all other vars have defaults. The plan should touch only that S3 object.
2. `gh workflow run deploy-dev.yml --ref dev`. It has `workflow_dispatch` (`deploy-dev.yml:29`), streams the object to the host (`release-host.sh configure`, key already allowlisted at line 44) and restarts the containers. `deploy/compose.yaml:42` forwards the variable.
3. **Revert gotcha:** `configure` only adds or overwrites keys, it never deletes (`release-host.sh:81-90`). After the talk set it back to `40320`, not remove it.
4. Create the demo group **after** the deploy, then check Home: the countdown should read about 1 hour.
5. Do not edit `rewind.env` by hand: the next deploy refuses on a digest mismatch (`release-host.sh:73-75`).
- A deploy restarts the server and clears in-memory state (media tokens, rate limits). Freeze merges to `dev` from step 2 until after the talk.
- Compile time on the hosted micro host is unmeasured [inferred: under a few minutes for under 10 short clips; the local benchmark did 25 clips in 9 s].

**`make run-real` (fallback).** `scripts/run-real-local.mjs`: builds the server, starts it with SQLite in `.local-data/real` and disk media, starts Expo web on 8081, and serves everything on `http://localhost:8090` through a same-origin proxy bound to 127.0.0.1. `REWIND_REAL_CYCLE_MINUTES` defaults to 10 (line 29; override with the env var, minimum 1). Developer sign-in only. Ports 8090/8081/8787 are free now [verified `lsof`].
- Works locally: capture on a desktop browser (localhost counts as secure), looks, upload, ledger, chat, cycle close, film, Archive, Save film, outsider denial.
- Does not work: iPhone (HTTP on 127.0.0.1), PWA install, Cognito, S3, **web push** (no VAPID keys set, so `reminders_unavailable` 503, `real-routes.ts:155-160`).
- Host has Node v26.3.1 and ffmpeg 9.0.2; `.nvmrc` pins 22.23.3, so use nvm to match [inferred risk].

**Accounts and devices for a convincing demo**
- 3 accounts: Owner (Cognito, iPhone Home Screen app), Friend (member), Outsider (never invited, separate browser profile).
- Devices: owner's iPhone (install, camera, push prompt), laptop (friend and outsider, recording), ideally a second phone for the friend; a laptop Chrome window works.
- Cognito users need real inboxes for the sign-up code (pre-create tonight). Developer accounts need only a 12+ character password, and are the quick way to make the outsider.
- Three hosted-only things need HTTPS: iPhone camera, PWA install, push. All are on the CloudFront URL.

## 3. Problems that would block or weaken the demo (ranked)

1. **No film without compressing the cycle.** See section 2. Needs an owner go-ahead for the Terraform apply and one deploy. Fallback after two failed attempts: run the cycle and film scenes on `make run-real` (10-minute cycles) and say so.
2. **The reminder push cannot fire in time.** The only push is the weekly reminder, Sunday 19:00 in the group's zone (`server/src/reminders/schedule.ts:55-69`, only kind `weekly-reminder`, `outbox.ts:26-28`). It is queued only if the opt-in, membership and destination were all created **before** that Sunday instant and it is within 24 h after it (`outbox.ts:337-347`). The Sunday that matters (25 Oct, any zone in the picker, `TimeZoneScreen.tsx:18-31`) is already past, so nothing created now qualifies. Next natural delivery: Sun 1 Nov. [verified from code]. Options: (a) show the opt-in plus the iOS permission prompt and say delivery is weekly; (b) check whether the owner's phone already holds a real Rewind banner from Sun 25 Oct 19:00 SGT (long shot); (c) stage a push by backdating rows in the **local** SQLite plus own VAPID keys, labelled "staged" on screen. Do not edit the hosted PostgreSQL without an explicit owner decision.
3. **Cognito inside the iPhone Home Screen app is unverified.** iOS keeps separate storage for the installed app, so the owner must sign in inside it. The earlier note says the owner's iPhone PWA Cognito check was still pending. Test first tonight; fallback is Developer sign-in in the PWA and a laptop recording of Cognito. [inferred risk]
4. **Owner media has format limits.** File route needs MP4 H.264+AAC with audio, <=15 s, <=50 MiB; photos JPEG/PNG <=10 MiB. iPhone `.mov`/HEIC are rejected (`platform.ts:867-900`, `CameraCaptureScreen.tsx:340`). Convert with `ffmpeg -i in.mov -t 14.5 -c:v libx264 -pix_fmt yuv420p -c:a aac -movflags +faststart out.mp4`. Per member the film budget is 30 s total (a photo costs 3 s).
5. **On-screen copy contradicts a compressed cycle.** "The first cycle lasts four weeks and starts now." (`src/real/GroupFlows.tsx:200`), the welcome tagline "every 4 weeks" (`App.tsx:558`) and "Week N of 4" (`Home.tsx:90`; it scales to the cycle, so it advances inside the hour). Caption the footage "demo build: 60-minute cycle".
6. **Other merges to `dev` redeploy hosted dev** and will interrupt a take (`deploy-dev.yml`, `on: push: dev`). Docs-only changes skip the deploy.
7. **Empty successor cycles.** After the demo cycle closes, a new empty one starts and closes each hour. Its film job fails and will read "Taking a little longer" once the 24 h premiere ends (the premiere card takes precedence before that). Harmless for 14:30 [inferred].
8. **State unknowns on hosted dev:** existing Cognito users, leftover groups, whether VAPID keys exist (needs a signed-in call to `/api/real/reminders/config`), and whether the planned account wipe ran. Group creation is limited to 5 per account per 24 h (in-memory, reset by each deploy).
9. **Phone-only behaviours not proven:** `Save film` on the iPhone PWA, MP4 video recording on Home Screen Safari, and camera/screen-lock interruption while a clip "develops". Do Save on the laptop; keep the iPhone awake while submitting.
10. Playwright fake-camera route (section 5) is untested; Playwright's bundled Chromium may lack an H.264 MediaRecorder, so use installed Chrome or the file route.

## 4. Storyboard (target about 13:30; Section 5 allows 12-15)

R = recorded real footage, edited. Everything is on hosted dev `dev-f6cd896`. Narrate live over the video so a lecturer interruption can pause it.

| # | Scene (use case) | Device / account | On screen | Time | R/L |
|---|---|---|---|---|---|
| 0 | Frame | slide | Three accounts, 60-minute demo cycle, what is real | 0:20 | R |
| 1 | Install the PWA (UC14) | iPhone / Owner | Safari -> Share -> Add to Home Screen -> open standalone | 0:50 | R |
| 2 | Sign in (UC01) | iPhone PWA / Owner | Continue with Cognito -> Managed Login -> back -> display name; flash "Developer sign-in is dev-only" | 1:00 | R |
| 3 | Create group (UC02, UC09) | iPhone / Owner | New group, prompt, limit, Home with countdown; Settings prompt and time zone | 0:50 | R |
| 4 | Invite a friend (UC03) | iPhone then laptop / Owner, Friend | Code "works once, 24 h", share; friend signs in, "Have an invite?", Accept; Members shows two | 1:30 | R |
| 5 | Photo (UC05) | iPhone / Owner | Shutter, pick a look, review, submit; sealed in Your moments | 1:00 | R |
| 6 | Video + allowance (UC04, UC06) | iPhone / Owner; laptop / Friend | 8-10 s clip, trim, submit (cut the wait); ledger shows "2 of 5, 11 of 30 s"; Friend adds real files; optional delete-and-retake | 2:00 | R |
| 7 | Chat (UC11) | laptop + iPhone | Friend sends, Owner replies and reacts, no refresh | 0:45 | R |
| 8 | Reminder opt-in (UC10) | iPhone PWA / Owner | Settings toggle, "Get the Sunday reminder?", iOS prompt, "Sundays at 7 PM"; say delivery is weekly | 0:40 | R |
| 9 | Cycle closes itself (UC07) | laptop / Owner | Home countdown to 0 -> "Your film is developing" -> "Your film is here" | 0:50 | R |
| 10 | Watch the film (UC08, UC12) | iPhone / Owner | Premiere card, Watch, tap through moments, real sound, end screen | 1:30 | R |
| 11 | Archive and Save (UC12, UC13) | laptop / Owner | Archive, Save film downloads the MP4, open it | 0:50 | R, tail L |
| 12 | Outsider denied (security) | laptop, third profile / Outsider | Reuse the spent code -> "already been used"; no group in app; copied `/media/access/<token>` -> denied | 1:00 | R |
| 13 | Close | slide | What was real, one honest limit (weekly push, single host) | 0:30 | R |

Scene 11 can end with 20-30 s live: open the hosted Archive in a browser tab. Keep that tab ready for Q&A.

## 5. Prep timeline (SGT; now Mon 21:55)

**Mon 26 Oct**
- 22:00 Owner decision (5 min): approve the 60-minute setting and the Terraform apply plus one deploy. Tell other agents to stop merging to `dev`.
- 22:05-22:40 Agent (automatable): terraform plan/apply (media root), `gh workflow run deploy-dev.yml --ref dev`, watch to green, re-check `/api/health` and `dev-f6cd896`. Two failed tries -> switch to `make run-real` and tell the owner.
- 22:05-22:40 Owner, in parallel: convert media (section 3 item 4); sign up Owner and Friend in Cognito; plan screen recording (iPhone Control Center recording with mic, QuickTime on the Mac for the laptop).
- 22:40-23:00 Owner, **physical iPhone**: Add to Home Screen, Cognito sign-in in the PWA, camera and mic prompts, one photo and one video into a rehearsal group. Also confirms the cycle length on Home. Its film (about 23:55) is insurance footage.
- 23:00 Go/no-go on Cognito-in-PWA (fallback in section 3 item 3).
- 23:10 T0: create the take group. Cycle ends 00:10.
- 23:10-00:05 Shoot scenes 3-8. Keep a wall-clock log of each scene start.
- 00:05-00:25 Start the laptop recording at 00:05, keep Home open through 00:10, shoot scene 10 once the premiere appears (about 00:15).
- 00:25-00:50 Scenes 11-12. AirDrop and copy all raw footage to two places. Stop by 01:00.
- Automatable while the owner films (Playwright; Chromium, WebKit and Firefox are installed): friend and outsider laptop sessions using known test ids (`cognito-sign-in`, `developer-sign-in`, `real-group-menu-join`, `real-archive-play`, `real-film-save`), uploads through the `filechooser` event with the camera denied (untested), and a poller that waits for the premiere card.

**Tue 27 Oct**
- 07:30 Health check: `/api/health`, then Owner opens Archive on the phone: film plays, premiere still has hours left (published about 00:15, so it lasts to about 00:15 Wed).
- 08:00-12:00 Owner edits. Captions: date, `dev-f6cd896`, "demo cycle compressed to 60 minutes".
- 12:00-12:30 Export 1080p MP4 (13-14 min), check audio on the presenting laptop; copies on laptop, USB and phone.
- 12:30-13:30 One timed run with narration and a mid-video pause.
- 14:30 Talk starts. Section 5 begins about 14:50 if Sections 1-4 run to their 22-24 minutes [inferred].
- After the talk: set `REWIND_REAL_CYCLE_MINUTES=40320` and redeploy (section 2, item 3).

## 6. Questions for the owner

1. Approve the hosted cycle change (60 minutes) and the deploy? If not, scenes 9-11 come from `make run-real`.
2. Is a second person or phone available for the Friend account tonight?
3. Reminder: accept "opt-in only, delivery is weekly", or want a staged local push labelled as staged?
4. Should the Cognito sign-up (with email code) be shown, or only a sign-in with a pre-made account?
