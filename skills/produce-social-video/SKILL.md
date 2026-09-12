---
name: produce-social-video
description: Discover requirements through a mandatory pre-production interview, obtain an explicit brief confirmation, then autonomously plan, script, source, narrate, caption, edit, animate, render, score, repair, and deliver high-quality self-media or paid-course videos. Use when Codex, Claude, Cursor, or another agent must create or substantially revise a social video from a topic, script, source footage, transcript, or asset library while preserving provenance, meeting modern retention practices, and enforcing the score-social-video 10-point release standard.
---

# Produce social video

Create the finished viewing experience, not merely a technically valid MP4.

## Mandatory pre-production gate

Authorization precedence: an explicit request to design and produce from scratch, with permission to revise the script, authorizes those stages. Record the current instruction and make a concrete plan before production; continue without repeating an approval question. The interview/version-approval procedure below applies to unresolved or not-yet-authorized production. Established series defaults need no new interview. Read `../cutcircuit/references/verified-production.md` for rebuilds and premium production, and run its shared-timeline validator before rendering.

Do not start production merely because the user supplies a topic, URL, script, or asset folder. Begin with a short requirements interview, even when the initial request appears detailed.

Before explicit confirmation, allow read-only discovery and planning work: inspect supplied files, existing series defaults, prior approved outputs, source metadata, and transcripts already supplied or safely available without material acquisition. Write the proposed script and planning documents, but do not download production footage, generate voice or images, edit, animate, render, publish, or mutate supplied project assets.

### Requirements interview

Read [references/novice-intake.md](references/novice-intake.md) and conduct the interview in the user's language. Assume no knowledge of editing terminology.

Ask concise questions in small batches, prioritizing decisions that change the finished viewing experience. Establish:

1. **Goal and audience** — publication goal, target viewer, assumed background knowledge, and the action or impression the viewer should leave with.
2. **Topic and editorial boundary** — central question, required claims, excluded themes, desired stance, and whether disputed claims need neutral framing.
3. **Format and platform** — platform(s), aspect ratio, target duration, number of videos, language, and deadline.
4. **Structure and tone** — hook style, narration/source-audio balance, pacing, emotional register, and reference examples.
5. **Assets and rights** — supplied footage, must-use moments, sourcing permission, brand assets, speaker likeness, and rights constraints.
6. **Delivery identity** — intro, captions, watermark, outro, TTS voice, music, cover image, titles, descriptions, and editable-source requirements.
7. **Acceptance criteria** — what previously made a video unusable, non-negotiable quality requirements, and how approval will be judged.

Do not ask the user to repeat established series defaults or facts that can be discovered locally. Translate specialist choices into viewer-facing consequences. Recommend one option first, explain it in one sentence, and allow “你帮我决定” as a complete answer. Ask no more than three questions in one message unless the user explicitly requests a full questionnaire.

### Professional pre-production plan

After the requirements interview, read [references/preproduction-plan.md](references/preproduction-plan.md) and create a reviewable plan from [assets/preproduction-plan.template.md](assets/preproduction-plan.template.md). Do not reduce the plan to a short creative brief. Include enough detail for the user to understand what will be said, what will be shown, how the story progresses, and how quality will be judged before production cost is incurred.

The plan must contain:

- audience and viewer promise;
- topic, thesis, exclusions, and factual framing;
- video count, duration, platform, aspect ratio, language, and deadline;
- complete narration/dialogue script with source-audio quotations clearly separated;
- time-budgeted narrative structure and beat sheet;
- shot list mapping every spoken unit to its visual purpose and intended source;
- storyboard panels or textual frames showing composition, action, captions, overlays, transitions, and approximate duration;
- source-footage, motion, narration, captions, voice, music, sound design, intro, watermark, outro, and cover treatment;
- asset/source list with must-use moments, missing-material plan, provenance, rights assumptions, and substitutes;
- deliverables, rights assumptions, and release target;
- technical delivery specification, QA gates, known risks, fallbacks, and assumptions still being made.

For short or simple work, concise textual storyboard panels are acceptable. For complex, branded, paid, or `9.5+` work, provide scene-by-scene rows with time ranges. Never use “按素材灵活处理” as a substitute for planning the core viewing experience.

### Plan confirmation

Return the plan with a compact **制作确认单** summarizing the binding decisions. Assign a visible plan version such as `v1`. End with one explicit confirmation question that names that version.

