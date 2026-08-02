# Audio boundary safety

Apply this procedure whenever narration or source speech is trimmed, split, replaced, reordered, or concatenated.

## Build the boundary ledger

1. Derive word or phrase timestamps from the actual final audio, not estimated reading speed.
2. Run silence detection only as a locator. Confirm each proposed boundary against the transcript and by normal-speed listening.
3. Record for every speech unit: canonical text, source file, audible start, audible end, chosen trim start, chosen trim end, and destination interval.
4. Place cuts inside verified silence. Preserve roughly 220–380 ms between sentences unless the approved performance clearly requires another cadence.

## Prove continuity before rendering

- Require `trim_end <= next_trim_start` for adjacent ranges from the same source. Any overlap is a repeated-word risk and blocks rendering.
- Ensure the chosen end follows the last audible phoneme. Cutting at an estimated duration or caption boundary is forbidden.
- Ensure the next start precedes its first intended phoneme but follows every phoneme belonging to the previous sentence.
- Pad with silence to preserve destination duration when shortening a replacement. Do not pull the next sentence earlier merely to fill a visual slot.
- Regenerate captions from the final audio map or shift them from the same ledger. Never maintain an independent hand-entered timing map.

## Regression test every affected seam

1. Export a review clip beginning at least one complete sentence before the edit and ending at least one complete sentence after it.
2. Listen at normal speed without seeking. Verify exact canonical wording: no missing final character, leading residue, repeated word or phrase, click, abrupt breath, or unnatural pause.
3. Compare the concatenated spoken-token sequence with the canonical script. Treat missing, substituted, or duplicated tokens as a fatal failure.
4. Run silence and peak checks, but never use them as proof of semantic correctness.
5. Recheck the assembled master after muxing; a passing source segment does not prove the final file.

## Known failure patterns

- **Truncated sentence ending:** the trim ended before the last phoneme because caption or estimated duration was treated as speech duration.
- **Leading residue:** the next clip began before the prior sentence's final phoneme had ended.
- **Repeated phrase:** adjacent source ranges overlapped, often after repairing only one side of a seam.
- **Patch cascade:** repeated local fixes changed one boundary while leaving the neighboring boundary stale. Rebuild the complete local sentence chain instead of patching one clip in isolation.

Do not label a speech edit final until the ledger checks and the normal-speed seam audition both pass.
