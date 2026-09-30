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


# Time labels that move on every rebuild even when the underlying content is identical:
#   "52 分钟前更新" / "3 小时前" / "2 天前"   relative
#   "9月30日 17:55 更新"                     absolute, stamped with the rebuild minute
RELATIVE_TIME = re.compile(r"\d+\s*(?:秒|分钟|小时|天)前")
ABSOLUTE_STAMP = re.compile(r"\d{1,2}月\d{1,2}日\s+\d{1,2}:\d{2}(?=</span>|\s*更新)")


# Sparkline / chart geometry: the 24-hour heat trend is redrawn from a rolling window, so its path
# coordinates shift a little on every rebuild while the story and its numbers stay the same. The
# axis labels (<text>) and the headline numbers are NOT touched, so a real data change still shows up.
# Numeric geometry only. Text, aria-labels, `href`/`xlink:href` (nameplate references) and the
# <text> axis labels are deliberately left alone, so a genuine content change still moves the digest.
# SVG path data keeps its command letters (M/L/h/v), so `d` allows them; the other geometry
# attributes are numeric. `href` is absent from the list on purpose: the nameplate SVGs are
# referenced through it, and a real brand swap must still change the digest.
_SVG_NUM = r'[0-9eE.,;\s+-]*(?:(?:translate|scale|rotate|matrix)\([^)]*\)[0-9eE.,;\s+-]*)*'
CHART_GEOMETRY = re.compile(
    r'(\bd=")[A-Za-z0-9eE.,;\s+-]*(")'
    r'|(\b(?:points|cx|cy|x1|y1|x2|y2|x|y|r|transform|style)=)(")' .replace('=)(")', '=")' ) + r'(' + _SVG_NUM + r')(")'
)


def normalize(text: str) -> str:
    for pattern in VOLATILE:
        text = pattern.sub('"VOLATILE"', text)
    text = RELATIVE_TIME.sub("N 前", text)
    text = ABSOLUTE_STAMP.sub("T 更新", text)
    # Only inside SVG chart elements, so ordinary text/attributes are untouched.
    text = re.sub(r'(<svg\b[^>]*>(?:(?!</svg>).)*?</svg>)', lambda m: CHART_GEOMETRY.sub(r'\1CHART\2', m.group(1)), text, flags=re.S)
    return text


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
