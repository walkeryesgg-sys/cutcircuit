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

1. Use `$produce-social-video` to interview the user and obtain explicit approval of the production brief.
2. For `硬核火星人`, classify both `program_type` (`member_original`, `public_story`, or `custom`) and `edit_model` (`source_led`, `narration_led_montage`, or `hybrid_evidence_lesson`). Never infer member rules from editing appearance alone.
3. Plan the argument, evidence, script, media, narration, captions, edit, sound, and delivery identity.
4. If YouTube material is required, use `$youtube-research-downloader` for the authorized transfer and verification. Record provenance and reuse-rights assumptions.
5. Render in reviewable segments, run automated checks, assemble the candidate, and watch it linearly.
6. Hand the candidate to `$score-social-video`. Treat its fatal gates and score caps as independent release constraints.
7. Repair every P0 issue. Repair P1 issues while the target remains unmet. Re-render every affected segment and rescore the assembled candidate.
8. Repeat for at most three scored repair cycles. Never lower the target or weaken a gate to make a candidate pass.
9. Deliver when the target passes. If three cycles do not pass, report the actual score, remaining blockers, and best candidate without calling it final or publishable.

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
