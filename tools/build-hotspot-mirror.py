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
import json
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
from pathlib import Path

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

# The snapshot has no server, so the reader-facing actions are restored by a small self-contained
# script injected into every page (localStorage 收藏, local index 搜索, canvas 海报, history 返回,
# mailto 反馈). See tools/hotspot-mirror-interactive.js for what it replaces and why.
INTERACTIVE_JS = (Path(__file__).resolve().parent / "hotspot-mirror-interactive.js").read_text(encoding="utf-8")
# Public feedback address, taken from the industry pack's contactEmail.
SITE_STRINGS = {
    "ai": {"site": "AI", "feedbackEmail": "rong.ouyang@tpsee8.com"},
    "sec": {"site": "安防", "feedbackEmail": "rong.ouyang@tpsee8.com"},
}


# The feed filters ("全部 / 一手 / 各分类") are plain links carrying a query string. A static host
# ignores the query string, so a snapshot would keep showing the unfiltered list no matter what the
# visitor clicks. Each filter state is rendered once from the live site and published as its own
# directory, then the links are rewritten to point at it — filtering works with no JavaScript:
#   ?channel=firstParty   -> /channel-firstparty/
#   ?category=ai-models   -> /category-ai-models/
FILTER_KEYS = ("channel", "category")
FILTER_LINK_RE = re.compile(r'href="([^"]*)\?((?:channel|category)=[^"&]+)"')


def filter_dir_name(query: str) -> str:
    key, value = query.split("=", 1)
    return f"{key}-{re.sub(r'[^a-z0-9-]', '-', value.lower())}"


def discover_filters(doc: str) -> set[str]:
    """Collect the single-parameter channel/category queries linked from a page."""
    out: set[str] = set()
    for match in FILTER_LINK_RE.finditer(doc):
        query = html_mod.unescape(match.group(2))
        key, value = query.split("=", 1)
        if key in FILTER_KEYS and value and "&" not in query:
            out.add(query)
    return out


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


def rewrite_html(text: str, base: str, public_base: str, source: str, filters: set[str] | None = None) -> str:
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

    text = ATTR_RE.sub(fix, text)

    # Point query-string filters at their pre-rendered static directories.
    for query in sorted(filters or ()):
        text = text.replace(f'href="{base}/?{query}"', f'href="{base}/{filter_dir_name(query)}/"')
    text = FILTER_LINK_RE.sub(
        lambda m: f'href="{base}/{filter_dir_name(html_mod.unescape(m.group(2)))}/"'
        if html_mod.unescape(m.group(2)) in (filters or set())
        else m.group(0),
        text,
    )

    # Drop the app bundle: it cannot boot under a nested path (React Router reroutes, the synthetic
    # filter directories 404, and every action fetches a backend Pages does not serve). Keep the CSS.
    # The reader-facing interactions come back through the injected mirror layer just below.
    text = re.sub(r"<script\b[^>]*>.*?</script>", "", text, flags=re.S)
    text = re.sub(r"<script\b[^>]*/>", "", text)
    text = re.sub(r'<link\b[^>]*rel="(?:prefetch|preload|modulepreload)"[^>]*/?>', "", text)

    slug = base.rstrip("/").rsplit("/", 1)[-1]
    strings = SITE_STRINGS.get(slug, SITE_STRINGS["sec"])
    cfg = {"base": base, "site": strings["site"], "feedbackEmail": strings["feedbackEmail"]}
    inject = (
        "<script>window.__HOTSPOT_MIRROR__=" + json.dumps(cfg, ensure_ascii=False) + ";</script>"
        "<script>" + INTERACTIVE_JS + "</script>"
    )
    text = text.replace("</body>", inject + "</body>", 1) if "</body>" in text else text + inject
    return text


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


def sitemap_paths(source: str) -> list[str]:
    """All public routes the site advertises. Some (older story pages) are not linked from the home
    page any more, so crawling alone would leave them out and the mirror would 404 on a shared link."""
    try:
        xml = fetch(f"{source}/sitemap.xml").decode("utf-8", "replace")
    except Exception:
        return []
    out: list[str] = []
    for raw in re.findall(r"<loc>([^<]+)</loc>", xml):
        rest = raw.split("://", 1)[-1]
        path = "/" + rest.split("/", 1)[1] if "/" in rest else "/"
        path = html_mod.unescape(path).strip()
        if path and path not in out:
            out.append(path)
    return out


def crawl(source: str, extra: tuple[str, ...]) -> tuple[list[str], set[str]]:
    seen = {"/"}
    order = ["/"]
    filters: set[str] = set()
    queue: deque[str] = deque(["/"])
    for path in list(extra) + sitemap_paths(source):
        if path not in seen and is_route(path):
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
        filters |= discover_filters(doc)
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
    return order, filters


def write_pages(order, source, out, base, public_base, filters: set[str] | None = None) -> None:
    for path in order:
        try:
            doc = fetch(source + path)
        except (urllib.error.URLError, OSError) as exc:
            print(f"  ! HTML {path}: {exc}", file=sys.stderr)
            continue
        text = rebase_srcset(rewrite_html(doc.decode("utf-8", "replace"), base, public_base, source, filters), base)
        html_path = os.path.join(out, "index.html") if path == "/" else os.path.join(out, path.strip("/"), "index.html")
        os.makedirs(os.path.dirname(html_path), exist_ok=True)
        with open(html_path, "w", encoding="utf-8") as fh:
            fh.write(text)

        # No ".data" payloads are written: every <script> is stripped above, so nothing in the
        # published snapshot fetches them, while their pointer-indexed serialization shifts whenever
        # any item is added — a permanent source of hundred-file pseudo-diffs.


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


