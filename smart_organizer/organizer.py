"""Core file organization pipeline."""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path

from .config import CATEGORY_BY_EXTENSION, DEFAULT_TARGET_ROOT, MODEL_PATH
from .duplicates import detect_duplicates
from .ml import FilenameClassifier
from .search import FilenameSearchIndex, SearchResult


@dataclass
class OrganizationAction:
    source: Path
    destination: Path


class SmartFileOrganizer:
    def __init__(self, source_dir: Path, target_root: Path = DEFAULT_TARGET_ROOT) -> None:
        self.source_dir = source_dir
        self.target_root = target_root
        self.classifier = FilenameClassifier()
        self.search_index = FilenameSearchIndex()
        self.undo_log_path = self.target_root / "undo_log.json"

        if MODEL_PATH.exists():
            self.classifier.load(MODEL_PATH)
        else:
            self.classifier.train()
            self.classifier.save(MODEL_PATH)

    def _category_from_extension(self, file_path: Path) -> str | None:
        ext = file_path.suffix.lower()
        for category, ext_set in CATEGORY_BY_EXTENSION.items():
            if ext in ext_set:
                return category
        return None

    def _category_from_ai_name(self, file_path: Path) -> str | None:
        filename = file_path.stem.lower().replace("_", " ").replace("-", " ")
        return self.classifier.predict(filename)

    def classify(self, file_path: Path) -> str:
        return self._category_from_extension(file_path) or self._category_from_ai_name(file_path) or "others"

    def smart_rename(self, file_path: Path) -> str:
        stem = file_path.stem.lower().replace(" ", "_")
        stem = "_".join(filter(None, stem.split("_")))
        return f"{stem}{file_path.suffix.lower()}"

    def list_files(self) -> list[Path]:
        return [p for p in self.source_dir.iterdir() if p.is_file()]

    def detect_duplicates(self) -> dict[str, list[Path]]:
        return detect_duplicates(self.list_files())

    def organize(self) -> list[OrganizationAction]:
        self.target_root.mkdir(parents=True, exist_ok=True)
        actions: list[OrganizationAction] = []

        for file_path in self.list_files():
            category = self.classify(file_path)
            category_dir = self.target_root / category
            category_dir.mkdir(parents=True, exist_ok=True)
            new_name = self.smart_rename(file_path)
            destination = category_dir / new_name
            counter = 1
            while destination.exists():
                destination = category_dir / f"{destination.stem}_{counter}{destination.suffix}"
                counter += 1
            shutil.move(str(file_path), str(destination))
            actions.append(OrganizationAction(source=file_path, destination=destination))

        self._save_undo(actions)
        self.search_index.build([a.destination for a in actions])
        return actions

    def _save_undo(self, actions: list[OrganizationAction]) -> None:
        payload = [{"source": str(a.source), "destination": str(a.destination)} for a in actions]
        self.undo_log_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def undo_last(self) -> int:
        if not self.undo_log_path.exists():
            return 0
        payload = json.loads(self.undo_log_path.read_text(encoding="utf-8"))
        reverted = 0
        for item in payload:
            source = Path(item["source"])
            destination = Path(item["destination"])
            if destination.exists():
                source.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(destination), str(source))
                reverted += 1
        self.undo_log_path.unlink(missing_ok=True)
        return reverted

    def semantic_search(self, query: str, top_k: int = 5) -> list[SearchResult]:
        if not self.search_index.paths:
            files = [p for p in self.target_root.rglob("*") if p.is_file() and p.name != "undo_log.json"]
            self.search_index.build(files)
        return self.search_index.query(query, top_k=top_k)
