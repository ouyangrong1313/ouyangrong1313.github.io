#!/usr/bin/env python3
"""Refresh the committed static snapshots under hotspot-src/.

The hotspot sites are SSR React Router apps backed by a live API. GitHub Pages
can only serve files, so each site ships as a prebuilt snapshot that the deploy
workflow copies into _site *after* htmlproofer runs.

A snapshot is only usable if all of this holds, which this script maintains:

  * every reachable in-app route is written as <route>/index.html, so direct
    links and hard refreshes work;
  * every route also gets its React Router ".data" payload, so client-side
    navigation keeps working after hydration;
  * the router basename and every root-relative URL point at the mirror's public
    sub-path instead of the app origin;
  * the hashed build chunks are copied and their "/assets/..." references are
    rebased;
  * source avatars are downloaded locally: the live /api/img-proxy URLs carry an
    expiring signature, so a static mirror must not depend on them.

Usage:
    python3 tools/build-hotspot-mirror.py --site ai \
        --source http://127.0.0.1:3000 \
        --assets /path/to/AIHOT/ai/apps/web/build/client/assets \
        --out hotspot-src/reports/hotspot/ai
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import html as html_mod
import os
import re
import shutil
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import deque
from concurrent.futures import ThreadPoolExecutor

ATTR_RE = re.compile(r'(href|src|poster)="([^"]*)"')
SRCSET_RE = re.compile(r'srcSet="([^"]*)"')
PROXY_RE = re.compile(r'/api/img-proxy\?u=[^"\'\\\s,)]*')
LOCAL_HOSTS = ("127.0.0.1", "localhost", "0.0.0.0")
SKIP_PREFIXES = ("/api/", "/assets/", "/__", "/@")
SKIP_SUFFIXES = (
    ".ico", ".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".css", ".js",
    ".json", ".webmanifest", ".xml", ".txt", ".map", ".woff", ".woff2",
)
ROOT_FILES = (
    "/favicon.ico", "/icon.png", "/icon-192.png", "/apple-icon.png",
    "/manifest.webmanifest", "/robots.txt", "/feed.xml", "/og/site.png",
    "/llms.txt", "/openapi-v1.json",
)
# Reachable routes that sitemap.xml omits (noindex pages).
EXTRA_PATHS = {
    "ai": ("/starred", "/more", "/leaderboard/rules", "/leaderboard/sources", "/leaderboard"),
    "sec": ("/starred", "/more"),
}


def fetch(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, headers={"Accept-Encoding": "identity"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def rewrite_text(text: str, base: str, public_base: str, source: str) -> str:
    text = text.replace('"basename":"/"', f'"basename":"{base}"')
    for host in LOCAL_HOSTS:
        for scheme in ("http", "https"):
            text = text.replace(f"{scheme}://{host}:{source}", public_base)
            text = text.replace(f"{scheme}://{host}", public_base)
    text = text.replace(source, public_base)
    for quote in ('"', "'", "`", "("):
        text = text.replace(f"{quote}/assets/", f"{quote}{base}/assets/")
    return text


def rewrite_html(text: str, base: str, public_base: str, source: str) -> str:
    text = rewrite_text(text, base, public_base, source)

    def fix(match: re.Match[str]) -> str:
        attr, value = match.group(1), match.group(2)
        if value.startswith(("#", "//", "http://", "https://", "mailto:", "tel:", "data:")):
            return match.group(0)
        if value == base or value.startswith(base + "/"):
            return match.group(0)
        if value.startswith("/"):
            return f'{attr}="{base}{value}"'
        return match.group(0)

    return ATTR_RE.sub(fix, text)


def rebase_srcset(text: str, base: str) -> str:
    def fix(match: re.Match[str]) -> str:
        items = []
        for item in match.group(1).split(","):
            parts = item.strip().split(" ")
            url = parts[0]
            if url.startswith("/") and not url.startswith("//") and not url.startswith(base + "/"):
                url = base + url
            items.append(" ".join([url, *parts[1:]]).strip())
        return 'srcSet="' + ", ".join(items) + '"'

    return SRCSET_RE.sub(fix, text)


def to_path(raw: str) -> str:
    if raw.startswith("http://") or raw.startswith("https://"):
        rest = raw.split("://", 1)[1]
        raw = "/" + rest.split("/", 1)[1] if "/" in rest else "/"
    raw = raw.split("#", 1)[0].split("?", 1)[0]
    return raw if raw.startswith("/") else "/" + raw


def is_route(path: str) -> bool:
    if path in ("", "/"):
        return False
    if path.startswith(SKIP_PREFIXES):
        return False
    return not path.lower().endswith(SKIP_SUFFIXES)


def crawl(source: str, extra: tuple[str, ...]) -> list[str]:
    seen = {"/"}
    order = ["/"]
    queue: deque[str] = deque(["/"])
    for path in extra:
        if path not in seen:
            seen.add(path)
            order.append(path)
            queue.append(path)
    while queue:
        path = queue.popleft()
        try:
            doc = fetch(source + path).decode("utf-8", "replace")
        except (urllib.error.URLError, OSError) as exc:
            print(f"  ! cannot load {path}: {exc}", file=sys.stderr)
            continue
        for match in ATTR_RE.finditer(doc):
            value = html_mod.unescape(match.group(2))
            if not value.startswith("/") or value.startswith("//"):
                continue
            target = to_path(value)
            if not is_route(target) or target in seen:
                continue
            seen.add(target)
            order.append(target)
            queue.append(target)
    return order


def write_pages(order, source, out, base, public_base) -> None:
    for path in order:
        try:
            doc = fetch(source + path)
        except (urllib.error.URLError, OSError) as exc:
            print(f"  ! HTML {path}: {exc}", file=sys.stderr)
            continue
        text = rebase_srcset(rewrite_html(doc.decode("utf-8", "replace"), base, public_base, source), base)
        html_path = os.path.join(out, "index.html") if path == "/" else os.path.join(out, path.strip("/"), "index.html")
        os.makedirs(os.path.dirname(html_path), exist_ok=True)
        with open(html_path, "w", encoding="utf-8") as fh:
            fh.write(text)

        try:
            data = fetch(source + path + ".data")
        except (urllib.error.URLError, OSError):
            continue
        payload = rewrite_text(data.decode("utf-8", "replace"), base, public_base, source)
        data_path = os.path.join(out, "_.data") if path == "/" else os.path.join(out, path.strip("/") + ".data")
        os.makedirs(os.path.dirname(data_path) or out, exist_ok=True)
        with open(data_path, "w", encoding="utf-8") as fh:
            fh.write(payload)


def copy_assets(assets, out, base, public_base, source) -> int:
    dest = os.path.join(out, "assets")
    if os.path.isdir(dest):
        shutil.rmtree(dest)
    os.makedirs(dest, exist_ok=True)
    copied = 0
    for name in sorted(os.listdir(assets)):
        src = os.path.join(assets, name)
        if not os.path.isfile(src):
            continue
        with open(src, "rb") as fh:
            blob = fh.read()
        if name.endswith((".js", ".css")):
            blob = rewrite_text(blob.decode("utf-8", "replace"), base, public_base, source).encode("utf-8")
        with open(os.path.join(dest, name), "wb") as fh:
            fh.write(blob)
        copied += 1
    return copied


def copy_root_files(source, out, base, public_base) -> int:
    copied = 0
    for path in ROOT_FILES:
        try:
            blob = fetch(source + path)
        except (urllib.error.URLError, OSError):
            continue
        dest = os.path.join(out, path.lstrip("/"))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        if path.endswith((".xml", ".txt", ".webmanifest")):
            blob = rewrite_text(blob.decode("utf-8", "replace"), base, public_base, source).encode("utf-8")
        with open(dest, "wb") as fh:
            fh.write(blob)
        copied += 1
    return copied


def upstream_of(ref: str) -> str | None:
    s = html_mod.unescape(ref).replace("\\u0026", "&").replace("\\/", "/")
    return urllib.parse.parse_qs(s.split("?", 1)[1]).get("u", [None])[0]


def avatar_name(url: str) -> str:
    ext = os.path.splitext(urllib.parse.urlparse(url).path)[1].lower()
    if ext not in (".png", ".jpg", ".jpeg", ".webp", ".gif", ".ico", ".svg"):
        ext = ".png"
    return hashlib.sha1(url.encode("utf-8")).hexdigest()[:20] + ext


AVATAR_TAIL_RE = re.compile(r'/avatars/([A-Za-z0-9._-]+)(?:&amp;|&|\\u0026)[^"\'\s,)]*')


def _avatar_names(mapping: dict[str, str]) -> set[str]:
    return set(mapping.values())


def localize_avatars(source, out, base) -> int:
    """Download proxied avatar/icon images so no expiring signature is needed."""
    outdir = os.path.join(out, "avatars")
    os.makedirs(outdir, exist_ok=True)

    files: list[str] = []
    for dirpath, _, names in os.walk(out):
        if os.sep + "avatars" in dirpath:
            continue
        for name in names:
            if name.endswith((".html", ".data")):
                files.append(os.path.join(dirpath, name))

    refs: set[str] = set()
    for path in files:
        with open(path, encoding="utf-8", errors="replace") as fh:
            refs.update(m.group(0) for m in PROXY_RE.finditer(fh.read()))

    def download(ref: str) -> tuple[str, str | None]:
        url = upstream_of(ref)
        if not url:
            return ref, None
        dest = os.path.join(outdir, avatar_name(url))
        if os.path.exists(dest) and os.path.getsize(dest) > 100:
            return ref, os.path.basename(dest)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; MyHOT-mirror)"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                blob = resp.read()
        except Exception:
            return ref, None
        if len(blob) < 100:
            return ref, None
        if blob[:2] == b"\x1f\x8b":  # some hosts return gzip regardless of Accept-Encoding
            try:
                blob = gzip.decompress(blob)
            except OSError:
                return ref, None
        with open(dest, "wb") as fh:
            fh.write(blob)
        return ref, os.path.basename(dest)

    mapping: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=10) as pool:
        for ref, name in pool.map(download, sorted(refs)):
            if name:
                mapping[ref] = name

    for path in files:
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        original = text
        # Replace the fully-qualified mirror path first, then any bare form.
        for ref, name in sorted(mapping.items(), key=lambda kv: -len(kv[0])):
            dest = f"{base}/avatars/{name}"
            for variant in (base + ref, ref, html_mod.escape(ref)):
                text = text.replace(variant, dest)
        # Defensive second pass: a partial match can leave "&mode=avatar-48&exp=.."
        # stuck to the file name, which would make the image 404 at runtime.
        text = AVATAR_TAIL_RE.sub(lambda m: f"{base}/avatars/{m.group(1)}" if m.group(1) in _avatar_names(mapping) else m.group(0), text)
        # Anything we could not download falls back to the upstream image so the
        # browser still shows the real icon instead of a 404 placeholder.
        for ref in refs:
            if ref in mapping:
                continue
            url = upstream_of(ref)
            if url and ref in text:
                text = text.replace(ref, url)
        if text != original:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
    return len(mapping)


STATIC_ASSET_DIRS = ("/model-providers/", "/leaderboard-sources/")


def download_static_assets(source, out, base) -> int:
    wanted: set[str] = set()
    for dirpath, _, names in os.walk(out):
        if os.sep + "avatars" in dirpath:
            continue
        for name in names:
            if not name.endswith(".html"):
                continue
            with open(os.path.join(dirpath, name), encoding="utf-8", errors="replace") as fh:
                text = fh.read()
            candidates = [html_mod.unescape(m.group(1)) for m in re.finditer(r'(?:src|href|poster)="([^"]*)"', text)]
            for m in SRCSET_RE.finditer(text):
                candidates += [i.strip().split(" ")[0] for i in m.group(1).split(",")]
            for value in candidates:
                if value.startswith(base):
                    value = value[len(base):]
                for prefix in STATIC_ASSET_DIRS:
                    if value.startswith(prefix):
                        wanted.add(value)
    copied = 0
    for path in sorted(wanted):
        dest = os.path.join(out, path.lstrip("/"))
        if os.path.exists(dest):
            continue
        try:
            blob = fetch(source + path)
        except (urllib.error.URLError, OSError):
            continue
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as fh:
            fh.write(blob)
        copied += 1
    return copied


def write_basename_data(out, base) -> int:
    """Mirror the index payload beside the mirror directory.

    React Router resolves the index route's data against the router basename, so
    a browser sitting on /reports/hotspot/ai/all asks for
    /reports/hotspot/ai.data rather than /reports/hotspot/ai/_.data.
    """
    src = os.path.join(out, "_.data")
    if not os.path.exists(src):
        return 0
    dest = os.path.join(os.path.dirname(out), os.path.basename(out) + ".data")
    with open(src, encoding="utf-8", errors="replace") as fh:
        payload = fh.read()
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(payload)
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--site", required=True, choices=sorted(EXTRA_PATHS))
    parser.add_argument("--source", required=True, help="running site origin, e.g. http://127.0.0.1:3000")
    parser.add_argument("--assets", required=True, help="apps/web/build/client/assets directory")
    parser.add_argument("--out", required=True, help="output dir, e.g. hotspot-src/reports/hotspot/ai")
    parser.add_argument("--public-base", default=None, help="deployed base URL; defaults to https://ouyangrong.com<base path>")
    args = parser.parse_args()

    source = args.source.rstrip("/")
    out = args.out.rstrip("/")

    # The router basename and asset paths must match where the mirror is served,
    # which is the path component of the public URL (not the local output dir).
    def path_of(url: str) -> str:
        rest = url.split("://", 1)[-1]
        return ("/" + rest.split("/", 1)[1]).rstrip("/") if "/" in rest else ""

    if args.public_base:
        public_base = args.public_base.rstrip("/")
        base = path_of(public_base) or "/"
    else:
        base = "/" + out.replace(os.sep, "/").split("hotspot-src/", 1)[-1].rstrip("/")
        public_base = f"https://ouyangrong.com{base}"

    if not os.path.isdir(args.assets):
        print(f"assets directory not found: {args.assets}", file=sys.stderr)
        return 2

    order = crawl(source, EXTRA_PATHS[args.site])
    print(f"{args.site}: {len(order)} routes")
    os.makedirs(out, exist_ok=True)
    write_pages(order, source, out, base, public_base)
    print(f"{args.site}: copied {copy_assets(args.assets, out, base, public_base, source)} assets")
    print(f"{args.site}: copied {copy_root_files(source, out, base, public_base)} root files")
    print(f"{args.site}: localized {localize_avatars(source, out, base)} avatars")
    print(f"{args.site}: copied {download_static_assets(source, out, base)} static assets")
    print(f"{args.site}: wrote {write_basename_data(out, base)} basename data file")
    print(f"{args.site}: wrote mirror to {out} (base {base})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
