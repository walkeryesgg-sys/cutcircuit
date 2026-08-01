#!/usr/bin/env python3
import argparse
import json
import platform
import re
import shutil
import subprocess
import sys


TOOLS = {
    "python3": {"required": True, "args": ["--version"]},
    "node": {"required": True, "args": ["--version"]},
    "npx": {"required": True, "args": ["--version"]},
    "ffmpeg": {"required": True, "args": ["-version"]},
    "ffprobe": {"required": True, "args": ["-version"]},
    "git": {"required": True, "args": ["--version"]},
    "yt-dlp": {"required": False, "args": ["--version"]},
    "magick": {"required": False, "args": ["-version"]},
    "jq": {"required": False, "args": ["--version"]},
}


def first_line(path, args):
    try:
        result = subprocess.run(
            [path, *args], text=True, capture_output=True, timeout=8, check=False
        )
        text = (result.stdout or result.stderr).strip()
        return text.splitlines()[0] if text else "available"
    except Exception as exc:
        return f"available ({exc})"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    checks = {}
    for name, spec in TOOLS.items():
        path = shutil.which(name)
        checks[name] = {
            "required": spec["required"],
            "found": bool(path),
            "path": path,
            "version": first_line(path, spec["args"]) if path else None,
        }
    if checks["python3"]["found"] and sys.version_info < (3, 9):
        checks["python3"]["found"] = False
        checks["python3"]["version"] += " (requires 3.9+)"
    if checks["node"]["found"]:
        match = re.search(r"v?(\d+)", checks["node"]["version"] or "")
        if not match or int(match.group(1)) < 20:
            checks["node"]["found"] = False
            checks["node"]["version"] = (
                (checks["node"]["version"] or "unknown") + " (requires 20+)"
            )

    browser = next(
        (
            path
            for candidate in (
                "google-chrome",
                "google-chrome-stable",
                "chromium",
                "chromium-browser",
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Chromium.app/Contents/MacOS/Chromium",
            )
            if (path := shutil.which(candidate)) or (
                candidate.startswith("/") and __import__("pathlib").Path(candidate).exists()
                and (path := candidate)
            )
        ),
        None,
    )
    checks["browser"] = {
        "required": True,
        "found": bool(browser),
        "path": browser,
        "version": None,
    }
    missing_required = [
        name for name, item in checks.items() if item["required"] and not item["found"]
    ]
    report = {
        "system": platform.platform(),
        "ready": not missing_required,
        "missing_required": missing_required,
        "capabilities": {
            "youtube_search_download": checks["yt-dlp"]["found"],
        },
        "checks": checks,
        "next": (
            "Ready for production."
            if not missing_required
            else "Read references/toolchain.md and install only the missing required tools."
        ),
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for name, item in checks.items():
            mark = "OK" if item["found"] else ("MISSING" if item["required"] else "optional")
            print(f"{mark:8} {name:10} {item['version'] or item['path'] or ''}")
        print(report["next"])
    raise SystemExit(0 if report["ready"] else 2)


if __name__ == "__main__":
    main()
