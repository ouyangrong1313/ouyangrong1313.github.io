#!/usr/bin/env python3
"""Check and normalize the structural rules of MyAIWiki.

Usage:
  python3 scripts/wiki-health-check.py
  python3 scripts/wiki-health-check.py --fix

The optional --fix only changes two mechanical forms:
  * YAML frontmatter tags become a YAML list without a leading '#'.
  * Taxonomy tags in Markdown prose gain a whitespace boundary before '#'.
"""

from __future__ import annotations

import argparse
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = ROOT / "wiki"
CANONICAL_CATEGORIES = (
    "01-ai-agents",
    "02-ai-coding",
    "03-productivity",
    "04-app-dev",
    "05-content-creation",
    "06-ai-tech",
    "07-rag-systems",
)
LEGACY_CATEGORY_MAP = {
    "ai-agents": "01-ai-agents",
    "ai-coding": "02-ai-coding",
    "productivity": "03-productivity",
    "content-creation": "05-content-creation",
    "ai-tech": "06-ai-tech",
}
CROSS_PROJECT_LINK_PREFIXES = ("seetong-",)
REQUIRED_FRONTMATTER_FIELDS = ("title", "category", "tags", "nodes", "date")
TAXONOMY_PREFIXES = (
    "主题",
    "手法",
    "场景",
    "节点",
    "作者",
    "来源",
    "公司",
    "公众号",
    "播客",
    "项目",
    "编辑",
)
INLINE_TAG_RE = re.compile(
    r"(?<!\s)(?P<tag>#(?:" + "|".join(TAXONOMY_PREFIXES) + r")/[^\s`*_.,;，。；:：!?！？\]\)\}]+)"
)
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
WIKILINK_FULL_RE = re.compile(r"\[\[([^\]|#]+)(#[^\]|]+)?(\|[^\]]+)?\]\]")
FRONTMATTER_KEY_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):")


@dataclass
class Findings:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    changed_files: list[Path] = field(default_factory=list)
    metrics: Counter = field(default_factory=Counter)
    unresolved_targets: Counter = field(default_factory=Counter)


def markdown_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.md") if ".obsidian" not in path.parts)


def frontmatter_bounds(lines: list[str]) -> tuple[int, int] | None:
    if not lines or lines[0].strip() != "---":
        return None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return 0, index
    return None


def parse_frontmatter_keys(lines: list[str], bounds: tuple[int, int]) -> set[str]:
    _, end = bounds
    keys: set[str] = set()
    for line in lines[1:end]:
        match = FRONTMATTER_KEY_RE.match(line)
        if match:
            keys.add(match.group(1))
    return keys


def normalize_tag_value(value: str) -> str:
    cleaned = value.strip().strip("'\"").lstrip("#").strip()
    return re.sub(r"\s+", "-", cleaned)


def collection_values(lines: list[str], bounds: tuple[int, int], key: str) -> list[str]:
    start, end = bounds
    key_index = next(
        (index for index in range(start + 1, end) if lines[index].startswith(f"{key}:")),
        None,
    )
    if key_index is None:
        return []
    value = lines[key_index].split(":", 1)[1].strip()
    if value:
        inner = value[1:-1] if value.startswith("[") and value.endswith("]") else value
        protected = re.sub(r"\[\[([^\]]+)\]\]", lambda match: "[[" + match.group(1).replace(",", "<comma>") + "]]", inner)
        return [part.strip().strip("'\"").replace("<comma>", ",") for part in protected.split(",") if part.strip()]

    values: list[str] = []
    for candidate in lines[key_index + 1 : end]:
        if FRONTMATTER_KEY_RE.match(candidate):
            break
        match = re.match(r"^\s*-\s+(.+?)\s*$", candidate)
        if match:
            values.append(match.group(1).strip().strip("'\""))
    return values


def split_inline_tags(value: str) -> list[str]:
    inner = value.strip()
    if inner.startswith("[") and inner.endswith("]"):
        inner = inner[1:-1]
    if not inner:
        return []
    parts = re.split(r"\s*(?:,)?\s*(?=#)", inner) if "#" in inner else inner.split(",")
    return [normalized for part in parts if (normalized := normalize_tag_value(part))]


