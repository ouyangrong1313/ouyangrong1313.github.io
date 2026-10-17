from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from build_wechat_raw import build_raw_markdown
from compile_wechat_to_wiki import build_wiki_markdown, compile_article, validate_published_wiki


ARTICLE = {
    "title": "测试文章",
    "author": "测试作者",
    "publish_time": "2026-09-02",
    "url": "https://mp.weixin.qq.com/s/example",
    "content_text": "这是第一段完整正文。\n\n这是第二段完整正文。",
    "fetch_mode": "isolated-chrome-cdp",
}


class WechatIngestContractTests(unittest.TestCase):
    def test_raw_keeps_complete_content_and_fetch_metadata(self) -> None:
        raw = build_raw_markdown(ARTICLE)

        self.assertIn("这是第一段完整正文。", raw)
        self.assertIn("这是第二段完整正文。", raw)
        self.assertIn("**抓取方式：** isolated-chrome-cdp", raw)

    def test_empty_content_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            build_raw_markdown({**ARTICLE, "content_text": ""})

    def test_draft_wiki_has_publish_contract_fields(self) -> None:
        wiki = build_wiki_markdown(ARTICLE, "#主题/AI-Coding", "02-ai-coding")

        self.assertTrue(wiki.startswith("---\n"))
        self.assertIn("status: draft", wiki)
        self.assertIn("nodes:", wiki)
        self.assertIn("links:", wiki)
        self.assertIn("## 关联图谱", wiki)

    def test_published_wiki_requires_real_links_and_graph_sections(self) -> None:
        draft = build_wiki_markdown(ARTICLE, "#主题/AI-Coding", "02-ai-coding")
        with self.assertRaises(ValueError):
            validate_published_wiki(draft)

        published = draft.replace("links: []", "links: [[02-ai-coding/existing]]").replace("status: draft", "status: published")
        self.assertIsNone(validate_published_wiki(published))
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            target = root / "wiki" / "02-ai-coding" / "existing.md"
            target.parent.mkdir(parents=True)
            target.write_text("# Existing\n", encoding="utf-8")
            self.assertIsNone(validate_published_wiki(published, root))
            with self.assertRaises(ValueError):
                validate_published_wiki(published.replace("existing", "missing"), root)

    def test_draft_ingest_does_not_publish_indexes_or_log(self) -> None:
        with TemporaryDirectory() as temp_dir, patch("compile_wechat_to_wiki.fetch_article", return_value=ARTICLE):
            root = Path(temp_dir)
            paths, statuses = compile_article(
                ARTICLE["url"], root, "02-ai-coding", "test-article", None, False
            )

            self.assertTrue(paths.raw.exists())
            self.assertTrue(paths.wiki.exists())
            self.assertEqual(statuses["state"], "drafted")
            self.assertEqual(statuses["category_index"], "pending_publish")
            self.assertFalse(paths.category_index.exists())
            self.assertFalse(paths.master_index.exists())
            self.assertFalse(paths.log.exists())
