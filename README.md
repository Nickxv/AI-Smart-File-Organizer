# AI Smart File Organizer + Local AI Chat Suite

This repository now includes two separate AI assistant experiences built with Python:

1. **Desktop Application** (Tkinter): local chat-style app for basic solutions, coding help, summarization, and planning.
2. **Website Application** (Flask + HTML/CSS/JS): browser-based chat interface with REST endpoints.

The original smart file organizer modules are still present.

## Features

### AI Assistant (new)
- Chat interface similar to a lightweight ChatGPT/Gemini workflow
- Basic Q&A assistance
- Small Python code drafting support
- Debugging checklists
- Summarization and planning prompts
- Conversation history + clear chat

### Smart File Organizer (existing)
- Monitor a folder with `watchdog`
- Auto-classify files and move into organized folders
- Duplicate detection using SHA256
- Semantic-ish filename search

## Project Structure

- `desktop_chat_app.py`: Desktop chat application (Tkinter)
- `web_chat/server.py`: Flask server for web chat
- `web_chat/templates/index.html`: Web UI template
- `web_chat/static/styles.css`: Web UI styling
- `web_chat/static/app.js`: Web chat frontend logic
- `ai_assistant/core.py`: Reusable local assistant engine
- `smart_organizer/*`: File organizer modules

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the Desktop App (separate app)

```bash
python desktop_chat_app.py
```

## Run the Website (separate app)

```bash
python web_chat/server.py
```

Then open: `http://localhost:5001`

## Run Tests

```bash
pytest -q
```

## Existing Organizer Usage

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
