# Regression lessons

Use this checklist to prevent defects observed during iterative source-led and member-video production from recurring.

## Opening contract

- Make frame one sharp, bright enough, full-screen, and immediately understandable. Reject blurred vlog titles, embedded subscribe graphics, player controls, portrait footage with side bars, or distant subjects as the hero opening.
- Verify that narration begins where the approved script begins. Silence before the first line is intentional only when the brief explicitly requires it.
- Listen to the first 15 seconds without looking at captions. Confirm every character of the canonical hook is audible; do not accept a line that loses its last syllable at the first cut.
- Check 0–3, 3–7, 7–15, and 15–30 seconds separately, then watch the entire first 30 seconds continuously. Local passes do not prove opening continuity.
- Compare cold-open shot fingerprints or a recent-shot ledger against prior episodes. A technically sharp shot can still fail when the audience has already seen it repeatedly; reserve reused series imagery for a deliberate callback, not the default spectacle montage.
- Combine proven strengths from an older approved opening only through a rebuilt paper edit and audio ledger. Do not splice two masters by visual timing alone.

## Speech and audio invariants

- Use one approved TTS voice and one target loudness across the entire program. Do not normalize individual sentences to visibly or audibly different levels.
- Treat the TTS provider as part of the approved creative contract, not merely the perceived timbre. Record provider and voice identity before generation and prove the final assets came from that path. Never describe a cloned or zero-shot voice as native Jianying output.
- Before review export, audition the first generated sentence from absolute sample zero and the first/last 500 ms of every TTS asset. Reject stray musical notes, seed/prompt leakage, clicks, clipped consonants, duplicated phonemes, and residual reference audio.
- Measure and audition the final assembled audio, not only source clips. Seeking can hide decoder, timestamp, or concatenation defects that appear during linear playback.
- Treat silence that disappears after seeking as a fatal timeline/mux defect. Re-encode or rebuild timestamps; never dismiss it as a player glitch without cross-player proof.
- Treat late-program hiss, buzzing, phase changes, or codec residue as fatal. Normalize sample rate/channel layout before assembly and perform one final audio encode.
- After every trim, test for missing final phonemes, leading residue, duplicated words, boundary clicks, abrupt breaths, and unintended pauses using `audio-boundary-safety.md`.
- When a local repair creates another speech error one second later, rebuild the complete neighboring sentence chain rather than applying another isolated patch.

## Picture and sequence invariants

- Inspect every replacement at its actual output crop and at 100% scale. Metadata marked 1080p does not prove perceptual sharpness.
- Preserve native geometry. Fill the frame with proportional scale plus crop, or use an intentional designed matte; never stretch width and height independently.
- Require a sentence-level reason for every B-roll choice. Shared company, founder, or industry identity does not make Tesla factories, generic power equipment, or repeated rocket landings relevant to a specific rocket-system claim.
- Grade for a bright, clear subject without clipped whites, crushed blacks, halos, crunchy skin, or noisy shadow lifting.
- Place failure, explosion, or uncertainty in the first half when the argument is about iteration. Delay the clean launch, reveal, or triumphant spectacle until the second half so picture rhythm follows the story.
- Label vehicles and events from evidence. Do not substitute Falcon, Starship, launch, abort, diversion, or explosion based on visual resemblance.
- Keep full-screen source footage full-screen. Do not end on portrait footage padded by side bars when a horizontal grand image is available.
- End with the emotionally largest horizontal moving hero image, normally for at least 6 seconds, followed by a readable 0.8–1.2 second hold.
- Count source-shot reuse in the assembled timeline. A distinct shot should normally appear no more than twice; rotation code must use the clip's probed native duration rather than an assumed duration, or the tail can render black.
- Before a long render, re-encode sparse-keyframe source excerpts to a seek-safe delivery mezzanine (normally GOP 30 at 30 fps) and inspect start, midpoint, and end−0.2s. Container duration alone does not prove frame availability.
- Normalize all scheduled sources to CFR at the delivery fps before composition. Do not ignore renderer warnings about sparse keyframes or proceed because static snapshots look correct; verify motion at normal speed and run repeated-frame/freeze detection on the assembled master.
- Reject any full-frame shot that is visibly soft or smeared in ordinary playback. A semantically correct shot is still unusable when its perceptual clarity breaks the surrounding quality level; replace it rather than sharpening or upscaling it.
- Time source-language captions from real transcript timestamps. For member originals, bind the Chinese translation and English transcript to the same cue object and render them as a synchronized bilingual pair. Equal-duration subdivision, topic-summary captions, and captions inferred only from the surrounding article are not acceptable substitutes for translation coverage.
- Do not solve caption length by cutting text at the midpoint. Keep the sentence visible until its final phoneme and wrap it visually when necessary. If a temporal split is unavoidable, place it at a real pause after a completed clause and inspect the preceding/current/following cue together.
- When timed elements inherit a global `.clip { inset: 0 }`, every non-full-screen card must explicitly unset `right` and `bottom` and declare its width/height behavior. Otherwise a small card can silently become a full-screen opaque mask.
- Normalize the final delivery audio with an explicit 48 kHz output rate and verify the muxed stream. Filter settings do not guarantee the encoder preserves the required sample rate.
- Reject a static or near-black brand slate as the final emotional image. Keep the Chinese-only brand mark over moving horizontal hero footage, then allow a short readable hold.

## Repair discipline

- A defect first discovered in a full-length user review must be traced back to a missing or bypassed preflight gate. Add the preventive check before making the local repair.
- Do not treat version count as progress. After the risk reel is locked, round 2 should be a coherent full candidate; round 3 may repair bounded defects but must not introduce a new asset family, layout system, voice, caption model, or outro.

1. Preserve the last approved master and name every candidate with a new version.
2. Record the defect, affected interval, expected canonical text/state, and repair scope before editing.
3. Re-render the smallest safe segment, including one complete sentence or shot before and after the defect.
4. Run black, freeze, silence, peak, caption, exposure, sharpness, and media-window checks on the changed segment.
5. Compare the changed segment with the prior approved version for unintended differences.
6. Reassemble and recheck timestamps, duration, audio continuity, captions, watermark, and scene seams.
7. Watch the changed neighborhood linearly, then watch the full master linearly before claiming `9.5+`.

Never trade one known defect for another. A repair is incomplete until both the target defect and the adjacent regression surface pass.
