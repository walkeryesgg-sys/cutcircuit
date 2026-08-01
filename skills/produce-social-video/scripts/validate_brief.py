#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


REQUIRED_TEXT = (
    "goal.purpose",
    "goal.viewer_takeaway",
    "audience.description",
    "audience.knowledge_level",
    "editorial.topic",
    "editorial.viewer_promise",
    "editorial.thesis",
    "editorial.factual_framing",
    "delivery.aspect_ratio",
    "delivery.language",
    "creative.opening",
    "creative.structure",
    "creative.tone",
    "creative.source_narration_balance",
    "identity.intro",
    "identity.captions",
    "identity.watermark",
    "identity.outro",
    "identity.voice",
    "identity.music",
    "identity.cover",
    "assets_rights.sourcing_permission",
)

REQUIRED_LIST = (
    "delivery.platforms",
    "deliverables",
    "acceptance.non_negotiables",
)


def get_path(data, dotted):
    value = data
    for part in dotted.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value


def validate_brief(data):
    errors = []
    if not isinstance(data, dict):
        return ["Brief must be a JSON object."]

    for dotted in REQUIRED_TEXT:
        value = get_path(data, dotted)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{dotted}: required non-empty text")

    for dotted in REQUIRED_LIST:
        value = get_path(data, dotted)
        if not isinstance(value, list) or not value:
            errors.append(f"{dotted}: required non-empty list")

    count = get_path(data, "delivery.video_count")
    if not isinstance(count, int) or isinstance(count, bool) or count < 1:
        errors.append("delivery.video_count: must be an integer >= 1")

    duration = get_path(data, "delivery.duration_target_seconds")
    if not isinstance(duration, (int, float)) or isinstance(duration, bool) or duration <= 0:
        errors.append("delivery.duration_target_seconds: must be a number > 0")

    target = get_path(data, "acceptance.release_target")
    if not isinstance(target, (int, float)) or isinstance(target, bool) or not 0 <= target <= 10:
        errors.append("acceptance.release_target: must be between 0 and 10")

    ratio = get_path(data, "delivery.aspect_ratio")
    if isinstance(ratio, str) and ratio not in {"16:9", "9:16", "1:1", "4:3", "3:4"}:
        errors.append("delivery.aspect_ratio: unsupported ratio")

    return errors


def load_and_validate(path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read brief JSON: {exc}") from exc
    return data, validate_brief(data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("brief", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        _, errors = load_and_validate(args.brief)
    except ValueError as exc:
        errors = [str(exc)]

    report = {"valid": not errors, "errors": errors}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif errors:
        print("Brief is incomplete:")
        for error in errors:
            print(f"- {error}")
    else:
        print("Brief is valid.")
    raise SystemExit(0 if not errors else 2)


if __name__ == "__main__":
    main()
