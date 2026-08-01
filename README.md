# CutCircuit

**Source. Cut. Score. Repair.**

CutCircuit is a Codex plugin for evidence-led video production. It combines four installable skills:

- `cutcircuit` routes requests and runs the quality loop.
- `produce-social-video` plans, scripts, edits, renders, repairs, and delivers.
- `score-social-video` independently evaluates finished videos against measurable release gates.
- `youtube-research-downloader` downloads and verifies authorized YouTube research media.

The full workflow is:

```text
brief → evidence plan → source → produce → score → repair → rescore → deliver
```

Ordinary videos target 9.0/10, paid or member content targets 9.5/10, and premium work targets 9.8/10 plus a complete linear watch. CutCircuit reports the real result when a target is not met; it does not weaken quality gates to manufacture a pass.

## Install

Install the repository as a Codex plugin or copy the desired folders under `skills/` into your Codex skills directory. Restart or open a new Codex session after installation so the skills are discovered.

Start with:

```text
Use $cutcircuit to produce this video and run the quality loop.
```

The downloader only handles material you are authorized to obtain. Download success does not grant reuse rights.

## Requirements

The core scripts use Python 3 and probe media with FFmpeg/FFprobe. YouTube transfers additionally require yt-dlp. Production may use an installed rendering or editing toolchain selected for the project.

## License

MIT
