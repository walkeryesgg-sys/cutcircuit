# Jianying-native TTS on macOS: observed workflow

Verified on 2026-09-08: Jianying 11.4, macOS 14.7.6 Intel, app `VideoFusion-macOS.app`, bundle `com.lemon.lvpro`. A separate draft generated 89 new narration files using the native voice named **利落男声**. User wording “利落男生” refers to this selected UI voice in this task. Future versions must be re-observed, not assumed identical.

## Safety and identity

- Preserve the original draft. Create an independent draft through 文件 → 新建草稿 and inspect the confirmation before accepting it.
- If the console is locked, stop GUI work and ask the user to unlock it. Never bypass lock state.
- Multiple processes can have the same display name. Identify the visible process and the named main window `剪映专业版`; `window 1` can be a tiny unnamed utility window rather than the editor.
- Raise the named main window and verify its screenshot before interaction. Re-observe screen dimensions; physical screenshot pixels and logical click coordinates can differ by 2×.
- Never mutate the new encrypted draft JSON. Local `textReading` media can be read/copied after native generation for preservation and measurement.

## Generation sequence

1. Freeze the complete script as stable semantic IDs. Prepare an **acquisition-only** SRT with enough time for each unit to be generated. Clearly label it not for delivery timing.
2. In 文本 → 导入本地字幕, import this SRT. In the native macOS picker, Cmd-Shift-G opens a nested “go to folder” sheet. Wait for that sheet to exist before entering a directory.
3. If paste/keystroke does not visibly change the path, do not keep submitting blindly. The tested recovery was Accessibility `set value` of the nested sheet's text field to the absolute directory, followed by Return, waiting for the actual directory listing, selecting the SRT, and clicking the visible `导入` button. Reacquire the AX hierarchy each time; do not hard-code stale nested indices.
4. Add the imported SRT asset to the timeline and select its text units. Verify the selected count. Asset drag placement may create a leading offset; this is tolerable only in the acquisition draft and must not become final timing.
5. Open 朗读, search the exact voice label, select its visible card, capture evidence of the selection, and choose 开始朗读. Search may also require AX field-value assignment and Return rather than blind paste.
6. Wait for actual generated audio tracks and files. Record completion evidence. File count alone is not proof of correct spoken content; verify all script IDs through ASR and contextual listening.
7. Preserve the native media, hashes, script hash, app version, voice label and generation screenshots. Files with `.wav` suffix can contain another encoded audio format: probe/decode them with FFmpeg instead of assuming RIFF PCM.

## From generation to edit

- The acquisition SRT's 30-second slots, import offsets and resulting timeline duration are not the film clock. Build the delivery timeline from decoded native durations and verified boundaries.
- Never bind speech by UUID filename sorting or creation order. Retrieve a one-to-one text match, normalize traditional/simplified forms for retrieval, and separately verify numerical wording. Retrieval normalization must not erase numerical errors from the review.
- Keep `proposed_not_verified` and `awaiting_contextual_listening` states honest. An untrimmed standalone dry-voice audition is a QA surface, not a risk reel or a release candidate. It can help a real reviewer check the complete chain without first risking phoneme cuts.
- Final output has one caption owner. Remove/hide acquisition text in the delivery composition; do not stack its text over burned captions in a guide video.
- Native provider evidence, ASR, silence detection, screenshots and actual listening each answer different questions. None of the first four proves the last one happened.
