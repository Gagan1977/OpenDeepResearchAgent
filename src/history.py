import json
import os

HISTORY_FILE = "history.json"


def load_history() -> list:
    """Reads history from file. Returns empty list if file doesn't exist or is empty."""
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            return []
        return json.loads(content)


def save_to_history(question: str):
    """Adds a new question to the top of the history list."""
    history = load_history()

    if question in history:
        history.remove(question)

    history.insert(0, question)
    history = history[:20]

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)