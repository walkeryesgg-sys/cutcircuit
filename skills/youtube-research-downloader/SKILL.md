---
name: youtube-research-downloader
description: Download authorized YouTube videos, Shorts, audio, subtitles, metadata, or opt-in playlists for academic and research use with yt-dlp and FFmpeg. Use when a user asks to download, archive, preserve, extract, or verify YouTube media, including difficult cases involving 429/403 errors, browser cookies, proxies or Clash Verge nodes, SABR/JavaScript challenges, missing formats, old Python or yt-dlp versions, interrupted downloads, audio-video merging, and output integrity checks.
---

# YouTube Research Downloader

Download only content the user is authorized to obtain. Do not bypass DRM, paywalls, memberships, private-video authorization, geographic access controls, or account restrictions. Treat browser cookies as sensitive: request permission before using them and never print, copy, or persist their contents.

## Workflow

1. Confirm the URL and intended output directory. Treat a `t=` parameter as a playback position; download the full video unless the user explicitly requests a clip.
2. Check available tools:

   ```bash
   command -v yt-dlp
   yt-dlp --version
   command -v ffmpeg
   command -v ffprobe
   ```

3. Run `scripts/download_youtube.py URL`. Pass only the options needed for the request.
4. If anonymous extraction requests login or reports bot detection, obtain permission and retry with `--cookies-from-browser chrome` (or the user's browser).
5. If the network requires a proxy, pass `--proxy http://127.0.0.1:PORT`. Never assume a proxy port; discover or ask.
6. Keep the process attached until it completes. Report real media progress only after `[download] Destination`; `Testing format` is not downloaded data.
7. Require the script's final JSON verification report. Confirm the final file exists, has nonzero duration, and contains both audio and video unless audio-only was requested.

## Common commands

```bash
# Highest available quality, single video
python3 scripts/download_youtube.py URL --output ./downloads

# Login verification and proxy
python3 scripts/download_youtube.py URL --cookies-from-browser chrome \
  --proxy http://127.0.0.1:7897

# Non-default Chrome profile or isolated user-data directory
python3 scripts/download_youtube.py URL --cookies-from-browser chrome \
  --browser-profile "/absolute/path/to/chrome-user-data"

# Cap resolution and preserve research artifacts
python3 scripts/download_youtube.py URL --max-height 1080 \
  --subtitles --metadata

# Audio only or explicitly authorized playlist
python3 scripts/download_youtube.py URL --audio-only
python3 scripts/download_youtube.py PLAYLIST_URL --playlist
```

## Failure handling

Read [references/troubleshooting.md](references/troubleshooting.md) whenever a download does not reach media transfer, stalls, returns HTTP errors, or produces an unverifiable file. Apply one change at a time, then retry with the identical URL and output directory so partial files resume.

Do not repeatedly hammer YouTube. Stop rapid retries after two equivalent failures. For proxy changes, verify that the public exit IP actually changes before retrying. Do not claim progress based on extraction, challenge solving, format tests, or empty directories.

## Output reporting

Report the clickable absolute file path, resolution, codecs, duration, size, and merge/verification status. If incomplete, report bytes actually present and the exact blocking stage. Never say “downloading” after the process has exited.