Production begins only after the user clearly approves the complete plan version with language such as “确认 v1”“同意这个制作方案”“按这版开始制作” or an equivalent unambiguous instruction. Silence, an unanswered question, an earlier generic “直接做”, approval of only one sub-decision, or approval given before the plan was presented does not satisfy this gate.

Record the approved plan version, approval statement, and planning artifact paths in `assets/approved-brief.template.json`. Validate the machine-readable contract with `scripts/validate_brief.py`. Do not ask the user to read JSON; show the human plan and keep the validated JSON as the production contract.

If the user changes a material requirement after confirmation, increment the plan version, update the affected plan sections and confirmation sheet, and reconfirm the changed scope. Small reversible implementation choices do not require renewed approval.

## Autonomous production after confirmation

After confirmation, operate autonomously and make reasonable creative and technical decisions without requesting approval at every stage.

Communicate on two layers:

- show the novice user outcomes, choices, visible risks, previews, and plain-language quality judgments;
- keep codecs, filters, timing math, render commands, repair logs, and other implementation detail inside project artifacts unless the user asks.

Act as the integrated director, researcher, story editor, picture editor, motion designer, sound editor, caption editor, and release producer. Do not make the user coordinate these roles.

Pause only when:

- the confirmed subject/input becomes genuinely unavailable;
- a central factual claim cannot be verified or safely qualified;
- source rights, privacy, or likeness risk is material and unresolved;
- an action requires payment, account login, publication, or external messaging;
- two confirmed requirements conflict and materially change the outcome.

Record assumptions in the project manifest and continue. Do not turn reversible layout, pacing, music, voice, or transition decisions into approval gates.

## Required reads

1. Read [references/novice-intake.md](references/novice-intake.md) before asking production questions.
2. Read [references/editorial-blueprint.md](references/editorial-blueprint.md) and [references/preproduction-plan.md](references/preproduction-plan.md) after the interview and before presenting the production plan.
3. Read [references/automation-workflow.md](references/automation-workflow.md) before production.
4. Read [references/toolchain.md](references/toolchain.md) when checking or installing tools.
5. Read [references/release-gates.md](references/release-gates.md) before previews and final render.
6. Read [references/audio-boundary-safety.md](references/audio-boundary-safety.md) before trimming, splitting, replacing, or concatenating narration or source speech.
7. Read [references/picture-quality.md](references/picture-quality.md) before selecting, grading, or approving full-frame footage.
8. Read [references/iteration-budget.md](references/iteration-budget.md) before the first render and enforce its risk-reel and round-budget gates.
9. Read [references/caption-segmentation.md](references/caption-segmentation.md) before generating narration or source captions.
10. For a `硬核火星人` video, classify it with [references/hardcore-martian-program-types.md](references/hardcore-martian-program-types.md). If it is `member_original`, also read [references/hardcore-martian-member-standard.md](references/hardcore-martian-member-standard.md).
    If it is a `马斯克商业解读` member original, also read [references/musk-business-member-template.md](references/musk-business-member-template.md). When programmed explanation UI is planned, read [references/opendesign-motion-ui.md](references/opendesign-motion-ui.md).
11. Read [references/portability.md](references/portability.md) when installing this skill in another agent.
12. Read [references/youtube-sourcing.md](references/youtube-sourcing.md) when YouTube discovery, subtitles, or footage are needed.
13. Read and use `$score-social-video` as the independent evaluation surface. Do not weaken its caps.
14. Read and use `$youtube-research-downloader` for authorized YouTube transfers when the editorial plan identifies a concrete evidence or visual gap. Keep discovery and candidate ranking here; keep transfer, retry, merge, and verification logic in the downloader skill.
15. Read [references/source-led-commentary-template.md](references/source-led-commentary-template.md) when the approved format alternates full-screen source footage, narration, and original-audio evidence, especially for public-facing 4–8 minute videos.
16. Read [references/character-pressure-moment-short.md](references/character-pressure-moment-short.md) when making a 25–60 second public `character_pressure_moment` short built around a person's visible reaction to one high-stakes event.
17. Read [references/motion-craft.md](references/motion-craft.md) before programming camera moves, animated overlays, kinetic typography, or multi-step scene motion.
18. Read [references/regression-lessons.md](references/regression-lessons.md) before approving the opening, after every local repair, and before the final linear watch.
19. For an explicit self-learning or continuous-optimization request, read [references/creator-learning-loop.md](references/creator-learning-loop.md). Keep observations, hypotheses, experiments, and confirmed rules separate; never silently generalize one creator's mannerisms into the house style.
20. For this user's future business videos or “流水账 / 没重点 / 记不住” feedback, read [references/five-minute-focus-and-recall.md](references/five-minute-focus-and-recall.md). The 2026-09-09 house default is about five minutes including the outro. Scope one question before TTS; use a cut list and actual recall evidence, not a new-concept quota.

