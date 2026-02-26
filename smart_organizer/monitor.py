"""Real-time folder monitoring using watchdog (optional dependency)."""

from __future__ import annotations

import time
from pathlib import Path

from .organizer import SmartFileOrganizer


class NewFileHandler:
    def __init__(self, organizer: SmartFileOrganizer) -> None:
        self.organizer = organizer

    def on_created(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.exists():
            self.organizer.organize()


def monitor_folder(path: Path, organizer: SmartFileOrganizer) -> None:
    try:
        from watchdog.events import FileSystemEventHandler
        from watchdog.observers import Observer
    except ImportError as exc:
        raise RuntimeError("watchdog is required for --monitor mode. Install dependencies first.") from exc

    class _Handler(FileSystemEventHandler, NewFileHandler):
        pass

    observer = Observer()
    observer.schedule(_Handler(organizer), str(path), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