def write_filter_pages(filters: set[str], source, out, base, public_base) -> int:
    """Render each ?channel=/?category= state once and publish it as a directory."""
    written = 0
    for query in sorted(filters):
        try:
            doc = fetch(f"{source}/?{query}")
        except (urllib.error.URLError, OSError) as exc:
            print(f"  ! filter {query}: {exc}", file=sys.stderr)
            continue
        text = rebase_srcset(rewrite_html(doc.decode("utf-8", "replace"), base, public_base, source, filters), base)
        dest = os.path.join(out, filter_dir_name(query), "index.html")
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(text)
        written += 1
    return written


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


def write_share_posters(source, out, base, item_ids: list[str]) -> int:
    """Mirror the per-item share poster (1080x1440 PNG) used by 生成分享海报.

    The poster is rendered on demand by the live API, so it only exists as a URL; download it while
    the local site is up, and keep it beside the page that links to it. The interactive layer points
    at BASE + /og/posters/<id>.png; a poster that fails to download is left absent and the layer then
    falls back to drawing one in the browser.
    """
    if not item_ids:
        return 0
    dest_dir = os.path.join(out, "og", "posters")
    os.makedirs(dest_dir, exist_ok=True)
    copied = 0
    for iid in item_ids:
        dest = os.path.join(dest_dir, iid + ".png")
        if os.path.exists(dest) and os.path.getsize(dest) > 1000:
            copied += 1
            continue
        try:
            blob = fetch(f"{source}/og/posters/{iid}.png")
        except SystemExit:
            continue
        except Exception:
            continue
        if len(blob) < 1000:
            continue
        with open(dest, "wb") as fh:
            fh.write(blob)
        copied += 1
    return copied


def write_search_index(source, out, base) -> int:
    """Write a small client-side search index so 搜索 works without a backend.

    The public API caps a page at 100 items, so this walks the cursor to collect everything public,
    then keeps only the fields the mirror's search needs (title, summary, source, link).
    """
    items: list[dict] = []
    cursor: str | None = None
    for _ in range(20):
        url = f"{source}/api/v1/items?mode=all&window=7d&limit=100"
        if cursor:
            url += "&cursor=" + urllib.parse.quote(cursor)
        try:
            body = json.loads(fetch(url).decode("utf-8", "replace"))
        except Exception:
            break
        page = body.get("items") or []
        for it in page:
            iid = it.get("id")
            if not iid:
                continue
            links = it.get("links") or {}
            items.append({
                "id": iid,
                "title": it.get("title") or "",
                "summary": it.get("summary") or "",
                "source": (it.get("source") or {}).get("name") or "",
                "href": f"{base}/items/{iid}/",
                "original": links.get("original") or "",
            })
        meta = body.get("page") or {}
        cursor = meta.get("nextCursor")
        if not cursor or not meta.get("hasMore"):
            break
    dest = os.path.join(out, "search-index.json")
    with open(dest, "w", encoding="utf-8") as fh:
        json.dump({"items": items}, fh, ensure_ascii=False, separators=(",", ":"))
    return len(items)


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

    order, filters = crawl(source, EXTRA_PATHS[args.site])
    print(f"{args.site}: {len(order)} routes, {len(filters)} filter states")

    # Remove route directories from a previous build before repopulating. Otherwise routes that
    # disappear (or that a narrower builder once wrote) would linger in the snapshot forever.
    # Remove legacy ".data" payloads from earlier builds (see write_pages).
    for dirpath, _dirs, names in os.walk(out):
        for name in names:
            if name.endswith(".data"):
                os.remove(os.path.join(dirpath, name))

    keep = {"assets", "avatars", "og"}
    for name in os.listdir(out):
        full = os.path.join(out, name)
        if name not in keep and name not in ("index.html",):
            if os.path.isdir(full):
                shutil.rmtree(full)
    os.makedirs(out, exist_ok=True)
    write_pages(order, source, out, base, public_base, filters)
    print(f"{args.site}: wrote {write_filter_pages(filters, source, out, base, public_base)} filter pages")
    print(f"{args.site}: wrote {write_search_index(source, out, base)} search entries")
    item_ids = []
    for root, _dirs, names in os.walk(os.path.join(out, "items")):
        for name in names:
            if name == "index.html":
                item_ids.append(os.path.basename(root))
    print(f"{args.site}: mirrored {write_share_posters(source, out, base, item_ids)} share posters")
    print(f"{args.site}: copied {copy_assets(args.assets, out, base, public_base, source)} assets")
    print(f"{args.site}: copied {copy_root_files(source, out, base, public_base)} root files")
    print(f"{args.site}: localized {localize_avatars(source, out, base)} avatars")
    print(f"{args.site}: copied {download_static_assets(source, out, base)} static assets")
    print(f"{args.site}: wrote mirror to {out} (base {base})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
