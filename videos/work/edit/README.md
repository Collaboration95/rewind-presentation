# Phone feature renderer

Python 3 standard library, `ffmpeg`, `ffprobe`, ImageMagick `magick`. No install, shell execution, simulator access or UI generation. All generated assets, caches, reports and MP4s are confined to this `edit/` directory. Inputs are read only. Existing MP4 outputs are refused; choose a new output name for a revision. Output paths are relative to `edit/` or absolute within it.

Run from any directory:

```sh
python3 /Users/speedpowermac/Documents/projects/CODE_MAIN/NUS/SWE5006/presentation-prep/videos/work/edit/render.py /absolute/path/to/edit-list.json
```

Append `--plan` to inspect the resolved timeline without rendering, `--preset veryfast` for quicker encoding, or `--crf 18` (default) to set quality. Default preset is `fast`. Source paths must be absolute. JSON uses double quotes.

## Minimal exact input

```json
{
  "number": 1,
  "name": "Install to Home Screen",
  "output": "install-review.mp4",
  "add_island": true,
  "segments": [
    {
      "source": "/absolute/path/to/raw.mov",
      "in": 0,
      "out": 5,
      "duration": 5
    }
  ]
}
```

Change only the source path and output when ready. No final feature clips have been rendered. `test6.json` is runnable as delivered and uses the supplied real blank sign-in screenshot.

## Mixed video, PNG and optional audio

```json
{
  "number": 1,
  "name": "Install to Home Screen",
  "output": "install-with-card-review.mp4",
  "title_card": true,
  "add_island": true,
  "segments": [
    {
      "source": "/absolute/path/to/raw.mov",
      "in": 0,
      "out": 5,
      "duration": 5,
      "audio": false
    },
    {
      "source": "/absolute/path/to/screenshot.png",
      "duration": 3,
      "add_island": false,
      "audio": {
        "source": "/absolute/path/to/narration.wav",
        "in": 0,
        "volume": 1
      }
    }
  ]
}
```

Total here is exactly **9 seconds**: 1-second card + 5-second video + 3-second still. `title_card` defaults false. A standalone assembly card is the exact JSON `{"number":1,"name":"Install to Home Screen","output":"install-card-review.mp4","segments":[{"type":"title"}]}`. Each `type: title` segment is exactly one second, with silence. Cards show only the number and feature name on the same cream backdrop. Names are one line, maximum 40 characters.

## Timing and sound

- `in` defaults 0, `out` is exclusive, and both are seconds in the **encoded source timeline**. No wall-clock reconstruction, time stretching, interpolation or invented actions. `duration` is output time. If omitted, it is `out - in`; at least one of `duration` or `out` is required.
- Output durations must be positive multiples of 1/30 second; impossible exact durations are rejected rather than rounded silently. `duration: 6` gives 180 frames. Segment totals include any title card. Audio is exactly 1600 samples per video frame at 48 kHz.
- Videos play at recorded timing. The selected interval is cut short when `duration` is smaller, or its last frame is held when `duration` is larger. If sparse simulator footage ends before `out`, its last frame is held. Sparse footage cannot reveal elapsed wall-clock time: use PNG holds for intentional pauses. An `in` beyond the encoded duration is rejected.
- PNGs hold for `duration`. `in` must be zero; `out` is optional. PNG is the supported still format.
- `audio` defaults true: retain source video audio if present, otherwise silence. `false` forces silence. An absolute audio filename string or `{ "source": "/absolute/audio.wav", "in": 0, "volume": 1 }` replaces segment sound. Audio starts with the segment, is trimmed/padded with silence to its duration, and is never stretched or mixed with source sound. No narration is generated.
- Cached segments contain H.264 + PCM. Assembly copies the video and encodes AAC once, avoiding accumulated AAC join padding. Final MP4 is H.264 High, yuv420p, BT.709, 1920×1080, 30 fps, AAC 48 kHz stereo, faststart.

## Phone and cleanup

Screen bounds are `(740,60,440,957)` within 1920×1080, with a rounded black physical bezel, subtle shadow, cream backdrop and orange glow. Source aspect ratio is preserved; 1206×2622 fits with at most one pixel of padding. The small feature label is at the top left. No captions, stamps or environment text are added.

`add_island` defaults **false** and can be set globally or per segment. Set true only for raw recordings lacking the island. The supplied PNG already has an island. All phone frames clip the screenshot corners cleanly.

Prefer clean source captures. Optional `crop: [x,y,width,height]` uses original source pixels; the cropped result is fitted into the screen without stretching, so cropping may introduce padding. Optional `mask` is a list of rectangles applied **before crop and scaling**, using original source coordinates:

```json
"mask": [
  {"x": 100, "y": 900, "width": 220, "height": 60, "color": "#f6efe5"},
  {
    "x": 100,
    "y": 1000,
    "width": 220,
    "height": 60,
    "sample": [90, 1010],
    "reference": "/absolute/path/to/matching-frame.png"
  }
]
```

These coordinates are illustrative, not an approved mask location. Supply measured rectangles covering forbidden cycle duration labels. `color` and `sample` are mutually exclusive. Sampling reads one exact pixel from a PNG; `reference` can be omitted when the segment source itself is a PNG. A flat patch is pixel matched only to a flat background; gradients or moving content need clean footage/crop. No replacement text or UI is created. Review masked frames visually.

## Verification and cache

After rendering, the script checks codec/profile, dimensions, frame count, 30 fps, pixel format, and exact video/audio/container durations with `ffprobe`. It writes sibling `.validation.json` and `.plan.json` reports. Failure leaves a `.partial.mp4` for diagnosis rather than publishing the output. Cache keys include the script, source path/size/nanosecond mtime, masks, audio, framing and encoder settings. Cache is under `edit/.cache/`; reuse a different MP4 output name to reuse unchanged segments. Changing the script invalidates prior cache entries.

The delivered `test6.mp4` is a six-second hold of `02-signin-blank.png`. Its extracted frame is `test6-frame.png`. This verifies rendering appearance and encoding, not simulator capture behavior or application acceptance. Additional technical fixture checks, if present under `checks/`, use only this real screenshot and silent audio.

Verified locally on 26 October 2026: `test6.mp4` has 180 frames and exactly 6.000 seconds for video, audio and container; decoded AAC is digitally silent. Extracted frame viewed. `checks/mixed-check.mp4` has 60 frames and exactly 2.000 seconds: one-second card, half-second sampled-mask/full-source-crop PNG, half-second video extended from a 0.2-second recording of the same screenshot, with external silent AAC input. All encoding/timing checks pass; title frame viewed. `checks/cache-check.mp4` confirms all three segment cache hits and identical timing. This is a sparse-length hold check from the real screenshot, not a real simulator video capture or proof of moving-content synchronization.
