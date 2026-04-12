# trip-blog 最小セットアップ案

## 結論
- 入力元は `D:\ai\openclaw\trip\` に統一する。
- 1旅行 = 1フォルダで `plan.md`, `live-log.md`, `summary.md`, `photos\` を持つ。
- 公開用出力は `D:\ai\openclaw\trip-blog\` に集約する。
- 公開直前の最終確認だけ人が行い、その後 GitHub へ push して Cloudflare Pages で公開する。

## 推奨フォルダ構成

### 入力側
- `D:\ai\openclaw\trip\`
  - `YYYY-MM-DD_area-slug\`
    - `plan.md`
    - `live-log.md`
    - `summary.md`
    - `photos\`
    - `export\` 任意, 中間生成物置き場

### 出力側
- `D:\ai\openclaw\trip-blog\`
  - `templates\`
    - `plan.template.md`
    - `live-log.template.md`
    - `summary.template.md`
    - `post.template.md`
  - `posts\`
    - `YYYY-MM-DD-area-slug.md`
  - `drafts\`
    - `YYYY-MM-DD-area-slug-preview.md`
    - `YYYY-MM-DD-area-slug-meta.json`
  - `public\images\YYYY-MM-DD-area-slug\`
  - `scripts\` 自動化スクリプト置き場
  - `README.md`

## テンプレート配置方法
- テンプレートは `D:\ai\openclaw\trip-blog\templates\` に固定配置する。
- 新規旅行作成時は、このテンプレートを元に `D:\ai\openclaw\trip\YYYY-MM-DD_area-slug\` へ展開する。
- テンプレート差し込み項目は以下で統一する。
  - `{{trip_name}}`
  - `{{date}}`
  - `{{area}}`
  - `{{slug}}`
  - `{{start_city}}`

## 新規旅行作成フロー
1. 旅行名を決める。
2. スラッグを決める。
3. `D:\ai\openclaw\trip\YYYY-MM-DD_area-slug\` を作成する。
4. 以下を自動生成する。
   - `plan.md`
   - `live-log.md`
   - `summary.md`
   - `photos\`
5. 必要なら `plan.md` から導入候補を仮生成する。

## ブログ記事生成フロー
1. `summary.md` を最優先で読む。
2. `plan.md` から出発前計画, 立ち寄り候補, タイトル案, 想定読者を補足する。
3. `live-log.md` から現地の描写, 良かった点, 失敗点, 写真候補を補足する。
4. 公開不要情報を除去する。
   - 個人情報
   - 自宅周辺情報
   - 公開不要な内部メモ
   - 公開価値の低い愚痴
   - セキュリティ上よくない情報
5. `trip-blog\drafts\` に preview と meta を出力する。
6. `trip-blog\posts\YYYY-MM-DD-area-slug.md` に `draft: true` で記事を書き出す。
7. 写真候補を `trip-blog\public\images\YYYY-MM-DD-area-slug\` に整理する。

## 完成品を Gフォルダに保存してから公開する流れ
1. `trip-blog\posts\YYYY-MM-DD-area-slug.md` を人が最終確認する。
2. OKなら完成版HTMLを `D:\GoogleDrive\openclaw\trip-blog-ready\` に保存する。
3. 必要に応じて画像も同じ旅行スラッグ単位で保存する。
4. 保存確認後、GitHub管理フォルダへ反映する。
5. GitHubへ push する。
6. Cloudflare Pages が自動ビルドして公開する。

## GitHub と Cloudflare Pages 連携準備
1. `trip-blog` を GitHub リポジトリ化する。
2. Cloudflare Pages に対象リポジトリを接続する。
3. デプロイ方式を決める。
   - 単純な静的公開
   - 静的サイトジェネレータ利用
4. 最初は複雑にせず、Markdown + 静的HTML変換の最小構成から始める。
5. 認証情報は workspace や memory に書かず、Windows側の安全な保管先で管理する。

## OpenClaw で自動化する準備内容
- 新規旅行フォルダ作成コマンド
- テンプレート展開
- `live-log.md` 追記支援
- `summary.md` 自動生成
- `posts\` 記事生成
- `Gフォルダ` へのHTML保存
- GitHub 反映前の差分確認
- push は人確認後に実行

## Windowsで扱いやすくするポイント
- 実体パスは `D:` に統一する。
- 旅行単位フォルダ名は `YYYY-MM-DD_area-slug` 形式に固定する。
- 日本語名は表示用に使い、ファイルや公開URLはスラッグ基準にする。
- 公開前原稿, 公開記事, 画像を別ディレクトリに分離する。

## 次の実装単位
1. テンプレート3種 + post template を固定化
2. 新規旅行作成スクリプトを作成
3. summary 生成スクリプトを作成
4. post 生成スクリプトを作成
5. Gフォルダ保存と GitHub反映の半自動フローを作成
