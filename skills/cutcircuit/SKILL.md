---
name: cutcircuit
description: Route and orchestrate an evidence-led video workflow across sourcing, production, independent scoring, repair, and delivery. Use when the user asks CutCircuit to create, substantially revise, review, or source material for a social-media, educational, interview, documentary, or paid-course video, especially when the finished video must pass a measurable release threshold.
---

# CutCircuit

Run video work as a quality circuit: **source → cut → score → repair**.

## Execution contract

Read [references/verified-production.md](references/verified-production.md) for a rebuild, native-TTS replacement, or premium target. It defines executable checks for the shared clock, caption ownership, speech gaps, semantic shot bindings, and candidate-specific review evidence.

For macOS Jianying-native TTS, also read [references/jianying-native-ui.md](references/jianying-native-ui.md). It records an observed working 11.4 UI path, state verification and acquisition-only SRT handling; it is not permission to edit encrypted drafts or a substitute for listening.

Respect authorization already given in the conversation. When the user authorizes end-to-end production or a from-scratch rebuild with editorial discretion, record that scope, write a reviewable plan, and proceed. Do not re-request approval merely because the plan did not exist when authorization was given. Ask only for unresolved decisions that materially exceed that scope. Treat the plan-confirmation steps below as applying when production has not already been authorized.

Do not attribute quality to a model label. Re-evaluate capabilities with observable task results; retain deterministic validation and independent review across model upgrades. A stronger model may choose shots and arguments more effectively, but a generated artifact is not verified until checked.

## Route the request

- For a new video or substantial revision, read and follow `$produce-social-video`.
- When the approved treatment is full-screen source footage alternating narration with original-audio evidence, require `$produce-social-video` to load its source-led commentary template.
- When the approved treatment is a 25–60 second public short built around one person's visible waiting, silence, or micro-reaction during a verified high-stakes event, classify it as `public_story + character_pressure_moment` and require `$produce-social-video` to load `character-pressure-moment-short.md`.
- For an existing MP4 or MOV that only needs evaluation, read and follow `$score-social-video`.
- For an authorized YouTube download, subtitle extraction, metadata archive, or download failure, read and follow `$youtube-research-downloader`.
- For a full production, invoke the downloader only when the approved editorial plan contains a specific evidence or visual gap. Do not download speculative filler.

## Run the production circuit

1. Use `$produce-social-video` to interview the user, deliver a complete pre-production plan, and obtain explicit approval of that exact plan version. The plan must include the script, narrative structure, beat sheet, shot list, storyboard, audio/caption plan, asset plan, risks, deliverables, and acceptance criteria. Do not begin media acquisition, voice generation, editing, animation, or rendering before approval.
2. For `硬核火星人`, classify both `program_type` (`member_original`, `public_story`, or `custom`) and `edit_model` (`source_led`, `narration_led_montage`, or `hybrid_evidence_lesson`). Never infer member rules from editing appearance alone.
   When the episode belongs to `马斯克商业解读`, require `$produce-social-video` to load its Musk-business member template. This is a distinct paid explanatory format, not a generic Musk montage or a slide deck.
3. Before composing frames, require `$produce-social-video` to read `references/visual-hierarchy.md`, assign every beat to `watch` or `understand`, and preserve footage-first hierarchy.
   Require the producer to read `references/iteration-budget.md` and treat two review rounds plus one bounded repair round as the production budget. A full-length render is not an acceptable discovery tool for unresolved creative direction, asset fitness, voice provenance, caption segmentation, or brand identity.
   For self-media and paid lessons, also lock a distribution-and-learning contract before scripting: state the concrete audience problem, the skill or decision rule the viewer can use immediately, the opening promise, and the reason the lesson is worth finishing or paying for. “干货”“深度” and topic importance are not viewer benefits.
   For this user's future videos (2026-09-09 preference), plan approximately five minutes including the outro; do not inherit the superseded ten-minute default. For business lessons or “流水账 / 记不住” feedback, require the producer's `references/five-minute-focus-and-recall.md`: lock one question, one takeaway, a necessary causal chain, and an explicit cut list before TTS. Information rewards may deepen the same model; they are not a quota of new concepts. Record a cold-reader's actual retelling/application, distinguishing model review from human feedback; generated answer keys and technical scores do not prove human recall.
