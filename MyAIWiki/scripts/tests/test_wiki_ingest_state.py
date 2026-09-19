from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from wiki_ingest_state import IngestStateStore, StateTransitionError


class IngestStateStoreTests(unittest.TestCase):
    def test_lifecycle_is_persisted_and_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = IngestStateStore(Path(temp_dir))
            record = store.start("https://mp.weixin.qq.com/s/example")

            self.assertEqual(record["status"], "fetched")
            self.assertEqual(store.start("https://mp.weixin.qq.com/s/example")["id"], record["id"])

            store.transition(record["id"], "drafted", artifacts={"raw": "raw/example.md"})
            store.transition(record["id"], "polished")
            store.transition(record["id"], "validated")
            published = store.transition(record["id"], "published")
            self.assertEqual(published["status"], "published")
            self.assertEqual(store.read(record["id"])["artifacts"]["raw"], "raw/example.md")

    def test_invalid_transition_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = IngestStateStore(Path(temp_dir))
            record = store.start("https://mp.weixin.qq.com/s/example")

            with self.assertRaises(StateTransitionError):
                store.transition(record["id"], "published")
