# portfolio

しろつの制作物（動くループ作品・画像）を1ページで一覧する静的サイト。

- 素の HTML / CSS / Vanilla JS のみ。フレームワーク・外部CDN依存ゼロ。
- 作品一覧だけ、ローカルで `python build.py` を叩いて `works/` から再生成する（依存は Python 標準ライブラリのみ）。
- ホスティング: GitHub Pages（リポジトリルートの `index.html` を直接配信）。Actions・ワークフロー不要。

## ファイル構成

```
/
├── index.html             # 単一ページ。<main> 内の作品一覧は build.py が生成する
├── style.css              # デザイン案2「白い展示室」。手書きCSS
├── main.js                # IntersectionObserver による動画の再生/停止制御のみ
├── build.py               # works/ → index.html の作品一覧を再生成するツール
└── works/                 # ★唯一の正（source of truth）
    └── NN-<カテゴリ>/
        └── NNN-slug/      # 1作品 = 1ディレクトリ（メディア + caption.txt）
```

## 運用：作品を追加・差し替える

**`works/` にファイルを置く → `python build.py` を実行** するだけ。
`index.html` の `<main>` 内（`<!-- WORKS:START -->` 〜 `<!-- WORKS:END -->`）が `works/` の現在の内容で再生成される。
マーカーの外（`<head>`・OGP・`<header>` など）は手編集領域で、ビルドでは変更されない。

```sh
python build.py
```

> 動画・画像ファイルを**同名で上書き**するだけの差し替えなら、`index.html` は変わらないので再生成も不要。
> キャプション（`caption.txt`）やフォルダ構成を変えた場合は再生成する。

## フォルダの形（これが全て）

```
works/
  NN-<カテゴリ名>/           ← NN=2桁の連番。カテゴリの並び順を決める（小さい順に上から表示）
    _label.txt              ← 見出しの表示名（1行目）。フォルダ名の prefix は表示に出ない
    NNN-<slug>/             ← 1作品。NNN=3桁の連番（カテゴリ内の並び順）、slug=半角英小文字とハイフン
      caption.txt           ← 【必須】1行目＝画面に出すキャプション（2行目以降は将来用に予約）
      （以下、在るものだけ置く）
      video.mp4             ← 動画本体（H.264）
      video.webm            ← 任意（VP9。あれば優先配信）
      poster.jpg            ← 動画があるなら必須（静止画／reduced-motion 時の表示）
      image.jpg             ← 画像1枚のとき
      image-1.jpg image-2.jpg …   ← 画像が複数のとき（連番）
      image.webp / image-1.webp … ← 任意（あれば優先配信）
```

### ルール
- **1作品 = 1フォルダ**。中に動画・画像を何個入れてもよい（動画のみ／画像のみ／動画+画像／複数画像、何でも可）。
- **カテゴリ = `NN-` 付きの親フォルダ**。新カテゴリは `NN-名前` フォルダを作り、中に `_label.txt` と作品フォルダを置く。
- **並び順 = フォルダ名の連番**。カテゴリは `NN-`、作品は `NNN-` の数値順。並べ替えは prefix の番号を振り直す。
- **見出しの表示名 = `_label.txt` の1行目**。フォルダ名（`02-グラフィックス実装` 等）の prefix は表示されない。
- **キャプション = `caption.txt` の1行目**。`figcaption` と各メディアの `aria-label`／`alt` に反映される。
- **メディアの表示順** = 動画 → 画像（`image-1`→`image-2`… のファイル名順）。
- フォルダ名・パスに日本語はOK。半角スペースは使わない運用（`%20` を避けるため）。

### よくある操作
- **既存作品の差し替え**: フォルダ内の同名ファイルを上書き。ファイルだけなら再生成不要、キャプション変更時は `python build.py`。
- **作品を追加**: `NN-<カテゴリ>/NNN-slug/` を作りメディアと `caption.txt` を置く → `python build.py`。
- **カテゴリを追加/改名/並べ替え**: `NN-名前` フォルダを作る／`_label.txt` を書き換える／`NN` の番号を振り直す → `python build.py`。

## ページ構造（カテゴリ × 作品の塊）

```
カテゴリ（見出し）            <section class="category"> + <h2 class="category__label">
└─ 作品の塊（1個以上）        <li><figure class="work">
   ├─ メディア群（1個以上）   <div class="work__media-group"> … 動画/画像 …
   └─ キャプション（1行）     <figcaption class="work__caption">
```

- メディアは記述順に**上から縦に**並ぶ。キャプションは塊の最後に1行。

> 現在 `works/` に入っているのはレイアウト確認用の **プレースホルダ**（generated パターン、著作物なし）。
> 本番メディアを**同じファイル名で上書き**すれば差し替え完了。

## 動画ファイルの推奨仕様

- コーデック: H.264 (mp4)。可能なら VP9 (webm) も併置。
- 属性は生成HTML側で設定済み: `autoplay muted loop playsinline preload="metadata"`。
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
公開前に `python build.py` を実行して `index.html` を最新化し、コミットしてからプッシュする。

> 補足: OGP の `og:image` は現在リポジトリ相対パス。SNS で正しくカード表示させるには、
> 独自ドメイン/公開URL確定後に `index.html` の `og:image` を**絶対URL**へ書き換えること（`<head>` 内＝手編集領域）。
