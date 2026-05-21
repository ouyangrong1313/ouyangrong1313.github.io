#!/usr/bin/env python3
"""
Apply polished digest/wiki markdown blocks back into MyAIWiki files.

Usage:
  python3 scripts/apply_wechat_polish_output.py --slug my-article --input /path/to/output.md
  python3 scripts/apply_wechat_polish_output.py --slug my-article --category 02-ai-coding < output.md
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent


def read_input(input_path: str | None) -> str:
    if input_path:
        return Path(input_path).expanduser().read_text(encoding="utf-8")
    return sys.stdin.read()


def extract_markdown_blocks(text: str) -> tuple[str, str]:
    pattern = re.compile(r"```(?:markdown)?\s*\n(.*?)```", re.DOTALL)
    blocks = [match.strip() + "\n" for match in pattern.findall(text)]
    if len(blocks) != 2:
        raise ValueError(
            "Expected exactly 2 markdown code blocks: first digest, second wiki."
        )
    return blocks[0], blocks[1]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Apply polished digest/wiki markdown blocks back into MyAIWiki files."
    )
    parser.add_argument("--slug", required=True, help="Article slug")
    parser.add_argument(
        "--category",
        default="02-ai-coding",
        help="Wiki category directory, default: 02-ai-coding",
    )
    parser.add_argument(
        "--input",
        help="Optional file path containing the model output. If omitted, read from stdin.",
    )
    parser.add_argument(
        "--output-root",
        default=str(ROOT),
        help="Root directory of the target MyAIWiki, default: current repo root",
    )
    args = parser.parse_args()

    text = read_input(args.input)
    digest_markdown, wiki_markdown = extract_markdown_blocks(text)

    root = Path(args.output_root).expanduser().resolve()
    digest_path = root / "raw" / f"{args.slug}-digest.md"
    wiki_path = root / "wiki" / args.category / f"{args.slug}.md"

    digest_path.parent.mkdir(parents=True, exist_ok=True)
    wiki_path.parent.mkdir(parents=True, exist_ok=True)
    digest_path.write_text(digest_markdown, encoding="utf-8")
    wiki_path.write_text(wiki_markdown, encoding="utf-8")

    print(f"digest -> {digest_path}")
    print(f"wiki -> {wiki_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
