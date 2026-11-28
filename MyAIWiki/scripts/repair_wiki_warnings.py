#!/usr/bin/env python3
"""Repair mechanical MyAIWiki health warnings without inventing content.

It fills only required frontmatter keys that are absent and converts wiki links
with no resolvable local target into their visible text. Existing content and
resolvable links are preserved.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = ROOT / "wiki"
CHECKER_PATH = Path(__file__).with_name("wiki-health-check.py")
SPEC = importlib.util.spec_from_file_location("wiki_health_check", CHECKER_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load {CHECKER_PATH}")
checker = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = checker
SPEC.loader.exec_module(checker)

REQUIRED = ("title", "category", "tags", "nodes", "date")


def title_for(path: Path, lines: list[str]) -> str:
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def taxonomy_tags(lines: list[str]) -> list[str]:
    tags = re.findall(r"#主题/([^\s`*_.,;，。；:：!?！？\]\)\}]+)", "".join(lines))
    return list(dict.fromkeys(f"主题/{tag}" for tag in tags)) or ["主题/未分类"]


def required_frontmatter(path: Path, lines: list[str]) -> list[str]:
    category = path.relative_to(WIKI_DIR).parts[0]
    return [
        "---\n",
        f"title: {title_for(path, lines)}\n",
        f"category: {category}\n",
        "tags:\n",
        *(f"  - {tag}\n" for tag in taxonomy_tags(lines)),
        "nodes: []\n",
        f"date: {date.today().isoformat()}\n",
        "---\n",
        "\n",
    ]


def fill_missing_frontmatter(path: Path, text: str) -> str:
    lines = text.splitlines(keepends=True)
    bounds = checker.frontmatter_bounds(lines)
    if bounds is None:
        return text

    keys = checker.parse_frontmatter_keys(lines, bounds)
    missing = [field for field in REQUIRED if field not in keys]
    if not missing:
        return text

    insertion: list[str] = []
    category = path.relative_to(WIKI_DIR).parts[0]
    if "title" in missing:
        insertion.append(f"title: {title_for(path, lines[bounds[1] + 1:])}\n")
    if "category" in missing:
        insertion.append(f"category: {category}\n")
    if "tags" in missing:
        insertion.append("tags:\n")
        insertion.extend(f"  - {tag}\n" for tag in taxonomy_tags(lines[bounds[1] + 1:]))
    if "nodes" in missing:
        insertion.append("nodes: []\n")
    if "date" in missing:
        insertion.append(f"date: {date.today().isoformat()}\n")
    return "".join(lines[:bounds[1]] + insertion + lines[bounds[1]:])


def link_is_resolved(target: str, targets: set[str], stem_counts, title_counts, aliases) -> bool:
    normalized, _ = checker.canonical_target(target)
    if normalized.startswith((".", "/", *checker.CROSS_PROJECT_LINK_PREFIXES)):
        return True
    if normalized == "index" or normalized in targets:
        return True
    if "/" not in normalized and (stem_counts[normalized] == 1 or title_counts[normalized] == 1):
        return True
    return checker.resolve_link_alias(target, targets, aliases) is not None


def remove_unresolved_links(text: str, targets: set[str], stem_counts, title_counts, aliases) -> str:
    def replace(match: re.Match[str]) -> str:
        target = match.group(1).strip()
        if link_is_resolved(target, targets, stem_counts, title_counts, aliases):
            return match.group(0)
        label = (match.group(3) or "").removeprefix("|").strip()
        return label or target.rsplit("/", 1)[-1]

    return checker.WIKILINK_FULL_RE.sub(replace, text)


def repair(write: bool) -> list[Path]:
    targets, stem_counts, title_counts, aliases = checker.known_wiki_targets()
    changed: list[Path] = []
    for path in checker.markdown_files(WIKI_DIR):
        original = path.read_text(encoding="utf-8")
        updated = original if path.name == "index.md" else fill_missing_frontmatter(path, original)
        updated = remove_unresolved_links(updated, targets, stem_counts, title_counts, aliases)
        if updated != original:
            changed.append(path)
            if write:
                path.write_text(updated, encoding="utf-8")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Apply repairs; default is a dry run.")
    args = parser.parse_args()
    changed = repair(args.write)
    action = "updated" if args.write else "would update"
    print(f"{action}: {len(changed)} files")
    for path in changed:
        print(path.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
