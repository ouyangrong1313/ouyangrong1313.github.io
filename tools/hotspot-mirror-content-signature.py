#!/usr/bin/env python3
"""A stable signature of what the hotspot mirrors *contain*.

The pages also carry live-derived numbers: the 48h heat trend, the "更新" clock, the relative
"N 分钟前" label, and SVG sparkline geometry. All of those drift on every rebuild even when no
news arrived, so hashing the raw snapshot would commit a few dozen files every two hours.

This signature keeps only the things a reader would lose if they were stale:

  * every mirrored route (a page appeared or disappeared), and
  * for each item/story page, its title and publication minute.

Rolling heat scores are deliberately excluded — they are recomputed from the current window on
every visit to the live site anyway, and a snapshot copy is a moment-in-time record.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

TITLE = re.compile(r"<title>(.*?)</title>", re.S)
TOOLS = Path(__file__).resolve().parent

# The builder and the injected interaction layer decide what the pages *do*, not just what they say.
# Hashed in too, so shipping a fix to either one is never mistaken for "nothing changed".
BUILDER_FILES = ("build-hotspot-mirror.py", "hotspot-mirror-interactive.js")


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "hotspot-src")
    digest = hashlib.sha256()
    for name in BUILDER_FILES:
        f = TOOLS / name
        digest.update(name.encode())
        digest.update(b"=")
        digest.update(hashlib.sha256(f.read_bytes()).hexdigest().encode() if f.exists() else b"missing")
        digest.update(b"\0")
    for path in sorted(root.rglob("index.html")):
        rel = str(path.parent.relative_to(root))
        digest.update(rel.encode())
        digest.update(b"\0")
        text = path.read_text(encoding="utf-8", errors="replace")
        m = TITLE.search(text)
        if m:
            digest.update(m.group(1).strip().encode())
        digest.update(b"\0")
    print(digest.hexdigest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
