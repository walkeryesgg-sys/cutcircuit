# Open Design 动态图解母版工作流

Use this reference when an episode uses the Open Design UI system developed for `马斯克商业解读`.

## Design identity

The approved direction is natural, editorial, minimal, and Apple-influenced—not corporate-formal and not a spacecraft HUD:

- warm white or softly tinted canvas;
- generous negative space and system-like typography;
- one oversized fact or relationship per frame;
- restrained blue/orange accents;
- low-density charts and soft causal motion;
- no neon outlines, control-room chrome, dense technical labels, or SaaS-dashboard grids.

## Six reusable template families

1. **Data overview:** one headline number, one comparison, one source/date.
2. **Timeline:** a small number of milestones with the causal change highlighted.
3. **Cost tree:** total → major drivers → controllable/non-controllable boundary.
4. **Causal chain:** payer/input → operating mechanism → output → consequence.
5. **Comparison matrix:** only decision-changing dimensions; reveal rows/columns with narration.
6. **Evidence card:** crop of original filing/document plus highlighted line, plain-language interpretation, and source/date.

Choose a family because it answers a viewer question, never merely to create variety.

## From design to motion

- Treat the Open Design frame as semantic states, not a finished slide to pan across.
- Define `state 0` (what the viewer already knows), `state 1` (new evidence), `state 2` (relationship or contradiction), and `state 3` (takeaway/exit).
- Animate on the same seek-safe master timeline as narration. Each state must be correct when captured directly at any time.
- Prefer opacity, transform, mask, line growth, number interpolation, and restrained camera movement. Avoid constant floating, decorative particles, and simultaneous motion without hierarchy.
- Make narration own timing. A graphic reveal begins near the spoken concept and finishes before the next reasoning step.
- Use transparent-overlay mode when footage should remain the subject. Use full-canvas mode only when the relationship genuinely needs the whole frame.

## Integration contract

For each UI use, record:

| Field | Requirement |
|---|---|
| Viewer question | The exact uncertainty the graphic resolves |
| Template family | One of the six families |
| Source | Document/data provenance and date |
| Narration window | Exact sentence/clauses |
| Semantic states | State 0–3 with timestamps |
| Entry/exit | Motivated seam from/to footage or evidence |
| Density check | Maximum text/data state at 1920×1080 |
| Accessibility | Contrast, safe area, and silent-view legibility |

Reject the graphic when the same point is clearer in a full-screen source shot or one short caption.

## Review gates

- inspect every semantic state, not only the resting frame;
- verify text and numbers at maximum density;
- verify transparent overlays against bright and busy footage;
- check that no UI run becomes a succession of static cards;
- ensure the six families share tokens and motion grammar without repeating identical compositions;
- confirm every chart or calculation can be traced to the evidence ledger.
