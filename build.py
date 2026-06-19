#!/usr/bin/env python3
"""works/ の内容から index.html の作品一覧を再生成する。

使い方:
    python build.py

works/ が唯一の正（source of truth）。このスクリプトは index.html 内の
<!-- WORKS:START --> 〜 <!-- WORKS:END --> の間だけを書き換える。
それ以外（<head>/OGP/<header> など）は手編集領域として保持される。

フォルダ規約（詳細は README.md）:
    works/
      NN-<カテゴリ>/          NN=2桁。並び順を決める。表示名は _label.txt の1行目
        _label.txt           見出しの表示名（1行目）
        NNN-<slug>/          1作品。NNN=3桁。カテゴリ内の並び順
          caption.txt        1行目＝キャプション
          video.mp4 / video.webm / poster.jpg
          image.jpg / image.webp                （画像1枚）
          image-1.jpg / image-1.webp / image-2… （画像複数）
"""

import html
import re
import sys
from pathlib import Path

# Windows コンソール（cp932）でも日本語ログが化けないよう UTF-8 に統一
for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent
WORKS = ROOT / "works"
INDEX = ROOT / "index.html"

START = "<!-- WORKS:START -->"
END = "<!-- WORKS:END -->"

# NN- / NNN- の連番prefix（NN=カテゴリ, NNN=作品。桁数は問わず先頭の数字列で判定）
PREFIX_RE = re.compile(r"^(\d+)-")


def first_line(path: Path) -> str:
    """ファイルの1行目を返す（前後空白除去）。無ければ空文字。"""
    if not path.is_file():
        return ""
    for line in path.read_text(encoding="utf-8").splitlines():
        return line.strip()
    return ""


def numbered_dirs(parent: Path):
    """parent 直下の NN-... 形式ディレクトリを連番昇順で返す。"""
    dirs = [p for p in parent.iterdir() if p.is_dir() and PREFIX_RE.match(p.name)]
    return sorted(dirs, key=lambda p: (int(PREFIX_RE.match(p.name).group(1)), p.name))


def attr(text: str) -> str:
    """HTML属性値用エスケープ。"""
    return html.escape(text, quote=True)


def text(value: str) -> str:
    """HTMLテキスト用エスケープ。"""
    return html.escape(value, quote=False)


def video_block(work: Path, rel: str, caption: str) -> str:
    """動画ブロック。poster は在れば付与。"""
    poster = f' poster="{attr(rel)}/poster.jpg"' if (work / "poster.jpg").is_file() else ""
    sources = []
    if (work / "video.webm").is_file():
        sources.append(f'                <source src="{attr(rel)}/video.webm" type="video/webm">')
    sources.append(f'                <source src="{attr(rel)}/video.mp4"  type="video/mp4">')
    return (
        f'              <video class="work__media"{poster}\n'
        f'                     width="480" height="270"\n'
        f'                     autoplay muted loop playsinline preload="metadata"\n'
        f'                     aria-label="{attr(caption)}（動画）">\n'
        + "\n".join(sources)
        + "\n              </video>"
    )


def image_block(work: Path, rel: str, caption: str, stem: str, label_suffix: str) -> str:
    """画像ブロック。webp は在れば <source> として付与。"""
    webp = (
        f'                <source srcset="{attr(rel)}/{stem}.webp" type="image/webp">\n'
        if (work / f"{stem}.webp").is_file()
        else ""
    )
    return (
        f"              <picture>\n"
        f"{webp}"
        f'                <img class="work__media" src="{attr(rel)}/{stem}.jpg"\n'
        f'                     width="480" height="270" loading="lazy" decoding="async"\n'
        f'                     alt="{attr(caption)}（{label_suffix}）">\n'
        f"              </picture>"
    )


def media_blocks(work: Path, rel: str, caption: str) -> list:
    """作品フォルダ内の在るファイルからメディアブロックを順に組み立てる（動画→画像）。"""
    blocks = []
    if (work / "video.mp4").is_file():
        blocks.append(video_block(work, rel, caption))

    # 画像: image.jpg（1枚）か image-1.jpg, image-2.jpg…（複数）
    if (work / "image.jpg").is_file():
        blocks.append(image_block(work, rel, caption, "image", "画像"))
    else:
        numbered = sorted(
            (p for p in work.glob("image-*.jpg")),
            key=lambda p: int(re.search(r"image-(\d+)", p.stem).group(1)),
        )
        for p in numbered:
            n = re.search(r"image-(\d+)", p.stem).group(1)
            blocks.append(image_block(work, rel, caption, p.stem, f"画像{n}"))
    return blocks


def work_html(work: Path, category_dir: str) -> str:
    caption = first_line(work / "caption.txt")
    rel = f"works/{category_dir}/{work.name}"
    blocks = media_blocks(work, rel, caption)
    if not blocks:
        print(f"  ! メディアが無い作品をスキップ: {rel}", file=sys.stderr)
        return ""
    inner = "\n".join(blocks)
    return (
        "        <li>\n"
        '          <figure class="work">\n'
        '            <div class="work__media-group">\n'
        f"{inner}\n"
        "            </div>\n"
        f'            <figcaption class="work__caption">{text(caption)}</figcaption>\n'
        "          </figure>\n"
        "        </li>"
    )


def category_html(category: Path) -> str:
    label = first_line(category / "_label.txt") or category.name
    works = numbered_dirs(category)
    items = [w for w in (work_html(w, category.name) for w in works) if w]
    if not items:
        return ""
    body = "\n\n".join(items)
    return (
        '    <section class="category">\n'
        f'      <h2 class="category__label">{text(label)}</h2>\n'
        '      <ul class="gallery" role="list">\n\n'
        f"{body}\n\n"
        "      </ul>\n"
        "    </section>"
    )


def build_main() -> str:
    categories = numbered_dirs(WORKS)
    sections = [s for s in (category_html(c) for c in categories) if s]
    return "\n\n".join(sections)


def main() -> int:
    if not WORKS.is_dir():
        print("works/ が見つかりません", file=sys.stderr)
        return 1

    generated = build_main()
    source = INDEX.read_text(encoding="utf-8")

    if START not in source or END not in source:
        print(
            f"index.html に {START} / {END} マーカーが見つかりません。\n"
            "生成領域を囲むマーカーを <main> 内に1組だけ置いてください。",
            file=sys.stderr,
        )
        return 1

    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    replacement = f"{START}\n\n{generated}\n\n    {END}"
    updated = pattern.sub(lambda _m: replacement, source, count=1)

    if updated == source:
        print("変更なし（index.html は最新です）")
        return 0

    INDEX.write_text(updated, encoding="utf-8")
    print(f"index.html を再生成しました（カテゴリ {len(numbered_dirs(WORKS))} 件）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
