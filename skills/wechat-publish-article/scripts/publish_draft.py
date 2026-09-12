#!/usr/bin/env python3
"""Preflight and save a complete Markdown package to WeChat as a draft."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def find_publisher() -> Path:
    override = os.environ.get("BAOYU_POST_TO_WECHAT_DIR", "")
    candidates = [
        Path(override) if override else None,
        Path.home() / ".agents/skills/baoyu-post-to-wechat",
        Path.home() / ".codex/skills/baoyu-post-to-wechat",
    ]
    for base in candidates:
        if base and (base / "scripts/wechat-article.ts").is_file():
            return base / "scripts/wechat-article.ts"
    raise SystemExit(
        "baoyu-post-to-wechat was not found. Install it or set BAOYU_POST_TO_WECHAT_DIR."
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("article", type=Path)
    parser.add_argument("--theme", default="simple")
    parser.add_argument("--color", default="blue")
    parser.add_argument("--profile")
    parser.add_argument("--account")
    parser.add_argument("--cdp-port", type=int)
    args = parser.parse_args()

    article = args.article.expanduser().resolve()
    preflight_script = Path(__file__).with_name("preflight.py")
    checked = subprocess.run(
        [sys.executable, str(preflight_script), str(article)],
        text=True,
        capture_output=True,
    )
    try:
        report = json.loads(checked.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid preflight output: {exc}") from exc
    if checked.returncode or not report.get("ok"):
        print(json.dumps(report, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1
    if report.get("existing_receipt"):
        raise SystemExit(f"Successful receipt already exists: {report['existing_receipt']}")

    bun = shutil.which("bun")
    if not bun:
        raise SystemExit("bun is required")
    command = [
        bun,
        str(find_publisher()),
        "--markdown",
        str(article),
        "--theme",
        args.theme,
        "--color",
        args.color,
        "--title",
        report["title"],
        "--summary",
        report["summary"],
        "--cover",
        report["cover"],
        "--submit",
    ]
    if args.profile:
        command += ["--profile", args.profile]
    if args.account:
        command += ["--account", args.account]
    if args.cdp_port:
        command += ["--cdp-port", str(args.cdp_port)]

    print(
        json.dumps(
            {
                "action": "save-draft",
                "article": str(article),
                "cover": report["cover"],
                "content_hash": report["content_hash"],
            },
            ensure_ascii=False,
        )
    )
    return subprocess.run(command).returncode


if __name__ == "__main__":
    raise SystemExit(main())
