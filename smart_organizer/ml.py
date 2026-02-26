"""Lightweight filename understanding model."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


@dataclass
class FilenameClassifier:
    """A tiny bag-of-words classifier inspired by TF-IDF pipelines."""

    label_word_counts: dict[str, Counter] | None = None

    @staticmethod
    def default_training_rows() -> list[tuple[str, str]]:
        return [
            ("resume_final", "documents"),
            ("invoice_january", "documents"),
            ("project_notes_ml", "documents"),
            ("family_trip_photo", "images"),
            ("profile_pic", "images"),
            ("vacation_video", "videos"),
            ("lecture_recording", "videos"),
            ("main_app_py", "code"),
            ("frontend_component", "code"),
            ("backup_archive", "archives"),
            ("dataset_zip", "archives"),
        ]

    @staticmethod
    def _tokens(text: str) -> list[str]:
        return [t for t in text.lower().replace("-", " ").replace("_", " ").split() if t]

    def train(self, training_data: list[tuple[str, str]] | None = None) -> None:
        rows = training_data if training_data is not None else self.default_training_rows()
        bag: dict[str, Counter] = defaultdict(Counter)
        for filename, label in rows:
            bag[label].update(self._tokens(filename))
        self.label_word_counts = dict(bag)

    def predict(self, filename: str) -> str | None:
        if not self.label_word_counts:
            return None
        tokens = self._tokens(filename)
        best_label = None
        best_score = 0
        for label, counts in self.label_word_counts.items():
            score = sum(counts[token] for token in tokens)
            if score > best_score:
                best_label = label
                best_score = score
        return best_label

    def save(self, path: Path) -> None:
        if self.label_word_counts is None:
            raise ValueError("Model is not trained.")
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {label: dict(counter) for label, counter in self.label_word_counts.items()}
        path.write_text(json.dumps(payload), encoding="utf-8")

    def load(self, path: Path) -> None:
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.label_word_counts = {label: Counter(words) for label, words in payload.items()}
