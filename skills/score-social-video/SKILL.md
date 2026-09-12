---
name: score-social-video
description: Evaluate finished self-media and paid-course videos on a 10-point release scale. Use when Codex must review an MP4/MOV, judge whether a video is publishable, diagnose black frames, missing footage, frozen shots, layout overflow, subtitle or audio sync, pacing, storytelling, taste, algorithm-facing retention potential, audience appeal, or compare a new “硬核火星人” video against the account’s successful reference videos.
---

# Score social video

Judge the delivered viewing experience, not whether the render command succeeded.

## Required workflow

1. Read [references/scoring-standard.md](references/scoring-standard.md).
2. For a “硬核火星人” video, also read [references/hardcore-martian-benchmark.md](references/hardcore-martian-benchmark.md).
   For `马斯克商业解读`, also audit the episode against `../produce-social-video/references/musk-business-member-template.md`, including the single explanation engine, question-escalation chain, evidence/interpretation boundary, and footage-to-graphics ratio.
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
   - run `../produce-social-video/scripts/validate_caption_semantics.py --strict CAPTIONS.json` when a canonical caption ledger is available, then manually inspect every warning in context;
   - prefer one complete sentence in one timed cue, even when it wraps to two visual rows; never replace the first half while the spoken sentence is still continuing;
   - inspect TTS↔source-audio gaps;
   - verify music never masks speech.
7. Audit visual ownership and seams:
   - measure whether footage is a meaningful viewing surface rather than a small decorative window;
   - inspect every outgoing/incoming media boundary for an uncovered black or empty interval;
   - verify a reusable intro communicates both authority and viewer benefit;
   - verify the outro has enough moving footage and final hold to feel intentional.
   - reject non-uniformly stretched footage and B-roll that is only brand-adjacent rather than sentence-relevant.
8. Apply fatal gates before calculating the weighted score.
9. Compare genre and rhythm with the relevant account benchmark; do not force one benchmark’s cut rate onto every format.
10. Report evidence with timecodes and distinguish observed facts from inferred retention potential.

## Report contract

Bind the report to the candidate's SHA-256, the canonical script hash, timeline hash, reviewer identity, and review evidence paths. Report normal-speed watch coverage truthfully; starting playback, waiting for its duration, reading a transcript, or looking at contact sheets is not a completed audiovisual watch. If the available review surface cannot expose both moving picture and audible sound, mark that requirement incomplete and withhold a passing premium score. Any changed candidate hash invalidates the prior verdict. For rebuilds, run `../cutcircuit/scripts/validate_timeline.py` and separately audit the narration stem; silence detection on a music-backed mix cannot prove speech continuity.

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
Never award `9.8+` unless every 30-second window has a documented information reward or purposeful dramatic hold, the opening promise starts paying off by 15 seconds, the central model survives at least one limit/counterexample, the Open Design states are inspected at maximum density, and the final candidate has been independently rescored after all repairs.

Set `passed` to true only when the score reaches the requested target, no fatal gate remains, and all watch requirements for that target are satisfied. Set `rescore_required` to true whenever a proposed repair changes timing, speech, captions, music, media windows, or scene seams.

## Interpretation

- A technically valid file can still be unpublishable.
- “符合算法” means observable retention proxies, never a guaranteed recommendation rate.
- Modern self-media pacing does not mean meaningless cuts, exaggerated claims, or constant sensory overload.
- Taste is judged by coherence, restraint, evidence, emotional accuracy, and brand distinctiveness.
- Reward a shot only when it adds information, emotion, proof, or narrative movement.
