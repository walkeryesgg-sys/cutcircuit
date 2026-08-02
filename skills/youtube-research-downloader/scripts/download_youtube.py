#!/usr/bin/env python3
"""Robust, authorized YouTube downloader wrapper around yt-dlp."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Download and verify authorized YouTube media")
    p.add_argument("url")
    p.add_argument("-o", "--output", type=Path, default=Path("downloads"))
    p.add_argument("--max-height", type=int)
    p.add_argument("--playlist", action="store_true")
    p.add_argument("--audio-only", action="store_true")
    p.add_argument("--subtitles", action="store_true")
    p.add_argument("--subtitle-langs", default="zh-Hans,zh-Hant,zh,en")
    p.add_argument("--metadata", action="store_true")
    p.add_argument("--cookies-from-browser", choices=("chrome", "firefox", "safari", "edge", "brave"))
    p.add_argument("--browser-profile", help="Browser profile name or absolute user-data directory")
    p.add_argument("--proxy", help="HTTP or SOCKS proxy URL")
    p.add_argument("--yt-dlp", dest="yt_dlp", help="yt-dlp executable path")
    p.add_argument("--ffprobe", help="ffprobe executable path")
    return p


def executable(given: str | None, names: tuple[str, ...]) -> str:
    if given:
        path = shutil.which(given) or (given if Path(given).is_file() else None)
    else:
        path = next((shutil.which(name) for name in names if shutil.which(name)), None)
    if not path:
        raise RuntimeError(f"missing executable: {' or '.join(names)}")
    return str(path)


def version_tuple(text: str) -> tuple[int, ...]:
    value = text.strip().splitlines()[-1].replace(".", "")
    return (int(value),) if value.isdigit() else (0,)


def format_selector(args: argparse.Namespace) -> str:
    if args.audio_only:
        return "bestaudio[ext=m4a]/bestaudio"
    cap = f"[height<={args.max_height}]" if args.max_height else ""
    return f"bestvideo{cap}[ext=mp4]+bestaudio[ext=m4a]/bestvideo{cap}+bestaudio/best{cap}/best"


def supports_option(executable_path: str, option: str) -> bool:
    """Return whether this yt-dlp build advertises an optional CLI flag."""
    completed = subprocess.run(
        [executable_path, "--help"],
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.returncode == 0 and option in completed.stdout


def verify(ffprobe: str, path: Path, audio_only: bool) -> dict:
    command = [ffprobe, "-v", "error", "-show_entries",
               "format=duration,size:stream=codec_type,codec_name,width,height",
               "-of", "json", str(path)]
    data = json.loads(subprocess.check_output(command, text=True))
    streams = data.get("streams", [])
    types = {s.get("codec_type") for s in streams}
    duration = float(data.get("format", {}).get("duration", 0))
    size = int(data.get("format", {}).get("size", 0))
    required = {"audio"} if audio_only else {"audio", "video"}
    if duration <= 0 or size <= 0 or not required.issubset(types):
        raise RuntimeError(f"media verification failed: duration={duration}, size={size}, streams={sorted(types)}")
    return {"path": str(path.resolve()), "duration_seconds": duration, "size_bytes": size, "streams": streams}


def main() -> int:
    args = parser().parse_args()
    try:
        yt_dlp = executable(args.yt_dlp, ("yt-dlp",))
        ffprobe = executable(args.ffprobe, ("ffprobe",))
        if not args.audio_only:
            executable(None, ("ffmpeg",))
        version = subprocess.check_output([yt_dlp, "--version"], text=True).strip()
        if version_tuple(version) < (20250101,):
            print(f"WARNING: yt-dlp {version} is old; upgrade before diagnosing extractor failures", file=sys.stderr)

        output = args.output.expanduser().resolve()
        output.mkdir(parents=True, exist_ok=True)
        before = {p.resolve() for p in output.rglob("*") if p.is_file()}
        template = ("%(playlist_title)s/%(playlist_index)03d - %(title)s [%(id)s].%(ext)s"
                    if args.playlist else "%(title)s [%(id)s].%(ext)s")
        cmd = [yt_dlp]
        if supports_option(yt_dlp, "--remote-components"):
            cmd += ["--remote-components", "ejs:github"]
        cmd += ["--continue",
               "--retries", "10", "--fragment-retries", "10", "--concurrent-fragments", "4",
               "--merge-output-format", "mp4", "-P", str(output), "-o", template,
               "-f", format_selector(args), "--yes-playlist" if args.playlist else "--no-playlist"]
        if args.browser_profile and not args.cookies_from_browser:
            raise RuntimeError("--browser-profile requires --cookies-from-browser")
        if args.cookies_from_browser:
            browser_spec = args.cookies_from_browser
            if args.browser_profile:
                browser_spec += f":{args.browser_profile}"
            cmd += ["--cookies-from-browser", browser_spec]
        if args.proxy:
            cmd += ["--proxy", args.proxy]
        if args.subtitles:
            cmd += ["--write-subs", "--write-auto-subs", "--sub-langs", args.subtitle_langs, "--convert-subs", "srt"]
        if args.metadata:
            cmd += ["--write-description", "--write-info-json", "--write-thumbnail", "--embed-metadata", "--embed-thumbnail"]
        cmd.append(args.url)

        env = os.environ.copy()
        completed = subprocess.run(cmd, env=env)
        if completed.returncode:
            print(json.dumps({"status": "failed", "exit_code": completed.returncode,
                              "output_bytes": sum(p.stat().st_size for p in output.rglob("*") if p.is_file())},
                             ensure_ascii=False), file=sys.stderr)
            return completed.returncode

        candidates = [p for p in output.rglob("*") if p.is_file() and p.resolve() not in before
                      and p.suffix.lower() in ({".m4a", ".opus", ".mp3"} if args.audio_only else {".mp4", ".mkv", ".webm"})]
        if not candidates:
            # A resumed download may overwrite an existing final path.
            candidates = [p for p in output.rglob("*") if p.is_file()
                          and p.suffix.lower() in ({".m4a", ".opus", ".mp3"} if args.audio_only else {".mp4", ".mkv", ".webm"})]
        if not candidates:
            raise RuntimeError("download exited successfully but no final media file was found")
        reports = [verify(ffprobe, p, args.audio_only) for p in sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)[:1 if not args.playlist else None]]
        print(json.dumps({"status": "complete", "yt_dlp_version": version, "files": reports}, ensure_ascii=False, indent=2))
        return 0
    except (RuntimeError, OSError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