## Production contract

1. Complete the requirements interview, deliver the full professional pre-production plan, and receive explicit approval of its named version.
2. Run `scripts/doctor.py --json`; surface only missing required tools.
3. Save the approved plan contract using `assets/approved-brief.template.json`; consult `assets/approved-brief.example.json` when mapping plain-language answers. Record its version, approval statement, and plan artifact paths. Validate it, then create `video-project.json` with `scripts/init_project.py <project-dir> --subject <subject> --brief-file <file> --confirmed` plus the known audience, platform, and score-target options. The initializer must refuse unconfirmed or incomplete projects.
4. Resolve `creative.program_type` and `creative.edit_model` before editing, then resolve the delivery identity: intro treatment, spoken-language subtitle policy, watermark, outro copy, voice, and music. Reuse established series defaults recorded in the confirmation sheet; never silently invent missing identity elements.
5. Inventory all supplied assets before sourcing new media. Search YouTube only for a defined evidence or visual gap. For every selected video source, verify both metadata resolution and perceptual resolution from contact-sheet frames at multiple timestamps. A 1080p wrapper around visibly low-resolution footage fails the media gate.
6. Execute the approved editorial blueprint: facts ledger, one-sentence viewer promise, knowledge gap, story spine, emotional curve, evidence map, beat sheet, paper edit, narration, source quotes, shot list, storyboard, and section order. Do not silently replace its central structure after approval.
   Before voice generation, run an editorial-contribution pass. For every major source/evidence block, record: `证据说了什么`、`我们怎么看`、`这个判断改变什么`、`边界在哪里`. At least one non-trivial claim in each main chapter must be the program's own evidence-bounded interpretation or decision rule, clearly distinguished from the source speaker's words. Mere paraphrase, chronology, or neutral enumeration does not pass.
7. Generate or resolve all voice tracks early; real audio duration owns the timeline.
   For narration-led videos, preserve human breathing room. Reference ranges of 220–380 ms at sentence boundaries and 450–750 ms at paragraphs describe the TOTAL audible gap, never padding added on top of native pauses. Preserve approved natural cadence; do not force every boundary into a range or collapse every silence to zero. Preview consecutive sentences at normal speed and reject both dragging and rushed delivery.
   Never derive TTS cuts from estimated reading time. Build and validate a sentence-boundary ledger from the actual waveform/transcript, then trim only inside verified silence. Adjacent source ranges must neither overlap nor omit speech.
8. Build a deterministic, seekable composition. Prefer HyperFrames; use another renderer only when the project or user explicitly requires it.
   Treat motion as editorial emphasis, not decoration. Synchronize it to the narration and picture beats on one labeled timeline, use explicit start and end states, and keep the subject legible throughout the move.
9. Render and inspect a compact risk reel before any full-length render. It must include the opening 30 seconds plus representative evidence, the densest explanation/caption state, a source↔narration seam, and the ending. Judge it as a first-time viewer and as a brand/technical gate; lock its accepted decisions before rendering the remaining chapters.
   Use the intended final music/audio structure in that reel. Do not append silent technical-test seconds before the branded ending. The last spoken line, music continuation, and fixed outro must form one continuous viewing experience; measure any gap and fail an unintended pause over 0.75 seconds.
