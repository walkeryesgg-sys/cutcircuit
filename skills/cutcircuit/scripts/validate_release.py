#!/usr/bin/env python3
"""Check candidate-specific release receipts, not the truth of human judgments."""
import argparse
import hashlib
import json
import math
from pathlib import Path
from validate_timeline import validate as validate_timeline


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def validate(data, base):
    errors = []
    if not isinstance(data, dict):
        return ['release receipt must be an object']
    def check(ok, message):
        if not ok:
            errors.append(message)
    for key in ('candidate', 'script', 'timeline'):
        item = data.get(key, {})
        path = base / item.get('file', '__missing__')
        check(path.is_file(), key + ': missing artifact')
        if path.is_file():
            check(digest(path) == item.get('sha256'), key + ': stale hash')
        if key == 'timeline' and path.is_file():
            errors.extend(validate_timeline(json.loads(path.read_text()), path.parent))
    score = data.get('score')
    check(type(score) in (int, float) and math.isfinite(score) and 9.8 <= score <= 10, 'premium score not established')
    check(data.get('fatal_issues') == [], 'fatal issue list missing or unresolved')
    reviewer = data.get('reviewer', {})
    check(bool(reviewer.get('id')) and reviewer.get('independent') is True, 'independent reviewer missing')
    watch = data.get('full_watch', {})
    check(watch.get('completed') is True and watch.get('playback_rate') == 1, 'normal-speed full watch missing')
    check(watch.get('perceived_modalities') == ['video', 'audio'], 'full audiovisual perception not established')
    check(watch.get('candidate_sha256') == data.get('candidate', {}).get('sha256'), 'watch belongs to another candidate')
    for key in ('watch_notes', 'voice_provenance', 'boundary_audition', 'automated_checks', 'semantic_shot_review'):
        path = base / data.get('evidence', {}).get(key, '__missing__')
        check(path.is_file() and path.stat().st_size > 0, key + ': evidence missing')
    return errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('receipt', type=Path)
    args = parser.parse_args()
    try:
        failures = validate(json.loads(args.receipt.read_text()), args.receipt.resolve().parent)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        failures = [str(exc)]
    print(json.dumps({'passed': not failures, 'errors': failures}, ensure_ascii=False, indent=2))
    raise SystemExit(bool(failures))
