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
- viewer-facing dead air before the fixed outro, including a silent technical-test interval not required by the approved script;
- an approved music treatment that is absent, effectively inaudible after gain, discontinuous before the outro, or replaced by unintended silence;
- any unintended sound before, inside, or after narration, including a musical note, reference-prompt residue, click, breath fragment, duplicated phoneme, or synthesis artifact;
- an approved native TTS provider replaced by a clone, voice conversion, zero-shot imitation, or other provider without explicit approval;
- visible playback stutter, repeated/frozen frames, or uneven motion caused by sparse keyframes, VFR timing, frame extraction, or muxing;
- English source speech in a member-original program without real-time synchronized Chinese-English bilingual captions;
- captions divided by equal duration, midpoint character count, or another boundary that visibly replaces text before the spoken sentence/clause completes;
- missing or inconsistent required series watermark;
- full-frame footage forced into a non-native aspect ratio; use scale-and-crop or intentional padding, never geometric stretching;
- B-roll that is merely brand-adjacent but does not support the current spoken claim, such as Tesla factory footage standing in for a rocket-engine argument;
- a `硬核火星人` watermark containing an unapproved English line, placed outside the canonical lower-right safe area, or reconstructed instead of using the canonical asset;
- a required watermark that is technically present but visibly disappears against the scene;
- a source-audio evidence passage presented as a decorative inset inside a slide/page canvas without an approved functional reason;
- an outro teaser or next-episode claim that was not explicitly approved.

Any active fatal issue caps the score according to `$score-social-video`; never average it away.

## Mandatory automated coverage

- Probe every stream and declared media file.
- Inspect every media window at start+0.2s, midpoint, and end−0.2s.
- Inspect every transition before/at/after the cut.
- Inspect every text card at its longest state.
- Generate and inspect a contact sheet before review render; classify every sampled beat as `watch` or `understand` using `visual-hierarchy.md`.
- Detect black, freeze, silence, peak, duration mismatch, and missing assets.
- Sample luma throughout the candidate and inspect the subject at representative dark, median, and bright frames. Passing black-frame detection does not pass exposure: faces, machinery, and evidence details must remain legible on an ordinary display.
- Record bitrate and a blur/softness proxy for every full-frame source, then inspect perceived sharpness, motion blur, focus, and compression at 100%. Metadata resolution alone never passes the clarity gate.
- For the bright-and-clear `硬核火星人` house style, investigate an assembled-program mean YAVG outside roughly 80–110 and any sustained window below 55. These are review triggers, not auto-grading targets; subject visibility and highlight/shadow detail decide the verdict.
- Verify output resolution, fps, codec, duration, audio sample rate, and pixel format.
- Run `scripts/validate_caption_semantics.py` on the canonical caption ledger. Review every warning ending in a function word or opening with an orphaned continuation; no high-risk mid-clause split may remain in paid content.
- Probe every scheduled B-roll window against the file's native playable duration; assumed six-second windows over three-second assets are a black-frame defect, even when the HTML timeline is continuous.
- Compare every scheduled source's display aspect ratio with its native aspect ratio and inspect the actual output crop. Any non-uniform scale fails before render.
- Attach each B-roll window to the exact narration sentence or evidence beat it supports. A filename, company, or general technology theme is not sufficient semantic relevance.
- Report distinct-shot reuse counts and block paid-content release when a shot appears more than twice without an approved narrative reason.
- Compare source-video IDs/paths and perceptual fingerprints against recent series episodes. Treat a new crop or unused timestamp from an overexposed recurring source as familiar reuse, not as a new visual family.
- Require sparse-keyframe source clips to pass start/mid/end seek tests or be rebuilt to a seek-safe GOP before the full render.
- Normalize every scheduled source to CFR at the delivery frame rate and a GOP no longer than one second before HyperFrames capture. Treat compiler sparse-keyframe warnings as failed prerequisites; do not proceed to a monolithic final render with warnings active.
- Run freeze/repeated-frame detection on the assembled candidate, then watch every flagged interval and at least one fast-motion interval per source at normal speed. A sharp contact-sheet frame cannot pass motion smoothness.
- Measure integrated loudness and true peak; for the `硬核火星人` online master review around -16 LUFS and require true peak at or below -1 dBTP unless an approved platform specification overrides it.
- Export or analyze the post-gain music bus separately from dialogue. Track presence is not evidence of audibility; record its measured level and listen to the opening, a dense speech passage, the final conclusion, and the outro.

