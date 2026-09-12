#!/usr/bin/env python3
"""Dependency-light YouTube research collector built around the yt-dlp CLI."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import statistics
import struct
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, text=True, capture_output=True)


def read_dataset(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"generatedAt": now(), "videos": []}
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        return {"generatedAt": now(), "videos": []}
    data = json.loads(raw)
    if isinstance(data, list):
        data = {"videos": data}
    data.setdefault("videos", [])
    return data


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def video_id(entry: dict[str, Any]) -> str:
    return str(entry.get("id") or entry.get("video_id") or "")


def duration_seconds(entry: dict[str, Any]) -> int:
    direct = entry.get("durationSeconds") or entry.get("duration")
    if isinstance(direct, (int, float)):
        return int(direct)
    text = str(direct or "")
    match = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", text)
    if match:
        return int(match.group(1) or 0) * 3600 + int(match.group(2) or 0) * 60 + int(match.group(3) or 0)
    return 0


def normalize_entry(raw: dict[str, Any], route: str, query: str = "") -> dict[str, Any]:
    vid = video_id(raw)
    thumbnails = raw.get("thumbnails") or []
    height = max((int(item.get("height") or 0) for item in raw.get("formats") or []), default=int(raw.get("height") or 0))
    return {
        "id": vid,
        "url": raw.get("webpage_url") or raw.get("url") if str(raw.get("url", "")).startswith("http") else f"https://www.youtube.com/watch?v={vid}",
        "title": raw.get("title") or "",
        "channelTitle": raw.get("channel") or raw.get("uploader") or raw.get("channelTitle") or "",
        "channelId": raw.get("channel_id") or raw.get("channelId") or "",
        "publishedAt": raw.get("upload_date") or raw.get("timestamp") or raw.get("publishedAt") or "",
        "durationSeconds": duration_seconds(raw),
        "height": height,
        "thumbnail": raw.get("thumbnail") or (thumbnails[-1].get("url") if thumbnails else ""),
        "description": raw.get("description") or "",
        "availability": raw.get("availability") or "unknown",
        "subtitleStatus": "unknown",
        "sourceRoute": route,
        "sourceQuery": query,
        "collectedAt": now(),
    }


def merge(output: Path, incoming: list[dict[str, Any]]) -> dict[str, Any]:
    data = read_dataset(output)
    by_id = {video_id(row): row for row in data["videos"] if video_id(row)}
    for row in incoming:
        vid = video_id(row)
        if not vid:
            continue
        by_id[vid] = {**by_id.get(vid, {}), **{k: v for k, v in row.items() if v not in (None, "", [])}}
    data["videos"] = sorted(by_id.values(), key=lambda x: str(x.get("publishedAt", "")), reverse=True)
    data["generatedAt"] = now()
    write_json(output, data)
    return data


def ytdlp_json(target: str, flat: bool = False, limit: int | None = None) -> list[dict[str, Any]]:
    cmd = ["yt-dlp", "--skip-download", "--dump-json", "--no-warnings"]
    if flat:
        cmd.append("--flat-playlist")
    if limit:
        cmd.extend(["--playlist-end", str(limit)])
    cmd.append(target)
    result = run(cmd)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "yt-dlp failed")
    return [json.loads(line) for line in result.stdout.splitlines() if line.strip()]


def load_source_registry(path: Path | None) -> dict[str, Any]:
    if not path or not path.exists():
        return {"sources": []}
    return json.loads(path.read_text(encoding="utf-8"))


def provenance_score(v: dict[str, Any], registry: dict[str, Any]) -> tuple[int, str | None]:
    channel_id = str(v.get("channelId") or "")
    channel = str(v.get("channelTitle") or "").casefold().strip()
    title = str(v.get("title") or "").casefold()
    best, source_name = 0, None
    for source in registry.get("sources", []):
        source_channel_id = str(source.get("channelId") or "")
        names = [str(source.get("name") or ""), *(source.get("aliases") or [])]
        name_match = channel in {name.casefold().strip() for name in names if name}
        id_match = bool(channel_id and source_channel_id and channel_id == source_channel_id)
        terms = [str(term).casefold() for term in source.get("titleTerms") or []]
        context_match = not terms or any(term in title for term in terms)
        if id_match:
            points = int(source.get("provenanceScore") or 30)
        elif name_match and context_match:
            points = min(20, int(source.get("provenanceScore") or 20))
        else:
            continue
        if points > best:
            best, source_name = points, str(source.get("name") or channel)
    return best, source_name


def quality_score(v: dict[str, Any], registry: dict[str, Any] | None = None) -> tuple[int, list[str]]:
    title = str(v.get("title", "")).lower()
    channel = str(v.get("channelTitle", "")).lower()
    desc = str(v.get("description", "")).lower()
    text = f"{title} {desc}"
    score, reasons = 0, []
    if re.search(r"\belon musk\b|\bmusk\b", text): score += 12
    primary_speaker = bool(re.search(
        r"^(?:[^a-z0-9]+|\[[0-9]{4}\]\s*)?elon musk\b|^join elon musk\b|\b(conversation|interview|talking|tour|q&a)\s+with\s+elon musk\b|\b(with|w/)\s+elon musk\b|\belon musk\b.{0,35}\b(interview|conversation|talks?|speaks?|discuss|answers?)\b",
        title,
    ))
    if primary_speaker:
        score += 15
    else:
        score -= 20
        reasons.append("target_speaker_not_primary")
    if duration_seconds(v) >= 45 * 60: score += 15
    elif duration_seconds(v) >= 10 * 60: score += 10
    elif duration_seconds(v) < 8 * 60: score -= 12; reasons.append("shorter_than_8m")
    if re.search(r"interview|conversation|podcast|q&a|tour|walkthrough|inside|behind the scenes|discuss|talking|with elon|w/ elon", text): score += 15
    if re.search(r"factory|starbase|launch tower|shop floor|facility|engineering", text): score += 12
    if re.search(r"everyday astronaut|marques brownlee|mkbhd|munro live|spacex|tesla", channel): score += 12
    source_points, _ = provenance_score(v, registry or {"sources": []})
    score += min(15, source_points)
    if int(v.get("height") or 0) >= 2160: score += 5
    elif int(v.get("height") or 0) >= 720: score += 3
    if v.get("subtitleStatus") in {"complete", "partial"}: score += 5
    if re.search(r"reaction|breakdown|news|rumor|documentary|summary", title): score -= 20; reasons.append("likely_commentary")
    if re.search(r"shocks?|bombshell|urgent|you won.t believe|greatest", title): score -= 10; reasons.append("sensational_title")
    return max(0, min(100, score)), reasons


def command_discover(args: argparse.Namespace) -> None:
    rows = []
    for query in args.query:
        # Some yt-dlp builds do not expose the optional ytsearchdate alias.
        # Plain ytsearch is broadly supported; year/date terms remain part of
        # the query strategy and metadata is sorted after collection.
        for raw in ytdlp_json(f"ytsearch{args.limit}:{query}", flat=True):
            rows.append(normalize_entry(raw, "query", query))
    data = merge(args.output, rows)
    print(json.dumps({"videos": len(data["videos"]), "output": str(args.output)}, ensure_ascii=False))


def command_channel(args: argparse.Namespace) -> None:
    pattern = re.compile(args.match, re.I)
    rows = []
    for raw in ytdlp_json(args.channel_url, flat=True, limit=args.limit):
        text = f"{raw.get('title', '')} {raw.get('description', '')}"
        if pattern.search(text):
            rows.append(normalize_entry(raw, "channel", args.channel_url))
    data = merge(args.output, rows)
    print(json.dumps({"matched": len(rows), "videos": len(data["videos"]), "output": str(args.output)}, ensure_ascii=False))


def command_add(args: argparse.Namespace) -> None:
    rows = []
    for url in args.url:
        for raw in ytdlp_json(url):
            rows.append(normalize_entry(raw, "seed", url))
    data = merge(args.output, rows)
    print(json.dumps({"added": len(rows), "videos": len(data["videos"]), "output": str(args.output)}, ensure_ascii=False))


def command_enrich(args: argparse.Namespace) -> None:
    data = read_dataset(args.dataset)
    receipts = json.loads(args.receipt.read_text(encoding="utf-8")) if args.receipt.exists() else {}
    pending = [row for row in data["videos"] if video_id(row) and not row.get("metadataEnriched") and not receipts.get(video_id(row), {}).get("ok")]
    if args.limit:
        pending = pending[:args.limit]
    if not pending:
        print(json.dumps({"processed": 0, "enriched": 0, "receipt": str(args.receipt)}, ensure_ascii=False)); return
    cmd = ["yt-dlp", "--skip-download", "--dump-json", "--no-warnings", "--ignore-errors",
           *[f"https://www.youtube.com/watch?v={video_id(row)}" for row in pending]]
    result = run(cmd)
    enriched_rows = []
    returned = set()
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        raw = json.loads(line)
        normalized = normalize_entry(raw, "enriched", "yt-dlp-batch")
        normalized["metadataEnriched"] = True
        enriched_rows.append(normalized)
        returned.add(video_id(normalized))
    checked_at = now()
    for row in pending:
        vid = video_id(row)
        receipts[vid] = {"ok": vid in returned, "checkedAt": checked_at,
                         "retryEligible": vid not in returned}
    merge(args.dataset, enriched_rows)
    write_json(args.receipt, receipts)
    print(json.dumps({"processed": len(pending), "enriched": len(enriched_rows),
                      "receipt": str(args.receipt)}, ensure_ascii=False))


def command_captions(args: argparse.Namespace) -> None:
    data = read_dataset(args.dataset)
    receipts_path = args.output_dir / "caption-receipts.json"
    receipts = json.loads(receipts_path.read_text()) if receipts_path.exists() else {}
    processed = 0
    for row in data["videos"]:
        vid = video_id(row)
        if not vid or receipts.get(vid, {}).get("ok") or (args.limit and processed >= args.limit):
            continue
        folder = args.output_dir / vid
        folder.mkdir(parents=True, exist_ok=True)
        cmd = ["yt-dlp", "--skip-download", "--write-subs", "--write-auto-subs", "--sub-langs", args.langs,
               "--sub-format", "srt/best", "--convert-subs", "srt", "-o", str(folder / f"{vid}.%(ext)s"),
               f"https://www.youtube.com/watch?v={vid}"]
        result = run(cmd)
        files = [str(p) for p in folder.glob("*.srt")]
        ok = bool(files)
        row["subtitleStatus"] = "complete" if ok else "none" if result.returncode == 0 else "failed"
        row["subtitleFiles"] = files
        receipts[vid] = {"ok": ok, "checkedAt": now(), "files": files, "returnCode": result.returncode,
                         "error": result.stderr[-1000:] if result.returncode else ""}
        write_json(receipts_path, receipts)
        processed += 1
    data["generatedAt"] = now()
    write_json(args.dataset, data)
    print(json.dumps({"processed": processed, "receipts": str(receipts_path)}, ensure_ascii=False))


def command_migrate_captions(args: argparse.Namespace) -> None:
    data = read_dataset(args.dataset)
    owners: dict[str, list[str]] = defaultdict(list)
    for row in data["videos"]:
        for raw in row.get("subtitleFiles") or []:
            owners[str(Path(raw).resolve())].append(video_id(row))
    migrated, ambiguous, missing = 0, 0, 0
    receipts: dict[str, Any] = {}
    for row in data["videos"]:
        vid = video_id(row)
        sources = [Path(raw) for raw in row.get("subtitleFiles") or []]
        if not vid or not sources:
            continue
        row["legacySubtitleFiles"] = [str(path) for path in sources]
        if any(len(owners[str(path.resolve())]) > 1 for path in sources):
            row["subtitleFiles"] = []
            row["subtitleStatus"] = "needs-refetch"
            ambiguous += 1
            receipts[vid] = {"status": "ambiguous-shared-path", "sources": [str(path) for path in sources]}
            continue
        targets = []
        for source in sources:
            if not source.exists():
                missing += 1
                continue
            folder = args.output_dir / vid
            folder.mkdir(parents=True, exist_ok=True)
            target = folder / source.name
            if source.resolve() != target.resolve():
                shutil.copy2(source, target)
            targets.append(str(target.resolve()))
        row["subtitleFiles"] = targets
        row["subtitleStatus"] = "complete" if targets else "needs-refetch"
        row["captionStorage"] = "video-id"
        migrated += int(bool(targets))
        receipts[vid] = {"status": "migrated" if targets else "missing", "files": targets}
    data["generatedAt"] = now()
    data["captionMigrationAt"] = now()
    write_json(args.dataset, data)
    write_json(args.receipt, {"generatedAt": now(), "migrated": migrated, "ambiguous": ambiguous,
                              "missing": missing, "videos": receipts})
    print(json.dumps({"migrated": migrated, "ambiguous": ambiguous, "missing": missing,
                      "receipt": str(args.receipt)}, ensure_ascii=False))


def pcm_envelope(path: Path, seconds: int) -> str:
    cmd = ["ffmpeg", "-v", "error", "-i", str(path), "-t", str(seconds), "-ac", "1", "-ar", "8000",
           "-af", "highpass=f=100,lowpass=f=3000", "-f", "s16le", "-"]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode or len(result.stdout) < 16000:
        raise RuntimeError(result.stderr.decode("utf-8", errors="ignore")[-1000:] or "audio decode failed")
    samples = struct.unpack(f"<{len(result.stdout)//2}h", result.stdout[:len(result.stdout)//2*2])
    frame = 4000
    energies = [math.sqrt(sum(value * value for value in samples[i:i+frame]) / max(1, len(samples[i:i+frame])))
                for i in range(0, len(samples), frame) if len(samples[i:i+frame]) >= frame // 2]
    baseline = statistics.median(energies) or 1
    levels = [max(0, min(15, round(4 * math.log2(max(value, 1) / baseline) + 8))) for value in energies]
    # Coarse normalized loudness levels survive common AAC/Opus re-encoding
    # better than exact PCM hashes and are cheap to compare.
    return "".join("0123456789abcdef"[value] for value in levels)


def audio_envelope_similarity(a: str, b: str, max_offset: int = 10) -> float:
    if not a or not b:
        return 0.0
    best = 0.0
    minimum_overlap = int(min(len(a), len(b)) * .8)
    for offset in range(-max_offset, max_offset + 1):
        start_a, start_b = max(0, offset), max(0, -offset)
        overlap = min(len(a) - start_a, len(b) - start_b)
        if overlap < minimum_overlap:
            continue
        close = sum(abs(int(a[start_a+i], 16) - int(b[start_b+i], 16)) <= 1 for i in range(overlap))
        best = max(best, close / overlap)
    return best


def command_audio_fingerprints(args: argparse.Namespace) -> None:
    data = read_dataset(args.dataset)
    receipts = read_dataset(args.receipt) if args.receipt.exists() else {"videos": []}
    receipt_map = {row["id"]: row for row in receipts.get("videos", [])}
    requested = set(args.id or [])
    if args.dedupe_report and args.dedupe_report.exists():
        report = json.loads(args.dedupe_report.read_text(encoding="utf-8"))
        requested.update(member["id"] for group in report.get("groups", []) for member in group.get("members", []))
    processed = 0
    for row in data["videos"]:
        vid = video_id(row)
        if (not vid or (requested and vid not in requested) or row.get("audioFingerprint") or
                (vid in receipt_map and not args.retry_failures) or (args.limit and processed >= args.limit)):
            continue
        folder = args.output_dir / vid
        folder.mkdir(parents=True, exist_ok=True)
        media = next((Path(raw) for raw in row.get("localMediaFiles") or [] if Path(raw).exists()), None)
        if media is None and row.get("localFolder"):
            local_folder = Path(row["localFolder"])
            media = next((path for path in local_folder.glob("*")
                          if path.suffix.lower() in {".mp4", ".webm", ".mkv", ".m4a", ".mp3", ".wav"}), None)
        temporary = False
        try:
            if media is None:
                output = folder / "sample.%(ext)s"
                result = run(["yt-dlp", "--no-playlist", "-f", "worstaudio/bestaudio", "--download-sections",
                              f"*0-{args.seconds}", "-o", str(output), f"https://www.youtube.com/watch?v={vid}"])
                if result.returncode:
                    raise RuntimeError(result.stderr[-1000:] or "audio sample download failed")
                media = next((path for path in folder.glob("sample.*") if path.suffix != ".part"), None)
                temporary = True
            if media is None:
                raise RuntimeError("audio sample missing")
            signature = pcm_envelope(media, args.seconds)
            row["audioFingerprint"] = {"algorithm": "pcm-envelope-v1", "signature": signature,
                                       "sampleSeconds": args.seconds, "createdAt": now()}
            receipt_map[vid] = {"id": vid, "ok": True, "createdAt": now(), "sample": str(media)}
        except (RuntimeError, OSError) as exc:
            receipt_map[vid] = {"id": vid, "ok": False, "createdAt": now(), "error": str(exc), "retryEligible": True}
        finally:
            if temporary and media and media.exists() and not args.keep_samples:
                media.unlink()
            processed += 1
            write_json(args.dataset, data)
            write_json(args.receipt, {"generatedAt": now(), "videos": list(receipt_map.values())})
    print(json.dumps({"processed": processed, "successful": sum(1 for row in receipt_map.values() if row.get("ok")),
                      "receipt": str(args.receipt)}, ensure_ascii=False))


def clean_title(text: str) -> str:
    text = re.sub(r"&(?:amp|#39|quot);", " ", text.lower())
    text = re.sub(r"\b(full|new|latest|watch|live|official|complete|entire|interview|presentation|talk|speech)\b", " ", text)
    return " ".join(re.sub(r"[^a-z0-9]+", " ", text).split())


def caption_tokens(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8", errors="ignore").lower()
    text = re.sub(r"\d\d:\d\d:\d\d[^\n]*|^\d+$", " ", text, flags=re.M)
    words = re.findall(r"[a-z0-9']+", text)
    return {" ".join(words[i:i+5]) for i in range(max(0, len(words)-4))}


def caption_digest(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8", errors="ignore").lower()
    text = re.sub(r"\d\d:\d\d:\d\d[^\n]*|^\d+$", " ", text, flags=re.M)
    words = re.findall(r"[a-z0-9']+", text)
    if len(words) < 100:
        return None
    normalized = " ".join(words)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def command_dedupe(args: argparse.Namespace) -> None:
    videos = read_dataset(args.dataset)["videos"]
    registry = load_source_registry(args.source_registry)
    n, parent = len(videos), list(range(len(videos)))
    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    def union(a: int, b: int) -> None:
        a, b = find(a), find(b)
        if a != b: parent[b] = a
    def caption_path(v: dict[str, Any]) -> Path | None:
        # Existing archives may store captions in title-based folders and keep
        # their absolute locations in subtitleFiles.
        for raw in v.get("subtitleFiles") or []:
            path = Path(raw)
            if path.exists() and path.suffix.lower() == ".srt":
                return path
        return next(iter(args.captions_dir.glob(f"{video_id(v)}/**/*.srt")), None)

    caption_paths = {video_id(v): caption_path(v) for v in videos if video_id(v)}
    path_owners: dict[str, list[str]] = defaultdict(list)
    for vid, path in caption_paths.items():
        if path:
            path_owners[str(path)].append(vid)
    # Title-based legacy folders may be shared by distinct videos with the same
    # title. Such a file cannot safely prove that the videos are identical.
    for vid, path in list(caption_paths.items()):
        if path and len(path_owners[str(path)]) > 1:
            caption_paths[vid] = None
    signals: dict[tuple[int, int], list[str]] = defaultdict(list)
    # Metadata comparisons are blocked by 30-second duration buckets. This
    # avoids quadratic work across obviously unrelated long-form videos.
    duration_buckets: dict[int, list[int]] = defaultdict(list)
    for i, video in enumerate(videos):
        duration_buckets[duration_seconds(video) // 30].append(i)
    compared: set[tuple[int, int]] = set()
    for bucket, own in duration_buckets.items():
        nearby = own + duration_buckets.get(bucket - 1, []) + duration_buckets.get(bucket + 1, [])
        for i in own:
            for j in nearby:
                if i >= j or (i, j) in compared:
                    continue
                compared.add((i, j))
                a, b = videos[i], videos[j]
                if video_id(a) == video_id(b): union(i, j); signals[(i,j)].append("same_video_id"); continue
                da, db = duration_seconds(a), duration_seconds(b)
                if min(da, db) < 480 or abs(da-db) > 10:
                    continue
                title_sim = SequenceMatcher(None, clean_title(str(a.get("title", ""))), clean_title(str(b.get("title", "")))).ratio()
                if title_sim >= .78:
                    union(i, j); signals[(i,j)].append("title_duration")

    # Exact normalized-caption fingerprints are strong, fast evidence. Near
    # matches remain governed by title + duration to avoid unsafe over-deletion.
    digest_groups: dict[str, list[int]] = defaultdict(list)
    for i, video in enumerate(videos):
        path = caption_paths.get(video_id(video))
        if path:
            digest = caption_digest(path)
            if digest:
                digest_groups[digest].append(i)
    for indices in digest_groups.values():
        if len(indices) < 2:
            continue
        anchor = indices[0]
        for i in indices[1:]:
            union(anchor, i)
            signals[(anchor, i)].append("caption_exact")
    audio_indices = [i for i, video in enumerate(videos) if video.get("audioFingerprint", {}).get("signature")]
    audio_buckets: dict[int, list[int]] = defaultdict(list)
    for i in audio_indices:
        audio_buckets[duration_seconds(videos[i]) // 60].append(i)
    audio_compared: set[tuple[int, int]] = set()
    for bucket, own in audio_buckets.items():
        nearby = own + audio_buckets.get(bucket - 1, []) + audio_buckets.get(bucket + 1, [])
        for i in own:
            for j in nearby:
                if i >= j or (i, j) in audio_compared:
                    continue
                audio_compared.add((i, j))
                sa = videos[i]["audioFingerprint"]["signature"]
                sb = videos[j]["audioFingerprint"]["signature"]
                similarity = audio_envelope_similarity(sa, sb)
                if min(len(sa), len(sb)) >= 30 and similarity >= .90:
                    union(i, j)
                    signals[(i, j)].append(f"audio_envelope:{similarity:.3f}")
    groups: dict[int, list[int]] = defaultdict(list)
    for i in range(n): groups[find(i)].append(i)
    output = {"generatedAt": now(), "dataset": str(args.dataset), "groups": []}
    for indices in groups.values():
        if len(indices) < 2: continue
        def canonical_rank(i: int) -> tuple[int, int, int, int, int]:
            video = videos[i]
            source_points, _ = provenance_score(video, registry)
            published = str(video.get("publishedAt") or "99999999").replace("-", "").replace(":", "")
            digits = re.sub(r"\D", "", published)
            earliest = -int((digits + "9" * 20)[:14]) if digits else -99999999999999
            return (source_points, duration_seconds(video), int(video.get("height") or 0),
                    int(bool(video.get("subtitleFiles"))), earliest)
        ranked = sorted(indices, key=canonical_rank, reverse=True)
        canonical = ranked[0]
        members = []
        for i in ranked:
            pair_signals = [s for (a,b), ss in signals.items() if i in (a,b) for s in ss]
            members.append({"id": video_id(videos[i]), "role": "canonical" if i == canonical else "mirror", "signals": pair_signals})
        output["groups"].append({"groupId": f"DUP-{len(output['groups'])+1:04d}", "canonicalId": video_id(videos[canonical]), "members": members})
    output["duplicateGroups"] = len(output["groups"])
    output["extraCopies"] = sum(len(g["members"])-1 for g in output["groups"])
    write_json(args.output, output)
    print(json.dumps({"groups": output["duplicateGroups"], "extraCopies": output["extraCopies"], "output": str(args.output)}, ensure_ascii=False))


def command_queue(args: argparse.Namespace) -> None:
    videos = read_dataset(args.dataset)["videos"]
    registry = load_source_registry(args.source_registry)
    report = json.loads(args.dedupe_report.read_text()) if args.dedupe_report.exists() else {"groups": []}
    mirrors = {m["id"] for g in report.get("groups", []) for m in g["members"] if m["role"] != "canonical"}
    rows = []
    for video in videos:
        score, reasons = quality_score(video, registry)
        source_points, source_name = provenance_score(video, registry)
        video["provenanceScore"] = source_points
        if source_name:
            video["provenanceSource"] = source_name
        video["qualityScore"], video["rejectionReasons"] = score, reasons
        if video_id(video) not in mirrors and score >= args.min_score:
            rows.append(video)
    rows.sort(key=lambda x: (-x["qualityScore"], -duration_seconds(x), video_id(x)))
    write_json(args.output, {"generatedAt": now(), "minScore": args.min_score, "videos": rows})
    print(json.dumps({"queued": len(rows), "output": str(args.output)}, ensure_ascii=False))


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    sub = root.add_subparsers(dest="command", required=True)
    p = sub.add_parser("discover"); p.add_argument("--query", action="append", required=True); p.add_argument("--limit", type=int, default=25); p.add_argument("--output", type=Path, required=True); p.set_defaults(func=command_discover)
    p = sub.add_parser("channel"); p.add_argument("--channel-url", required=True); p.add_argument("--match", default="elon|musk"); p.add_argument("--limit", type=int, default=300); p.add_argument("--output", type=Path, required=True); p.set_defaults(func=command_channel)
    p = sub.add_parser("add"); p.add_argument("--url", action="append", required=True); p.add_argument("--output", type=Path, required=True); p.set_defaults(func=command_add)
    p = sub.add_parser("enrich"); p.add_argument("--dataset", type=Path, required=True); p.add_argument("--receipt", type=Path, required=True); p.add_argument("--limit", type=int); p.set_defaults(func=command_enrich)
    p = sub.add_parser("captions"); p.add_argument("--dataset", type=Path, required=True); p.add_argument("--output-dir", type=Path, required=True); p.add_argument("--langs", default="en,en-orig,zh-Hans"); p.add_argument("--limit", type=int); p.set_defaults(func=command_captions)
    p = sub.add_parser("migrate-captions"); p.add_argument("--dataset", type=Path, required=True); p.add_argument("--output-dir", type=Path, required=True); p.add_argument("--receipt", type=Path, required=True); p.set_defaults(func=command_migrate_captions)
    p = sub.add_parser("audio-fingerprints"); p.add_argument("--dataset", type=Path, required=True); p.add_argument("--output-dir", type=Path, required=True); p.add_argument("--receipt", type=Path, required=True); p.add_argument("--seconds", type=int, default=120); p.add_argument("--limit", type=int); p.add_argument("--id", action="append"); p.add_argument("--dedupe-report", type=Path); p.add_argument("--keep-samples", action="store_true"); p.add_argument("--retry-failures", action="store_true"); p.set_defaults(func=command_audio_fingerprints)
    p = sub.add_parser("dedupe"); p.add_argument("--dataset", type=Path, required=True); p.add_argument("--captions-dir", type=Path, required=True); p.add_argument("--output", type=Path, required=True); p.add_argument("--source-registry", type=Path); p.set_defaults(func=command_dedupe)
    p = sub.add_parser("queue"); p.add_argument("--dataset", type=Path, required=True); p.add_argument("--dedupe-report", type=Path, required=True); p.add_argument("--output", type=Path, required=True); p.add_argument("--min-score", type=int, default=60); p.add_argument("--source-registry", type=Path); p.set_defaults(func=command_queue)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        args.func(args); return 0
    except (RuntimeError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr); return 1


if __name__ == "__main__":
    raise SystemExit(main())
