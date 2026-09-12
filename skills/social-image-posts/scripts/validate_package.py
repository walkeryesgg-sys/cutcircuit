#!/usr/bin/env python3
"""Validate package completeness; does not certify truth, aesthetics or platform approval."""
import argparse
import json
from pathlib import Path

PLATFORMS = {'xiaohongshu', 'wechat-channels', 'douyin'}


def validate(root):
    errors = []
    root = Path(root).resolve()

    def file(value, label):
        if not isinstance(value, str) or not value:
            errors.append(f'{label}: missing path')
            return None
        p = (root / value).resolve()
        if not p.is_relative_to(root):
            errors.append(f'{label}: path escapes package')
            return None
        if not p.is_file() or p.stat().st_size == 0:
            errors.append(f'{label}: missing/empty file {value}')
            return None
        return p

    for name in ('sources.md', 'storyboard.md', 'platform-check.md', 'review.md'):
        file(name, name)
    try:
        data = json.loads((root / 'manifest.json').read_text())
    except (OSError, ValueError) as e:
        return errors + [f'manifest.json: {e}']
    if not isinstance(data, dict):
        return errors + ['manifest must be an object']
    mode = data.get('mode')
    if mode not in {'copy', 'prompts', 'full'}:
        errors.append('mode must be copy, prompts or full')
    platforms = data.get('platforms')
    if (not isinstance(platforms, list) or not platforms
            or any(not isinstance(p, str) or p not in PLATFORMS for p in platforms)):
        return errors + ['platforms must be a nonempty list of supported platforms']
    if len(platforms) != len(set(platforms)):
        errors.append('duplicate platforms')
    for p in platforms:
        file(f'{p}/post.md', f'{p} copy')
    pages = data.get('pages')
    if not isinstance(pages, list):
        return errors + ['pages must be a list']
    Image = None
    if mode == 'full':
        try:
            from PIL import Image
        except ImportError:
            errors.append('Pillow required for image decoding: python3 -m pip install Pillow')
    orders = {p: [] for p in platforms}
    seen_images = set()
    for i, page in enumerate(pages, 1):
        label = f'page {i}'
        if not isinstance(page, dict):
            errors.append(f'{label}: must be an object')
            continue
        platform, order = page.get('platform'), page.get('order')
        if not isinstance(platform, str) or platform not in orders:
            errors.append(f'{label}: platform not in requested platforms')
            continue
        if type(order) is not int or order < 1:
            errors.append(f'{label}: order must be a positive integer')
        else:
            orders[platform].append(order)
        if mode in {'prompts', 'full'}:
            file(page.get('prompt'), f'{label} prompt')
        if mode != 'full':
            continue
        image = file(page.get('image'), f'{label} image')
        if image:
            key = (platform, image)
            if key in seen_images:
                errors.append(f'{label}: same image repeated within platform')
            seen_images.add(key)
        if type(page.get('ai_generated')) is not bool:
            errors.append(f'{label}: ai_generated must be boolean')
        if page.get('ai_generated') is True:
            disclosure = page.get('disclosure')
            if not isinstance(disclosure, str) or not disclosure.strip():
                errors.append(f'{label}: AI disclosure missing')
        if page.get('visual_review') != 'passed':
            errors.append(f'{label}: visual review not passed')
        if any(type(page.get(k)) is not int or page[k] <= 0 for k in ('width', 'height')):
            errors.append(f'{label}: invalid dimensions')
        if image and Image:
            try:
                with Image.open(image) as im:
                    actual_size = im.size
                    image_format = im.format
                    im.verify()
                with Image.open(image) as im:
                    im.load()
                if image_format not in {'PNG', 'JPEG', 'WEBP'}:
                    errors.append(f'{label}: unsupported delivery format {image_format}')
                if actual_size != (page.get('width'), page.get('height')):
                    errors.append(f'{label}: recorded dimensions differ from actual {actual_size}')
            except Exception as e:
                errors.append(f'{label}: image cannot be decoded ({e})')
    for p, seq in orders.items():
        if mode != 'copy' and not seq:
            errors.append(f'{p}: no pages delivered')
        if sorted(seq) != list(range(1, len(seq) + 1)):
            errors.append(f'{p}: page order must be unique and contiguous from 1')
    return errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package')
    args = parser.parse_args()
    issues = validate(args.package)
    print(json.dumps({'passed': not issues, 'errors': issues,
                      'scope': 'artifact consistency only; not factual or platform approval'},
                     ensure_ascii=False, indent=2))
    raise SystemExit(1 if issues else 0)
