# Autonomous production workflow

## 1. Bootstrap

Run the doctor and initialize `video-project.json`. Derive defaults from destination:

- WeChat Video Account / YouTube / course: 1920×1080.
- Shorts/Reels/TikTok: 1080×1920.
- Default delivery: H.264, yuv420p, 30fps, AAC 48kHz.

Record target audience, platform, duration, language, release threshold, brand, supplied assets, and factual-source policy.

## 2. Asset and rights inventory

Index files with duration, dimensions, audio, transcript/subtitles, creation source, and rights status. Reuse supplied assets before sourcing.

When a specific evidence or visual gap remains, use `scripts/youtube_media.py search`. Inspect metadata and shortlist candidates before downloading. Prefer official channels, original speakers, primary sources, and footage with usable subtitles. Read `youtube-sourcing.md`.

Create `provenance.json` with:

- path/hash;
- creator/source URL;
- license/authorization status;
- persons/brands visible;
- intended time range and use;
- risk: low/medium/high.

Mute or exclude unresolved high-risk footage.

## 3. Content lock

Produce:

- one-sentence thesis;
- viewer promise;
- opening conflict;
- source claims and evidence;
- story spine;
- section outcomes;
- final repeatable conclusion.

For fact-sensitive work, distinguish verified fact, source claim, interpretation, and prediction.

Lock narration before expensive assembly. Avoid repeated user review unless the user explicitly requests collaborative writing.

## 4. Audio-first timing

Generate TTS or adopt source voice, then probe real durations. Normalize spoken audio consistently. Create word/phrase timing for captions.

Rules:

- never cut a speaker mid-sentence;
- use source audio as evidence, not wallpaper;
- remove unexplained multi-second gaps;
- duck music under all speech;
- design music changes around chapters rather than arbitrary clip boundaries.

## 5. Scene plan

Assign every beat:

- purpose: hook/story/evidence/explanation/payoff;
- visual source;
- audio owner;
- caption state;
- expected motion;
- risk and fallback.

Choose rhythm by genre:

- source immersion: long shots are allowed;
- macro narrative: evidence and imagination alternate;
- personality/reveal: faster changes with continuous new information.

Do not target a universal cut interval.

For evidence-led paid courses, record a visual-ownership target for every beat:

- `footage-led`: real footage occupies about 55%–65% of the frame;
- `source-led`: the original speaker/evidence occupies at least 65% of the frame;
- `graphics-led`: reserve for diagrams, comparisons, calculations, or ideas that footage cannot explain.

Across the finished program, a useful default is about 40% designed explanation to 60% real footage. Do not satisfy the ratio with tiny decorative windows.

## 6. Build in segments

Create separate compositions for:

- fixed intro;
- opening/topic bridge;
- each chapter or 60–120 second block;
- outro.

Use deterministic local assets and seek-safe timelines. Render a segment contact sheet containing each media-window start/mid/end and each maximum text state.

## 7. Progressive QA

Gate order:

1. first frame;
2. opening 3/15/30 seconds;
3. each segment;
4. assembled transitions;
5. final full video.

Fail fast on black frames, missing media, frozen shots, overflow, subtitle timing, interrupted speech, or audio discontinuity.

For every media handoff, inspect the last 0.2 seconds of the outgoing shot and first 0.2 seconds of the incoming shot. Hard-cut or overlap adjacent clips by 4–8 frames. Unintended near-black longer than 0.15 seconds or an uncovered media slot longer than 0.25 seconds is P0 and must be repaired automatically.

## 8. Automatic repair

Repair P0/P1 findings without asking when the fix is reversible:

- replace broken media with an approved fallback;
- resize/reflow overflowing text;
- retime captions from speech;
- shorten dead gaps;
- rebalance music;
- reduce unsafe render concurrency;
- rerender only affected segments;
- reassemble and rescore.

Escalate only when repair changes factual meaning, rights exposure, paid services, or core brand intent.

## 9. Final gate

Run `$score-social-video` when available. Perform a full linear watch for paid or `>=9.5` claims. Deliver only after the threshold passes.

## 10. Reuse

Save stable intro/outro, caption system, watermarks, voices, music beds, audience profile, pacing benchmarks, and approved asset library as reusable project assets. Never copy factual claims or rights assumptions across projects without revalidation.
