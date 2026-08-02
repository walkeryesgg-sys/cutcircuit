---
name: produce-social-video
description: Discover requirements through a mandatory pre-production interview, obtain an explicit brief confirmation, then autonomously plan, script, source, narrate, caption, edit, animate, render, score, repair, and deliver high-quality self-media or paid-course videos. Use when Codex, Claude, Cursor, or another agent must create or substantially revise a social video from a topic, script, source footage, transcript, or asset library while preserving provenance, meeting modern retention practices, and enforcing the score-social-video 10-point release standard.
---

# Produce social video

Create the finished viewing experience, not merely a technically valid MP4.

## Mandatory pre-production gate

Do not start production merely because the user supplies a topic, URL, script, or asset folder. Begin with a short requirements interview, even when the initial request appears detailed.

Before explicit confirmation, allow only read-only discovery needed to ask informed questions: inspect supplied files, existing series defaults, prior approved outputs, and source metadata. Do not download footage, write a script, generate voice or images, edit, render, publish, or mutate project assets.

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

### Brief confirmation

When the material decisions are known, return a compact **制作确认单** containing:

- audience and viewer promise;
- topic, thesis, exclusions, and factual framing;
- video count, duration, platform, aspect ratio, language, and deadline;
- hook and section structure;
- source-footage, narration, captions, voice, music, intro, watermark, outro, and cover treatment;
- deliverables, rights assumptions, and release target;
- any assumptions still being made.

End with one explicit confirmation question. Production begins only after the user clearly approves the confirmation sheet with language such as “确认”“同意”“开始制作” or an equivalent unambiguous instruction. Silence, an unanswered question, an earlier generic “直接做”, or approval of only one sub-decision does not satisfy this gate.

Validate the machine-readable confirmation sheet with `scripts/validate_brief.py`. Do not ask the user to read JSON; show the human summary and keep the validated JSON as the production contract.

If the user changes a material requirement after confirmation, update the confirmation sheet and reconfirm only the changed scope. Small reversible implementation choices do not require renewed approval.

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
2. Read [references/editorial-blueprint.md](references/editorial-blueprint.md) after confirmation and before scripting.
3. Read [references/automation-workflow.md](references/automation-workflow.md) before production.
4. Read [references/toolchain.md](references/toolchain.md) when checking or installing tools.
5. Read [references/release-gates.md](references/release-gates.md) before previews and final render.
6. Read [references/portability.md](references/portability.md) when installing this skill in another agent.
7. Read [references/youtube-sourcing.md](references/youtube-sourcing.md) when YouTube discovery, subtitles, or footage are needed.
8. Read and use `$score-social-video` as the independent evaluation surface. Do not weaken its caps.
9. Read and use `$youtube-research-downloader` for authorized YouTube transfers when the editorial plan identifies a concrete evidence or visual gap. Keep discovery and candidate ranking here; keep transfer, retry, merge, and verification logic in the downloader skill.
10. Read [references/source-led-commentary-template.md](references/source-led-commentary-template.md) when the approved format alternates full-screen source footage, narration, and original-audio evidence, especially for public-facing 4–8 minute videos.

## Production contract

