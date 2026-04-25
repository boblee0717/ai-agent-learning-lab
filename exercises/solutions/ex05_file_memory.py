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
        # Atomic write that works on Windows, macOS, and Linux:
        # write to a sibling temp file, fsync, then atomically rename. On
        # any failure we clean the temp file up so it does not litter the
        # directory (Windows is especially unhappy with stray temp files).
        tmp = tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=self.path.parent,
            delete=False,
            newline="\n",
        )
        tmp_path = tmp.name
        try:
            try:
                json.dump(data, tmp, ensure_ascii=False, indent=2)
                tmp.flush()
                os.fsync(tmp.fileno())
            finally:
                tmp.close()
            os.replace(tmp_path, self.path)
        except Exception:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise

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