def normalize_frontmatter_tags(lines: list[str], bounds: tuple[int, int]) -> tuple[list[str], bool]:
    start, end = bounds
    tag_index = next(
        (index for index in range(start + 1, end) if lines[index].startswith("tags:")),
        None,
    )
    if tag_index is None:
        return lines, False

    value = lines[tag_index].split(":", 1)[1].strip()
    remove_until = tag_index + 1
    if value:
        tags = split_inline_tags(value)
    else:
        tag_values: list[str] = []
        while remove_until < end:
            candidate = lines[remove_until]
            if FRONTMATTER_KEY_RE.match(candidate):
                break
            match = re.match(r"^\s*-\s+(.+?)\s*$", candidate)
            if match:
                tag_values.append(match.group(1))
            remove_until += 1
        tags = [normalized for item in tag_values if (normalized := normalize_tag_value(item))]

    if not tags:
        return lines, False

    replacement = ["tags:\n"] + [f"  - {tag}\n" for tag in tags]
    original = lines[tag_index:remove_until]
    if original == replacement:
        return lines, False
    return lines[:tag_index] + replacement + lines[remove_until:], True


def normalize_prose_tags(lines: list[str], start_index: int) -> tuple[list[str], int]:
    changed = 0
    in_fence = False
    result = lines[:]
    for index in range(start_index, len(result)):
        line = result[index]
        if re.match(r"^\s*(```|~~~)", line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        parts = re.split(r"(`[^`]*`)", line)
        for part_index in range(0, len(parts), 2):
            normalized, count = INLINE_TAG_RE.subn(r" \g<tag>", parts[part_index])
            parts[part_index] = normalized
            changed += count
        result[index] = "".join(parts)
    return result, changed


def normalize_file(path: Path) -> str:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    bounds = frontmatter_bounds(lines)
    body_start = 0
    if bounds:
        lines, _ = normalize_frontmatter_tags(lines, bounds)
        refreshed_bounds = frontmatter_bounds(lines)
        body_start = refreshed_bounds[1] + 1 if refreshed_bounds else 0
    lines, _ = normalize_prose_tags(lines, body_start)
    return "".join(lines)


def invalid_prose_tag_count(lines: list[str], start_index: int) -> int:
    count = 0
    in_fence = False
    for line in lines[start_index:]:
        if re.match(r"^\s*(```|~~~)", line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for part_index, part in enumerate(re.split(r"(`[^`]*`)", line)):
            if part_index % 2 == 0:
                count += len(INLINE_TAG_RE.findall(part))
    return count


def canonical_target(target: str) -> tuple[str, bool]:
    normalized = target.strip().removeprefix("wiki/").removesuffix(".md")
    parts = normalized.split("/")
    if parts and parts[0] in LEGACY_CATEGORY_MAP:
        parts[0] = LEGACY_CATEGORY_MAP[parts[0]]
        return "/".join(parts), True
    return normalized, False


def identifier_key(value: str) -> str:
    basename = value.rsplit("/", 1)[-1]
    basename = re.sub(r"^20\d{2}(?:[-_]\d{2}){0,2}[-_]", "", basename)
    return re.sub(r"[^0-9a-z\u4e00-\u9fff]+", "", basename.lower())


def resolve_link_alias(target: str, targets: set[str], alias_targets: dict[str, set[str]]) -> str | None:
    normalized, _ = canonical_target(target)
    if normalized.startswith((".", "/")) or normalized in targets:
        return None
    candidates = alias_targets.get(identifier_key(normalized), set())
    return next(iter(candidates)) if len(candidates) == 1 else None


def page_title(lines: list[str], bounds: tuple[int, int] | None) -> str:
    if bounds:
        for line in lines[1 : bounds[1]]:
            if line.startswith("title:"):
                return line.split(":", 1)[1].strip().strip("'\"")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def known_wiki_targets() -> tuple[set[str], Counter, Counter, dict[str, set[str]]]:
    targets: set[str] = set()
    stem_counts: Counter = Counter()
    title_counts: Counter = Counter()
    alias_targets: dict[str, set[str]] = {}
    for path in markdown_files(WIKI_DIR):
        relative = path.relative_to(WIKI_DIR).with_suffix("").as_posix()
        targets.add(relative)
        stem_counts[path.stem] += 1
        lines = path.read_text(encoding="utf-8").splitlines()
        title = page_title(lines, frontmatter_bounds(lines))
        if title:
            title_counts[title] += 1
        for value in (path.stem, title):
            if value:
                alias_targets.setdefault(identifier_key(value), set()).add(relative)
    return targets, stem_counts, title_counts, alias_targets


def display(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def check_legacy_directories(findings: Findings) -> None:
    for legacy, canonical in LEGACY_CATEGORY_MAP.items():
        path = WIKI_DIR / legacy
        if path.exists():
            count = len(markdown_files(path))
            findings.errors.append(f"legacy category directory {display(path)} ({count} Markdown files); use {canonical}")
            findings.metrics["legacy_directories"] += 1


def check_file(path: Path, targets: set[str], stem_counts: Counter, title_counts: Counter, alias_targets: dict[str, set[str]], findings: Findings) -> None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    bounds = frontmatter_bounds(lines)
    path_label = display(path)
    findings.metrics["markdown_files"] += 1

    if bounds:
        findings.metrics["frontmatter_files"] += 1
        keys = parse_frontmatter_keys(lines, bounds)
        relative_parts = path.relative_to(WIKI_DIR).parts if path.is_relative_to(WIKI_DIR) else ()
        if relative_parts and relative_parts[0] in CANONICAL_CATEGORIES and path.name != "index.md":
            missing = [field for field in REQUIRED_FRONTMATTER_FIELDS if field not in keys]
            if missing:
                findings.warnings.append(f"{path_label}: missing frontmatter fields: {', '.join(missing)}")
                findings.metrics["frontmatter_missing"] += 1
            category_line = next((line for line in lines[1 : bounds[1]] if line.startswith("category:")), "")
            category = category_line.split(":", 1)[1].strip().strip("'\"") if category_line else ""
            if category and category != relative_parts[0]:
                findings.errors.append(f"{path_label}: category {category!r} does not match directory {relative_parts[0]!r}")
                findings.metrics["category_mismatch"] += 1

    body_start = bounds[1] + 1 if bounds else 0
    inline_violations = invalid_prose_tag_count(lines, body_start)
    if inline_violations:
        findings.errors.append(f"{path_label}: {inline_violations} inline tag(s) lack a whitespace boundary")
        findings.metrics["invalid_inline_tags"] += inline_violations

    if not path.is_relative_to(WIKI_DIR):
        return
    for match in WIKILINK_RE.finditer(text):
        target, legacy = canonical_target(match.group(1))
        if target.startswith(".") or target.startswith("/"):
            continue
        if target.startswith(CROSS_PROJECT_LINK_PREFIXES):
            findings.metrics["cross_project_links"] += 1
            continue
        if legacy:
            findings.errors.append(f"{path_label}: legacy wiki link [[{match.group(1)}]]")
            findings.metrics["legacy_links"] += 1
        if (
            target == "index"
            or target in targets
            or ("/" not in target and stem_counts[target] == 1)
            or title_counts[target] == 1
        ):
            continue
        alias = resolve_link_alias(match.group(1), targets, alias_targets)
        if alias:
            findings.warnings.append(f"{path_label}: noncanonical wiki link [[{match.group(1)}]] -> [[{alias}]]")
            findings.metrics["alias_links"] += 1
            continue
        findings.warnings.append(f"{path_label}: unresolved wiki link [[{match.group(1)}]]")
        findings.metrics["unresolved_links"] += 1
        findings.unresolved_targets[match.group(1)] += 1


def check_index_coverage(findings: Findings) -> None:
    for category in CANONICAL_CATEGORIES:
        directory = WIKI_DIR / category
        index = directory / "index.md"
        if not index.exists():
            findings.errors.append(f"missing category index: {display(index)}")
            findings.metrics["missing_indexes"] += 1
            continue
        index_text = index.read_text(encoding="utf-8")
        for page in directory.glob("*.md"):
            if page.name != "index.md" and page.stem not in index_text:
                findings.warnings.append(f"{display(page)}: no matching entry in {display(index)}")
                findings.metrics["unindexed_pages"] += 1

    for directory in sorted(path for path in WIKI_DIR.rglob("*") if path.is_dir()):
        if len(directory.relative_to(WIKI_DIR).parts) < 2:
            continue
        pages = [path for path in directory.glob("*.md") if path.name != "index.md"]
        if not pages:
            continue
        index = directory / "index.md"
        if not index.exists():
            findings.errors.append(f"missing directory index: {display(index)}")
            findings.metrics["missing_directory_indexes"] += 1
            continue
        index_text = index.read_text(encoding="utf-8")
        for page in pages:
            if page.stem not in index_text:
                findings.warnings.append(f"{display(page)}: no matching entry in {display(index)}")
                findings.metrics["unindexed_pages"] += 1


def normalize_indexes() -> list[Path]:
    changed: list[Path] = []
    heading = "### 自动补全条目（待补摘要）"
    for category in CANONICAL_CATEGORIES:
        directory = WIKI_DIR / category
        index = directory / "index.md"
        if not index.exists():
            continue
        text = index.read_text(encoding="utf-8")
        missing = [
            page.relative_to(directory).with_suffix("").as_posix()
            for page in markdown_files(directory)
            if page.name != "index.md" and page.stem not in text
        ]
        if not missing:
            continue
        block = "\n".join(f"- [[{target}]]" for target in missing)
        if heading in text:
            insertion = text.index(heading) + len(heading)
            text = text[:insertion] + "\n" + block + text[insertion:]
        else:
            text = text.rstrip() + f"\n\n{heading}\n\n{block}\n"
        index.write_text(text, encoding="utf-8")
        changed.append(index)
    return changed


def check_node_orphans(findings: Findings) -> None:
    nodes: set[str] = set()
    link_targets: set[str] = set()
    for path in markdown_files(WIKI_DIR):
        if path.name == "index.md":
            continue
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        bounds = frontmatter_bounds(lines)
        if bounds:
            nodes.update(collection_values(lines, bounds, "nodes"))
        for match in WIKILINK_RE.finditer(text):
            link_targets.add(match.group(1).strip())
    orphan_count = sum(1 for node in nodes if node not in link_targets)
    if orphan_count:
        findings.warnings.append(f"knowledge graph: {orphan_count} declared nodes have no inbound wikilink")
        findings.metrics["orphan_nodes"] = orphan_count


def normalize_link_aliases(path: Path, targets: set[str], alias_targets: dict[str, set[str]]) -> str:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)

    def replace(match: re.Match[str]) -> str:
        target = match.group(1)
        alias = resolve_link_alias(target, targets, alias_targets)
        if not alias:
            return match.group(0)
        heading = match.group(2) or ""
        label = match.group(3) or ""
        return f"[[{alias}{heading}{label}]]"

    in_fence = False
    for index, line in enumerate(lines):
        if re.match(r"^\s*(```|~~~)", line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        parts = re.split(r"(`[^`]*`)", line)
        for part_index in range(0, len(parts), 2):
            parts[part_index] = WIKILINK_FULL_RE.sub(replace, parts[part_index])
        lines[index] = "".join(parts)
    return "".join(lines)


def summarize_cross_project_links(findings: Findings) -> None:
    count = findings.metrics["cross_project_links"]
    if count:
        findings.warnings.append(f"cross-project links: {count} seetong references are outside this vault")


def print_report(findings: Findings, fixed: bool) -> None:
    print("MyAIWiki health report")
    print(f"Markdown files checked: {findings.metrics['markdown_files']}")
    print(f"Files with frontmatter: {findings.metrics['frontmatter_files']}")
    if fixed:
        print(f"Files normalized: {len(findings.changed_files)}")
    print(f"Errors: {len(findings.errors)}")
    print(f"Warnings: {len(findings.warnings)}")
    for name in ("invalid_inline_tags", "category_mismatch", "legacy_links", "frontmatter_missing", "alias_links", "unresolved_links", "missing_indexes", "missing_directory_indexes", "unindexed_pages", "orphan_nodes", "cross_project_links"):
        if findings.metrics[name]:
            print(f"{name}: {findings.metrics[name]}")
    if findings.unresolved_targets:
        print("Most frequent unresolved targets:")
        for target, count in findings.unresolved_targets.most_common(10):
            print(f"- [[{target}]]: {count}")
    for title, items in (("Errors", findings.errors), ("Warnings", findings.warnings)):
        if items:
            print(f"\n{title}:")
            for item in items[:80]:
                print(f"- {item}")
            if len(items) > 80:
                print(f"- ... {len(items) - 80} more")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit MyAIWiki structure and Obsidian tag syntax.")
    parser.add_argument("--fix", action="store_true", help="Normalize frontmatter tags and inline tag boundaries.")
    parser.add_argument("--fix-link-aliases", action="store_true", help="Rewrite only uniquely matched wiki-link aliases.")
    parser.add_argument("--fix-indexes", action="store_true", help="Append unindexed pages to each category's pending-summary section.")
    parser.add_argument("--strict", action="store_true", help="Return nonzero for warnings as well as errors.")
    args = parser.parse_args()

    changed_files: list[Path] = []
    if args.fix:
        for path in markdown_files(ROOT):
            original = path.read_text(encoding="utf-8")
            normalized = normalize_file(path)
            if normalized != original:
                path.write_text(normalized, encoding="utf-8")
                changed_files.append(path)

    findings = Findings(changed_files=changed_files)
    targets, stem_counts, title_counts, alias_targets = known_wiki_targets()
    if args.fix_link_aliases:
        for path in markdown_files(WIKI_DIR):
            original = path.read_text(encoding="utf-8")
            normalized = normalize_link_aliases(path, targets, alias_targets)
            if normalized != original:
                path.write_text(normalized, encoding="utf-8")
                changed_files.append(path)
    if args.fix_indexes:
        changed_files.extend(normalize_indexes())
    check_legacy_directories(findings)
    for path in markdown_files(ROOT):
        check_file(path, targets, stem_counts, title_counts, alias_targets, findings)
    check_index_coverage(findings)
    check_node_orphans(findings)
    summarize_cross_project_links(findings)
    print_report(findings, args.fix)
    return 1 if findings.errors or (args.strict and findings.warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