## Mandatory experiential coverage

- Watch first 30 seconds at normal speed.
- Listen to the first complete narration sentence with the picture hidden or eyes closed. Confirm that audio begins with the canonical first phoneme and contains no note, tone, prompt residue, click, or extra syllable.
- Listen to the start and end of every generated TTS asset in the assembled candidate, not only the source WAV. Record pass/fail in the release report.
- Verify voice provenance against the approved brief: provider, exact voice name/ID, generation artifact, and rendered-file binding must all match. Similar timbre is not provenance.
- Run a cold-viewer comprehension check without relying on the project brief: after 30 seconds, the reviewer must be able to state who/what the video concerns, the central question, why it matters, and what payoff is promised. If any answer is missing, revise the opening.
- At the first source excerpt, verify that a viewer unfamiliar with the original material can identify the speaker, subject, relevant background, and reason the excerpt is evidence.
- Confirm a reusable series intro communicates both subject authority and the viewer's practical reward; biography or spectacle alone does not pass.
- Watch every source↔TTS boundary.
- 连续试听至少 5 组相邻句子：句间停顿应自然且一致，不能紧迫得像倍速播报，也不能出现超过 1 秒的无意静音。
- 对每个原声窗口核对原文、翻译、时间码和邻接旁白的语义关系；任何静音、错句或无关发言均为发布阻断项。
- 原声字幕必须来自逐段时间码；整段主题概述不能冒充逐句翻译，也不能通过字幕覆盖率验收。
- 对每个额外 B-roll 窗口核对逐句相关性；泛科技填充、无关网页/引文截图和重复素材必须删除。
- Watch each chapter transition.
- Watch final 15 seconds.
- Confirm the final 15 seconds contain a completed conclusion, a perceptible musical lift or deliberate release, and a motivated transition into the fixed outro; an abrupt cut from an unfinished teaching beat fails.
- Verify the final conclusion answers the opening question in language a beginner can repeat without specialist vocabulary.
- Verify each main chapter contains an evidence-bounded program judgment or decision rule beyond source paraphrase, and that the viewer can distinguish it from the speaker's original claim.
- Verify every foreign-language source-audio interval against a subtitle-coverage ledger; topic summaries do not satisfy this check.
- For member-original English sources, verify Chinese and English lines are generated from the same cue start/end values, cover the complete audible interval, and remain perceptibly synchronized at the beginning, middle, and end of every excerpt.
- Verify a looped music bed at every loop boundary for clicks, gaps, gain jumps, and tempo discontinuity; verify the normal program bed uses one fixed gain apart from approved intro/outro fades.
- Verify the series watermark at the start, midpoint, and end of every materially different scene style.
- Confirm captions remain in the lower safe area unless each exception avoids a verified collision.
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
- bright, clean subject separation without sharpening halos, crunchy skin, clipped whites, crushed blacks, or template-like overgrading;
- no meaningless fast cuts, fake suspense, or marketing-noise overload.
- real footage is visually substantial rather than reduced to a decorative thumbnail; for evidence-led courses, use roughly 40:60 graphics-to-footage overall and full-screen source during source audio unless an approved functional comparison requires otherwise.
- no persistent white/light presentation canvas wrapping live footage; brightness must come from footage correction and clear hierarchy, not a slide shell.
- adjacent media changes contain no exposed black/empty interval; use a hard cut or 4–8-frame overlap.
- a cinematic outro has time to resolve: moving hero footage around 6 seconds or longer and a readable final hold around 0.8–1.2 seconds.

## Threshold

- `>=9.0`: publishable.
- `>=9.5`: paid-content quality.
- `>=9.8`: premium, with no fatal gate and completed full watch.
