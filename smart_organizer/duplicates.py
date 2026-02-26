"""Duplicate file detection based on SHA256 hash."""

from __future__ import annotations

import hashlib
from pathlib import Path


def file_hash(path: Path, chunk_size: int = 8192) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            hasher.update(chunk)
    return hasher.hexdigest()


def detect_duplicates(paths: list[Path]) -> dict[str, list[Path]]:
    hash_map: dict[str, list[Path]] = {}
    for path in paths:
        if not path.is_file():
            continue
        digest = file_hash(path)
        hash_map.setdefault(digest, []).append(path)
    return {digest: files for digest, files in hash_map.items() if len(files) > 1}
