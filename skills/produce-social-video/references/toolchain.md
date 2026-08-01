# Portable toolchain

## Required

| Tool | Purpose | Check |
|---|---|---|
| Python 3.9+ | orchestration and QA scripts | `python3 --version` |
| Node.js 20+ and npm/npx | HyperFrames CLI/runtime | `node --version` |
| FFmpeg + ffprobe | probe, transcode, audio mix, concat, black/freeze detection | `ffmpeg -version` |
| Chrome or Chromium | deterministic HTML video capture | browser executable exists |
| Git | versioning and reproducible handoff | `git --version` |

Run `scripts/doctor.py --json`.

## Recommended

| Tool | Purpose |
|---|---|
| HyperFrames | default HTML composition and rendering |
| yt-dlp | authorized YouTube search, source download and subtitle discovery |
| Whisper/Parakeet | transcription and word timing |
| Jianying/CapCut | optional fast TTS or manual emergency finishing |
| ImageMagick | contact sheets and image diagnostics |
| jq | manifest inspection |

## Installation guidance

### macOS

```bash
brew install ffmpeg node git python
npx hyperframes doctor
```

Install Chrome normally. Install optional `yt-dlp` with `brew install yt-dlp`.

When YouTube sourcing is requested, `yt-dlp` becomes required for that run.

### Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install -y ffmpeg git python3 python3-venv chromium
```

Install a current Node.js LTS using the official NodeSource or `nvm`, then run `npx hyperframes doctor`.

### Windows

Install Python, Node.js LTS, Git, FFmpeg, and Chrome with `winget`, then ensure every executable is on `PATH`.

## HyperFrames bootstrap

```bash
npx hyperframes skills update general-video
npx hyperframes doctor
```

Do not install packages silently. Diagnose first, show the exact missing dependencies, and obtain approval before system-level installation.

## Provider policy

- Prefer local or already authenticated tools.
- Before paid or authenticated generation, show provider, expected cost class, and what will be sent externally.
- Freeze every downloaded/generated asset into the project; never depend on network fetches during render.
