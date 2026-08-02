# Regression lessons

Use this checklist to prevent defects observed during iterative source-led and member-video production from recurring.

## Opening contract

- Make frame one sharp, bright enough, full-screen, and immediately understandable. Reject blurred vlog titles, embedded subscribe graphics, player controls, portrait footage with side bars, or distant subjects as the hero opening.
- Verify that narration begins where the approved script begins. Silence before the first line is intentional only when the brief explicitly requires it.
- Listen to the first 15 seconds without looking at captions. Confirm every character of the canonical hook is audible; do not accept a line that loses its last syllable at the first cut.
- Check 0–3, 3–7, 7–15, and 15–30 seconds separately, then watch the entire first 30 seconds continuously. Local passes do not prove opening continuity.
- Combine proven strengths from an older approved opening only through a rebuilt paper edit and audio ledger. Do not splice two masters by visual timing alone.

## Speech and audio invariants

- Use one approved TTS voice and one target loudness across the entire program. Do not normalize individual sentences to visibly or audibly different levels.
- Measure and audition the final assembled audio, not only source clips. Seeking can hide decoder, timestamp, or concatenation defects that appear during linear playback.
- Treat silence that disappears after seeking as a fatal timeline/mux defect. Re-encode or rebuild timestamps; never dismiss it as a player glitch without cross-player proof.
- Treat late-program hiss, buzzing, phase changes, or codec residue as fatal. Normalize sample rate/channel layout before assembly and perform one final audio encode.
- After every trim, test for missing final phonemes, leading residue, duplicated words, boundary clicks, abrupt breaths, and unintended pauses using `audio-boundary-safety.md`.
- When a local repair creates another speech error one second later, rebuild the complete neighboring sentence chain rather than applying another isolated patch.

## Picture and sequence invariants

- Inspect every replacement at its actual output crop and at 100% scale. Metadata marked 1080p does not prove perceptual sharpness.
- Grade for a bright, clear subject without clipped whites, crushed blacks, halos, crunchy skin, or noisy shadow lifting.
- Place failure, explosion, or uncertainty in the first half when the argument is about iteration. Delay the clean launch, reveal, or triumphant spectacle until the second half so picture rhythm follows the story.
- Label vehicles and events from evidence. Do not substitute Falcon, Starship, launch, abort, diversion, or explosion based on visual resemblance.
- Keep full-screen source footage full-screen. Do not end on portrait footage padded by side bars when a horizontal grand image is available.
- End with the emotionally largest horizontal moving hero image, normally for at least 6 seconds, followed by a readable 0.8–1.2 second hold.

## Repair discipline

1. Preserve the last approved master and name every candidate with a new version.
2. Record the defect, affected interval, expected canonical text/state, and repair scope before editing.
3. Re-render the smallest safe segment, including one complete sentence or shot before and after the defect.
4. Run black, freeze, silence, peak, caption, exposure, sharpness, and media-window checks on the changed segment.
5. Compare the changed segment with the prior approved version for unintended differences.
6. Reassemble and recheck timestamps, duration, audio continuity, captions, watermark, and scene seams.
7. Watch the changed neighborhood linearly, then watch the full master linearly before claiming `9.5+`.

Never trade one known defect for another. A repair is incomplete until both the target defect and the adjacent regression surface pass.
