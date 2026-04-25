"""Reference solution for Exercise 05 — File-backed memory."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path


class FileStore:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write({})

    def _read(self) -> dict[str, str]:
        try:
            return json.loads(self.path.read_text(encoding="utf-8") or "{}")
        except json.JSONDecodeError:
            return {}

    def _write(self, data: dict[str, str]) -> None:
        # Atomic write: temp file in the same directory + os.replace.
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=self.path.parent,
            delete=False,
        ) as tmp:
            json.dump(data, tmp, ensure_ascii=False, indent=2)
            tmp_path = tmp.name
        os.replace(tmp_path, self.path)

    def remember(self, key: str, value: str) -> None:
        data = self._read()
        data[key.strip().lower()] = value.strip()
        self._write(data)

    def recall(self, query: str) -> list[str]:
        q = query.lower()
        return [
            f"{k}: {v}"
            for k, v in self._read().items()
            if k in q or any(token and token in q for token in v.lower().split())
        ]

    def all(self) -> dict[str, str]:
        return self._read()
