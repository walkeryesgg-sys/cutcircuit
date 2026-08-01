#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
from pathlib import Path


def run(cmd):
    return subprocess.run(cmd, text=True, capture_output=True, check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--duration", type=float, help="Analyze only the first N seconds")
    args = parser.parse_args()

    probe = json.loads(run([
        "ffprobe", "-v", "error", "-show_streams", "-show_format",
        "-of", "json", str(args.video),
    ]).stdout)
    limit = [] if args.duration is None else ["-t", str(args.duration)]
    analysis = run([
        "ffmpeg", "-hide_banner", "-i", str(args.video), *limit,
        "-vf", "scale=320:-1,blackdetect=d=0.20:pix_th=0.08,"
               "freezedetect=n=-50dB:d=1.5,"
               "select='gt(scene,0.32)',showinfo",
        "-af", "silencedetect=noise=-45dB:d=0.50,volumedetect",
        "-f", "null", "-",
    ]).stderr

    black = [
        {"start": float(a), "end": float(b), "duration": float(c)}
        for a, b, c in re.findall(
            r"black_start:([0-9.]+) black_end:([0-9.]+) black_duration:([0-9.]+)",
            analysis,
        )
    ]
    freeze_starts = [float(x) for x in re.findall(r"freeze_start: ([0-9.]+)", analysis)]
    freeze_ends = [float(x) for x in re.findall(r"freeze_end: ([0-9.]+)", analysis)]
    silence_starts = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", analysis)]
    silence_ends = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", analysis)]
    scene_changes = len(re.findall(r"showinfo.*pts_time:", analysis))
    mean = re.search(r"mean_volume: ([-0-9.]+) dB", analysis)
    peak = re.search(r"max_volume: ([-0-9.]+) dB", analysis)

    result = {
        "file": str(args.video),
        "format": probe.get("format", {}),
        "streams": probe.get("streams", []),
        "analyzed_seconds": args.duration,
        "black_segments": black,
        "freeze_starts": freeze_starts,
        "freeze_ends": freeze_ends,
        "silence_starts": silence_starts,
        "silence_ends": silence_ends,
        "scene_change_proxy": scene_changes,
        "mean_volume_db": float(mean.group(1)) if mean else None,
        "peak_volume_db": float(peak.group(1)) if peak else None,
        "notes": [
            "Automated signals are candidates, not final judgments.",
            "Full linear viewing and layout/sync review remain mandatory.",
        ],
    }
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
