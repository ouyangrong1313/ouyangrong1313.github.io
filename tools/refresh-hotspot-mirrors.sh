#!/usr/bin/env bash
#
# Rebuild the committed hotspot snapshots under hotspot-src/ from the live local sites.
#
# The two hotspot sites run from /Volumes/TopSee/AIHOT and are only reachable on localhost.
# GitHub Pages can only serve files, so each site is published as a prebuilt multi-page
# snapshot. This script is the single supported refresh entry point; run it whenever the
# sites have new content.
#
# Usage:
#   tools/refresh-hotspot-mirrors.sh [--push]
#
#   (default) rebuild only, leaving the changes in the working tree
#   --push    also commit hotspot-src/ and push to origin/master, which triggers Pages
#
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

AIHOT="${AIHOT_ROOT:-/Volumes/TopSee/AIHOT}"
PUSH=false
for arg in "$@"; do
  case "$arg" in
    --push) PUSH=true ;;
    --no-push) PUSH=false ;;
    *) echo "unknown option: $arg" >&2; exit 2 ;;
  esac
done

SITES=(
  "ai|http://127.0.0.1:3000|$AIHOT/ai/apps/web/build/client/assets|hotspot-src/reports/hotspot/ai"
  "sec|http://127.0.0.1:3100|$AIHOT/sec/apps/web/build/client/assets|hotspot-src/reports/hotspot/sec"
)

# Gate: both sites must be up before anything is written, so a half-refreshed snapshot
# (one site current, one stale) cannot be committed.
for entry in "${SITES[@]}"; do
  IFS='|' read -r site source assets out <<<"$entry"
  if ! "$AIHOT/bin/site.sh" "$site" status >/dev/null 2>&1; then
    echo "[refresh] $site 站点未运行；先执行 $AIHOT/bin/site.sh $site start" >&2
    exit 1
  fi
  if [[ ! -d "$assets" ]]; then
    echo "[refresh] 找不到前端资源目录：$assets" >&2
    exit 1
  fi
done

# Whether this refresh is worth a commit is decided by the *content signature*: which routes exist
# plus each page's title, plus the hash of the builder and the injected interaction layer. Live-derived
# numbers (rolling 48h heat, the "更新" clock, sparkline geometry) drift on every run and must never
# trigger a push on their own. The last published signature is committed as
# hotspot-src/.mirror-signature, so this compares against what readers actually have.
SIG_FILE="hotspot-src/.mirror-signature"
SIG_PUBLISHED="$(git show HEAD:$SIG_FILE 2>/dev/null | tr -d '[:space:]' || true)"

for entry in "${SITES[@]}"; do
  IFS='|' read -r site source assets out <<<"$entry"
  if ! "$AIHOT/bin/site.sh" "$site" status >/dev/null 2>&1; then
    echo "[refresh] $site 站点未运行；先执行 $AIHOT/bin/site.sh $site start" >&2
    exit 1
  fi
  if [[ ! -d "$assets" ]]; then
    echo "[refresh] 找不到前端资源目录：$assets" >&2
    exit 1
  fi
done

# Two signatures decide whether this refresh is worth a commit:
#   * content signature  — routes plus each page's title/date. A new item changes it.
#   * raw digest         — everything except clock fields. Catches a builder fix that must ship.
# Volatile live-derived numbers (rolling 48h heat, "更新" clock, sparkline geometry) move the raw
# digest on every run, so they alone must never trigger a push. Compare against HEAD so real
# uncommitted changes are never mistaken for noise.
SIG_BEFORE="$(python3 tools/hotspot-mirror-content-signature.py hotspot-src)"
SIG_HEAD="$(python3 tools/hotspot-mirror-content-signature.py hotspot-src)"

for entry in "${SITES[@]}"; do
  IFS='|' read -r site source assets out <<<"$entry"
  if ! "$AIHOT/bin/site.sh" "$site" status >/dev/null 2>&1; then
    echo "[refresh] $site 站点未运行；先执行 $AIHOT/bin/site.sh $site start" >&2
    exit 1
  fi
  if [[ ! -d "$assets" ]]; then
    echo "[refresh] 找不到前端资源目录：$assets" >&2
    exit 1
  fi
done

# Fingerprint the COMMITTED mirrors (HEAD), ignoring clock fields. Comparing against HEAD — not the
# working tree — keeps a refresh from being mistaken for pure noise when the tree already carries
# legitimate uncommitted changes (e.g. a builder change that drops obsolete files).
DIGEST_BEFORE="$(git stash list >/dev/null 2>&1; python3 tools/hotspot-mirror-digest.py hotspot-src)"
if git diff --quiet -- hotspot-src && git diff --cached --quiet -- hotspot-src; then
  DIGEST_HEAD="$DIGEST_BEFORE"
else
  DIGEST_HEAD="$(git show HEAD:hotspot-src >/dev/null 2>&1 || true; python3 - <<'PY'
import subprocess, tempfile, os, sys, importlib.util, pathlib
spec = importlib.util.spec_from_file_location("d", "tools/hotspot-mirror-digest.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
names = subprocess.run(["git", "ls-tree", "-r", "--name-only", "HEAD", "hotspot-src"], capture_output=True, text=True).stdout.split()
import hashlib
digest = hashlib.sha256()
for name in sorted(names):
    blob = subprocess.run(["git", "show", f"HEAD:{name}"], capture_output=True).stdout
    if name.endswith((".html", ".data", ".json", ".xml", ".txt", ".webmanifest")):
        blob = m.normalize(blob.decode("utf-8", "replace")).encode()
    digest.update(name.encode()); digest.update(b"\0"); digest.update(blob); digest.update(b"\0")
print(digest.hexdigest())
PY
)"
fi

for entry in "${SITES[@]}"; do
  IFS='|' read -r site source assets out <<<"$entry"
  echo "[refresh] 重建 $site 镜像：$out"
  python3 tools/build-hotspot-mirror.py --site "$site" --source "$source" --assets "$assets" --out "$out"
  pages="$(find "$out" -name index.html | wc -l | tr -d ' ')"
  avatars="$(find "$out/avatars" -type f 2>/dev/null | wc -l | tr -d ' ')"
  bytes="$(du -sk "$out" | awk '{print $1 * 1024}')"
  echo "[refresh] $site: $pages 个页面，$avatars 个头像，${bytes} 字节"
done

SIG_AFTER="$(python3 tools/hotspot-mirror-content-signature.py hotspot-src)"

if [[ -n "$SIG_PUBLISHED" && "$SIG_PUBLISHED" == "$SIG_AFTER" ]]; then
  # Nothing a reader would notice changed: no page appeared, disappeared or was retitled, and neither
  # the builder nor the interaction layer changed. Only live-derived numbers moved. Roll back so the
  # two-hourly job leaves the repository clean.
  git checkout -- hotspot-src 2>/dev/null || true
  echo "[refresh] 内容集合无变化（仅热度/时间等派生数值），已还原工作区"
  exit 0
fi

# Record what is about to be published, so the next run can compare against it.
printf '%s\n' "$SIG_AFTER" > "$SIG_FILE"

echo "[refresh] 完成。变更文件："
git status --short hotspot-src | head -40

if $PUSH; then
  if git diff --quiet -- hotspot-src; then
    echo "[refresh] 无变更，跳过提交"
  else
    git add hotspot-src
    git commit -m "chore: refresh hotspot mirrors"
    git push origin master
    echo "[refresh] 已推送到 origin/master，Pages 部署已触发"
  fi
fi
