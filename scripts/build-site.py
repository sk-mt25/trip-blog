#!/usr/bin/env python3
from pathlib import Path
import html
import re

ROOT = Path('/mnt/d/ai/openclaw/trip-blog')
POSTS = ROOT / 'posts'
SITE = ROOT / 'site'
G_READY = Path('/mnt/d/GoogleDrive/openclaw/trip-blog-ready')
TEMPLATE = (ROOT / 'templates' / 'site.template.html').read_text(encoding='utf-8')


def md_to_html(text: str) -> str:
    lines = text.splitlines()
    out = []
    in_list = False
    in_frontmatter = False
    for line in lines:
        if line.strip() == '---':
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter:
            continue
        if line.startswith('# '):
            if in_list:
                out.append('</ul>')
                in_list = False
            out.append(f'<h1>{html.escape(line[2:].strip())}</h1>')
        elif line.startswith('## '):
            if in_list:
                out.append('</ul>')
                in_list = False
            out.append(f'<h2>{html.escape(line[3:].strip())}</h2>')
        elif line.startswith('- '):
            if not in_list:
                out.append('<ul>')
                in_list = True
            out.append(f'<li>{html.escape(line[2:].strip())}</li>')
        elif not line.strip():
            if in_list:
                out.append('</ul>')
                in_list = False
        else:
            if in_list:
                out.append('</ul>')
                in_list = False
            out.append(f'<p>{html.escape(line.strip())}</p>')
    if in_list:
        out.append('</ul>')
    return '\n'.join(out)


def first_match(pattern: str, text: str, default: str = '') -> str:
    m = re.search(pattern, text, re.M)
    return m.group(1).strip() if m else default


def render_page(title: str, description: str, content: str) -> str:
    page = TEMPLATE.replace('{{title}}', html.escape(title))
    page = page.replace('{{description}}', html.escape(description))
    page = page.replace('{{content}}', content)
    return page


def main():
    SITE.mkdir(parents=True, exist_ok=True)
    (SITE / 'posts').mkdir(parents=True, exist_ok=True)
    G_READY.mkdir(parents=True, exist_ok=True)

    cards = []
    for md_path in sorted(POSTS.glob('*.md')):
        text = md_path.read_text(encoding='utf-8')
        title = first_match(r'^title:\s*"?(.+?)"?$', text, md_path.stem)
        date = first_match(r'^date:\s*(.+)$', text)
        slug = first_match(r'^slug:\s*(.+)$', text, md_path.stem)
        description = first_match(r'^area:\s*"?(.+?)"?$', text, '')
        body = md_to_html(text)
        page = render_page(title, description, body)
        out = SITE / 'posts' / f'{slug}.html'
        out.write_text(page, encoding='utf-8')
        (G_READY / f'{slug}.html').write_text(page, encoding='utf-8')
        cards.append(f'<li><a href="./posts/{slug}.html">{html.escape(title)}</a> <span>({html.escape(date)})</span></li>')

    index_content = '<h1>trip-blog</h1><p>公開用記事一覧</p><ul>' + ''.join(cards) + '</ul>'
    index_page = render_page('trip-blog', 'trip blog index', index_content)
    (SITE / 'index.html').write_text(index_page, encoding='utf-8')
    (G_READY / 'index.html').write_text(index_page, encoding='utf-8')
    print(SITE)
    print(G_READY)


if __name__ == '__main__':
    main()
