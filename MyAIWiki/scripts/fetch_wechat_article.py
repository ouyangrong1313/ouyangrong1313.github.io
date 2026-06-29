#!/usr/bin/env python3
"""
Fetch rendered WeChat article content via Playwright + local Chrome.

Usage:
  python3 scripts/fetch_wechat_article.py <url>
  python3 scripts/fetch_wechat_article.py <url> --pretty
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


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
    return f"""
const {{ chromium }} = require({escaped_path});

(async () => {{
  const browser = await chromium.launch({{ channel: 'chrome', headless: true }});
  const context = await browser.newContext({{
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
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


def fetch_article(url: str) -> dict:
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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch WeChat article title/author/time/content via Playwright + Chrome."
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
