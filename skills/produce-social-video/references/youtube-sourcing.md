# YouTube search and download

## Principle

Use YouTube to fill a declared evidence or visual need. Reuse local material first. Do not browse aimlessly or collect a large unreviewed library.

Only process public content the user is authorized to use. Do not bypass DRM, private access, paywalls, geographic restrictions, or platform controls. A successful download does not establish reuse rights.

## Search

```bash
python3 scripts/youtube_media.py search \
  "Elon Musk IAC 2016 making humans multiplanetary official" \
  --limit 10 \
  --output candidates.json
```

Evaluate:

- primary/official source;
- exact relevance to the claim or scene;
- visible speaker and event identity;
- upload date when freshness matters;
- duration and usable shot ranges;
- creator/automatic subtitle languages;
- achievable resolution;
- privacy, likeness, and copyright risk;
- duplication with local assets.

## Inspect

```bash
python3 scripts/youtube_media.py info "VIDEO_URL" --output video-info.json
```

Inspect metadata, subtitle languages, duration, channel, and formats before downloading.

## Download

```bash
python3 scripts/youtube_media.py download "VIDEO_URL" \
  --output-dir assets/youtube \
  --max-height 1080 \
  --sub-langs "zh.*,en.*"
```

The command stores video, thumbnail, `.info.json`, subtitles, and `provenance.json`.

For content that is public but requires the user’s own signed-in browser session:

```bash
python3 scripts/youtube_media.py download "VIDEO_URL" \
  --output-dir assets/youtube \
  --cookies-from-browser chrome
```

Do not copy or expose cookie files. Do not enable browser cookies unless needed.

## Selection

Score candidates before download:

| Dimension | Weight |
|---|---:|
| relevance to exact beat | 25% |
| source authority/originality | 20% |
| visual usefulness | 15% |
| subtitle/transcript quality | 10% |
| resolution and technical quality | 10% |
| rights/privacy confidence | 15% |
| novelty versus local library | 5% |

Reject a candidate with high unresolved rights/privacy risk regardless of weighted score.

## Editing

- Record the exact used time range.
- Never imply unrelated B-roll depicts the narrated event.
- Preserve original source audio only when it is used as evidence.
- Mute B-roll when narration owns the moment.
- Do not cut a source speaker mid-sentence.
- Keep the source URL and channel in the final provenance ledger.

