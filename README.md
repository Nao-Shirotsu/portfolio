# portfolio

しろつの制作物（動くループ作品・画像）を1ページで一覧する静的サイト。

- 素の HTML / CSS / Vanilla JS のみ。ビルドツール・フレームワーク・外部CDN依存ゼロ。
- ホスティング: GitHub Pages（リポジトリルートの `index.html` を直接配信）。

## ファイル構成

```
/
├── index.html      # 単一ページ。<figure> を規則的に並べる（後で 11ty 化しやすい形）
├── style.css       # デザイン案2「白い展示室」。手書きCSS
├── main.js         # IntersectionObserver による動画の再生/停止制御のみ
└── works/
    └── NNN-slug/   # 1作品 = 1ディレクトリ
```

## ページ構造（カテゴリ × 作品の塊）

```
カテゴリ（見出し）            <section class="category"> + <h2 class="category__label">
└─ 作品の塊（1個以上）        <li><figure class="work">
   ├─ メディア群（1個以上）   <div class="work__media-group"> … 動画/画像 …
   └─ キャプション（1行）     <figcaption class="work__caption">
```

- **1作品 = 1つの塊**。塊の中に動画・画像を**1個以上**自由に並べられる（動画のみ／画像のみ／動画+画像／動画+画像複数、何でも可）。
- メディアは記述順に**上から縦に**並ぶ。キャプションは塊の最後に1行。
- カテゴリは見出しの下にぶら下がる。カテゴリ自体は `index.html` の `<section>` を増減して管理する（フォルダ構成とは無関係）。

## 作品ファイルの命名規則（重要）

1作品ぶんのファイルは `works/NNN-slug/` に置く（`NNN`=3桁通し番号、`slug`=半角英小文字とハイフン）。例: `013-loop-spark`

| 用途 | 必須ファイル | 任意ファイル |
|------|--------------|--------------|
| 動画 | `video.mp4`（H.264）, `poster.jpg` | `video.webm`（VP9。あれば優先配信） |
| 画像（1枚） | `image.jpg` | `image.webp`（あれば優先配信） |
| 画像（複数枚） | `image-1.jpg`, `image-2.jpg`, … | `image-1.webp`, `image-2.webp`, … |

- 動画と画像を**同じ塊に同居**させる場合は、同じフォルダに両方のファイルを置く（例: `video.mp4` + `poster.jpg` + `image.jpg`）。
- **差し替えは「同名ファイルを上書きするだけ」**。`index.html` の編集は不要。

> 現在 `works/` に入っているのはレイアウト確認用の **プレースホルダ**（generated パターン、著作物なし）。
> 本番メディアを**同じファイル名で上書き**すれば差し替え完了。

## 作品を新規追加する手順

1. `works/NNN-slug/` を作り、上表のファイルを置く。
2. `index.html` で追加したいカテゴリ `<section>` 内の `<ul class="gallery">` に、既存の `<li><figure class="work">…</figure></li>` ブロックを1つコピペ複製する。
   - 塊に複数メディアを入れたいときは、`<div class="work__media-group">` の中に動画/画像の部品（`index.html` 冒頭のテンプレートコメント参照）を必要な数だけ並べる。
3. コピペしたブロックの **パス（`works/NNN-slug/…`）と 作品タイトル**（各メディアの `aria-label`／`alt`、`figcaption` の3系統）を書き換える。

## カテゴリを追加・変更する手順

- 追加: `<main>` 内に `<section class="category"><h2 class="category__label">カテゴリ名</h2><ul class="gallery" role="list"> … </ul></section>` を増やす。
- 並べ替え: `<section>` ブロックごと上下に動かす。
- 改名: `<h2 class="category__label">` のテキストを書き換えるだけ。

## 動画ファイルの推奨仕様

- コーデック: H.264 (mp4)。可能なら VP9 (webm) も併置。
- 属性は `index.html` 側で設定済み: `autoplay muted loop playsinline preload="metadata"`。
- 画面内に入った動画のみ `main.js` が再生し、画面外では停止する。
- `prefers-reduced-motion: reduce` のユーザーには自動再生せず `poster` 画像を表示する。

## ローカル確認

`file://` でも概ね動くが、`<video>` の挙動を正確に見るには簡易サーバ推奨:

```sh
python -m http.server 8000
# → http://localhost:8000/
```

## 公開（GitHub Pages）

リポジトリの Settings → Pages → Source を `main` ブランチ / `/ (root)` に設定するだけ。
Actions・ワークフローは不要。

> 補足: OGP の `og:image` は現在リポジトリ相対パス。SNS で正しくカード表示させるには、
> 独自ドメイン/公開URL確定後に `index.html` の `og:image` を**絶対URL**へ書き換えること。
