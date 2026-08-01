#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import shutil
import subprocess
from pathlib import Path


def yt_dlp():
    path = shutil.which("yt-dlp")
    if not path:
        raise SystemExit(
            "yt-dlp is required. Read references/toolchain.md and install it first."
        )
    return path


def run(args):
    result = subprocess.run(args, text=True, capture_output=True, check=False)
    if result.returncode:
        raise SystemExit(result.stderr.strip() or f"Command failed: {args}")
    return result.stdout


def write_json(data, output):
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
    print(text)


def cookie_args(browser):
    return ["--cookies-from-browser", browser] if browser else []


def search(args):
    raw = run([
        yt_dlp(),
        "--dump-single-json",
        "--flat-playlist",
        "--skip-download",
        "--no-warnings",
        *cookie_args(args.cookies_from_browser),
        f"ytsearch{args.limit}:{args.query}",
    ])
    payload = json.loads(raw)
    candidates = []
    for item in payload.get("entries", []):
        video_id = item.get("id")
        webpage_url = item.get("webpage_url")
        if not webpage_url and video_id:
            webpage_url = f"https://www.youtube.com/watch?v={video_id}"
        candidates.append({
            "id": video_id,
            "title": item.get("title"),
            "url": webpage_url or item.get("url"),
            "channel": item.get("channel") or item.get("uploader"),
            "channel_id": item.get("channel_id") or item.get("uploader_id"),
            "duration": item.get("duration"),
            "view_count": item.get("view_count"),
            "upload_date": item.get("upload_date"),
            "description": item.get("description"),
        })
    write_json(
        {"query": args.query, "count": len(candidates), "candidates": candidates},
        args.output,
    )


def info(args):
    raw = run([
        yt_dlp(),
        "--dump-single-json",
        "--skip-download",
        "--no-warnings",
        *cookie_args(args.cookies_from_browser),
        args.url,
    ])
    payload = json.loads(raw)
    formats = payload.get("formats") or []
    result = {
        "id": payload.get("id"),
        "title": payload.get("title"),
        "webpage_url": payload.get("webpage_url"),
        "channel": payload.get("channel") or payload.get("uploader"),
        "channel_url": payload.get("channel_url") or payload.get("uploader_url"),
        "upload_date": payload.get("upload_date"),
        "duration": payload.get("duration"),
        "license": payload.get("license"),
        "description": payload.get("description"),
        "subtitles": sorted((payload.get("subtitles") or {}).keys()),
        "automatic_captions": sorted(
            (payload.get("automatic_captions") or {}).keys()
        ),
        "max_height": max(
            (item.get("height") or 0 for item in formats), default=0
        ),
        "thumbnail": payload.get("thumbnail"),
    }
    write_json(result, args.output)


def download(args):
    args.output_dir.mkdir(parents=True, exist_ok=True)
    template = str(
        args.output_dir
        / "%(id)s"
        / "%(title).120B [%(id)s].%(ext)s"
    )
    command = [
        yt_dlp(),
        "--no-playlist",
        "--no-overwrites",
        "--restrict-filenames",
        "--write-info-json",
        "--write-thumbnail",
        "--write-subs",
        "--write-auto-subs",
        "--sub-langs",
        args.sub_langs,
        "--convert-subs",
        "srt",
        "--merge-output-format",
        "mp4",
        "-f",
        f"bv*[height<={args.max_height}]+ba/b[height<={args.max_height}]",
        "-o",
        template,
        *cookie_args(args.cookies_from_browser),
        args.url,
    ]
    subprocess.run(command, check=True)

    info_files = sorted(args.output_dir.glob("**/*.info.json"))
    if not info_files:
        raise SystemExit("Download completed but no .info.json was found.")
    info_payload = json.loads(info_files[-1].read_text(encoding="utf-8"))
    provenance = {
        "source_type": "youtube",
        "source_url": info_payload.get("webpage_url") or args.url,
        "video_id": info_payload.get("id"),
        "title": info_payload.get("title"),
        "channel": info_payload.get("channel") or info_payload.get("uploader"),
        "channel_url": info_payload.get("channel_url")
        or info_payload.get("uploader_url"),
        "upload_date": info_payload.get("upload_date"),
        "license": info_payload.get("license"),
        "downloaded_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "max_height_requested": args.max_height,
        "rights_status": "unreviewed",
        "intended_use": "",
        "used_ranges": [],
        "risk": "unreviewed",
    }
    provenance_path = info_files[-1].parent / "provenance.json"
    provenance_path.write_text(
        json.dumps(provenance, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_json(
        {
            "download_directory": str(info_files[-1].parent),
            "info": str(info_files[-1]),
            "provenance": str(provenance_path),
        },
        args.output,
    )


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("query")
    search_parser.add_argument("--limit", type=int, default=10)
    search_parser.add_argument("--output", type=Path)
    search_parser.add_argument("--cookies-from-browser")
    search_parser.set_defaults(handler=search)

    info_parser = subparsers.add_parser("info")
    info_parser.add_argument("url")
    info_parser.add_argument("--output", type=Path)
    info_parser.add_argument("--cookies-from-browser")
    info_parser.set_defaults(handler=info)

    download_parser = subparsers.add_parser("download")
    download_parser.add_argument("url")
    download_parser.add_argument("--output-dir", type=Path, required=True)
    download_parser.add_argument("--max-height", type=int, default=1080)
    download_parser.add_argument("--sub-langs", default="zh.*,en.*")
    download_parser.add_argument("--cookies-from-browser")
    download_parser.add_argument("--output", type=Path)
    download_parser.set_defaults(handler=download)

    args = parser.parse_args()
    if getattr(args, "limit", 1) < 1 or getattr(args, "limit", 1) > 50:
        parser.error("--limit must be between 1 and 50")
    if getattr(args, "max_height", 1080) not in (360, 480, 720, 1080, 1440, 2160):
        parser.error("--max-height must be a standard video height")
    args.handler(args)


if __name__ == "__main__":
    main()
