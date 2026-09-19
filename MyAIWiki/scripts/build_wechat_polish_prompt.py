#!/usr/bin/env python3
"""
Build a polish prompt for a compiled WeChat article.

This reads the existing raw, digest draft, and wiki draft, then packages them
into a single prompt that can be pasted into Codex or Claude for refinement.

Usage:
  python3 scripts/build_wechat_polish_prompt.py --slug my-article
  python3 scripts/build_wechat_polish_prompt.py --slug my-article --category 02-ai-coding
  python3 scripts/build_wechat_polish_prompt.py --slug my-article --output /tmp/prompt.md
"""

from __future__ import annotations

import argparse
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
PROMPT_TEMPLATE = ROOT / "prompts" / "wechat-compile-polish.md"


def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    return path.read_text(encoding="utf-8").strip()


def build_prompt(slug: str, category: str, root: Path = ROOT) -> str:
    template = read_text(PROMPT_TEMPLATE)
    raw_path = root / "raw" / f"{slug}.md"
    digest_path = root / "raw" / f"{slug}-digest.md"
    wiki_path = root / "wiki" / category / f"{slug}.md"

    raw_text = read_text(raw_path)
    digest_text = read_text(digest_path)
    wiki_text = read_text(wiki_path)

    sections = [
        template,
        "",
        "---",
        "",
        "## 输入材料",
        "",
        f"### raw/{slug}.md",
        "",
        "```markdown",
        raw_text,
        "```",
        "",
        f"### raw/{slug}-digest.md",
        "",
        "```markdown",
        digest_text,
        "```",
        "",
        f"### wiki/{category}/{slug}.md",
        "",
        "```markdown",
        wiki_text,
        "```",
    ]
    return "\n".join(sections).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a polish prompt for a compiled WeChat article."
    )
    parser.add_argument("--slug", required=True, help="Article slug")
    parser.add_argument(
        "--category",
        default="02-ai-coding",
        help="Wiki category directory, default: 02-ai-coding",
    )
    parser.add_argument(
        "--output",
        help="Optional output file path. If omitted, prints the prompt to stdout.",
    )
    args = parser.parse_args()

    prompt = build_prompt(args.slug, args.category)
    if args.output:
        output_path = Path(args.output).expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(prompt, encoding="utf-8")
        print(str(output_path))
        return 0

    print(prompt, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
