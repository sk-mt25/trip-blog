# trip-blog publish repo

## 目的
- `D:\ai\openclaw\trip\` の旅行メモから公開用記事を生成する。
- 公開前は `draft: true` を維持し、人が最終確認する。
- 確認後、GitHub へ push し Cloudflare Pages で公開する。

## 最小公開構成
- `index.html` 記事一覧
- `posts\*.html` 個別記事
- `public\images\<slug>\` 画像
- `drafts\` 下書き確認用
- `templates\` 生成テンプレート
- `scripts\` 生成スクリプト

## 公開導線
1. `trip\YYYY-MM-DD_slug\` に plan/live-log/summary を置く
2. `generate-summary.py`
3. `generate-post.py`
4. `build-site.py`
5. Gフォルダへ HTML 保存
6. 人が最終確認
7. GitHub push
8. Cloudflare Pages 自動公開
