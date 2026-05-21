#!/usr/bin/env python3
"""
Build a raw markdown draft from a WeChat article URL.

Usage:
  python3 scripts/build_wechat_raw.py <url>
  python3 scripts/build_wechat_raw.py <url> --output /path/to/file.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
FETCHER_PATH = SCRIPT_DIR / "fetch_wechat_article.py"


def slugify(text: str) -> str:
    has_cjk = bool(re.search(r"[\u4e00-\u9fff]", text))
    cleaned = text.strip()
    cleaned = re.sub(r"\s+", "" if has_cjk else "-", cleaned)
    cleaned = re.sub(r"[\\/:*?\"<>|：，。！？；、（）()【】《》“”‘’…]+", "-", cleaned)
    cleaned = re.sub(r"-{2,}", "-", cleaned)
    return cleaned.strip("-") or "wechat-article"


def fetch_article(url: str) -> dict:
    import subprocess

    result = subprocess.run(
        ["python3", str(FETCHER_PATH), url],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def build_raw_markdown(article: dict) -> str:
    title = article.get("title", "").strip() or "未命名微信文章"
    author = article.get("author", "").strip() or "未知作者"
    publish_time = article.get("publish_time", "").strip() or "未知时间"
    url = article.get("url", "").strip()
    content = article.get("content_text", "").strip() or article.get("body_text", "").strip()

    lines = [
        f"# {title}",
        "",
        f"**来源：** 微信公众号",
        f"**作者：** {author}",
        f"**日期：** {publish_time}",
        f"**链接：** {url}",
        "",
        "---",
        "",
        "## 正文",
        "",
        content,
        "",
        "---",
        "",
        "标签：#主题/AI-Coding #场景/公众号长文",
    ]
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a raw markdown draft from a WeChat article URL."
    )
    parser.add_argument("url", help="WeChat article URL")
    parser.add_argument(
        "--output",
        help="Optional output file path. If omitted, prints markdown to stdout.",
    )
    args = parser.parse_args()

    article = fetch_article(args.url)
    markdown = build_raw_markdown(article)

    if args.output:
        output_path = Path(args.output).expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown, encoding="utf-8")
        print(str(output_path))
        return 0

    print(markdown, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
