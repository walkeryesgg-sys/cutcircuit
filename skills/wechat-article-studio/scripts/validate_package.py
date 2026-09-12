#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_FRONTMATTER = {
    "type",
    "channel",
    "status",
    "title",
    "description",
    "cover",
    "cover_text",
}


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    values: dict[str, str] = {}
    for line in text[4:end].splitlines():
        match = re.match(r"^([a-zA-Z_][\w-]*):\s*(.*)$", line)
        if match:
            values[match.group(1)] = match.group(2).strip().strip("\"'")
    return values


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package", type=Path)
    args = parser.parse_args()
    root = args.package.expanduser().resolve()
    errors: list[str] = []

    articles = sorted(root.glob("*-正文.md"))
    metadata_files = sorted(root.glob("*-发布信息.md"))
    scorecard_files = sorted(root.glob("*-内容自检.md"))
    prompts = sorted((root / "covers" / "prompts").glob("*-封面提示词.md"))
    covers = sorted((root / "covers").glob("*-封面.png"))
    article = articles[0] if len(articles) == 1 else root / "<unique>-正文.md"
    metadata = (
        metadata_files[0]
        if len(metadata_files) == 1
        else root / "<unique>-发布信息.md"
    )
    scorecard = (
        scorecard_files[0]
        if len(scorecard_files) == 1
        else root / "<unique>-内容自检.md"
    )
    prompt = (
        prompts[0]
        if len(prompts) == 1
        else root / "covers" / "prompts" / "<unique>-封面提示词.md"
    )
    cover = (
        covers[0]
        if len(covers) == 1
        else root / "covers" / "<unique>-封面.png"
    )

    for path in (article, metadata, scorecard, prompt, cover):
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"missing or empty: {path.relative_to(root)}")

    if article.is_file():
        frontmatter = parse_frontmatter(article.read_text(encoding="utf-8"))
        missing = sorted(REQUIRED_FRONTMATTER - frontmatter.keys())
        if missing:
            errors.append(f"article frontmatter missing: {', '.join(missing)}")
        cover_text = frontmatter.get("cover_text", "")
        if not 4 <= len(cover_text) <= 10:
            errors.append("cover_text must contain 4–10 characters")
        description = frontmatter.get("description", "")
        if not 60 <= len(description) <= 100:
            errors.append("description should contain 60–100 characters")

    if scorecard.is_file():
        score_text = scorecard.read_text(encoding="utf-8")
        compliance = re.search(r"合规闸门[：:]\s*(PASS|FAIL|REVIEW)", score_text, re.I)
        total = re.search(r"公众号总分[：:]\s*(\d{1,3})\s*/\s*100", score_text)
        title_first_screen = re.search(
            r"\|\s*标题与首屏兑现\s*\|\s*(\d{1,2})\s*\|\s*20\s*\|",
            score_text,
        )
        learning = re.search(r"\|\s*学习价值\s*\|\s*(\d{1,2})\s*\|\s*20\s*\|", score_text)
        evidence = re.search(r"\|\s*证据与边界\s*\|\s*(\d{1,2})\s*\|\s*20\s*\|", score_text)
        rounds = re.search(r"修订轮次[：:]\s*(\d+)", score_text)
        if not compliance or compliance.group(1).upper() != "PASS":
            errors.append("content compliance gate must be PASS")
        if not total or int(total.group(1)) < 85:
            errors.append("official-account content score must be at least 85/100")
        if not title_first_screen or int(title_first_screen.group(1)) < 16:
            errors.append("title and first-screen payoff must be at least 16/20")
        if not learning or int(learning.group(1)) < 16:
            errors.append("learning value must be at least 16/20")
        if not evidence or int(evidence.group(1)) < 16:
            errors.append("evidence and boundaries must be at least 16/20")
        if not rounds or int(rounds.group(1)) > 3:
            errors.append("revision rounds must be recorded and no greater than 3")

    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"VALID: {root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
