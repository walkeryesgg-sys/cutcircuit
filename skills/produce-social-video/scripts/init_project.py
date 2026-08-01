#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from validate_brief import load_and_validate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--audience", default="")
    parser.add_argument("--platform", default="wechat-video-account")
    parser.add_argument("--vertical", action="store_true")
    parser.add_argument("--score-target", type=float, default=9.5)
    parser.add_argument(
        "--brief-file",
        type=Path,
        required=True,
        help="JSON file containing the user-approved production brief",
    )
    parser.add_argument(
        "--confirmed",
        action="store_true",
        help="Assert that the user explicitly approved the supplied brief",
    )
    args = parser.parse_args()

    if not args.confirmed:
        raise SystemExit(
            "Production is gated: obtain explicit user approval, then rerun with --confirmed."
        )
    if not args.brief_file.is_file():
        raise SystemExit(f"Approved brief file not found: {args.brief_file}")
    try:
        approved_brief, brief_errors = load_and_validate(args.brief_file)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    if brief_errors:
        joined = "\n".join(f"- {item}" for item in brief_errors)
        raise SystemExit(f"Approved brief is incomplete:\n{joined}")

    args.project.mkdir(parents=True, exist_ok=True)
    template = Path(__file__).resolve().parent.parent / "assets/video-project.template.json"
    data = json.loads(template.read_text(encoding="utf-8"))
    data.update(
        {
            "subject": args.subject,
            "audience": args.audience,
            "platform": args.platform,
            "width": 1080 if args.vertical else 1920,
            "height": 1920 if args.vertical else 1080,
            "release_score_target": args.score_target,
            "duration_target_seconds": approved_brief["delivery"][
                "duration_target_seconds"
            ],
            "brief_confirmation": {
                "confirmed": True,
                "confirmed_at": datetime.now(timezone.utc).isoformat(),
                "brief_file": str(args.brief_file.resolve()),
            },
            "approved_brief": approved_brief,
        }
    )
    data["checkpoints"]["brief_confirmed"] = True
    output = args.project / "video-project.json"
    if output.exists():
        raise SystemExit(f"Refusing to overwrite existing manifest: {output}")
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for folder in ("assets", "segments", "reports", "renders", "source"):
        (args.project / folder).mkdir(exist_ok=True)
    print(output)


if __name__ == "__main__":
    main()
