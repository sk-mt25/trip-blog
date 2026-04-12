#!/usr/bin/env python3
from pathlib import Path
import argparse
import re

TRIP_ROOT = Path('/mnt/d/ai/openclaw/trip')
TEMPLATE_ROOT = Path('/mnt/d/ai/openclaw/trip-blog/templates')


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r'[^a-z0-9\-\s_]+', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text).strip('-')
    return text or 'trip'


def render(template: str, values: dict[str, str]) -> str:
    out = template
    for k, v in values.items():
        out = out.replace('{{' + k + '}}', v)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--date', required=True)
    ap.add_argument('--trip-name', required=True)
    ap.add_argument('--area', required=True)
    ap.add_argument('--start-city', default='福山市')
    ap.add_argument('--slug', default='')
    args = ap.parse_args()

    slug = args.slug or slugify(args.trip_name)
    folder = TRIP_ROOT / f'{args.date}_{slug}'
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'photos').mkdir(exist_ok=True)
    (folder / 'export').mkdir(exist_ok=True)

    values = {
        'trip_name': args.trip_name,
        'date': args.date,
        'area': args.area,
        'slug': slug,
        'start_city': args.start_city,
    }

    for name in ['plan.template.md', 'live-log.template.md', 'summary.template.md']:
        src = TEMPLATE_ROOT / name
        dst = folder / name.replace('.template', '')
        if not dst.exists():
            dst.write_text(render(src.read_text(encoding='utf-8'), values), encoding='utf-8')

    print(folder)


if __name__ == '__main__':
    main()
