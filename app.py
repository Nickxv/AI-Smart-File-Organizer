from pathlib import Path

import streamlit as st

from smart_organizer.organizer import SmartFileOrganizer

st.set_page_config(page_title="AI Smart File Organizer", layout="wide")
st.title("📂 AI Smart File Organizer")
st.caption("Auto-categorize files, detect duplicates, and semantic search.")

source_path_input = st.text_input("Folder to organize", value=str(Path.home() / "Downloads"))
target_path_input = st.text_input("Target folder", value="Organized")

if source_path_input:
    organizer = SmartFileOrganizer(Path(source_path_input), Path(target_path_input))

    col1, col2, col3 = st.columns(3)
    if col1.button("Organize now"):
        actions = organizer.organize()
        st.success(f"Moved {len(actions)} file(s).")
        st.dataframe(
            [{"from": str(a.source), "to": str(a.destination)} for a in actions], use_container_width=True
        )

    if col2.button("Detect duplicates"):
        dups = organizer.detect_duplicates()
        if not dups:
            st.info("No duplicates found.")
        else:
            for digest, files in dups.items():
                st.write(f"Hash: `{digest[:12]}...`")
                st.write([str(f) for f in files])

    if col3.button("Undo last organization"):
        count = organizer.undo_last()
        st.warning(f"Restored {count} file(s).")

    st.subheader("Semantic Search")
    query = st.text_input("Search query", value="show my resume")
    if st.button("Search"):
        results = organizer.semantic_search(query)
        if results:
            st.table([{"file": str(r.path), "score": round(r.score, 3)} for r in results])
        else:
            st.info("No matching files found.")
