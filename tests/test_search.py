from pathlib import Path

from smart_organizer.search import FilenameSearchIndex


def test_semantic_filename_search():
    index = FilenameSearchIndex()
    files = [Path("resume_nishit_final.pdf"), Path("holiday_photo.jpg"), Path("invoice_jan.pdf")]
    index.build(files)

    results = index.query("show my resume")
    assert results
    assert "resume" in results[0].path.name
