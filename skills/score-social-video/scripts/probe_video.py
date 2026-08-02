#!/usr/bin/env python3
import argparse
import json
import math
import re
import subprocess
from pathlib import Path


def run(cmd):
    return subprocess.run(cmd, text=True, capture_output=True, check=True)


def percentile(values, p):
    if not values:
        return None
    ordered = sorted(values)
    index = (len(ordered) - 1) * p
    low = math.floor(index)
    high = math.ceil(index)
    if low == high:
        return ordered[low]
    return ordered[low] * (high - index) + ordered[high] * (index - low)


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
    luminance_analysis = run([
        "ffmpeg", "-hide_banner", "-i", str(args.video), *limit,
        "-vf", "fps=1,scale=320:-1,signalstats,"
               "metadata=print:key=lavfi.signalstats.YAVG,"
               "blurdetect=block_width=32:block_height=32:block_pct=80",
        "-an", "-f", "null", "-",
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
    yavg = [float(x) for x in re.findall(
        r"lavfi\.signalstats\.YAVG=([0-9.]+)", luminance_analysis
    )]
    underexposed_ratio = (
        sum(value < 55 for value in yavg) / len(yavg) if yavg else None
    )
    blur = re.search(r"blur mean: ([0-9.]+)", luminance_analysis)

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
        "luminance": {
            "sample_count": len(yavg),
            "mean_yavg": round(sum(yavg) / len(yavg), 2) if yavg else None,
            "p10_yavg": round(percentile(yavg, 0.10), 2) if yavg else None,
            "median_yavg": round(percentile(yavg, 0.50), 2) if yavg else None,
            "p90_yavg": round(percentile(yavg, 0.90), 2) if yavg else None,
            "underexposed_frame_ratio_below_55": round(underexposed_ratio, 3)
            if underexposed_ratio is not None else None,
        },
        "visual_clarity": {
            "blurdetect_mean_proxy": round(float(blur.group(1)), 4) if blur else None,
            "requires_human_review": True,
        },
        "notes": [
            "Automated signals are candidates, not final judgments.",
            "Luminance samples use 1 fps YAVG; dark creative intent still requires human review.",
            "Blurdetect is a content-dependent softness proxy, not a pass/fail score; compare similar shots and inspect motion at 100%.",
            "Full linear viewing and layout/sync review remain mandatory.",
        ],
    }
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
