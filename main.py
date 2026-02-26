"""CLI entrypoint for AI Smart File Organizer."""

from __future__ import annotations

import argparse
from pathlib import Path

from smart_organizer.monitor import monitor_folder
from smart_organizer.organizer import SmartFileOrganizer


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AI Smart File Organizer")
    parser.add_argument("source", type=Path, help="Folder to monitor/organize")
    parser.add_argument("--target", type=Path, default=Path("Organized"), help="Target root for categories")
    parser.add_argument("--organize", action="store_true", help="Run one-time organization")
    parser.add_argument("--monitor", action="store_true", help="Run real-time monitoring")
    parser.add_argument("--duplicates", action="store_true", help="Print duplicate file groups")
    parser.add_argument("--search", type=str, help="Semantic search query")
    parser.add_argument("--undo", action="store_true", help="Undo last organization")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    organizer = SmartFileOrganizer(args.source, args.target)

    if args.organize:
        actions = organizer.organize()
        print(f"Moved {len(actions)} files.")

    if args.duplicates:
        duplicates = organizer.detect_duplicates()
        print(duplicates)

    if args.search:
        results = organizer.semantic_search(args.search)
        print([{"file": str(r.path), "score": r.score} for r in results])

    if args.undo:
        print(f"Restored {organizer.undo_last()} files")

    if args.monitor:
        monitor_folder(args.source, organizer)


if __name__ == "__main__":
    main()
