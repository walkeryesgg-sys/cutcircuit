# Verified production for rebuilds and premium work

Use a single canonical `timeline.json` as the production contract. Do not reuse a guide video as a clean base: inspect for burned captions, reference voice, and graphics already embedded in it. Preserve prior projects and build a separate candidate.

## Dependency order

1. Verify dated claims against primary sources; label calculations, assumptions and interpretation. Freeze canonical narration with stable unit IDs.
2. Generate native voice and freeze local artifacts. Bind each file to its actual spoken text using ASR and contextual listening, not filenames, creation order, or a provider requirement flag. Record provider, voice ID, hash, measured source duration, word/phrase timestamps, and generation evidence.
3. Choose `audio_first_rebuild` unless picture is explicitly locked. Trim only verified leading/trailing silence, retain phonemes, then set destination times. Reference starting gaps: 0.22–0.38 s sentence, 0.45–0.75 s paragraph. Exceptions need a reason; do not erase all breaths or fill old estimated slots.
4. For each spoken unit, select an explicit source window and visible reason, or design a necessary explanation graphic. Inspect the actual window. Generic topic matching, source-pool rotation, random/modulo time selection and fallback to arbitrary library footage are forbidden.
5. Generate captions, diagrams, cuts and music placement from those IDs and times. A missing or duplicate ID fails the build; never fall back to time zero. No timing by character count.
6. Declare exactly one visible caption renderer. Jianying TTS input text is not a second output-caption layer. Burned captions count as visible layers; bilingual source captions are one synchronized unit with two languages. Inspect sources and final frames; a manifest alone cannot detect baked text.
7. Validate before risk reel, chapters and final assembly. Review the actual candidate independently, with evidence and hash binding. Failed prerequisites remain failed even if a script exits successfully.

## Timeline schema, version 1

`mode`: `audio_first_rebuild` or `locked_picture_patch`; `duration`: seconds.

`caption_renderer`: a nonempty renderer name. `visible_caption_layers`: exactly one item matching that name. `baked_caption_sources`: empty for a clean rebuild; rebuild from clean originals if this is not empty.

`units`: ordered records containing `id`, `text`, `start`, `end`, `audio` (local path), `audio_sha256`, `provider`, `voice_id`, `generation_evidence` (local artifact path), `binding_review` (local ASR/listening receipt), `source_duration`, `trim_start`, `trim_end`, `audible_start`, `audible_end` (source seconds), optional `gap_reason`. Destination duration equals the trim interval; do not stretch voice to hit runtime. Hash and measurements must describe real audio.

Each `binding_review` is a JSON object with matching `audio_sha256`, `text_sha256` (UTF-8 canonical text), `trim_start`, `trim_end`, `asr_text`, `review_status: verified`, and `review_evidence` pointing to an existing contextual listening/content-review artifact. A large ASR mismatch additionally needs `asr_correction_explanation`; it is a review trigger, not an instruction to rewrite what was actually spoken. Preserve unreviewed status until the required listening occurs.

`captions`: ordered records with `unit_id`, `start`, `end`, `text`; same canonical text after removal of terminal `。` only. For multi-clause units, represent measured subunits first; do not estimate subcue times. Each unit has one cue (possibly visually wrapped).

`shots`: records with `unit_ids`, `start`, `end`, `kind` (`footage` or `graphic`), `file`, `picture_reason`, `review_evidence` (local inspected frames/notes). Footage also has `source_start`, `source_duration`, `clarity_pass: true`, `embedded_captions: false`. The declared source window must be within media duration. Planned and inspected are distinct states.

Run:

```sh
python3 skills/cutcircuit/scripts/validate_timeline.py /absolute/project/timeline.json
```

This validator checks deterministic consistency, not whether a claim, transcript, picture reason, or listening receipt is truthful. Independent review must inspect those artifacts, decoded frames, audible seams and final moving video.

Premium release uses a separate `release.json` and `scripts/validate_release.py`. Its `candidate`, `script`, and `timeline` objects each contain `file` and actual `sha256`; also include `score`, `fatal_issues`, `reviewer: {id, independent}`, and `full_watch: {completed, playback_rate, perceived_modalities, candidate_sha256}`. Full watch requires rate 1 and perceived modalities `["video", "audio"]`. `evidence` contains existing artifact paths for `watch_notes`, `voice_provenance`, `boundary_audition`, `automated_checks`, and `semantic_shot_review`. This gate revalidates the timeline and rejects stale hashes. A fabricated receipt can still lie: the evaluator must actually perceive the candidate, and unavailable listening/video review remains a blocker.

## Model-upgrade regression cases

Before adopting a revised workflow, demonstrate rejection of: burned plus overlay captions; continuous BGM with a two-second narration gap; missing anchor; estimated or stale audio duration; end-of-script audio bound to the first unit; missing semantic footage coverage; stale candidate score. Preserve user preferences and authorization while exercising model judgment on editorial choices. Do not encode a model name as evidence of passing.
