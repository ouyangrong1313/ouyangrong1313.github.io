#!/usr/bin/env python3
"""
One-stop WeChat article ingest entry for MyAIWiki.

This wraps the existing steps:
1. fetch and compile a WeChat article into raw/digest/wiki/index/log drafts
2. optionally build a polish prompt for Codex/Claude
3. optionally apply polished digest/wiki output back into the knowledge base

Usage:
  python3 scripts/ingest_wechat_article.py <url>
  python3 scripts/ingest_wechat_article.py <url> --polish-prompt-output /tmp/prompt.md
  python3 scripts/ingest_wechat_article.py <url> --apply-polish-output /tmp/model-output.md
"""

from __future__ import annotations

import argparse
from pathlib import Path

from apply_wechat_polish_output import extract_markdown_blocks, read_input
from build_wechat_polish_prompt import build_prompt
from compile_wechat_to_wiki import compile_article


def apply_polish_output(
    *,
    slug: str,
    category: str,
    output_root: Path,
    input_path: str,
) -> tuple[Path, Path]:
    text = read_input(input_path)
    digest_markdown, wiki_markdown = extract_markdown_blocks(text)

    digest_path = output_root / "raw" / f"{slug}-digest.md"
    wiki_path = output_root / "wiki" / category / f"{slug}.md"
    digest_path.parent.mkdir(parents=True, exist_ok=True)
    wiki_path.parent.mkdir(parents=True, exist_ok=True)
    digest_path.write_text(digest_markdown, encoding="utf-8")
    wiki_path.write_text(wiki_markdown, encoding="utf-8")
    return digest_path, wiki_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="One-stop WeChat article ingest entry for MyAIWiki."
    )
    parser.add_argument("url", help="WeChat article URL")
    parser.add_argument(
        "--category",
        default="02-ai-coding",
        help="Wiki category directory, default: 02-ai-coding",
    )
    parser.add_argument("--slug", help="Optional output slug")
    parser.add_argument("--tags", help="Optional tag string")
    parser.add_argument(
        "--output-root",
        default=str(Path(__file__).resolve().parent.parent),
        help="Root directory of the target MyAIWiki",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing raw/digest/wiki draft files during compile",
    )
    parser.add_argument(
        "--skip-polish-prompt",
        action="store_true",
        help="Skip generating the polish prompt artifact",
    )
    parser.add_argument(
        "--polish-prompt-output",
        help="Optional output file path for the generated polish prompt",
    )
    parser.add_argument(
        "--apply-polish-output",
        help="Optional file path containing the model's two markdown blocks to apply back",
    )
    args = parser.parse_args()

    output_root = Path(args.output_root).expanduser().resolve()
    paths, statuses = compile_article(
        url=args.url,
        root=output_root,
        category=args.category,
        slug=args.slug,
        tags=args.tags,
        force=args.force,
    )

    for name in ("raw", "digest", "wiki", "category_index", "master_index", "log"):
        print(f"{name}: {statuses[name]} -> {getattr(paths, name)}")

    prompt_path = None
    if not args.skip_polish_prompt:
        prompt = build_prompt(paths.raw.stem, args.category, root=output_root)
        if args.polish_prompt_output:
            prompt_path = Path(args.polish_prompt_output).expanduser()
        else:
            prompt_path = output_root / "raw" / f"{paths.raw.stem}-polish-prompt.md"
        prompt_path.parent.mkdir(parents=True, exist_ok=True)
        prompt_path.write_text(prompt, encoding="utf-8")
        print(f"polish_prompt: written -> {prompt_path}")

    if args.apply_polish_output:
        digest_path, wiki_path = apply_polish_output(
            slug=paths.raw.stem,
            category=args.category,
            output_root=output_root,
            input_path=args.apply_polish_output,
        )
        print(f"apply_polish_digest: written -> {digest_path}")
        print(f"apply_polish_wiki: written -> {wiki_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
