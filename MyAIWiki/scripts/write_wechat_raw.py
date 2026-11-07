#!/usr/bin/env python3
"""
Fetch a WeChat article and write a raw markdown draft into MyAIWiki/raw.

Usage:
  python3 scripts/write_wechat_raw.py <url>
  python3 scripts/write_wechat_raw.py <url> --slug my-article
  python3 scripts/write_wechat_raw.py <url> --force
"""

from __future__ import annotations

import argparse
from pathlib import Path

from build_wechat_raw import build_raw_markdown, fetch_article, slugify


SCRIPT_DIR = Path(__file__).resolve().parent
RAW_DIR = SCRIPT_DIR.parent / "raw"


def resolve_output_path(slug: str) -> Path:
    return RAW_DIR / f"{slug}.md"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch a WeChat article and write a raw markdown draft into MyAIWiki/raw."
    )
    parser.add_argument("url", help="WeChat article URL")
    parser.add_argument(
        "--slug",
        help="Optional file slug. Defaults to a slugified article title.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing raw file with the same slug.",
    )
    args = parser.parse_args()

    article = fetch_article(args.url)
    title = article.get("title", "").strip() or "wechat-article"
    slug = args.slug or slugify(title)
    output_path = resolve_output_path(slug)

    if output_path.exists() and not args.force:
        raise SystemExit(
            f"Output file already exists: {output_path}\n"
            "Use --force to overwrite or --slug to choose another file name."
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_raw_markdown(article), encoding="utf-8")
    print(str(output_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
