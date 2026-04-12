#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import re


TRIP_BLOG = Path('/mnt/d/ai/openclaw/trip-blog')
G_READY = Path('/mnt/d/GoogleDrive/openclaw/trip-blog-ready')


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def extract_block(text: str, heading: str) -> str:
    m = re.search(rf'^## {re.escape(heading)}\n(.*?)(?=^## |\Z)', text, re.M | re.S)
    return m.group(1).strip() if m else ''


def extract_bullets(text: str, heading: str) -> list[str]:
    block = extract_block(text, heading)
    return [re.sub(r'^-\s*', '', line).strip() for line in block.splitlines() if line.strip().startswith('- ')]


def first_value(text: str, label: str) -> str:
    m = re.search(rf'- {re.escape(label)}:\s*(.+)', text)
    return m.group(1).strip() if m else ''


def sanitize_public_text(text: str) -> str:
    text = text.replace('自宅周辺', '福山市周辺')
    return text.replace('福山を出発', '福山市を出発')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('trip_dir')
    args = ap.parse_args()

    trip_dir = Path(args.trip_dir)
    plan = read_text(trip_dir / 'plan.md')
    live = read_text(trip_dir / 'live-log.md')
    summary = read_text(trip_dir / 'summary.md')
    template = read_text(TRIP_BLOG / 'templates' / 'post.template.md')

    trip_name = first_value(summary, '旅行名') or trip_dir.name
    date = first_value(summary, '日付')
    area = first_value(summary, 'エリア')
    slug = first_value(summary, '公開用スラッグ') or trip_dir.name
    title = re.search(r'- タイトル候補1:\s*(.+)', extract_block(summary, 'ブログ化用要点'))
    title = title.group(1).strip() if title else trip_name

    intro_src = sanitize_public_text(extract_block(plan, '出発前計画'))
    total = sanitize_public_text(extract_block(summary, '総評'))
    intro = intro_src + ('\n\n' + total if total else '')

    route_block = extract_block(plan, '立ち寄り候補')
    route = []
    for line in route_block.splitlines():
        s = line.strip()
        if re.match(r'^\d+\.', s):
            route.append(re.sub(r'^\d+\.\s*', '', s))
    route_summary = '\n'.join([f'- {x}' for x in route]) or '- ルートは後で追記。'

    highlights = '\n'.join([f'- {x}' for x in extract_bullets(summary, '印象に残った場所')])
    good_points = '\n'.join([f'- {x}' for x in extract_bullets(summary, '良かった点')])
    bad_points = '\n'.join([f'- {x}' for x in extract_bullets(summary, '微妙だった点')])
    next_time = '\n'.join([f'- {x}' for x in extract_bullets(summary, '次回改善')])

    photo_candidates = re.findall(r'^  - (.+)$', extract_block(summary, 'ブログ化用要点'), re.M)
    cover_image = ''
    if photo_candidates:
        cover_image = f'/images/{slug}/cover.jpg'

    values = {
        'title': title,
        'date': date,
        'slug': slug,
        'area': area,
        'area_tag': area.replace('・', '-').replace(' ', '-'),
        'cover_image': cover_image,
        'intro': intro.strip(),
        'route_summary': route_summary.strip(),
        'highlights': highlights.strip(),
        'good_points': good_points.strip(),
        'bad_points': bad_points.strip(),
        'next_time': next_time.strip(),
    }

    post = template
    for k, v in values.items():
        post = post.replace('{{' + k + '}}', v)

    drafts = TRIP_BLOG / 'drafts'
    posts = TRIP_BLOG / 'posts'
    public_images = TRIP_BLOG / 'public' / 'images' / slug
    drafts.mkdir(parents=True, exist_ok=True)
    posts.mkdir(parents=True, exist_ok=True)
    public_images.mkdir(parents=True, exist_ok=True)
    G_READY.mkdir(parents=True, exist_ok=True)

    preview_path = drafts / f'{slug}-preview.md'
    meta_path = drafts / f'{slug}-meta.json'
    filename_slug = slug
    if date and slug.startswith(date + '-'):
        filename_slug = slug[len(date) + 1:]
    post_path = posts / f'{date}-{filename_slug}.md'
    g_ready_post = G_READY / f'{date}-{filename_slug}.html'

    preview_path.write_text(post, encoding='utf-8')
    post_path.write_text(post, encoding='utf-8')

    meta = {
        'trip_name': trip_name,
        'date': date,
        'area': area,
        'slug': slug,
        'draft': True,
        'trip_dir': str(trip_dir),
        'post_path': str(post_path),
        'g_ready_path': str(g_ready_post),
        'photo_candidates': photo_candidates,
        'source_files': ['plan.md', 'live-log.md', 'summary.md'],
        'publish_check': 'human_required'
    }
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')

    print(post_path)
    print(g_ready_post)


if __name__ == '__main__':
    main()
