# Portability

This skill uses plain Markdown, Python standard library, JSON, FFmpeg, and command-line tools. Keep agent-specific metadata optional.

## Install

Run:

```bash
python3 scripts/install_skill.py --target codex
python3 scripts/install_skill.py --target claude
python3 scripts/install_skill.py --target cursor
python3 scripts/install_skill.py --target all
```

Default user locations:

| Agent | Directory |
|---|---|
| Codex | `~/.codex/skills/produce-social-video` |
| Claude Code | `~/.claude/skills/produce-social-video` |
| Cursor | `~/.cursor/skills/produce-social-video` |

Use `--project PATH` to install under `PATH/.agents/skills/produce-social-video`, which is the preferred shared repository location when multiple agents work on one project.

## Compatibility rules

- Treat `SKILL.md` as the source of truth.
- Do not depend on Codex-only tools in the core workflow.
- Keep shell examples POSIX where possible; provide Python scripts for cross-platform operations.
- Use the host agent’s normal approval mechanism for system installs, network access, payments, publication, or destructive operations.
- If HyperFrames is unavailable, preserve the same stages and release gates with the host renderer; do not skip QA.

## Package

Copy the entire `produce-social-video` directory. Do not package caches, project footage, credentials, or generated outputs.

