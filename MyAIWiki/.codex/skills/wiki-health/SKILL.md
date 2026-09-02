---
name: wiki-health
description: Audit and maintain the MyAIWiki knowledge base. Use when the user asks for a knowledge-base health check, directory or index consistency, Obsidian tag fixes, broken wiki-link checks, or a repeatable /lint workflow.
---

# Wiki Health

Run `python3 scripts/wiki-health-check.py` from the MyAIWiki root before reporting a health result.

Also run `python3 scripts/normalize_raw_archive.py --check` when auditing
directory consistency. The canonical raw archive is flat (`raw/{slug}.md` and
`raw/{slug}-digest.md`); only `inbox/`, `notes/`, `screenshots/`, and
`source-cache/` may be subdirectories. Use `--apply` only after its collision
check succeeds, because it moves legacy files and rewrites their textual
references.

Use `python3 scripts/wiki-health-check.py --fix` only for the two deterministic normalizations it supports:

- Convert frontmatter `tags` to a YAML list without `#` prefixes.
- Ensure taxonomy tags in Markdown prose have a whitespace boundary before `#`.

Use `--fix-link-aliases` only for wiki links that normalize to one existing page. Use `--fix-indexes` to add otherwise unindexed pages under each category's pending-summary section.

Keep the canonical wiki categories numbered: `01-ai-agents` through `07-rag-systems`. Migrate legacy aliases rather than creating another parallel category tree.

Treat unresolved links and pages absent from a category index as review findings. Do not delete or rewrite source content solely to silence the checker.

After any write, run the checker again and report the remaining errors separately from warnings.

For a newly ingested article, run `python3 scripts/wiki-health-check.py --scope <slug>` before publishing. Draft pages and raw sources without complete-body metadata are findings, not publishable content.
