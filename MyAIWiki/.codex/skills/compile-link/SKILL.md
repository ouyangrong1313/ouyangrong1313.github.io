---
name: compile-link
description: Ingest a web article into MyAIWiki as raw source, digest, wiki page, category index, master index, and log entry. Use when the user provides a URL and asks to compile, archive, save, ingest, or add it to the knowledge base.
---

# Compile Link

Read `prompts/compile-link-skill.md` for the content and quality contract.

For WeChat URLs, preflight the source before compiling:

```bash
python3 scripts/fetch_wechat_article.py <url> --pretty
```

The fetcher attempts Playwright, then a temporary isolated Chrome profile through DevTools, then direct HTML. Do not use a personal browser profile or WeChat local/chat data. A page containing `环境异常`, an empty title, or empty article text is a retrieval failure: do not fabricate an archive; ask for source text or an accessible mirror.

Use the existing ingest entry point only after the preflight succeeds. This produces a `drafted` raw/digest/wiki set; it does not publish indexes or log entries:

```bash
python3 scripts/ingest_wechat_article.py <url> --category <numbered-category>
```

Use only the numbered wiki categories. Do not default an uncertain category without evidence from the source; ask only when the classification materially affects the result.

Polish the draft into a `status: published` wiki page with real links and the three graph sections, then apply it through the ingest entry point. Publication updates indexes and the log only after the page contract is valid:

```bash
python3 scripts/ingest_wechat_article.py <url> --category <numbered-category> --apply-polish-output <model-output.md>
python3 scripts/wiki-health-check.py --scope <slug>
```

Use `python3 scripts/wiki-ingest-status.py <url-or-slug>` to inspect an interrupted ingest. Resolve errors before reporting completion. Treat remaining warnings as explicit content or graph debt, not as a reason to invent links or metadata.
