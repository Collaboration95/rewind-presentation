# Stage video derivative handoff

Completed ten portrait MP4s and ten JPEG posters in `deck/clips/device/`, plus `manifest.json`. Total playback: **570.000 seconds (9:30)**. Every source interval is retained in full: no authentication, onboarding or 30-minute cycle footage was found in the inspected samples, so no temporal cuts were needed. No footage was re-filmed, replaced, retimed or newly retouched in this pass. No text or labels were added to the videos or posters.

## Files and timing

All paths below are relative to `presentation-prep/`. Video directory: `deck/clips/device/`. Each poster uses the same stem plus `-poster.jpg`.

| Video basename | Duration | Retained source interval | Output size | Poster time |
|---|---:|---|---|---:|
| 03-create-group.mp4 | 60.000 s | [0,60) | 416×776 | 35 s |
| 04-invite-and-join.mp4 | 60.000 s | [0,60) | 416×858 | 47 s |
| 05-photo-with-a-look.mp4 | 55.000 s | [0,55) | 416×776 | 28 s |
| 06-video-and-allowance.mp4 | 65.000 s | [0,65) | 416×776 | 59 s |
| 07-group-chat.mp4 | 55.000 s | [0,55) | 416×776 | 46 s |
| 08-weekly-reminder.mp4 | 50.000 s | [0,50) | 416×776 | 34 s |
| 09-cycle-ends-film-ready.mp4 | 40.000 s | [0,40) | 416×776 | 2 s |
| 10-watch-the-film.mp4 | 80.000 s | [0,80) | 416×858 | 8 s |
| 11-archive-and-save.mp4 | 55.000 s | [0,55) | 416×858 | 2 s |
| 12-outsider-denied.mp4 | 50.000 s | [0,50) | 416×776 | 35 s |

Crop coordinates refer to the 1920×1080 sources: x=752, y=124, width=416, height=776; clips 04, 10 and 11 use height=858. These remove the composited outer device outline, Dynamic Island and status bar. The taller crops preserve native share-sheet, playback scrubber and download controls. They retain some Safari chrome; further cropping would remove meaningful controls. Standard crops remove the Safari toolbar. Crop metadata, absolute paths, SHA-256 hashes and poster times are in `manifest.json`.

## Inspection and verification

Read `RESUME-BRIEF.md` and `videos/SHOTLIST.md`. Inspected source and derivative contact sheets for all ten clips. Source OCR covers every integer second across [0,duration), **570 samples**, plus **218 samples** at the first/last frame and immediately around documented production edit boundaries. No sign-in, sign-up, password/onboarding flow or 30-minute cycle text was detected. This is sampled visual/OCR inspection, not frame-by-frame semantic certification. A visible 30-second capture allowance is separate from cycle duration and remains part of the actual UI.

`inspection-manifest.json` lists every inspected timestamp and sheet. `source-ocr.json` and `boundary-ocr.json` retain text results. For each clip, `<stem>-source-overview.jpg` and `<stem>-device-contact.jpg` show source-screen and decoded-derivative screenshots at 0,5,10… seconds plus the final frame, labelled only outside images in these QA sheets. Individual screenshots are in `source-frames/`, `boundary-frames/` and `device-frames/`.

All final videos passed full-stream decoding: H.264, yuv420p, 30 fps, faststart. Original AAC tracks were copied, and decoded-audio hashes match source audio exactly. Existing silence remains silence. `validation.json` records checks. Source and `videos/demo.mp4` SHA-256 hashes before/after match; backup remains untouched.

## Provenance and outstanding concerns for parent

- Existing production notes explicitly identify authorized HTML camera/reminder reproductions. Clips 05 and the camera/review/upload/sealed portions of 06 show `127.0.0.1` in the original Safari toolbar. Clip 08 switches from hosted settings to a locally reproduced Home/banner around 28 s. Cropping removes that toolbar in these clips; it does not establish hosted capture, real hardware camera operation or delivered web-push proof. No new hosted or physical-device verification was performed.
- Existing production EDLs contain held stills and retouching: clip 03 smooths selected form fields; clip 09 begins/ends on an already cleaned premiere Home still; clip 04 uses invite/member stills; clip 11 uses a completed-download still and an editorial closing Archive still. This pass preserves the supplied exports. See production EDLs under `videos/work/cuts-a/`, `cuts-b/`, `cuts-c/` and `finalize/` for original decisions.
- Clip 04 demonstrates share actions and joined membership, not Jun entering an account or visibly submitting a join. Clip 12 enters an invitation code, not account credentials, then shows the used-code rejection and empty group state. Both remain meaningful without authentication footage.
- Premiere/Archive refer to the existing “The little things” capsule; earlier create/capture/chat footage uses “At table”. Keep the existing-completed-capsule transition clear in narration.
- Final CSS phone sizing, poster fit, muted/manual playback, Space/click controls and 1280×720 browser legibility remain parent QA. Use the intrinsic aspect ratios (416/776 or 416/858) without stretching or `object-fit: cover` that clips controls. Native source UI is only about 416 pixels wide; tiny secondary text cannot gain detail through scaling.

Writes were confined to `deck/clips/device/` and `deck/out/resume-qa/video/`. No browser, GitHub, Git mutation, AWS, app-code changes or writes to source videos were used.