1. Complete the requirements interview and receive explicit approval of the 制作确认单.
2. Run `scripts/doctor.py --json`; surface only missing required tools.
3. Save the approved 制作确认单 using `assets/approved-brief.template.json`; consult `assets/approved-brief.example.json` when mapping plain-language answers. Validate it, then create `video-project.json` with `scripts/init_project.py <project-dir> --subject <subject> --brief-file <file> --confirmed` plus the known audience, platform, and score-target options. The initializer must refuse unconfirmed or incomplete projects.
4. Resolve the delivery identity before editing: intro treatment, spoken-language subtitle policy, watermark, outro copy, voice, and music. Reuse established series defaults recorded in the confirmation sheet; never silently invent missing identity elements.
5. Inventory all supplied assets before sourcing new media. Search YouTube only for a defined evidence or visual gap. For every selected video source, verify both metadata resolution and perceptual resolution from contact-sheet frames at multiple timestamps. A 1080p wrapper around visibly low-resolution footage fails the media gate.
6. Build the editorial blueprint: facts ledger, one-sentence viewer promise, knowledge gap, story spine, emotional curve, evidence map, beat sheet, paper edit, narration, source quotes, and section order. Lock it before full rendering.
7. Generate or resolve all voice tracks early; real audio duration owns the timeline.
   For narration-led videos, preserve human breathing room: default sentence-boundary pauses to 220–380 ms and paragraph/section pauses to 450–750 ms. Do not collapse every detected silence to zero. Preview several consecutive sentences at normal speed and reject delivery that feels rushed even when every word is intelligible.
8. Build a deterministic, seekable composition. Prefer HyperFrames; use another renderer only when the project or user explicitly requires it.
9. Render and inspect the opening 30 seconds first. Judge it as a first-time viewer with no background knowledge; repair it before rendering the remaining chapters.
10. Render each chapter or hard scene group independently. Never make a 10-minute monolithic render the first meaningful QA surface.
11. Run automated black/freeze/silence/media-window/layout checks on every segment. For generated narration, also run speech recognition or an equivalent listening check for noise, missing speech, repeated words, reference-prompt leakage, and caption drift.
12. Assemble segments only after segment gates pass.
13. Run `$score-social-video`, save its machine-readable report as `score-report.json`, and automatically repair P0/P1 findings. The caption gate must report canonical line count, exact text equality, terminal-punctuation policy, overflow status, and a rendered-frame spot check. The media gate must report every source's declared dimensions plus a human/perceptual verdict; metadata alone cannot pass it.
14. Repeat build → test → score for at most three scored repair cycles. Stop early only when the release target passes. Never lower the target or weaken a fatal gate to force a pass.
15. Deliver the final video, score report, provenance ledger, project manifest, and editable source.

## Musk Method series defaults

Apply these defaults to every `马斯克方法论` / `硬核火星人` episode unless the user explicitly overrides them:

- Use the approved high-definition series intro or its latest approved revision. Do not silently redesign it.
- Add timed Chinese subtitles for every English source-audio passage. A persistent topic summary, bilingual label, or evidence card does not count as spoken subtitles. Check coverage from the first spoken word through the last.
- Keep the approved `硬核火星人 / HARDCORE MARTIAN` watermark visible and consistent across the main program. Reuse the established orbit mark, typography, size, opacity, and safe-area placement.
- End with the fixed `硬核火星人` brand outro. Do not announce or invent a next episode.
- Use the approved native Jianying voice (currently `利落男声`) where narration is required; do not substitute a cloned voice without explicit approval.
- When the user confirms Jianying-native TTS, treat the provider choice as a hard requirement: create or update a Jianying text-reading draft and obtain native output. Do not silently fall back to CosyVoice, voice conversion, zero-shot cloning, Edge TTS, or another voice provider merely because it is easier to automate.
- For Jianying narration, retain natural sentence cadence. Removing intentionally inserted source-audio gaps must not produce machine-gun delivery: rebuild the narration timeline with roughly 0.22–0.38 s between sentences and 0.45–0.75 s between paragraphs, then regenerate captions from that exact audio timeline.
- Preserve energetic intro music. Duck it only under speech and restore its intended level between spoken phrases.
- Build from original high-definition footage when available. Reject low-resolution, second-generation, repetitive, or semantically empty shots.
- Caption copy must come from one canonical narration/script manifest. Before release, compare every rendered caption entry character-for-character against that manifest after applying only explicitly approved style transforms. For the current `硬核火星人` series, remove the terminal Chinese full stop `。` from on-screen captions; do not remove or invent any other character. Any missing, duplicated, or substituted caption character is a fatal release failure.
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
