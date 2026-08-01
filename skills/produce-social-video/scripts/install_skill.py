#!/usr/bin/env python3
import argparse
import shutil
from pathlib import Path


TARGETS = {
    "codex": Path.home() / ".codex/skills/produce-social-video",
    "claude": Path.home() / ".claude/skills/produce-social-video",
    "cursor": Path.home() / ".cursor/skills/produce-social-video",
}


def install(source, destination, dry_run, force):
    print(f"{source} -> {destination}")
    if dry_run:
        return
    if destination.exists():
        if not force:
            raise SystemExit(
                f"Target exists: {destination}. Re-run with --force only after reviewing it."
            )
        backup = destination.with_name(destination.name + ".backup")
        if backup.exists():
            raise SystemExit(f"Backup target already exists: {backup}")
        destination.rename(backup)
        print(f"Existing skill moved to {backup}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", choices=["codex", "claude", "cursor", "all"])
    parser.add_argument("--project", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if not args.target and not args.project:
        parser.error("Choose --target or --project")

    source = Path(__file__).resolve().parent.parent
    destinations = []
    if args.target:
        destinations.extend(
            TARGETS.values() if args.target == "all" else [TARGETS[args.target]]
        )
    if args.project:
        destinations.append(
            args.project.resolve() / ".agents/skills/produce-social-video"
        )
    for destination in destinations:
        install(source, destination, args.dry_run, args.force)


if __name__ == "__main__":
    main()
