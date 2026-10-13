#!/usr/bin/env bash
#
# DEPRECATED forwarder — do not add logic here.
#
# This used to rebuild the hotspot snapshots with tools/build-hotspot-mirror.py. That builder
# only wrote pages reachable from the home page plus sitemap entries, so a refresh could drop
# the mirrored detail pages and leave the published site linking to files that were never
# written. htmlproofer then failed the pages job and the gh-pages deploy froze (2026-10-13
# outage; detail-page 404s).
#
# The supported entry point is now:
#   python3 ~/.openclaw/workspace/scripts/refresh-hotspot-mirrors.py --root <this repo>
# which mirrors every page (home + filters + routes + detail pages, iterated to a fixpoint),
# runs a link gate before writing, and publishes only when reader-visible content changed.
#
# This wrapper forwards to it so any older caller (cron, a habit, a doc) converges on the one
# pipeline instead of silently resurrecting the destructive one. Arguments passed through.
#
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NEW_SCRIPT="/Users/topsee/.openclaw/workspace/scripts/refresh-hotspot-mirrors.py"

if [[ ! -f "$NEW_SCRIPT" ]]; then
  echo "[refresh] 收敛脚本缺失：$NEW_SCRIPT" >&2
  echo "[refresh] 本脚本已废弃，不再自行重建镜像（会丢详情页）。" >&2
  exit 1
fi

echo "[refresh] 已废弃：转发到 $NEW_SCRIPT" >&2

ARGS=("--root" "$ROOT")
for arg in "$@"; do
  case "$arg" in
    --push)    ARGS+=(--push) ;;      # accepted for compatibility; new script pushes by default
    --no-push) ARGS+=(--no-push) ;;
    *) echo "[refresh] 忽略未知参数：$arg" >&2 ;;
  esac
done

exec python3 "$NEW_SCRIPT" "${ARGS[@]}"