4. Execute the approved argument, evidence, script, media, narration, captions, edit, sound, motion, and delivery identity. If a material change becomes necessary, revise the plan, identify the changed sections, and obtain approval before continuing that scope. For programmed camera or graphic motion, require the producer to load `references/motion-craft.md` and build one seek-safe labeled timeline instead of disconnected delayed animations.
   For member originals and evidence-led lessons, require an explicit editorial-contribution pass: after the primary evidence, the script must add the program's own labeled interpretation, decision rule, boundary, or consequence. A sequence that only paraphrases the source, lists facts, or restates a framework without taking an evidence-bounded position fails the script gate.
   Require a retention-and-learning ledger for every narration beat: `viewer question → new reward → usable rule/example → next open loop → visual proof`. Deliver an initial useful answer within the first 15 seconds, then add a new fact, mechanism, misconception correction, worked example, decision rule, or executable action every 15–30 seconds. Delete mood-only bridges and repeated conclusions. By the end, a target viewer must be able to restate the method and apply it to one real task without rewatching.
   For WeChat Channels, optimize for silent autoplay, friend recommendations, forwarding, and paid-value perception: the first frame needs a recognizable subject; the first three seconds need a concrete conflict, abnormal consequence, or costly mistake; the first 15 seconds must state both the payoff and the first answer. Use natural spoken Chinese rather than lecture introductions, official phrasing, or generic hype. Treat retention as earned information progress, not faster cutting.
   For member originals, do not force a public-video profile CTA. End by resolving the opening promise with one memorable, operational conclusion.
5. If YouTube material is required, use `$youtube-research-downloader` for the authorized transfer and verification. Record provenance and reuse-rights assumptions.
6. Produce and inspect a contact sheet before the review render. Reject slide-like source presentation, unjustified top captions, decorative footage insets, low-contrast watermarks, off-topic filler, distorted aspect ratios, and repeated motifs. Build a shot-usage ledger keyed by source file plus source-time range; flag every repeated range and every near-duplicate composition. A repeated shot is allowed only when the recurrence has a stated editorial purpose, and the same signature/brand shot must not be spent in the body if it is reserved for the ending. Then render the compact risk reel required by `references/iteration-budget.md`; it must cover the opening, representative evidence, densest explanation/caption state, one source↔narration seam, and the branded ending.
   For documentary-style lessons, design the body as coherent 20–40 second scene groups rather than fixed-duration asset rotation. Each group needs an establishing state, action, change, and result while preserving a person, place, object, product, or event. Every shot must have exactly one primary job—evidence, explanation, emotion, or seam. Stop and source better material when no shot is both semantically exact and premium; generic Musk, rocket, factory, keyboard, meeting, or “technology” footage cannot fill a sentence merely because it matches the broad topic. Use information graphics only for relationships real footage cannot express.
