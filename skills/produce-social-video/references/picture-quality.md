# Bright, clear picture-quality doctrine

## Viewer promise

Default to a bright, clean, immediately legible image. Viewers should recognize the person, machine, action, and relevant evidence at a glance on an ordinary phone or laptop display. A dark cinematic palette is not permission to hide detail, and a nominal 1080p label is not proof of clarity.

## Source gate before grading

For every candidate used full-frame, inspect metadata and representative frames at native output size. Reject or replace footage when any of these are material:

- low-bitrate or second-generation compression that smears faces, hair, text, machinery, or edges;
- upscaled SD/low-resolution footage inside a 720p/1080p container;
- motion blur, missed focus, unstable digital zoom, or a crop too severe for the subject;
- crushed shadows, clipped highlights, color casts, banding, or noise that grading cannot repair;
- player UI, embedded captions, third-party watermarks, or repost artifacts.

Resolution is only one signal. Record codec, dimensions, frame rate, bitrate, perceptual sharpness, motion-blur verdict, compression verdict, and intended display size in the media ledger. Prefer native 1080p or better for full-frame use. A historically important soft source may appear only as an explicitly justified evidence insert; do not disguise it as premium B-roll.

## Clean-enhancement order

Use the restrained logic common to good consumer-editor enhancement presets, but tune each source instead of applying one global look:

1. Normalize color space and range; fix obvious white-balance errors.
2. Set exposure so the subject is clear before adding graphics.
3. Recover highlights and open shadows without flattening the image.
4. Add a mild S-curve or local/midtone contrast for separation.
5. Add restrained saturation or vibrance; keep skin and brand colors natural.
6. Apply light denoise only when noise blocks detail.
7. Apply output-size-aware sharpening last, then inspect faces, text, hair, and machinery at 100%.

Never use sharpening to rescue missing source detail. Reject ringing, halos, crunchy skin, doubled edges, amplified compression blocks, neon saturation, clipped whites, or crushed blacks. If enhancement makes defects more visible, replace the source.

## Exposure guidance

Use 8-bit FFmpeg `signalstats` YAVG as a triage signal, not a creative law:

- For the current bright-and-clear `硬核火星人` house style, aim for an assembled-program mean YAVG roughly `80–110`.
- A legitimately dark interview may sit around `65–85` only when the face and clothing separation remain immediately legible.
- Bright factories, daylight, launch, and engineering footage commonly sit around `95–135` without clipped highlights.
- Investigate sustained windows below `55`; transitions, space imagery, and deliberate black frames are exceptions only when brief and intentional.

Also inspect representative subject regions. Whole-frame averages can hide a dark face against a bright screen or a clipped subject against a dark room. Do not auto-grade solely to reach a number.

## Text and overlays

Keep footage naturally visible. Solve text readability with placement, typography, a restrained shadow/stroke, or a localized low-opacity gradient. Do not cover the whole frame with a heavy black wash. On full-screen footage, any overlay that materially reduces subject detail requires a before/after frame check.

## Required review evidence

Before preview or release:

- generate a contact sheet from every selected source at full-frame intended use;
- inspect opening, median, and closing frames plus the fastest-motion moment;
- sample luminance and run a blur/softness proxy, treating both as triage rather than automatic truth;
- watch motion at normal speed; a sharp paused frame does not prove clean motion;
- compare representative frames before and after grading at 100%;
- record a human verdict for subject sharpness, motion blur, compression, exposure, highlight retention, shadow detail, and enhancement artifacts.

Any full-frame hero, interview, factory, rocket, or evidence shot that is visibly soft on an ordinary display is a release blocker for premium/member content unless the brief explicitly approves archival softness.
