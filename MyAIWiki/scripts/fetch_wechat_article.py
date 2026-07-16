#!/usr/bin/env python3
"""
Fetch WeChat article content with Playwright first, then fall back to direct HTML parsing.

Usage:
  python3 scripts/fetch_wechat_article.py <url>
  python3 scripts/fetch_wechat_article.py <url> --pretty
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from html import unescape
from pathlib import Path

from bs4 import BeautifulSoup


MOBILE_USER_AGENT = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
    "Mobile/15E148 Safari/604.1"
)


def find_playwright_package() -> Path:
    npm_npx_root = Path.home() / ".npm" / "_npx"
    candidates = sorted(
        npm_npx_root.glob("*/node_modules/playwright"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if candidates:
        return candidates[0]
    raise FileNotFoundError(
        "No cached Playwright package found under ~/.npm/_npx. "
        "Reuse the Claude Code / Playwright path first, then rerun this script."
    )


def build_node_script(playwright_path: str, url: str) -> str:
    escaped_path = json.dumps(playwright_path)
    escaped_url = json.dumps(url)
    escaped_user_agent = json.dumps(MOBILE_USER_AGENT)
    return f"""
const {{ chromium }} = require({escaped_path});

(async () => {{
  const browser = await chromium.launch({{ channel: 'chrome', headless: true }});
  const context = await browser.newContext({{
    userAgent: {escaped_user_agent}
  }});
  const page = await context.newPage();
  await page.goto({escaped_url}, {{ waitUntil: 'domcontentloaded', timeout: 45000 }});
  await page.waitForTimeout(5000);
  const data = await page.evaluate(() => {{
    const bodyText = document.body ? document.body.innerText : '';
    const contentText = document.querySelector('#js_content')?.innerText || '';
    return {{
      title: document.title || '',
      author: document.querySelector('#js_name')?.textContent?.trim() || '',
      publish_time: document.querySelector('#publish_time')?.textContent?.trim() || '',
      url: location.href,
      body_text: bodyText,
      content_text: contentText,
    }};
  }});
  console.log(JSON.stringify(data));
  await browser.close();
}})().catch((error) => {{
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
}});
"""


def fetch_article_via_playwright(url: str) -> dict:
    playwright_path = find_playwright_package()
    script = build_node_script(str(playwright_path), url)
    result = subprocess.run(
        ["node", "-e", script],
        check=True,
        capture_output=True,
        text=True,
        env=os.environ.copy(),
    )
    data = json.loads(result.stdout)
    if not data.get("title") and not data.get("content_text"):
        raise RuntimeError("Fetched page did not return title/content.")
    return data


def normalize_wechat_text(text: str) -> str:
    text = unescape(text)
    text = text.replace("\xa0", " ")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def fetch_article_via_html(url: str) -> dict:
    result = subprocess.run(
        [
            "curl",
            "-L",
            "-A",
            MOBILE_USER_AGENT,
            url,
        ],
        check=True,
        capture_output=True,
        text=True,
        env=os.environ.copy(),
    )
    html_text = result.stdout

    soup = BeautifulSoup(html_text, "html.parser")
    content_node = soup.select_one("#js_content")
    if content_node is None:
        raise RuntimeError("Fetched page did not contain #js_content.")

    for tag in content_node.select("script, style"):
        tag.decompose()

    title = ""
    title_meta = soup.select_one('meta[property="og:title"]')
    if title_meta and title_meta.get("content"):
        title = title_meta["content"].strip()
    if not title:
        title = (soup.title.string or "").strip() if soup.title else ""

    author = ""
    author_meta = soup.select_one('meta[name="author"]')
    if author_meta and author_meta.get("content"):
        author = author_meta["content"].strip()
    if not author:
        match = re.search(r'var nickname = htmlDecode\("([^"]+)"\)', html_text)
        if match:
            author = unescape(match.group(1))

    publish_time = ""
    match = re.search(r'var ct = "(\d{10})"', html_text)
    if match:
        publish_time = datetime.fromtimestamp(int(match.group(1))).strftime("%Y-%m-%d")

    content_text = normalize_wechat_text(content_node.get_text("\n", strip=True))
    body = soup.body
    body_text = normalize_wechat_text(body.get_text("\n", strip=True) if body else content_text)

    data = {
        "title": title,
        "author": author,
        "publish_time": publish_time,
        "url": url,
        "body_text": body_text,
        "content_text": content_text,
        "fetch_mode": "html-fallback",
    }
    if not data.get("title") and not data.get("content_text"):
        raise RuntimeError("Fetched page did not return title/content.")
    return data


def fetch_article(url: str) -> dict:
    try:
        return fetch_article_via_playwright(url)
    except (FileNotFoundError, subprocess.CalledProcessError, RuntimeError) as exc:
        data = fetch_article_via_html(url)
        data["playwright_error"] = str(exc)
        return data


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch WeChat article title/author/time/content via Playwright, with an HTML fallback."
    )
    parser.add_argument("url", help="WeChat article URL")
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output",
    )
    args = parser.parse_args()

    data = fetch_article(args.url)
    if args.pretty:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(data, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
