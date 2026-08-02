# Release gates

## Fatal gate

Block release for:

- black/missing/frozen media;
- text overflow, clipping, unsafe-area failure, or production labels;
- interrupted speech or obvious subtitle drift;
- unintended silence, clipping, or music masking voice;
- unsupported factual claims presented as fact;
- material rights/privacy risk;
- broken opening or ending.
- untranslated English source speech in a Chinese-language program;
- missing or inconsistent required series watermark;
- an outro teaser or next-episode claim that was not explicitly approved.

Any active fatal issue caps the score according to `$score-social-video`; never average it away.

## Mandatory automated coverage

- Probe every stream and declared media file.
- Inspect every media window at start+0.2s, midpoint, and end−0.2s.
- Inspect every transition before/at/after the cut.
- Inspect every text card at its longest state.
- Detect black, freeze, silence, peak, duration mismatch, and missing assets.
- Sample luma throughout the candidate and inspect the subject at representative dark, median, and bright frames. Passing black-frame detection does not pass exposure: faces, machinery, and evidence details must remain legible on an ordinary display.
- Verify output resolution, fps, codec, duration, audio sample rate, and pixel format.

## Mandatory experiential coverage

- Watch first 30 seconds at normal speed.
- Run a cold-viewer comprehension check without relying on the project brief: after 30 seconds, the reviewer must be able to state who/what the video concerns, the central question, why it matters, and what payoff is promised. If any answer is missing, revise the opening.
- At the first source excerpt, verify that a viewer unfamiliar with the original material can identify the speaker, subject, relevant background, and reason the excerpt is evidence.
- Confirm a reusable series intro communicates both subject authority and the viewer's practical reward; biography or spectacle alone does not pass.
- Watch every source↔TTS boundary.
- 连续试听至少 5 组相邻句子：句间停顿应自然且一致，不能紧迫得像倍速播报，也不能出现超过 1 秒的无意静音。
- 对每个原声窗口核对原文、翻译、时间码和邻接旁白的语义关系；任何静音、错句或无关发言均为发布阻断项。
- 对每个额外 B-roll 窗口核对逐句相关性；泛科技填充、无关网页/引文截图和重复素材必须删除。
- Watch each chapter transition.
- Watch final 15 seconds.
- Verify the final conclusion answers the opening question in language a beginner can repeat without specialist vocabulary.
- Verify every foreign-language source-audio interval against a subtitle-coverage ledger; topic summaries do not satisfy this check.
- Verify the series watermark at the start, midpoint, and end of the main program.
- Verify the outro uses the approved fixed brand copy and contains no invented next-episode preview.
- For paid or 9.5+ delivery, watch the entire video linearly.

## Attraction and taste

Check:

- effective first frame;
- 3-second stop potential;
- 15-second curiosity and promised reward;
- 30-second topic clarity;
- new question/evidence/story/payoff through the middle;
- memorable conclusion;
- save/share/comment/follow-next reasons;
- coherent, restrained, recognizable taste;
- a dark palette without crushed subject detail; overlays and gradients must support text contrast without making footage feel dim or muddy;
- no meaningless fast cuts, fake suspense, or marketing-noise overload.
- real footage is visually substantial rather than reduced to a decorative thumbnail; for evidence-led courses, use roughly 40:60 graphics-to-footage overall and at least 65% frame ownership during source-audio evidence unless a deliberate full-frame diagram is required.
- adjacent media changes contain no exposed black/empty interval; use a hard cut or 4–8-frame overlap.
- a cinematic outro has time to resolve: moving hero footage around 6 seconds or longer and a readable final hold around 0.8–1.2 seconds.

## Threshold

- `>=9.0`: publishable.
- `>=9.5`: paid-content quality.
- `>=9.8`: premium, with no fatal gate and completed full watch.
