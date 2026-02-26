# AI Smart File Organizer

An AI-powered file organizer that cleans messy Downloads/Desktop folders by automatically classifying, renaming, deduplicating, and enabling semantic file search.

## Features

### Core
- Monitor a folder (Downloads/Desktop) with `watchdog`
- Auto-classify files into Documents, Images, Videos, Code, Archives
- Move files into proper folders
- Detect duplicates using SHA256 hash
- Simple + semantic-ish search over file names

### Advanced
- AI filename understanding with TF-IDF + Logistic Regression
- Auto smart renaming (`My Resume Final.pdf` -> `my_resume_final.pdf`)
- Undo last organization action
- Real-time monitoring
- Streamlit dashboard

## Project Structure

- `main.py`: CLI interface
- `app.py`: Streamlit dashboard
- `smart_organizer/organizer.py`: Core orchestration
- `smart_organizer/ml.py`: Filename classifier
- `smart_organizer/duplicates.py`: Hash-based duplicate detection
- `smart_organizer/search.py`: Semantic search index
- `smart_organizer/monitor.py`: Watchdog monitoring loop

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Organize once
```bash
python main.py ~/Downloads --target Organized --organize
```

### Monitor in real time
```bash
python main.py ~/Downloads --target Organized --monitor
```

### Detect duplicates
```bash
python main.py ~/Downloads --duplicates
```

### Semantic search
```bash
python main.py ~/Downloads --target Organized --search "show my resume"
```

### Undo last organize
```bash
python main.py ~/Downloads --target Organized --undo
```

### Streamlit GUI
```bash
streamlit run app.py
```

## 4-Week Build Plan Alignment

- Week 1: Rule-based extension sorting + folder creation
- Week 2: AI filename classifier with TF-IDF + Logistic Regression
- Week 3: Duplicate detection + Streamlit dashboard
- Week 4: Real-time monitoring + semantic search + undo feature
