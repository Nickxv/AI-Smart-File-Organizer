"""Semantic-ish search over filenames using cosine similarity."""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SearchResult:
    path: Path
    score: float


class FilenameSearchIndex:
    def __init__(self) -> None:
        self.paths: list[Path] = []
        self.vectors: list[Counter] = []

    @staticmethod
    def _tokens(text: str) -> list[str]:
        return [t for t in text.lower().replace("-", " ").replace("_", " ").split() if t]

    @staticmethod
    def _cosine(a: Counter, b: Counter) -> float:
        common = set(a) & set(b)
        dot = sum(a[k] * b[k] for k in common)
        norm_a = math.sqrt(sum(v * v for v in a.values()))
        norm_b = math.sqrt(sum(v * v for v in b.values()))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    def build(self, file_paths: list[Path]) -> None:
        self.paths = file_paths
        self.vectors = [Counter(self._tokens(p.stem)) for p in file_paths]

    def query(self, text: str, top_k: int = 5) -> list[SearchResult]:
        if not self.paths:
            return []
        q = Counter(self._tokens(text))
        scores = [self._cosine(q, v) for v in self.vectors]
        ranking = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:top_k]
        return [SearchResult(path=self.paths[i], score=s) for i, s in ranking if s > 0]
