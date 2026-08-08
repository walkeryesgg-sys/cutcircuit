---
name: cutcircuit
description: Route and orchestrate an evidence-led video workflow across sourcing, production, independent scoring, repair, and delivery. Use when the user asks CutCircuit to create, substantially revise, review, or source material for a social-media, educational, interview, documentary, or paid-course video, especially when the finished video must pass a measurable release threshold.
---

# CutCircuit

Run video work as a quality circuit: **source → cut → score → repair**.

## Route the request

- For a new video or substantial revision, read and follow `$produce-social-video`.
- When the approved treatment is full-screen source footage alternating narration with original-audio evidence, require `$produce-social-video` to load its source-led commentary template.
- For an existing MP4 or MOV that only needs evaluation, read and follow `$score-social-video`.
- For an authorized YouTube download, subtitle extraction, metadata archive, or download failure, read and follow `$youtube-research-downloader`.
- For a full production, invoke the downloader only when the approved editorial plan contains a specific evidence or visual gap. Do not download speculative filler.

## Run the production circuit

1. Use `$produce-social-video` to interview the user, deliver a complete pre-production plan, and obtain explicit approval of that exact plan version. The plan must include the script, narrative structure, beat sheet, shot list, storyboard, audio/caption plan, asset plan, risks, deliverables, and acceptance criteria. Do not begin media acquisition, voice generation, editing, animation, or rendering before approval.
2. For `硬核火星人`, classify both `program_type` (`member_original`, `public_story`, or `custom`) and `edit_model` (`source_led`, `narration_led_montage`, or `hybrid_evidence_lesson`). Never infer member rules from editing appearance alone.
3. Before composing frames, require `$produce-social-video` to read `references/visual-hierarchy.md`, assign every beat to `watch` or `understand`, and preserve footage-first hierarchy.
   Require the producer to read `references/iteration-budget.md` and treat two review rounds plus one bounded repair round as the production budget. A full-length render is not an acceptable discovery tool for unresolved creative direction, asset fitness, voice provenance, caption segmentation, or brand identity.
4. Execute the approved argument, evidence, script, media, narration, captions, edit, sound, motion, and delivery identity. If a material change becomes necessary, revise the plan, identify the changed sections, and obtain approval before continuing that scope. For programmed camera or graphic motion, require the producer to load `references/motion-craft.md` and build one seek-safe labeled timeline instead of disconnected delayed animations.
5. If YouTube material is required, use `$youtube-research-downloader` for the authorized transfer and verification. Record provenance and reuse-rights assumptions.
6. Produce and inspect a contact sheet before the review render. Reject slide-like source presentation, unjustified top captions, decorative footage insets, low-contrast watermarks, off-topic filler, distorted aspect ratios, and repeated motifs. Then render the compact risk reel required by `references/iteration-budget.md`; it must cover the opening, representative evidence, densest explanation/caption state, one source↔narration seam, and the branded ending.
7. Before the first review render, enforce three provenance/transport gates:
   - **Voice provenance:** record the exact provider, voice ID/name, generation artifact, and evidence that the rendered waveform came from that provider. A clone, conversion, or zero-shot imitation is not Jianying-native TTS. If the approved provider cannot be obtained, stop and report the blocker instead of substituting it.
   - **Picture fitness:** inspect every full-frame source at output size and normal playback speed. Reject visibly soft, smeared, motion-blurred, or second-generation footage even when its container says 1080p/4K.
   - **Seek safety:** normalize every scheduled video source to CFR delivery fps and a one-second-or-shorter GOP before HyperFrames capture. Sparse-keyframe warnings are release blockers, not informational warnings.
   - **Caption semantics:** build captions from complete spoken sentences or clauses using `references/caption-segmentation.md`; run `scripts/validate_caption_semantics.py` before rendering. Do not split cues by character count or equal duration.
8. Render in reviewable segments, run automated checks, assemble the candidate, and watch it linearly.
   For every narration edit, require the producer to follow its `references/audio-boundary-safety.md`: use measured sentence boundaries, prove adjacent source ranges do not overlap, and audition the complete affected sentence chain before accepting the render.
   Require the producer to run `references/regression-lessons.md` after every repair so a local fix cannot reintroduce a previously eliminated opening, audio, picture, sequencing, or ending defect.
9. For narration, listen to the first complete sentence and every generated segment start/end from the rendered candidate. Any stray note, prompt residue, click, breath fragment, duplicated phoneme, or provider mismatch blocks release; ASR/text equality alone cannot pass this gate.
10. Hand the candidate to `$score-social-video`. Treat its fatal gates and score caps as independent release constraints.
11. Repair every P0 issue. Repair P1 issues while the target remains unmet. Re-render every affected segment and rescore the assembled candidate.
12. Permit at most three user-visible review rounds total: (1) risk reel/design lock, (2) first full candidate, and (3) bounded local repair. The independent scorer may run internally as often as needed before a user-visible round, but it may not conceal a structural redesign. Never lower the target or weaken a gate to make a candidate pass.
13. If round 2 reveals broad visual direction, asset-family, voice, caption-system, or brand-ending rejection, classify it as a failed preflight, return to the risk reel once, and record why the gate failed. Do not accumulate V4–V9 full renders as the normal workflow.
14. Deliver when the target passes. If the bounded round cannot pass, report the actual score, remaining blockers, and best candidate without calling it final or publishable.

## Release thresholds

- Ordinary social video: no fatal gate and score `>= 9.0`.
- Paid or member content: no fatal gate and score `>= 9.5`.
- Premium target: no fatal gate, score `>= 9.8`, and a completed full linear watch.

Any edit that changes timing, speech, captions, music, media windows, or scene seams requires the relevant automated checks again. It also requires another full linear watch before a `9.5+` claim.

## Preserve separation of duties

Keep production, evaluation, and downloading as separate skills even when they run in one circuit:

- The producer owns creative decisions and repairs.
- The scorer owns release judgment and must not soften findings to defend the edit.
- The downloader owns transfer integrity and access safety; a successful download does not establish reuse rights.

Make the user coordinate none of these roles. Surface outcomes, approvals, material risks, and the final evidence-backed verdict.
