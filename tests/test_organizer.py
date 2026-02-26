from pathlib import Path

from smart_organizer.organizer import SmartFileOrganizer


def test_organize_and_undo(tmp_path: Path):
    source = tmp_path / "source"
    target = tmp_path / "organized"
    source.mkdir()

    (source / "Resume Final.PDF").write_text("resume", encoding="utf-8")
    (source / "script.py").write_text("print('x')", encoding="utf-8")

    organizer = SmartFileOrganizer(source, target)
    actions = organizer.organize()

    assert len(actions) == 2
    assert any("documents" in str(a.destination) for a in actions)
    assert any("code" in str(a.destination) for a in actions)

    restored = organizer.undo_last()
    assert restored == 2
    assert (source / "Resume Final.PDF").exists()


def test_duplicate_detection(tmp_path: Path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "a.txt").write_text("same", encoding="utf-8")
    (source / "b.txt").write_text("same", encoding="utf-8")

    organizer = SmartFileOrganizer(source, tmp_path / "target")
    duplicates = organizer.detect_duplicates()

    assert len(duplicates) == 1
