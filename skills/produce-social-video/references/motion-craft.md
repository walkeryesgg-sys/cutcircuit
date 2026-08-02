# Motion craft

Use this reference for programmed camera movement, graphic overlays, kinetic type, or multi-step scene animation. It adapts the official GSAP core, timeline, and performance practices to deterministic video rendering.

## Editorial purpose

Assign every motion one job: reveal, redirect attention, connect two shots, clarify hierarchy, or land a payoff. Remove motion that only advertises the template.

- Use restrained push-ins to increase attention on a person or physical detail.
- Use pull-backs to reveal context or release tension.
- Use lateral movement only when it follows subject direction or connects spatially related information.
- Use scale/position continuity across a cut when it improves the seam; do not force a transition onto unrelated shots.
- Keep original footage visually dominant in evidence-led work. Animate overlays around the evidence, not over the speaker's face or the event's critical action.

## Build one seek-safe timeline

1. Derive durations from the real audio and editorial beat sheet.
2. Create one master timeline with defaults for repeated duration and easing.
3. Add named labels for narrative beats and important seams.
4. Place concurrent or overlapping moves with explicit positions relative to labels. Do not coordinate a scene with scattered delays.
5. Use explicit `fromTo()` states when the renderer may seek directly into the middle of a scene.
6. When multiple `from()` or `fromTo()` tweens touch the same property, set `immediateRender: false` on later tweens when necessary to prevent premature state changes.
7. Verify frames at the start, 25%, 50%, 75%, and end of every animated interval, then verify before/at/after each seam.

For GSAP, prefer this structure:

```javascript
const tl = gsap.timeline({
  paused: true,
  defaults: { duration: 0.6, ease: "power2.out" },
});

tl.addLabel("enter", 0)
  .fromTo(subject, { scale: 1, x: 0 }, { scale: 1.06, x: -18 }, "enter")
  .fromTo(caption, { autoAlpha: 0, y: 20 }, { autoAlpha: 1, y: 0 }, "enter+=0.12")
  .addLabel("hold", 0.8);
```

Drive the timeline from the composition's absolute media time. A frame rendered after seeking must match the same frame rendered linearly.

## Movement language

- Prefer `x`, `y`, `scale`, `rotation`, and `autoAlpha` over `left`, `top`, `width`, or `height`.
- Prefer `power1.out` or `power2.out` for clean entrances, `power2.inOut` or `power3.inOut` for deliberate camera moves, and `none` for constant-speed tracking.
- Reserve bounce, elastic, large overshoot, and conspicuous rotation for content that explicitly supports a playful style.
- Give a camera move time to settle before a hard cut. Avoid cutting during the fastest portion unless velocity matching is intentional and verified.
- Use stagger for related repeated elements, not for unrelated facts. Keep the group readable before the next narration beat.
- Define transform origins intentionally for maps, diagrams, screenshots, and SVG parts.

## Performance and render safety

- Animate transform and opacity wherever possible to avoid layout and paint instability.
- Batch layout reads before writes; do not query geometry repeatedly during frame rendering.
- Apply `will-change` only to elements that animate and remove it when practical.
- Reuse timelines; do not create new tweens every rendered frame.
- Kill or revert inactive animations and framework contexts during cleanup.
- Limit simultaneous blur, shadow, mask, and large full-frame filter animation. Test representative frames at full output resolution.
- Do not use `quickTo()` or pointer/scroll-driven state for offline video timing; drive all motion from deterministic composition time.

## Motion quality gates

Block release when:

- seeking produces a different visual state from linear playback;
- an element flashes at its end state before its entrance;
- the subject leaves the safe crop or becomes soft because digital zoom exceeds useful source resolution;
- an overlay hides the evidence, face, subtitle, or watermark;
- motion continues after the narration beat has landed or resets visibly at a segment boundary;
- movement judders, tears, exposes empty canvas, or causes an unintended black edge;
- easing, speed, or direction changes without editorial reason.

Inspect motion at normal playback speed. A technically correct keyframe sequence still fails when it feels distracting, rushed, or mechanically uniform.
