#!/usr/bin/env python3
"""
Fetch WeChat article content with browser fallbacks before direct HTML parsing.

Usage:
  python3 scripts/fetch_wechat_article.py <url>
  python3 scripts/fetch_wechat_article.py <url> --pretty
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
from datetime import datetime
from html import unescape
from pathlib import Path

from bs4 import BeautifulSoup


MOBILE_USER_AGENT = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 "
    "Mobile/15E148 Safari/604.1"
)
CHROME_CANDIDATES = (
    Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
    Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome for Testing"),
    Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
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


def find_chrome_binary() -> str:
    configured = os.environ.get("MYAIWIKI_CHROME_PATH")
    candidates = [Path(configured)] if configured else []
    candidates.extend(CHROME_CANDIDATES)
    candidates.extend(
        Path("/Volumes").glob(
            "*/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        )
    )
    for candidate in candidates:
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate)
    for name in ("google-chrome", "chromium", "chromium-browser"):
        if path := shutil.which(name):
            return path
    raise FileNotFoundError(
        "Chrome/Chromium was not found. Set MYAIWIKI_CHROME_PATH to an executable."
    )


def reserve_local_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("127.0.0.1", 0))
        return int(server.getsockname()[1])


def build_cdp_node_script(port: int, url: str) -> str:
    escaped_url = json.dumps(url)
    return f"""
const targetUrl = {escaped_url};
const endpoint = 'http://127.0.0.1:{port}/json/list';

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function evaluatePage() {{
  let pages = [];
  for (let attempt = 0; attempt < 30; attempt += 1) {{
    try {{
      pages = await (await fetch(endpoint)).json();
      const page = pages.find((item) => item.type === 'page' && item.url.startsWith(targetUrl));
      if (page && page.webSocketDebuggerUrl) {{
        await sleep(2500);
        return await new Promise((resolve, reject) => {{
          const ws = new WebSocket(page.webSocketDebuggerUrl);
          const timer = setTimeout(() => reject(new Error('Timed out evaluating Chrome page.')), 15000);
          ws.onopen = () => ws.send(JSON.stringify({{
            id: 1,
            method: 'Runtime.evaluate',
            params: {{
              expression: `JSON.stringify({{
                title: document.querySelector('#activity-name')?.innerText?.trim() || document.title || '',
                author: document.querySelector('#js_name')?.textContent?.trim() || '',
                publish_time: document.querySelector('#publish_time')?.textContent?.trim() || '',
                url: location.href,
                body_text: document.body?.innerText || '',
                content_text: document.querySelector('#js_content')?.innerText || ''
              }})`,
              returnByValue: true
            }}
          }}));
          ws.onmessage = (event) => {{
            clearTimeout(timer);
            const response = JSON.parse(event.data);
            ws.close();
            if (response.error || response.result?.exceptionDetails) {{
              reject(new Error('Chrome page evaluation failed.'));
              return;
            }}
            resolve(JSON.parse(response.result.result.value));
          }};
          ws.onerror = () => {{
            clearTimeout(timer);
            reject(new Error('Could not connect to Chrome DevTools.'));
          }};
        }});
      }}
    }} catch {{}}
    await sleep(250);
  }}
  throw new Error('Chrome DevTools did not expose the requested page.');
}}

evaluatePage().then((data) => console.log(JSON.stringify(data))).catch((error) => {{
  console.error(error.stack || String(error));
  process.exit(1);
}});
"""


def fetch_article_via_isolated_chrome(url: str) -> dict:
    chrome = find_chrome_binary()
    port = reserve_local_port()
    with tempfile.TemporaryDirectory(prefix="myaiwiki-wechat-") as profile:
        process = subprocess.Popen(
            [
                chrome,
                "--headless=new",
                f"--remote-debugging-port={port}",
                f"--user-data-dir={profile}",
                "--no-first-run",
                "--no-default-browser-check",
                url,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        try:
            result = subprocess.run(
                ["node", "-e", build_cdp_node_script(port, url)],
                check=True,
                capture_output=True,
                text=True,
                timeout=30,
                env=os.environ.copy(),
            )
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

    data = json.loads(result.stdout)
    rendered_text = data.get("content_text") or data.get("body_text") or ""
    blocked = "环境异常" in rendered_text or "当前环境异常" in rendered_text
    if not data.get("title") or not rendered_text or blocked:
        raise RuntimeError("Isolated Chrome did not return an accessible article page.")
    data["fetch_mode"] = "isolated-chrome-cdp"
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
    errors = []
    try:
        return fetch_article_via_playwright(url)
    except (FileNotFoundError, subprocess.CalledProcessError, RuntimeError) as exc:
        errors.append(f"playwright: {exc}")
    try:
        return fetch_article_via_isolated_chrome(url)
    except (
        FileNotFoundError,
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
        RuntimeError,
    ) as exc:
        errors.append(f"isolated-chrome-cdp: {exc}")
    try:
        data = fetch_article_via_html(url)
    except (subprocess.CalledProcessError, RuntimeError) as exc:
        errors.append(f"html-fallback: {exc}")
        raise RuntimeError("WeChat article fetch failed: " + " | ".join(errors)) from exc
    data["fetch_errors"] = errors
    return data


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch WeChat article via Playwright, isolated Chrome CDP, then direct HTML."
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