7. Before the first review render, enforce three provenance/transport gates:
   - **Voice provenance:** record the exact provider, voice ID/name, generation artifact, and evidence that the rendered waveform came from that provider. A clone, conversion, or zero-shot imitation is not Jianying-native TTS. If the approved provider cannot be obtained, stop and report the blocker instead of substituting it.
   - **Picture fitness:** inspect every full-frame source at output size and normal playback speed. Score sharpness and semantic relevance separately; a clip passes only when both are strong. Reject visibly soft, smeared, motion-blurred, stretched, upscaled, or second-generation footage even when its container says 1080p/4K. Reject sharp but merely adjacent-topic filler as well. Prefer a less familiar, directly relevant HD source over a frequently reused hero clip, and verify aspect ratio from the decoded picture rather than container metadata alone.
   - **TTS-to-picture binding:** for every TTS natural sentence or completed clause, write one auditable picture-reason note naming the visible person, action, object, result, or otherwise-unfilmable mechanism it conveys. A company/technology/theme match alone is not a valid mapping. In the risk reel and final score, sample at least ten TTS units across the opening, cases, method, and conclusion: if a reviewer cannot explain what the current image adds to that exact sentence, replace the shot or redesign the scene group. Do not turn literal word matching into cheap illustration; prefer a continuous real action, object transformation, or causal result that makes the sentence more intelligible.
   - **Premium visual authorship:** judge every 20–40 second scene group for a deliberate establishing state, action, change, and result—not merely clip variety. A group fails premium review when it could be reordered without changing meaning, relies on stock-style office acting/template graphics, or lacks a coherent visual subject. High-end feeling comes from specific evidence, controlled composition, bright clean exposure, restrained typography, motivated camera movement, and continuity of person/place/object—not from dark overlays, speed ramps, decorative transitions, or dense labels.
   - **Shot diversity:** compare the shot-usage ledger against the current episode and recent episodes in the same series. Replace unmotivated repeats before the risk reel. Do not let a small set of convenient Musk, factory, launch, or landing clips dominate when the local archive contains equally relevant alternatives.
   - **Series familiarity:** maintain a cross-episode fingerprint ledger for recurring hero sources and source-time ranges. If a viewer can recognize a shot or source video as routine member-video filler, replace it even when the exact time range is new. A fresh crop from an overused source is not fresh footage.
   - **Seek safety:** normalize every scheduled video source to CFR delivery fps and a one-second-or-shorter GOP before HyperFrames capture. Sparse-keyframe warnings are release blockers, not informational warnings.
   - **Caption semantics:** build captions from complete spoken sentences or clauses using `references/caption-segmentation.md`; run `scripts/validate_caption_semantics.py` before rendering. Do not split cues by character count or equal duration.
8. Render in reviewable segments, run automated checks, assemble the candidate, and watch it linearly.
   The risk reel must use the planned final audio topology: an approved music bed must be audible at measured post-gain loudness, narration/source speech must hand directly into the fixed ending, and any pause before the outro must be explicitly scripted. A silent watermark or technical-test interval may exist in a QA artifact, but it must not be presented as the viewing candidate.
   For every narration edit, require the producer to follow its `references/audio-boundary-safety.md`: use measured sentence boundaries, prove adjacent source ranges do not overlap, and audition the complete affected sentence chain before accepting the render.
   Require the producer to run `references/regression-lessons.md` after every repair so a local fix cannot reintroduce a previously eliminated opening, audio, picture, sequencing, or ending defect.
9. For narration, listen to the first complete sentence and every generated segment start/end from the rendered candidate. Any stray note, prompt residue, click, breath fragment, duplicated phoneme, or provider mismatch blocks release; ASR/text equality alone cannot pass this gate.
10. Hand the candidate to `$score-social-video`. Treat its fatal gates and score caps as independent release constraints.
    For self-media and paid lessons, add a viewer-value audit before scoring: sample every 30 seconds and record what new knowledge or usable skill was earned; test whether the title/cover/opening promise has already begun paying off by 15 seconds; and answer `会不会停下、会不会看完、学到了什么、为什么值得互动或付费`. Any 45-second span without a new information reward caps the candidate below paid-grade until rewritten or recut.
11. Repair every P0 issue. Repair P1 issues while the target remains unmet. Re-render every affected segment and rescore the assembled candidate.
12. Permit at most three user-visible review rounds total: (1) risk reel/design lock, (2) first full candidate, and (3) bounded local repair. The independent scorer may run internally as often as needed before a user-visible round, but it may not conceal a structural redesign. Never lower the target or weaken a gate to make a candidate pass.
13. If round 2 reveals broad visual direction, asset-family, voice, caption-system, or brand-ending rejection, classify it as a failed preflight, return to the risk reel once, and record why the gate failed. Do not accumulate V4–V9 full renders as the normal workflow.
14. Deliver when the target passes. If the bounded round cannot pass, report the actual score, remaining blockers, and best candidate without calling it final or publishable.

For a requested `98分以上` premium target, interpret the request as an independently audited internal score of `>=9.8/10` (equivalently `>=98/100`), zero fatal gates, completed full linear watch, and completed evidence/provenance ledgers. Never present this as a guarantee of views, retention, or sales.

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
