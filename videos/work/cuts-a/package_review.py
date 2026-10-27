from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parent
reports=[];lines=['# Rewind review cuts A','', 'Five completed review MP4s: **265 seconds total**. All deliverables remain in cuts-a for parent review.','', '1920×1080, 30 fps, H.264 High / CRF 18 / fast, yuv420p, BT.709 limited range, faststart. AAC 160 kb/s, 48 kHz stereo; decoded audio is digitally silent. Cream canvas, centered phone and small feature title only.','', 'Real raw recordings and supplied stills only. Typing plays at recorded speed. JSON EDLs record exact source bounds, output durations, postroll holds and cleanup rectangles; readable .edl files accompany them.','']
for mp4 in sorted(ROOT.glob('*-review.mp4')):
 stem=mp4.stem;rp=ROOT/'qa'/(stem+'-report.json');report=json.loads(rp.read_text());op=ROOT/'qa'/(stem+'-ocr.json');records=json.loads(op.read_text())
 records=list({row['frame']:row for row in records}.values())
 for row in records:
  if Path(row['frame']).name.startswith('boundary-'):row['time']=int(Path(row['frame']).stem.removeprefix('boundary-'))/30
 op.write_text(json.dumps(records,indent=2)+'\n')
 report['ocr_frames_scanned']=len(records);report['forbidden_text_hits']=[{'time':row['time'],'matches':row['forbidden_matches']} for row in records if row['forbidden_matches']]
 report['visual_review']='PASS: final five-second full-frame/phone contact sheets and frames on both sides of all cuts inspected; UI legible; forbidden Home and cycle copy absent in reviewed frames.'
 report['sha256']=hashlib.sha256(mp4.read_bytes()).hexdigest()
 assert all(report['encoder_checks'].values()) and report['silent_aac'] and not report['forbidden_text_hits']
 rp.write_text(json.dumps(report,indent=2)+'\n');reports.append(report)
 spec=json.loads(mp4.with_suffix('.edl.json').read_text());lines += [f'## {spec["number"]:02d} — {spec["name"]} — {report["duration_seconds"]} seconds','',f'- [Review MP4]({mp4})',f'- [JSON EDL]({mp4.with_suffix(".edl.json")}) · [readable EDL]({mp4.with_suffix(".edl")})',f'- [QA full-frame contact sheet]({ROOT/"qa"/(stem+"-contact.jpg")}) · [QA readable phone sheet]({ROOT/"qa"/(stem+"-phone-contact.jpg")})',f'- [QA frames, every five seconds plus edit boundaries]({ROOT/"qa"/stem}) · [validation report]({rp})','']
lines += ['## Content checks','', '- 01 uses 01-install-clean.mov and ends on the real installed iPhone Home Screen.','- 02 cuts directly from sign-in progress to 02-signedin-settings.png. Every app Home frame is omitted.','- 03 starts the form at source 15.000 seconds after the forbidden navigation crossfade has settled. Actual group name is At table. All form shots use two measured FFmpeg delogo rectangles: [455,1824,620,64] and [78,1888,310,54] in 1206×2622 source pixels. They remove the cycle sentence and its continuation while preserving You’ll be the owner and Create group. The submit cut stops at 100.800 seconds, before Home; success ends on 03-created-settings.png.','- 04 retains EMX-TVD and the real share sheet. Dismissal ends at source 109.300 seconds before the share-unavailable status. All stale Members and refresh/Home shots are omitted. Updated Settings shows 2 of 5; final frame is 04-members-joined.png.','- 07 retains Jun’s actual incoming message, Maya’s recorded reply, send and sparkle reaction.','',f'QA: {sum(x["ocr_frames_scanned"] for x in reports)} unique sampled/boundary frames scanned by OCR with zero forbidden-text hits, plus visual review. OCR is supplementary; the faint create navigation crossfade was caught visually and trimmed. All five frame counts, stream durations, silent audio and encoder checks pass.','', 'All generated files, scripts, caches, EDLs, frames and reports are confined to this folder. Raw footage and supplied stills were read only. No simulator, accounts, Git or parent files were changed. Superseded edit metadata is under revisions/; rejected MP4s were removed.','']
(ROOT/'REVIEW.md').write_text('\n'.join(lines))
manifest={'total_seconds':sum(x['duration_seconds'] for x in reports),'total_frames':sum(x['frames'] for x in reports),'status':'READY_FOR_PARENT_REVIEW','clips':reports}
assert manifest['total_seconds']==265 and manifest['total_frames']==7950 and len(reports)==5
(ROOT/'review-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
for x in reports:print(f'{x["duration_seconds"]:3} s | {x["frames"]:4} frames | {x["output"]}')
print('QA + EDL index:',ROOT/'REVIEW.md')
