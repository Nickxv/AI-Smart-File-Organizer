"""Configuration and defaults for file organization."""

from pathlib import Path

CATEGORY_BY_EXTENSION = {
    "documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"},
    "images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"},
    "videos": {".mp4", ".mov", ".avi", ".mkv", ".webm"},
    "code": {".py", ".js", ".ts", ".java", ".cpp", ".c", ".go", ".rs", ".html", ".css", ".ipynb"},
    "archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
}

DEFAULT_TARGET_ROOT = Path("Organized")
MODEL_DIR = Path("data")
MODEL_PATH = MODEL_DIR / "filename_classifier.joblib"
