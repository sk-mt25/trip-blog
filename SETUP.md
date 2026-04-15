# trip-blog 完成版運用フロー

## 結論
- 入力元は `D:\ai\openclaw\trip\` に統一する
- 1旅行 = 1フォルダで管理する
- 公開用出力は `D:\ai\openclaw\trip-blog\` に集約する
- 完成記事は GitHub へ push し、Cloudflare Pages で一般公開する
- Gドライブには完成版HTMLの最新版のみ保存する

## 推奨フォルダ構成

### 入力側
- `D:\ai\openclaw\trip\`
  - `YYYY-MM-DD_area-slug\`
    - `plan.md`
    - `live-log.md`
    - `summary.md`
    - `photos\`
    - `export\` 任意

### 出力側
- `D:\ai\openclaw\trip-blog\`
  - `posts\`
    - `YYYY-MM-DD-area-slug.md`
  - `public\images\YYYY-MM-DD-area-slug\`
  - `templates\site.template.html`
  - `scripts\build-site.py`
  - `site\`
    - `index.html`
    - `posts\*.html`
    - `images\YYYY-MM-DD-area-slug\`

## 実作業フロー
1. 旅行フォルダを作る
2. `summary.md` と `live-log.md` を整理する
3. 公開用記事を `posts/` に作る
4. 写真を選び、`public/images/<slug>/` に保存する
5. 記事本文に画像パスを入れる
6. `python3 scripts/build-site.py` を実行する
7. `site/` の見た目を確認する
8. 完成HTMLだけを `D:\GoogleDrive\openclaw\trip-blog-ready\` に保存する
9. `git add` → `git commit` → `git push`
10. Cloudflare Pages で production を確認する

## Cloudflare Pages 完成設定
- Project name: `trip-blog`
- GitHub repo: `sk-mt25/trip-blog`
- Framework preset: `None`
- Build command: `python3 scripts/build-site.py`
- Build output directory: `site`
- Root directory: `/`
- Access policy: 無効

## 公開確認ポイント
- `index.html` に重複記事がない
- 個別記事が正しく開く
- 写真が表示される
- スマホから production URL を直接開ける
- preview URL ではなく production URL を使う

## Gドライブ保存ルール
- 保存先: `D:\GoogleDrive\openclaw\trip-blog-ready\`
- 完成HTMLの最新版のみ置く
- 古い `.md`, `index.html`, 旧バージョンは削除する

## 今回の実績で確定した注意点
- 古い記事Markdownが `posts/` に残ると index に重複表示される
- build script は絶対パスではなく repo 相対で書く
- Cloudflare 上では Gドライブ出力を走らせない
- `public/images` は build 時に `site/images` へコピーする
- 公開できていても検索結果反映には時間がかかる
