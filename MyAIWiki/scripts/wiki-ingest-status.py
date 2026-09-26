#!/usr/bin/env python3
"""Show a recoverable ingest state for a source URL or article slug."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from wiki_ingest_state import IngestStateStore


ROOT = Path(__file__).resolve().parent.parent


def next_command(record: dict) -> str:
    artifact = record.get("artifacts", {}).get("wiki", "")
    slug = Path(artifact).stem if artifact else "<slug>"
    category = Path(artifact).parts[1] if len(Path(artifact).parts) > 2 else "<category>"
    status = record["status"]
    if status == "drafted":
        return f"python3 scripts/build_wechat_polish_prompt.py --slug {slug} --category {category}"
    if status == "polished":
        return f"python3 scripts/ingest_wechat_article.py <url> --category {category} --apply-polish-output <file>"
    if status == "validated":
        return f"python3 scripts/compile_wechat_to_wiki.py <url> --category {category}"
    if status == "failed":
        return "Rerun the original ingest command after fixing the reported retrieval or contract error."
    return "No action required."


def main() -> int:
    parser = argparse.ArgumentParser(description="Show a MyAIWiki ingest lifecycle record.")
    parser.add_argument("source", help="Original URL or article slug")
    args = parser.parse_args()
    store = IngestStateStore(ROOT)
    if args.source.startswith(("http://", "https://")):
        record = store.read(store.state_id(args.source))
    else:
        record = next((item for path in store.ingests.glob("*.json") if (item := store.read(path.stem)) and args.source in item.get("artifacts", {}).get("wiki", "")), None)
        if not record:
            raise SystemExit(f"No ingest state found for: {args.source}")
    print(json.dumps({**record, "next_command": next_command(record)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
