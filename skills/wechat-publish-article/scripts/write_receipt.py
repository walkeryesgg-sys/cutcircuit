#!/usr/bin/env python3
"""Write a non-secret WeChat delivery receipt beside an article package."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("article", type=Path)
    parser.add_argument("--content-hash", required=True)
    parser.add_argument("--method", choices=["browser", "api", "remote-api"], required=True)
    parser.add_argument("--status", choices=["draft", "published"], required=True)
    parser.add_argument("--result", choices=["success", "failed"], default="success")
    parser.add_argument("--remote-id", default="")
    args = parser.parse_args()

    article = args.article.expanduser().resolve()
    if not article.is_file():
        raise SystemExit(f"Article not found: {article}")
    publish_dir = article.parent / "publish"
    publish_dir.mkdir(exist_ok=True)
    receipt = publish_dir / f"wechat-{args.content_hash}.json"
    payload = {
        "channel": "wechat-official-account",
        "article": article.name,
        "content_hash": args.content_hash,
        "method": args.method,
        "status": args.status,
        "result": args.result,
        "remote_id": args.remote_id or None,
        "recorded_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    }
    receipt.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(receipt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
