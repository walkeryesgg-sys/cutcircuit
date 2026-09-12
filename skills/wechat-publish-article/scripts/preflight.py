#!/usr/bin/env python3
"""Validate a Markdown article package and emit a JSON preflight report."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, text
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if match:
            value = match.group(2).strip().strip("\"'")
            fields[match.group(1)] = value
    return fields, text[end + 5 :]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("article", type=Path)
    args = parser.parse_args()
    article = args.article.expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not article.is_file():
        print(json.dumps({"ok": False, "errors": [f"Article not found: {article}"]}, ensure_ascii=False))
        return 1

    text = article.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)
    title = meta.get("title", "").strip()
    summary = (meta.get("description") or meta.get("summary") or "").strip()
    cover_raw = (meta.get("cover") or meta.get("cover_image") or "").strip()

    if not title:
        errors.append("Missing frontmatter title")
    if not summary:
        errors.append("Missing frontmatter description or summary")
    elif not 40 <= len(summary) <= 140:
        warnings.append(f"Summary length is {len(summary)}; 60–120 Chinese characters is usually preferable")
    if not cover_raw:
        errors.append("Missing frontmatter cover")

    cover = (article.parent / cover_raw).resolve() if cover_raw and not Path(cover_raw).is_absolute() else Path(cover_raw)
    if cover_raw and not cover.is_file():
        errors.append(f"Cover not found: {cover}")

    if re.search(r"!\[\[.+?]]|\[\[.+?]]", body):
        errors.append("Unresolved Obsidian link or embed found")
    if re.search(r"\b(?:TODO|TBD|FIXME)\b|待补|待定", body, re.I):
        errors.append("Unresolved TODO marker found")
    if re.search(r"(?:/Users/|/home/|[A-Za-z]:\\\\)", text):
        errors.append("Private absolute filesystem path found in publishable content")

    for match in re.finditer(r"!\[[^\]]*]\(([^)]+)\)", body):
        raw = match.group(1).strip().split()[0].strip("<>")
        if re.match(r"^(?:https?:|data:)", raw):
            continue
        target = (article.parent / raw).resolve()
        if not target.is_file():
            errors.append(f"Inline image not found: {target}")

    digest = hashlib.sha256()
    digest.update(title.encode())
    digest.update(b"\0")
    digest.update(summary.encode())
    digest.update(b"\0")
    digest.update(body.strip().encode())
    digest.update(b"\0")
    if cover.is_file():
        digest.update(cover.read_bytes())
    content_hash = digest.hexdigest()
    receipt = article.parent / "publish" / f"wechat-{content_hash}.json"

    report = {
        "ok": not errors,
        "article": str(article),
        "package_root": str(article.parent),
        "title": title,
        "summary": summary,
        "cover": str(cover) if cover_raw else "",
        "content_hash": content_hash,
        "existing_receipt": str(receipt) if receipt.is_file() else None,
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
