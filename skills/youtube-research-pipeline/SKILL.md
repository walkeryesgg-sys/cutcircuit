---
name: youtube-research-pipeline
description: Discover, collect, score, subtitle, deduplicate, and queue long-form YouTube research videos. Use when Codex needs to search YouTube by topic or creator, expand from seed videos/channels, fetch video metadata and captions, detect reposts or event variants, choose canonical sources, build a download queue, resume interrupted collection, or audit an existing videos.json archive.
---

# YouTube Research Pipeline

Build an auditable candidate-to-canonical-source pipeline. Keep discovery broad; apply quality and duplicate decisions only after metadata and captions are available.

## Workflow

1. Inspect the workspace for an existing dataset, state file, caption directory, and project-specific scripts. Preserve them.
2. Create or reuse a project config. Read [quality-policy.md](references/quality-policy.md) when tuning search, scoring, or canonical selection. Read [schemas.md](references/schemas.md) when changing data formats.
3. Discover candidates through at least two routes:
   - topic/format queries;
   - seed creator/channel expansion.
4. Append candidates by video ID. Never discard candidates solely because their title lacks `interview`, `talk`, or `presentation`.
5. Score provenance, continuity, speaker participation, information density, field access, captions, resolution, and creator trust. Record every rejection reason.
6. Fetch English/original captions before semantic deduplication. Preserve subtitle status and receipts.
7. Deduplicate in layers: exact video ID, metadata similarity, caption fingerprint, then event grouping. Retain one canonical source plus mirrors and clips; do not silently delete provenance.
8. Generate a ranked download queue. Download media only when the user requests it and copyright/access conditions permit.
9. Save state after each page/video so quota or network failures resume safely.

## Commands

Use `scripts/video_pipeline.py` from the project directory.

Discover by diverse queries:

```bash
python3 <skill>/scripts/video_pipeline.py discover \
  --query "Elon Musk factory tour" \
  --query "inside SpaceX with Elon Musk" \
  --limit 30 --output data/candidates.json
```

Expand a promising creator without knowing every creator beforehand:

```bash
python3 <skill>/scripts/video_pipeline.py channel \
  --channel-url "https://www.youtube.com/@EverydayAstronaut/videos" \
  --match "elon|musk|spacex|starship|starbase" \
  --limit 300 --output data/channel-candidates.json
```

Add explicit seed URLs and obtain full metadata:

```bash
python3 <skill>/scripts/video_pipeline.py add \
  --url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --output data/candidates.json
```

Fetch captions with resumable receipts:

```bash
python3 <skill>/scripts/video_pipeline.py captions \
  --dataset data/candidates.json --output-dir media/captions --langs "en,en-orig,zh-Hans"
```

Migrate a legacy title-based subtitle archive to collision-safe video-ID folders:

```bash
python3 <skill>/scripts/video_pipeline.py migrate-captions \
  --dataset data/candidates.json --output-dir media/captions \
  --receipt data/caption-migration-receipt.json
```

Generate resumable low-bandwidth audio fingerprints. Remote samples are deleted by default:

```bash
python3 <skill>/scripts/video_pipeline.py audio-fingerprints \
  --dataset data/candidates.json --output-dir media/audio-fingerprint-samples \
  --receipt data/audio-fingerprint-receipts.json --seconds 120
```

Audit duplicates and select canonical sources:

```bash
python3 <skill>/scripts/video_pipeline.py dedupe \
  --dataset data/candidates.json --captions-dir media/captions \
  --source-registry data/youtube-source-registry.json \
  --output data/dedupe-report.json
```

Create a ranked download queue:

```bash
python3 <skill>/scripts/video_pipeline.py queue \
  --dataset data/candidates.json --dedupe-report data/dedupe-report.json \
  --output data/download-queue.json --min-score 60
```

## Guardrails

- Treat user-approved videos as golden recall tests, not hardcoded one-off exceptions.
- When a good video is found, inspect its channel and add the channel to the learned creator registry only after quality evidence.
- Use exact ID only for address deduplication; use captions/audio/event metadata for content deduplication.
- Store captions under `<captions-dir>/<videoId>/`; shared legacy title paths are ambiguous and must be refetched.
- Official-source trust improves provenance ranking but never proves the target speaker participates.
- Keep `canonical`, `mirror`, `clip`, and `commentary` roles separate.
- Do not count multiple uploads of the same event as independent evidence.
- Do not call a network/SSL `429` a quota exhaustion unless the response body identifies quota/rate limiting.
- Never expose API keys in logs. Prefer yt-dlp discovery when API quota is unavailable.
- Do not download full media merely to decide relevance; metadata and captions come first.

## Existing Projects

If a project already has a collector, adapt it rather than replacing it. Run the bundled audit against the existing dataset, add rejection logging and versioned search strategies, then backfill historical years whenever query/filter rules change.
