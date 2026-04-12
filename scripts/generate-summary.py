#!/usr/bin/env python3
from pathlib import Path
import argparse
import re


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def bullets_under(text: str, heading: str) -> list[str]:
    m = re.search(rf'^## {re.escape(heading)}\n(.*?)(?=^## |\Z)', text, re.M | re.S)
    if not m:
        return []
    return [re.sub(r'^-\s*', '', line).strip() for line in m.group(1).splitlines() if line.strip().startswith('- ')]


def paragraphs_under(text: str, heading: str) -> str:
    m = re.search(rf'^## {re.escape(heading)}\n(.*?)(?=^## |\Z)', text, re.M | re.S)
    return m.group(1).strip() if m else ''


def extract_live_sections(text: str) -> list[tuple[str, list[str]]]:
    sections = []
    for m in re.finditer(r'^###\s+(.*?)\n(.*?)(?=^###\s+|\Z)', text, re.M | re.S):
        title = m.group(1).strip()
        lines = [re.sub(r'^-\s*', '', x).strip() for x in m.group(2).splitlines() if x.strip().startswith('- ')]
        sections.append((title, lines))
    return sections


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('trip_dir')
    args = ap.parse_args()

    trip_dir = Path(args.trip_dir)
    plan = read_text(trip_dir / 'plan.md')
    live = read_text(trip_dir / 'live-log.md')
    summary_path = trip_dir / 'summary.md'
    existing = read_text(summary_path) if summary_path.exists() else ''

    title_line = re.search(r'- 旅行名:\s*(.+)', existing) or re.search(r'- 旅行名:\s*(.+)', plan)
    date_line = re.search(r'- 日付:\s*(.+)', existing) or re.search(r'- 日付:\s*(.+)', plan)
    area_line = re.search(r'- エリア:\s*(.+)', existing) or re.search(r'- エリア:\s*(.+)', plan)
    slug_line = re.search(r'- 公開用スラッグ:\s*(.+)', existing) or re.search(r'- スラッグ候補:\s*(.+)', plan)

    sections = extract_live_sections(live)
    highlights = []
    weak_points = []
    memorable = []
    next_time = []

    for title, lines in sections:
        joined = ' '.join(lines)
        if '写真' not in title:
            memorable.append(title)
        if any('良' in x or 'good' in x.lower() for x in lines):
            highlights.extend([x for x in lines if '写真:' not in x][:2])
        if any('行けなかった' in x or '厳し' in x or '未舗装' in x for x in lines):
            weak_points.extend([x for x in lines if '写真:' not in x][:2])
        if any('次回' in x for x in lines):
            next_time.extend([x for x in lines if '次回' in x])

    if not highlights:
        highlights = [x for _, lines in sections for x in lines if '写真:' not in x][:4]
    if not weak_points:
        weak_points = [x for _, lines in sections for x in lines if ('行けなかった' in x or '厳し' in x or '未舗装' in x)][:3]

    plan_intro = paragraphs_under(plan, '出発前計画').strip()
    candidate_text = paragraphs_under(plan, 'ブログ化メモ')
    title_candidates = re.findall(r'- タイトル案\d*:\s*(.+)', candidate_text)
    photo_candidates = [x.replace('写真:','').strip() for _, lines in sections for x in lines if x.startswith('写真:')]

    total_summary = plan_intro or '日帰りで景色の良い立ち寄り先を巡った旅行記録。'
    if highlights:
        total_summary += '\n' + '特に ' + '、'.join(dict.fromkeys(highlights[:2])) + ' が印象に残った。'

    content = f'''# summary.md

## 旅行概要
- 旅行名: {title_line.group(1).strip() if title_line else trip_dir.name}
- 日付: {date_line.group(1).strip() if date_line else ''}
- エリア: {area_line.group(1).strip() if area_line else ''}
- 公開用スラッグ: {slug_line.group(1).strip() if slug_line else trip_dir.name}
- draft: true

## 総評
{total_summary}

## 良かった点
'''
    for x in dict.fromkeys(highlights[:5]):
        content += f'- {x}\n'
    content += '\n## 微妙だった点\n'
    for x in dict.fromkeys(weak_points[:5]):
        content += f'- {x}\n'
    content += '\n## 印象に残った場所\n'
    for x in dict.fromkeys(memorable[:6]):
        content += f'- {x}\n'
    content += '\n## 次回改善\n'
    for x in dict.fromkeys(next_time[:5]):
        content += f'- {x}\n'
    if not next_time:
        content += '- 次回も再訪したい場所と改善点を追記する。\n'
    content += '\n## ブログ化用要点\n'
    for i, t in enumerate(title_candidates[:2], start=1):
        content += f'- タイトル候補{i}: {t}\n'
    if not title_candidates:
        content += f'- タイトル候補1: {title_line.group(1).strip() if title_line else trip_dir.name}\n'
    content += '- 見出し候補:\n'
    for x in dict.fromkeys(memorable[:4]):
        content += f'  - {x}\n'
    content += '- 使いたい写真:\n'
    for x in dict.fromkeys(photo_candidates[:6]):
        content += f'  - {x}\n'

    summary_path.write_text(content, encoding='utf-8')
    print(summary_path)


if __name__ == '__main__':
    main()