10. Render each chapter or hard scene group independently. Never make a 10-minute monolithic render the first meaningful QA surface.
11. Run automated black/freeze/silence/media-window/layout checks on every segment. For generated narration, also run speech recognition or an equivalent listening check for noise, missing speech, repeated words, reference-prompt leakage, and caption drift. After any speech-boundary edit, audition from the preceding complete sentence through the following complete sentence at normal speed; waveform metrics alone cannot pass this gate.
12. Assemble segments only after segment gates pass.
13. Run `$score-social-video`, save its machine-readable report as `score-report.json`, and automatically repair P0/P1 findings. The caption gate must report canonical line count, exact text equality, semantic-boundary validation, terminal-punctuation policy, overflow status, and a rendered-frame spot check. The media gate must report every source's declared dimensions plus a human/perceptual verdict; metadata alone cannot pass it.
14. Keep user-visible review to the three-round budget in `references/iteration-budget.md`: risk reel, full candidate, bounded repair. Run internal build/test/score passes before presenting each round. Stop early only when the release target passes. Never lower the target or weaken a fatal gate to force a pass.
15. Deliver the final video, score report, provenance ledger, project manifest, and editable source.

## Musk Method series defaults

Apply these defaults to every `马斯克方法论` / `硬核火星人` episode unless the user explicitly overrides them:

- Use the approved high-definition series intro or its latest approved revision. Do not silently redesign it.
- Add timed Chinese subtitles for every English source-audio passage. A persistent topic summary, bilingual label, or evidence card does not count as spoken subtitles. Check coverage from the first spoken word through the last.
- Keep the approved orbit-mark plus Chinese-only `硬核火星人` watermark visible and consistent across the main program. Use `assets/hardcore-martian-watermark-zh.svg` in the lower-right safe area; do not add an English watermark line or replace it with an upper-left label.
- End with the fixed `硬核火星人` brand outro. Do not announce or invent a next episode.
- Use the approved native Jianying voice (currently `利落男声`) where narration is required; do not substitute a cloned voice without explicit approval.
- When the user confirms Jianying-native TTS, treat the provider choice as a hard requirement: create or update a Jianying text-reading draft and obtain native output. Do not silently fall back to CosyVoice, voice conversion, zero-shot cloning, Edge TTS, or another voice provider merely because it is easier to automate.
- For Jianying narration, retain the approved natural cadence. Measure total audible gaps including native silence; never add 0.22–0.38 s / 0.45–0.75 s padding automatically. Repair excess gaps only with boundary evidence and continuous audition, then regenerate captions from the exact resulting timeline. Do not regenerate an already approved voice track merely to meet heuristic pause ranges.
- Preserve the approved music treatment. For the current user's stable-bed preference, maintain steady gain during normal playback; only music changes and the ending use fades. Do not pump the bed between spoken phrases.
- Build from original high-definition footage when available. Reject low-resolution, second-generation, repetitive, or semantically empty shots.
- Treat familiarity as a picture defect for paid series: compare source-file and perceptual fingerprints with recent member episodes. Replace an overused source video even when selecting a nominally unused timestamp or crop; do not make recurring Tesla-factory, launch, landing, or interview footage the default connective tissue.
- Default to a bright, clear house image. Apply source-specific exposure, gentle tonal contrast, restrained color, and output-size-aware sharpening in the order defined by `picture-quality.md`; never use a global dark wash or aggressive sharpening as a substitute for better footage.
- Caption copy must come from one canonical narration/script manifest. Segment it by complete sentence or natural clause boundaries, never by equal duration or midpoint character count. Prefer one cue for a complete sentence; when it is visually too long, wrap that same cue to two lines instead of replacing it halfway through a clause. Before release, run `scripts/validate_caption_semantics.py` and compare every rendered caption entry character-for-character against the manifest after applying only explicitly approved style transforms. For the current `硬核火星人` series, remove the terminal Chinese full stop `。` from on-screen captions; do not remove or invent any other character. Any missing, duplicated, substituted, or high-risk mid-clause break is a release failure.
- Treat declared file dimensions as insufficient proof of picture quality. Reject footage whose container reports 720p/1080p but whose visible source is an upscaled low-resolution recording, heavily compressed repost, blurred crop, or second-generation capture. Main-program footage must be visibly native 720p or better, with native 1080p preferred; legacy low-resolution footage is allowed only as a deliberately small evidence insert after explicit approval, never as a full-frame B-roll shot.

Treat missing English-source subtitle coverage, a missing series watermark, an unapproved outro teaser, or deviation from the approved intro/voice as fatal release-gate failures for paid content.

## Release targets

- Ordinary publishable self-media: no fatal issues and score `>= 9.0`.
- Paid content: no fatal issues and score `>= 9.5`.
- Premium target: score `>= 9.8`, plus a full linear watch.
- “专业剪辑师级”“顶级”“百万剪辑师式”等 quality requests: target at least `9.5`, require a full linear watch, and report evidence. Treat these as craft standards, never as a promise of views or virality.

