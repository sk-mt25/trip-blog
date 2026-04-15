# trip-blog publish repo

## 目的
- `D:\ai\openclaw\trip\` の旅行メモから公開用記事を生成する。
- 記事は Markdown で管理し、静的 HTML に変換して GitHub + Cloudflare Pages で公開する。
- 公開前は人が最終確認し、完成形だけを Gドライブへ保存する。

## 現在の公開構成
- `posts/` 公開用記事Markdown
- `public/images/<slug>/` 記事で使う画像
- `scripts/build-site.py` HTML生成スクリプト
- `templates/site.template.html` サイト共通テンプレート
- `site/index.html` 記事一覧
- `site/posts/*.html` 個別記事
- `site/images/<slug>/` 公開用画像

## 完成版の公開フロー
1. `D:\ai\openclaw\trip\YYYY-MM-DD_area-slug\` に旅行記録をまとめる
2. `summary.md` と `live-log.md` を元に記事草稿を作る
3. `trip-blog/posts/YYYY-MM-DD-area-slug.md` を仕上げる
4. 採用写真を `trip-blog/public/images/YYYY-MM-DD-area-slug/` に置く
5. `python3 scripts/build-site.py` で `site/` を再生成する
6. 人が見た目と文面を確認する
7. 完成HTMLのみを `D:\GoogleDrive\openclaw\trip-blog-ready\` に保存する
8. `git push` して Cloudflare Pages で公開する

## GitHub / Cloudflare Pages 設定
- GitHub repo: `https://github.com/sk-mt25/trip-blog`
- Cloudflare Pages project: `trip-blog`
- Framework preset: `None`
- Build command: `python3 scripts/build-site.py`
- Build output directory: `site`
- Root directory: `/`
- Access policy は無効化して一般公開する

## Gドライブ運用ルール
- 保存先: `D:\GoogleDrive\openclaw\trip-blog-ready\`
- 保存するのは **完成版HTMLの最新版のみ**
- 古い `.md` や旧HTMLは残さない
- 人向け保存は `.html` を優先する

## 注意点
- `public/images` は build 時に `site/images` へコピーされる
- Pages で確認するときは preview URL より production URL を優先する
- 公開直後は検索結果にすぐ出なくても正常
