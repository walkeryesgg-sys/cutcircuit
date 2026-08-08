#!/usr/bin/env python3
"""Flag high-risk Chinese caption boundaries in a JSON cue ledger."""

import argparse
import json
import re
import sys
from pathlib import Path

END_PARTICLES = ("和", "与", "或", "但", "而", "所以", "因为", "如果", "虽然", "以及", "并且", "把", "被", "对", "向", "从", "由", "为", "在", "通过", "根据")
START_ORPHANS = ("的", "了", "着", "过", "吗", "呢", "而且", "但是", "所以", "然后", "而是", "那么")


def cue_list(payload):
    if isinstance(payload, list):
        return payload
    for key in ("cues", "captions", "subtitles", "items"):
        if isinstance(payload.get(key), list):
            return payload[key]
    raise ValueError("JSON must be a cue list or contain cues/captions/subtitles/items")


def text_of(cue):
    for key in ("text", "zh", "caption", "content"):
        if isinstance(cue.get(key), str):
            return cue[key].strip()
    return ""


def stripped(text):
    return re.sub(r"[\s\"'“”‘’（）()【】\[\]]+$", "", text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--strict", action="store_true", help="exit 1 when warnings exist")
    args = parser.parse_args()
    cues = cue_list(json.loads(args.ledger.read_text(encoding="utf-8")))
    warnings = []
    for index, cue in enumerate(cues):
        text = stripped(text_of(cue))
        if not text:
            warnings.append({"cue": index + 1, "type": "empty", "text": text})
            continue
        visible = text.rstrip("，,。！？；：?!;:")
        for token in END_PARTICLES:
            if visible.endswith(token):
                warnings.append({"cue": index + 1, "type": "high-risk-ending", "token": token, "text": text})
                break
        if index + 1 < len(cues):
            next_text = text_of(cues[index + 1]).lstrip("，,。！？；：?!;: ")
            for token in START_ORPHANS:
                if next_text.startswith(token):
                    warnings.append({"cue": index + 2, "type": "orphaned-opening", "token": token, "text": next_text})
                    break
        if len(visible) > 44:
            warnings.append({"cue": index + 1, "type": "layout-review", "characters": len(visible), "text": text})
    report = {"cue_count": len(cues), "warning_count": len(warnings), "warnings": warnings}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if args.strict and warnings else 0


if __name__ == "__main__":
    sys.exit(main())
