#!/usr/bin/env python3
"""Fingerprint the hotspot mirrors while ignoring volatile timestamp fields.

Every rebuild stamps the pages with the moment it ran (serverNow, generatedAt, checkedAt …).
Without this, a 2-hourly refresh would commit a few hundred one-token diffs forever even when no
news arrived. The digest blanks those fields first, so the refresh script can tell a real content
change from clock noise and skip the commit when nothing actually moved.

Two serializations show up:
  * escaped JSON inside `.data`:  \\"serverNow\\":1790  
  * React Router's single-page data stream:  "generatedAt","2026-09-30T07:22:33.427Z"
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

VOLATILE_KEYS = (
    "serverNow", "generatedAt", "checkedAt", "refreshAt", "nextRunAtMs", "latestAt",
    "updatedAt", "lastRunAtMs", "refreshAtMs", "capturedAt", "fetchedAt",
)
KEY_ALT = "|".join(VOLATILE_KEYS)

VOLATILE = [
    # "key": <number|"string"|true|false|null>, with optional escaping on the quotes.
    re.compile(r'\\?"(?:' + KEY_ALT + r')\\?":(?:"[^"]*"|\d+(?:\.\d+)?|true|false|null)'),
    # React Router data stream: "key","value" (string) or "key",<number> as adjacent tokens.
    re.compile(r'"(?:' + KEY_ALT + r')","[^"]*"'),
    re.compile(r'"(?:' + KEY_ALT + r')",\d+(?:\.\d+)?'),
    # Array values, e.g. "calendar":[...]
    re.compile(r'\\?"(?:' + KEY_ALT + r')\\?":\[[^\]]*\]'),
]


# "52 分钟前更新" / "3 小时前" / "2 天前" — relative-time labels move on every rebuild even when
# the underlying content is identical.
RELATIVE_TIME = re.compile(r"\d+\s*(?:秒|分钟|小时|天)前")


def normalize(text: str) -> str:
    for pattern in VOLATILE:
        text = pattern.sub('"VOLATILE"', text)
    return RELATIVE_TIME.sub("N 前", text)


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "hotspot-src")
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        digest.update(str(path.relative_to(root)).encode())
        digest.update(b"\0")
        if path.suffix in {".html", ".data", ".json", ".xml", ".txt", ".webmanifest"}:
            try:
                digest.update(normalize(path.read_text(encoding="utf-8", errors="replace")).encode())
            except OSError:
                digest.update(path.read_bytes())
        else:
            digest.update(path.read_bytes())
        digest.update(b"\0")
    print(digest.hexdigest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
