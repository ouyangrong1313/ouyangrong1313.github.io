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

for entry in "${SITES[@]}"; do
  IFS='|' read -r site source assets out <<<"$entry"
  echo "[refresh] 重建 $site 镜像：$out"
  python3 tools/build-hotspot-mirror.py --site "$site" --source "$source" --assets "$assets" --out "$out"
  pages="$(find "$out" -name index.html | wc -l | tr -d ' ')"
  avatars="$(find "$out/avatars" -type f 2>/dev/null | wc -l | tr -d ' ')"
  bytes="$(du -sk "$out" | awk '{print $1 * 1024}')"
  echo "[refresh] $site: $pages 个页面，$avatars 个头像，${bytes} 字节"
done

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
