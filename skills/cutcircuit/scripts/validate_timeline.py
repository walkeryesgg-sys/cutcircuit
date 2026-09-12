#!/usr/bin/env python3
"""Validate a real audio-first edit contract. Does not replace audiovisual review."""
import argparse
import hashlib
import json
import math
import subprocess
import difflib
import re
from pathlib import Path


def validate(data, base):
    errors = []
    if not isinstance(data, dict):
        return ['timeline must be an object']
    def finite(value):
        return type(value) in (int, float) and math.isfinite(value)
    numeric_fields = {'start', 'end', 'duration', 'source_start', 'source_duration', 'trim_start', 'trim_end', 'audible_start', 'audible_end'}
    def numbers(obj, prefix=''):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key in numeric_fields and not finite(value):
                    errors.append(prefix + key + ': expected finite numeric seconds')
                numbers(value, prefix + key + '.')
        elif isinstance(obj, list):
            for i, value in enumerate(obj):
                numbers(value, prefix + str(i) + '.')
    numbers(data)
    if not finite(data.get('duration')) or data.get('duration', 0) <= 0:
        errors.append('duration: positive finite seconds required')
    for key in ('units', 'captions', 'shots'):
        if not isinstance(data.get(key), list) or not all(isinstance(x, dict) for x in data.get(key, [])):
            errors.append(key + ': expected array of objects')
    if errors:
        return errors
    def check(ok, message):
        if not ok:
            errors.append(message)
    def local(value):
        p = Path(value or '__missing__')
        return p if p.is_absolute() else base / p
    def artifact(value, label):
        p = local(value)
        check(p.is_file(), label + ': missing artifact')
        return p
    probes = {}
    def probe(p, kind, declared, label):
        if not p.is_file():
            return
        if str(p) not in probes:
            try:
                result = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(p)], capture_output=True, text=True, timeout=30, check=True)
                probes[str(p)] = json.loads(result.stdout)
            except (subprocess.SubprocessError, ValueError):
                probes[str(p)] = {}
        info = probes[str(p)]
        check(any(s.get('codec_type') == kind for s in info.get('streams', [])), label + ': real ' + kind + ' stream missing')
        try:
            actual = float(info['format']['duration'])
            check(finite(actual) and finite(declared) and abs(actual-declared) <= .05, label + ': declared duration differs from ffprobe')
        except (KeyError, TypeError, ValueError):
            check(False, label + ': cannot verify media duration')
    check(data.get('mode') in ('audio_first_rebuild', 'locked_picture_patch'), 'missing edit mode')
    renderer = data.get('caption_renderer')
    check(bool(renderer) and data.get('visible_caption_layers') == [renderer], 'exactly one visible caption renderer required')
    check(data.get('baked_caption_sources') == [], 'clean source required: baked captions present or not inspected')
    units = data.get('units', [])
    check(bool(units), 'no speech units')
    ids = [u.get('id') for u in units]
    check(all(ids) and len(set(ids)) == len(ids), 'missing/duplicate unit ID')
    by_id = {u.get('id'): u for u in units}
    previous = None
    for u in units:
        label = str(u.get('id'))
        check(bool(u.get('text', '').strip()), label + ': empty text')
        p = artifact(u.get('audio'), label + ' audio')
        if p.is_file():
            check(hashlib.sha256(p.read_bytes()).hexdigest() == u.get('audio_sha256'), label + ': stale audio hash')
            probe(p, 'audio', u.get('source_duration'), label)
        for field in ('generation_evidence', 'binding_review'):
            artifact(u.get(field), label + ' ' + field)
        receipt = local(u.get('binding_review'))
        if receipt.is_file():
            try:
                binding = json.loads(receipt.read_text())
                if not isinstance(binding, dict):
                    raise ValueError('binding must be an object')
                check(binding.get('audio_sha256') == u.get('audio_sha256') and binding.get('text_sha256') == hashlib.sha256(u.get('text', '').encode()).hexdigest(), label + ': binding receipt is stale or for another text')
                check(binding.get('trim_start') == u.get('trim_start') and binding.get('trim_end') == u.get('trim_end'), label + ': binding receipt trim differs')
                check(bool(binding.get('asr_text')) and binding.get('review_status') == 'verified' and bool(binding.get('review_evidence')), label + ': binding content not verified')
                artifact(binding.get('review_evidence'), label + ' content review evidence')
                normalize = lambda value: re.sub(r'[^\w]', '', str(value)).lower()
                similarity = difflib.SequenceMatcher(None, normalize(binding.get('asr_text', '')), normalize(u.get('text', ''))).ratio()
                check(similarity >= .55 or bool(binding.get('asr_correction_explanation')), label + ': substantial ASR mismatch without documented correction')
            except (ValueError, UnicodeError, OSError):
                check(False, label + ': invalid binding receipt JSON')
        check(bool(u.get('provider')) and bool(u.get('voice_id')), label + ': voice provenance missing')
        try:
            start, end = float(u['start']), float(u['end'])
            ts, te = float(u['trim_start']), float(u['trim_end'])
            a, b = float(u['audible_start']), float(u['audible_end'])
            check(0 <= ts <= a < b <= te <= float(u['source_duration']) + .002, label + ': invalid speech trim')
            check(0 <= start < end <= data['duration'] + .002, label + ': invalid destination')
            check(abs((end-start)-(te-ts)) <= .002, label + ': destination is not measured audio duration')
            audible_start, audible_end = start+a-ts, start+b-ts
            if previous:
                check(start >= previous['end']-.002, label + ': overlapping speech slots')
                gap = audible_start - previous['audible_end']
                check(gap >= -.002, label + ': overlapping audible words')
                check(.15 <= gap <= .75 or bool(u.get('gap_reason')), label + ': unexplained audible gap %.3fs' % gap)
            previous = dict(end=end, audible_end=audible_end)
        except (KeyError, TypeError, ValueError):
            errors.append(label + ': incomplete measured timing')
    captions = data.get('captions', [])
    check([c.get('unit_id') for c in captions] == ids, 'caption coverage/order differs from canonical units')
    last_end = -1
    for c in captions:
        u = by_id.get(c.get('unit_id'))
        if not u:
            errors.append('caption references unknown unit')
            continue
        check(c.get('text') == u.get('text', '').removesuffix('。'), str(u['id']) + ': caption text differs')
        try:
            onset = u['start'] + u['audible_start'] - u['trim_start']
            exit_time = u['start'] + u['audible_end'] - u['trim_start']
            check(abs(c['start']-onset) <= .1 and abs(c['end']-exit_time) <= .15, str(u['id']) + ': caption not bound to speech')
            check(c['start'] >= last_end-.002, 'overlapping caption cues')
            last_end = c['end']
        except (KeyError, TypeError):
            errors.append('incomplete caption timing')
    coverage = {key: [] for key in ids}
    for i, s in enumerate(data.get('shots', [])):
        label = 'shot %d' % i
        media = artifact(s.get('file'), label)
        artifact(s.get('review_evidence'), label + ' review')
        check(bool(s.get('picture_reason', '').strip()), label + ': no picture reason')
        check(s.get('kind') in ('footage', 'graphic'), label + ': unknown visual kind')
        check(bool(s.get('unit_ids')), label + ': no speech binding')
        try:
            check(0 <= s['start'] < s['end'] <= data['duration']+.002, label + ': invalid interval')
            if s.get('kind') == 'footage':
                probe(media, 'video', s.get('source_duration'), label)
                check(s.get('clarity_pass') is True and s.get('embedded_captions') is False, label + ': source inspection failed/missing')
                check(0 <= s['source_start'] and s['source_start'] + s['end']-s['start'] <= s['source_duration']+.002, label + ': source overrun')
            for key in s.get('unit_ids', []):
                check(key in by_id, label + ': unknown unit ' + str(key))
                if key in coverage:
                    coverage[key].append((s['start'], s['end']))
        except (KeyError, TypeError):
            errors.append(label + ': incomplete timing')
    for u in units:
        if 'start' not in u or 'end' not in u:
            continue
        cursor = u['start']
        for a, b in sorted(coverage[u.get('id')]):
            if a <= cursor+.002:
                cursor = max(cursor, b)
        check(cursor >= u['end']-.002, str(u.get('id')) + ': incomplete semantic picture coverage')
    cursor = 0
    for s in sorted(data.get('shots', []), key=lambda x: x.get('start', 0)):
        if 'start' in s and 'end' in s and s['start'] <= cursor+.002:
            cursor = max(cursor, s['end'])
    check(cursor >= data['duration']-.002, 'picture must cover entire timeline including opening, pauses and ending')
    return errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('timeline', type=Path)
    args = parser.parse_args()
    try:
        failures = validate(json.loads(args.timeline.read_text()), args.timeline.resolve().parent)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        failures = [str(exc)]
    print(json.dumps({'passed': not failures, 'errors': failures}, ensure_ascii=False, indent=2))
    raise SystemExit(bool(failures))
