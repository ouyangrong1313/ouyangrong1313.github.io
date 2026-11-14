#!/usr/bin/env python3
"""Normalize MyAIWiki raw archive paths without losing source material.

The canonical layout is flat for archived source/digest pairs:

    raw/{slug}.md
    raw/{slug}-digest.md

Only ``raw/inbox/``, ``raw/notes/``, ``raw/screenshots/`` and
``raw/source-cache/`` are retained as purpose-specific subdirectories.
Historical date folders and ``articles/`` are flattened, while leading
YYYY-MM or YYYY-MM-DD filename prefixes are removed. Dates remain in each
document's metadata instead of the path.

Usage:
  python3 scripts/normalize_raw_archive.py --check
  python3 scripts/normalize_raw_archive.py --apply
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "raw"
TEXT_SUFFIXES = {".md", ".py", ".json", ".yaml", ".yml", ".txt"}
RESERVED_RAW_DIRS = {"inbox", "notes", "screenshots", "source-cache"}
DATE_PREFIX_RE = re.compile(r"^\d{4}-\d{2}(?:-\d{2})?[-_]+")
POLISH_PROMPT_SUFFIX = "-polish-prompt.md"


@dataclass(frozen=True)
class Move:
    source: Path
    target: Path

    @property
    def source_ref(self) -> str:
        return self.source.relative_to(ROOT).as_posix()

    @property
    def target_ref(self) -> str:
        return self.target.relative_to(ROOT).as_posix()


def canonical_name(path: Path) -> str:
    return DATE_PREFIX_RE.sub("", path.name)


def is_archive_file(path: Path) -> bool:
    relative = path.relative_to(RAW_DIR)
    return not relative.parts or relative.parts[0] not in RESERVED_RAW_DIRS


def collect_moves() -> list[Move]:
    moves = []
    for source in sorted(RAW_DIR.rglob("*.md")):
        if not is_archive_file(source):
            continue
        if source.name.endswith(POLISH_PROMPT_SUFFIX):
            target = ROOT / "prompts" / "generated" / source.name
        else:
            target = RAW_DIR / canonical_name(source)
        if source != target:
            moves.append(Move(source=source, target=target))
    return moves


def find_conflicts(moves: list[Move]) -> list[str]:
    conflicts = []
    sources = {move.source for move in moves}
    targets: dict[Path, list[Path]] = {}
    for move in moves:
        targets.setdefault(move.target, []).append(move.source)

    for target, sources_for_target in sorted(targets.items()):
        if len(sources_for_target) > 1:
            rendered = ", ".join(str(path.relative_to(ROOT)) for path in sources_for_target)
            conflicts.append(f"multiple sources map to {target.relative_to(ROOT)}: {rendered}")
        elif target.exists() and target not in sources:
            conflicts.append(
                f"target already exists: {target.relative_to(ROOT)} "
                f"(from {sources_for_target[0].relative_to(ROOT)})"
            )
    return conflicts


def rewrite_references(moves: list[Move]) -> int:
    replacements: dict[str, str] = {}
    for move in moves:
        replacements[move.source_ref] = move.target_ref
        replacements[move.source_ref.removesuffix(".md")] = move.target_ref.removesuffix(".md")

    ordered_replacements = sorted(replacements.items(), key=lambda item: len(item[0]), reverse=True)
    changed_files = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        relative_parts = path.relative_to(ROOT).parts
        if ".git" in relative_parts or ".obsidian" in relative_parts or "__pycache__" in relative_parts:
            continue
        text = path.read_text(encoding="utf-8")
        updated = text
        for source_ref, target_ref in ordered_replacements:
            updated = updated.replace(source_ref, target_ref)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed_files += 1
    return changed_files


def pair_summary() -> tuple[int, int]:
    source_stems = set()
    digest_stems = set()
    for path in RAW_DIR.glob("*.md"):
        if path.name.endswith("-polish-prompt.md"):
            continue
        if path.name.endswith("-digest.md"):
            digest_stems.add(path.name.removesuffix("-digest.md"))
        else:
            source_stems.add(path.stem)
    return len(source_stems - digest_stems), len(digest_stems - source_stems)


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize MyAIWiki raw archive paths.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Report planned moves without writing.")
    mode.add_argument("--apply", action="store_true", help="Move files and rewrite textual references.")
    args = parser.parse_args()

    moves = collect_moves()
    conflicts = find_conflicts(moves)
    print(f"Archive files needing normalization: {len(moves)}")
    for move in moves:
        print(f"- {move.source_ref} -> {move.target_ref}")

    if conflicts:
        print("Conflicts:")
        for conflict in conflicts:
            print(f"- {conflict}")
        return 1

    if args.check:
        return 0

    for move in moves:
        move.target.parent.mkdir(parents=True, exist_ok=True)
        move.source.rename(move.target)

    reference_files = rewrite_references(moves)
    for directory in sorted(RAW_DIR.rglob("*"), reverse=True):
        if (
            directory.is_dir()
            and directory.parent == RAW_DIR
            and directory.name in RESERVED_RAW_DIRS
        ):
            continue
        if directory.is_dir() and not any(directory.iterdir()):
            directory.rmdir()

    sources_without_digest, digests_without_source = pair_summary()
    print(f"Moved files: {len(moves)}")
    print(f"Reference files updated: {reference_files}")
    print(f"Sources without digest: {sources_without_digest}")
    print(f"Digests without source: {digests_without_source}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
