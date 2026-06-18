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

## 作品ファイルの命名規則（重要）

| 種別 | 必須ファイル | 任意ファイル |
|------|--------------|--------------|
| 動画作品 | `video.mp4`（H.264）, `poster.jpg` | `video.webm`（VP9。あれば優先配信） |
| 画像作品 | `image.jpg` | `image.webp`（あれば優先配信） |

- ディレクトリ名は `NNN-slug`（`NNN`=3桁通し番号、`slug`=半角英小文字とハイフン）。例: `013-loop-spark`
- **差し替えは「同名ファイルを上書きするだけ」**。`index.html` の編集は不要。

> 現在 `works/` に入っているのはレイアウト確認用の **プレースホルダ**（generated パターン、著作物なし）。
> 本番メディアを**同じファイル名で上書き**すれば差し替え完了。

## 作品を新規追加する手順

1. `works/NNN-slug/` を作り、上表のファイルを置く。
2. `index.html` のテンプレートコメント（「動画作品テンプレート」/「画像作品テンプレート」）直下の `<li>…</li>` ブロックを1つコピペ複製する。
3. コピペしたブロックの **パス（`works/NNN-slug/…`）と 作品タイトル**（`aria-label`／`alt`／`figcaption` の3か所）を書き換える。

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
