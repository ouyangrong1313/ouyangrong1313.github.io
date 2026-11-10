#!/usr/bin/env python3
"""Prune expired dated remote-network reports and refresh remaining history links."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


REPORT_NAME = re.compile(r"^seetong-remote-network-metrics-(\d{4}-\d{2}-\d{2})\.html$")
STAT_DATE = re.compile(r"统计日期：(\d{4}-\d{2}-\d{2})")
HISTORY_SECTION = re.compile(r'<section class="history-block">[\s\S]*?</section>')
RETENTION_DAYS = 30
REPORT_TITLE = "异地组网设备指标日报"
EMPTY_HISTORY = "该日期窗口内暂无历史日报。"


@dataclass(frozen=True)
class Archive:
    path: Path
    report_date: date


def get_archives(archive_dir: Path) -> list[Archive]:
    archives = []
    for path in sorted(archive_dir.iterdir()):
        match = REPORT_NAME.fullmatch(path.name)
        if not match or path.is_symlink() or not path.is_file():
            continue

        try:
            report_date = date.fromisoformat(match.group(1))
        except ValueError:
            print(f"Skipping invalid archive date: {path.name}", file=sys.stderr)
            continue

        content = path.read_text(encoding="utf-8")
        stat_match = STAT_DATE.search(content)
        if not stat_match or stat_match.group(1) != report_date.isoformat():
            print(f"Skipping archive with mismatched report date: {path.name}", file=sys.stderr)
            continue

        archives.append(Archive(path=path, report_date=report_date))
    return archives


def render_history(report_date: date, archives: list[Archive], archive_page: bool) -> str:
    first_date = report_date - timedelta(days=9)
    history = sorted(
        (item for item in archives if first_date <= item.report_date < report_date),
        key=lambda item: item.report_date,
        reverse=True,
    )

    if not history:
        body = f'<p class="history-empty">{EMPTY_HISTORY}</p>'
    else:
        # 条目标记必须与 scripts/publish-group-report.py 的 remote_history_section
        # 逐字节一致（单个 history-day span）。历史上这里写的是 history-stamp +
        # history-title 两个 span，两边各写一套，导致每次运行都判定「内容变了」，
        # 于是清理任务和日报任务反复互相覆盖同一批文件，最终 push 分叉
        # （2026-11-10 事故：日报连续 6 次推送被拒，群里断更）。
        prefix = "" if archive_page else "archive/"
        items = "".join(
            '<li><a href="{}{}"><span class="history-day">{}</span></a></li>'.format(
                prefix,
                item.path.name,
                item.report_date.isoformat(),
            )
            for item in history
        )
        body = f'<ul class="history-list">{items}</ul>'

    return (
        '<section class="history-block"><h2><span class="h2-icon">🗂️</span>'
        f'历史日报</h2>{body}</section>'
    )


def update_history(page: Path, archives: list[Archive], archive_page: bool) -> bool:
    content = page.read_text(encoding="utf-8")
    date_match = STAT_DATE.search(content)
    if not date_match:
        raise ValueError(f"Missing report date in {page}")

    matches = list(HISTORY_SECTION.finditer(content))
    if len(matches) != 1:
        raise ValueError(f"Expected one history section in {page}, found {len(matches)}")

    report_date = date.fromisoformat(date_match.group(1))
    match = matches[0]
    section = render_history(report_date, archives, archive_page)
    updated = content[: match.start()] + section + content[match.end() :]
    if updated == content:
        return False

    page.write_text(updated, encoding="utf-8")
    return True


def cleanup_reports(reports_dir: Path, today: date, dry_run: bool = False) -> list[Path]:
    archive_dir = reports_dir / "archive"
    archives = get_archives(archive_dir)
    cutoff = today - timedelta(days=RETENTION_DAYS)
    expired = [item for item in archives if item.report_date < cutoff]

    if not expired:
        print("No dated remote-network report archives are older than 30 days.")
        return []

    for item in expired:
        print(f"{'Would remove' if dry_run else 'Removing'} {item.path}")
    if dry_run:
        return [item.path for item in expired]

    remaining = [item for item in archives if item not in expired]
    # 入口页（reports/seetong-remote-network-metrics.html）的写入权归日报任务独占。
    # 它只展示「统计日前 9 天」的归档，而这里删的是 30 天以前的，两者窗口不重叠，
    # 所以清理任务无需、也不得改动入口页——一旦两边都写，必然在 push 阶段分叉。
    for item in remaining:
        update_history(item.path, remaining, archive_page=True)

    for item in expired:
        item.path.unlink()
    print(f"Removed {len(expired)} expired archive(s); refreshed remaining history links.")
    return [item.path for item in expired]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="List expired archives without changing files")
    args = parser.parse_args()

    reports_dir = Path(__file__).resolve().parents[1] / "reports"
    today = datetime.now(ZoneInfo("Asia/Shanghai")).date()
    cleanup_reports(reports_dir, today, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
