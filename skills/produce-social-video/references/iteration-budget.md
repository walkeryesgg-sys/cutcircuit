# Two-to-three-round production budget

Use this workflow to reach paid-content quality without discovering foundational problems in V5–V9.

## Why repeated rework happens

Repeated full renders are usually a gate-order failure, not unavoidable polish. The common pattern is:

1. render before voice, caption, asset family, visual hierarchy, and brand ending are locked;
2. use metadata or contact sheets as substitutes for normal-speed picture review;
3. let the user become the first person to review the opening, seams, captions, and ending together;
4. repair one symptom without running regression checks on adjacent seams;
5. preserve unresolved checkpoints as `false` while continuing to assembly.

The result is cumulative redesign: each review round changes a different foundation and invalidates earlier work.

## Round 0 — internal readiness, not a user review

Do not render the full program until all are true:

- facts, thesis, paper edit, evidence map, source/narration ledger, and canonical script are locked;
- voice provider and exact voice are proven with a clean first sentence;
- captions are generated from the final audio ledger and pass semantic segmentation;
- every source has a semantic role, native aspect-ratio plan, perceptual clarity verdict, playable duration, CFR fps, and seek-safe GOP;
- recent-shot reuse, series watermark, intro, and fixed outro are resolved;
- contact sheets reveal no off-topic filler, repeated motif, slide-like wrapper, distortion, or low-contrast brand element;
- project checkpoint fields accurately reflect these passes. A false prerequisite blocks assembly.

Run independent scoring mentally/locally against the 9.5 standard before spending on a review render. Fix objective defects invisibly inside round 0.

## Round 1 — compact risk reel and design lock

Render a short diagnostic reel containing:

1. the complete opening 30 seconds;
2. one representative source-evidence passage with its real captions;
3. the densest explanation/card/caption state;
4. one narration↔source seam and one chapter seam;
5. one bright and one dark watermark background;
6. the complete fixed ending.

Use real audio, real fonts, real grading, real captions, and final aspect-ratio processing. Do not show placeholders. The user reviews the decisions with the highest subjective cost: tone, footage family, clarity, information style, caption behavior, and brand ending.

Once approved, freeze those decisions in the brief/ledger. Changing them later is a material scope change, not ordinary repair.

## Round 2 — first full candidate

Before showing it:

- render in tested segments and run all objective checks;
- complete the producer's full normal-speed linear watch;
- run independent scoring and repair known P0/P1 defects internally;
- verify the opening and all changed seams again after assembly.

The first full candidate should already be a coherent 9.5 attempt. Never present an obvious draft merely to collect a problem list.

## Round 3 — bounded repair and release

Accept only localized corrections: a small number of shots, caption boundaries, levels, seams, or factual labels. Re-render affected segments, run regression checks, reassemble, rescore, and complete another linear watch.

If round 3 requires a new visual system, wholesale asset replacement, voice replacement, or ending redesign, record a failed preflight. Return once to round 1 rather than calling the new master V4/V5 and continuing indefinitely.

## Required iteration ledger

For each user-visible round record:

- artifact and duration;
- decisions being reviewed;
- objective checks already passed;
- user decisions locked;
- defects found and their missing upstream gate;
- scope permitted in the next round;
- provisional score and active cap.

Version numbers alone are not an iteration ledger.

Start from [`../assets/iteration-ledger.template.md`](../assets/iteration-ledger.template.md). Do not count internal preflight failures as user review rounds; do record them so the failed gate becomes reusable process knowledge.
