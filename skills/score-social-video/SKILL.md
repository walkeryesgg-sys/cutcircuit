---
name: score-social-video
description: Evaluate finished self-media and paid-course videos on a 10-point release scale. Use when Codex must review an MP4/MOV, judge whether a video is publishable, diagnose black frames, missing footage, frozen shots, layout overflow, subtitle or audio sync, pacing, storytelling, taste, algorithm-facing retention potential, audience appeal, or compare a new “硬核火星人” video against the account’s successful reference videos.
---

# Score social video

Judge the delivered viewing experience, not whether the render command succeeded.

## Required workflow

1. Read [references/scoring-standard.md](references/scoring-standard.md).
2. For a “硬核火星人” video, also read [references/hardcore-martian-benchmark.md](references/hardcore-martian-benchmark.md).
3. Run `scripts/probe_video.py VIDEO --output REPORT.json` for objective signals.
4. Build a contact sheet that covers:
   - every media window at start, midpoint, and end;
   - every transition;
   - every title/card at its maximum text state;
   - first 3, 15, and 30 seconds;
   - final 10 seconds.
5. Watch the video linearly from beginning to end at least once. Do not replace this with scrubbing or sparse screenshots.
6. Audit speech boundaries and captions separately:
   - do not cut a speaker mid-sentence;
   - compare subtitle onset and exit to audible speech;
   - inspect TTS↔source-audio gaps;
   - verify music never masks speech.
7. Audit visual ownership and seams:
   - measure whether footage is a meaningful viewing surface rather than a small decorative window;
   - inspect every outgoing/incoming media boundary for an uncovered black or empty interval;
   - verify a reusable intro communicates both authority and viewer benefit;
   - verify the outro has enough moving footage and final hold to feel intentional.
8. Apply fatal gates before calculating the weighted score.
9. Compare genre and rhythm with the relevant account benchmark; do not force one benchmark’s cut rate onto every format.
10. Report evidence with timecodes and distinguish observed facts from inferred retention potential.

## Report contract

Return the human-readable verdict and save the same findings as `score-report.json` beside the reviewed candidate. The JSON must contain `verdict`, `score`, `target`, `passed`, `active_cap`, `full_watch_completed`, `fatal_issues`, `issues`, `repair_priority`, and `rescore_required`. Each issue must contain `timecode`, `category`, `severity`, `evidence`, and `fix`.

Return:

- `发布结论`: 不可发布 / 修改后发布 / 可以发布 / 付费级精品
- `总分`: one decimal on a 10-point scale
- `评分上限`: active fatal or quality cap and its reason
- `12项分数`: raw 0–10 plus weighted contribution
- `致命问题`: every release blocker with timecode
- `完整问题表`: timecode, category, severity, evidence, fix
- `算法与人的吸引力`: first-frame stop, 3s, 15s, 30s, mid-retention, completion, save, share, comment, follow-next potential as 高/中/低
- `三问`: 会不会停下、会不会看完、付费是否值得
- `修复优先级`: P0/P1/P2
- `修复后预计分数`
- `是否必须重新完整观看`

Never award `9.0+` from metadata and screenshots alone. Never award `9.5+` without a full linear watch and zero active fatal gates.

Set `passed` to true only when the score reaches the requested target, no fatal gate remains, and all watch requirements for that target are satisfied. Set `rescore_required` to true whenever a proposed repair changes timing, speech, captions, music, media windows, or scene seams.

## Interpretation

- A technically valid file can still be unpublishable.
- “符合算法” means observable retention proxies, never a guaranteed recommendation rate.
- Modern self-media pacing does not mean meaningless cuts, exaggerated claims, or constant sensory overload.
- Taste is judged by coherence, restraint, evidence, emotional accuracy, and brand distinctiveness.
- Reward a shot only when it adds information, emotion, proof, or narrative movement.
