# CutCircuit

**Source. Cut. Score. Repair.**

CutCircuit is a Codex plugin for evidence-led video production. It combines four installable skills:

- `cutcircuit` routes requests and runs the quality loop.
- `produce-social-video` plans, scripts, edits, renders, repairs, and delivers.
- `score-social-video` independently evaluates finished videos against measurable release gates.
- `youtube-research-downloader` downloads and verifies authorized YouTube research media.

The full workflow is:

```text
interview → script + structure + shot list + storyboard → user approval → source → produce → score → repair → rescore → deliver
```

CutCircuit does not begin production from a topic or URL alone. It first delivers a versioned professional pre-production plan covering the complete script, narrative structure, beat sheet, shot list, storyboard, sound and caption treatment, asset/rights plan, risks, delivery specification, and acceptance gates. Formal media acquisition, TTS, editing, animation, and rendering begin only after the user explicitly approves that plan version.

For source-led public videos, CutCircuit includes a reusable commentary template: full-screen real footage, Chinese narration alternating with complete original-audio evidence, failure or uncertainty before the midpoint, delayed visual payoff in the second half, and a horizontal full-bleed hero ending. The template keeps factual entity labels, subtitles, audio continuity, and final-shot composition inside the release gates.

Ordinary videos target 9.0/10, paid or member content targets 9.5/10, and premium work targets 9.8/10 plus a complete linear watch. CutCircuit reports the real result when a target is not met; it does not weaken quality gates to manufacture a pass.

CutCircuit also measures sampled video luminance and a blur/softness proxy alongside black/freeze/silence signals. These metrics are diagnostic rather than automatic style verdicts: nominally-HD or dark cinematic work passes only when faces, machinery, and evidence details remain visibly crisp and legible.
The probe also reports integrated LUFS and true peak dBTP so a file cannot pass merely because its average/sample volume looks reasonable.

Programmed motion follows a deterministic, seek-safe timeline contract derived from official GSAP practices: labeled beats, explicit start/end states, transform-first animation, restrained easing, full-resolution performance checks, and frame sampling across every animated interval. CutCircuit also carries a regression checklist learned from real revisions so TTS boundary errors, linear-playback silence, late-track noise, weak first frames, mistimed spectacle, and undersized final shots are not reintroduced by later repairs.

For `硬核火星人`, CutCircuit records two routing fields in every new production brief: `program_type` separates curriculum-based `member_original` work from free `public_story` work, while `edit_model` selects source-led, narration-led montage, or hybrid evidence-lesson cutting. The member profile uses the canonical lower-right Chinese-only `硬核火星人` orbit watermark.

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
