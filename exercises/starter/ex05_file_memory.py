"""Exercise 05 — A file-backed Memory implementation."""

from __future__ import annotations

from pathlib import Path


class FileStore:
    """Persist facts to a JSON file. Satisfies the ``Memory`` protocol."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        # TODO: ensure self.path's parent directory exists; create the file
        # with an empty dict ``{}`` if it does not exist yet.
        raise NotImplementedError

    def remember(self, key: str, value: str) -> None:
        # TODO:
        # 1) load the current dict from self.path (use ``json.loads``).
        # 2) update it with ``{key.strip().lower(): value.strip()}``.
        # 3) write it back atomically (write to a temp file, then os.replace).
        raise NotImplementedError

    def recall(self, query: str) -> list[str]:
        # TODO: load the dict, then return ["key: value", ...] for entries
        # whose key appears in ``query`` (case-insensitive) OR whose value's
        # words appear in ``query``. See InMemoryStore.recall for inspiration.
        raise NotImplementedError

    def all(self) -> dict[str, str]:
        # TODO: load and return the full dict.
        raise NotImplementedError
