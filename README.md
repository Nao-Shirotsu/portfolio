# portfolio

しろつの制作物（動くループ作品・画像）を1ページで一覧する静的サイト。

- 素の HTML / CSS / Vanilla JS のみ。ビルドツール・フレームワーク・外部CDN依存ゼロ。
- ホスティング: GitHub Pages（リポジトリルートの `index.html` を直接配信）。

## ファイル構成

```
/
├── index.html             # 単一ページ。works/ の内容に合わせて生成する
├── style.css              # デザイン案2「白い展示室」。手書きCSS
├── main.js                # IntersectionObserver による動画の再生/停止制御のみ
├── CONTENT-ADDITION.md    # 作品の追加・差し替えガイド（まずこれを読む）
└── works/
    └── <カテゴリ>/
        └── NNN-slug/      # 1作品 = 1ディレクトリ（メディア + caption.txt）
```

## 作品の追加・差し替え → [CONTENT-ADDITION.md](CONTENT-ADDITION.md)

運用は **「`works/` にファイルを置く → Claude Code に `index.html` 再生成を頼む」** 方式。
具体的な手順・命名規則・依頼テンプレは **[CONTENT-ADDITION.md](CONTENT-ADDITION.md)** に集約。
（動画・画像ファイルの差し替えだけなら同名上書きのみで `index.html` 編集は不要）

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

> 命名規則（カテゴリ / `NNN-slug` / `caption.txt` / メディアファイル名）と
> 追加・差し替えの具体手順は [CONTENT-ADDITION.md](CONTENT-ADDITION.md) を参照。

> 現在 `works/` に入っているのはレイアウト確認用の **プレースホルダ**（generated パターン、著作物なし）。
> 本番メディアを**同じファイル名で上書き**すれば差し替え完了。

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