Never describe an artifact as final when active fatal gates remain. Never claim a “100-point video” from metadata, sparse screenshots, or a successful renderer exit code.

## Creative principles

- Give the first frame a visible subject.
- Establish person/action/conflict/result within 3 seconds.
- State the topic and viewing reward within 30 seconds.
- Make complexity invisible to the novice user, not absent from the finished work. The agent owns format, pacing, codec, cut rhythm, layout, mixing, subtitle timing, visual sourcing, and repair decisions unless the user explicitly wants creative control.
- For interviews, debates, and source-led commentary, assume the viewer has not seen the original. Before asking the viewer to interpret a conflict, establish who is speaking, when and where the exchange occurred, what question is being disputed, and why it matters in plain language.
- Make narration bridge source excerpts causally: setup → source evidence → interpretation → consequence. Never drop viewers into a quotation whose subject, pronouns, or stakes depend on omitted context.
- Insert source audio only when the exact audible sentence is transcribed, translated, and semantically tied to the adjacent narration. A silent window or a merely on-topic interview shot is not a valid source excerpt. If that evidence cannot be verified, keep continuous narration instead.
- A reusable series intro must establish both brand authority and viewer utility. It may present the subject's achievements, but it must also say what thinking, decisions, or actions the viewer will learn; biography alone is not a value proposition.
- Use story, evidence, source audio, data, and visual imagination in purposeful alternation.
- Make every shot add information, proof, emotion, or narrative movement.
- Require a sentence-to-shot relevance note for every inserted B-roll window. Reject generic technology montages, unrelated documents/screenshots, repeated filler, or imagery whose meaning cannot be explained in one sentence. When in doubt, retain the authoritative high-definition source interview shot.
- Match cut density to genre; do not confuse fast cutting with retention.
- In evidence-led courses, real footage should visually dominate whenever useful footage exists. Treat graphics as explanation overlays, not the default full-frame substitute: target roughly 40% designed explanation to 60% real footage overall, and let source-audio passages devote at least 65% of the frame to the speaker or evidence.
- Never expose an empty/black background while changing media. Adjacent B-roll should hard-cut or overlap by 4–8 frames; if the next asset is unavailable, extend the previous approved shot with a restrained crop/zoom rather than leaving a gap.
- Keep captions readable in silent viewing.
- Align source-language captions to audible phrase boundaries, not just broad clip ranges. Treat perceptible subtitle delay, missing spoken-caption coverage, TTS noise, and inaudible narration as release-blocking defects.
- Treat music as emotional structure and mix it under speech.
- A review candidate longer than 30 seconds must demonstrate the approved music treatment unless the brief explicitly chooses silence. Verify the post-gain bed is audible, stable under speech, continuous across the last spoken line, and naturally faded through the fixed outro.
- End by answering the opening question and leaving one repeatable conclusion. A cinematic series outro should normally breathe for 7–9 seconds, keep its hero footage moving for at least 6 seconds, and hold the final lockup for 0.8–1.2 seconds.
- Prefer coherent taste, restraint, and brand identity over template spectacle.

## Efficiency and recovery

- Cache transcripts, TTS, probes, thumbnails, and rendered segments by content hash.
- Preserve successful segments across revisions.
- Use versioned outputs; never overwrite the last approved artifact.
- Keep a resumable state file after every major stage.
- Tune render concurrency from available RAM; prefer stability over maximum workers.
- For long videos, concatenate validated chapter renders and perform one final audio continuity pass.

## Completion report

Lead with a novice-readable verdict: what was made, who it is for, what the first 30 seconds promise, and whether it is safe to publish. Then return:

- final path, resolution, fps, codec, duration, and size;
- release score and active cap;
- segment coverage and full-watch status;
- repairs performed;
- provenance/rights warnings;
- remaining non-blocking limitations;
- editable project and manifest paths.

## YouTube capability

Use `scripts/youtube_media.py` to:

- search YouTube and return structured candidate metadata;
- inspect a video before downloading;
- download authorized public video at up to 1080P;
- download English/Chinese creator or automatic subtitles;
- save thumbnail, source metadata, and a provenance record.

Rank candidates by relevance, authority, visual usefulness, recency when relevant, subtitle availability, resolution, rights risk, and duplication with local assets. Never download a candidate merely because it ranks first.
