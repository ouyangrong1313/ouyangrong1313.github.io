"""Durable, credential-free state for a single wiki ingest."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


class StateTransitionError(ValueError):
    pass


ALLOWED_TRANSITIONS = {
    "fetched": {"drafted", "failed"},
    "drafted": {"polished", "failed"},
    "polished": {"validated", "failed"},
    "validated": {"published", "failed"},
    "published": {"fetched"},
    "failed": {"fetched"},
}


def normalize_url(url: str) -> str:
    parsed = urlsplit(url.strip())
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), parsed.path, parsed.query, ""))


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class IngestStateStore:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.ingests = root / ".wiki-state" / "ingests"

    def state_id(self, url: str) -> str:
        return hashlib.sha256(normalize_url(url).encode("utf-8")).hexdigest()[:16]

    def path_for(self, record_id: str) -> Path:
        return self.ingests / f"{record_id}.json"

    def read(self, record_id: str) -> dict:
        return json.loads(self.path_for(record_id).read_text(encoding="utf-8"))

    def find_by_artifact(self, relative_path: str) -> dict | None:
        if not self.ingests.exists():
            return None
        for path in self.ingests.glob("*.json"):
            record = json.loads(path.read_text(encoding="utf-8"))
            if relative_path in record.get("artifacts", {}).values():
                return record
        return None

    def _write(self, record: dict) -> dict:
        self.ingests.mkdir(parents=True, exist_ok=True)
        path = self.path_for(record["id"])
        temporary = path.with_suffix(".tmp")
        temporary.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temporary.replace(path)
        return record

    def start(self, url: str) -> dict:
        normalized = normalize_url(url)
        record_id = self.state_id(normalized)
        path = self.path_for(record_id)
        if path.exists():
            record = self.read(record_id)
            if record["status"] == "failed":
                record["status"] = "fetched"
                record["updated_at"] = utc_now()
                record["error"] = None
                return self._write(record)
            return record
        now = utc_now()
        return self._write({
            "id": record_id,
            "url": normalized,
            "status": "fetched",
            "created_at": now,
            "updated_at": now,
            "artifacts": {},
            "content_sha256": None,
            "error": None,
        })

    def transition(self, record_id: str, status: str, *, artifacts: dict | None = None, content_sha256: str | None = None, error: str | None = None) -> dict:
        record = self.read(record_id)
        current = record["status"]
        if status != current and status not in ALLOWED_TRANSITIONS.get(current, set()):
            raise StateTransitionError(f"Cannot transition {current!r} -> {status!r}")
        record["status"] = status
        record["updated_at"] = utc_now()
        if artifacts:
            record["artifacts"].update(artifacts)
        if content_sha256 is not None:
            record["content_sha256"] = content_sha256
        record["error"] = error
        return self._write(record)
