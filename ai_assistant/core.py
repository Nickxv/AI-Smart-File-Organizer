from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import re
from typing import List


@dataclass
class ChatMessage:
    role: str
    content: str
    timestamp: str


class AssistantEngine:
    """A lightweight local assistant engine for basic Q&A and code drafting."""

    def __init__(self) -> None:
        self.history: List[ChatMessage] = []

    def _append(self, role: str, content: str) -> None:
        self.history.append(
            ChatMessage(role=role, content=content, timestamp=datetime.utcnow().isoformat())
        )

    def clear(self) -> None:
        self.history.clear()

    def ask(self, prompt: str) -> str:
        prompt = prompt.strip()
        if not prompt:
            return "Please type a question so I can help."

        self._append("user", prompt)
        reply = self._generate_reply(prompt)
        self._append("assistant", reply)
        return reply

    def _generate_reply(self, prompt: str) -> str:
        lower = prompt.lower()

        if any(word in lower for word in ["hello", "hi", "hey"]):
            return (
                "Hi! I can help with:\n"
                "- basic explanations\n"
                "- short coding tasks\n"
                "- debugging tips\n"
                "- productivity ideas\n"
                "Ask me anything."
            )

        if "python" in lower and any(k in lower for k in ["code", "write", "function", "script"]):
            return self._python_code_response(prompt)

        if any(k in lower for k in ["bug", "error", "fix", "traceback"]):
            return (
                "Debug checklist:\n"
                "1. Share the full error and stack trace.\n"
                "2. Reproduce with the smallest possible script.\n"
                "3. Print intermediate values around the failing line.\n"
                "4. Confirm dependency versions and Python version.\n"
                "5. Add/adjust tests after the fix.\n\n"
                "If you paste your traceback, I can suggest a targeted fix."
            )

        if any(k in lower for k in ["summarize", "summary"]):
            return self._summarize_text(prompt)

        if any(k in lower for k in ["plan", "roadmap", "steps"]):
            return (
                "Simple execution plan:\n"
                "1. Define your goal and constraints.\n"
                "2. Break work into 3-7 tasks.\n"
                "3. Deliver a minimal working version first.\n"
                "4. Test with realistic inputs.\n"
                "5. Refine UX/performance.\n"
                "6. Document usage and edge cases."
            )

        return (
            "I can help with practical answers, coding snippets, debugging, and planning.\n"
            "For better output, include:\n"
            "- your goal\n"
            "- language/tooling\n"
            "- constraints (time, format, complexity)."
        )

    def _python_code_response(self, prompt: str) -> str:
        task_match = re.search(r"(?:for|to)\s+(.+)", prompt, flags=re.IGNORECASE)
        task = task_match.group(1).strip(" .") if task_match else "your task"

        snippet = f'''Here is a Python starter for {task}:\n\n```python
def solve(data):
    """Update this function with your business logic."""
    # TODO: parse/process data
    result = data
    return result


if __name__ == "__main__":
    sample = "replace-with-input"
    print(solve(sample))
```\n\nTips:\n- Keep functions small and testable.\n- Validate inputs early.\n- Add unit tests for normal and edge cases.'''
        return snippet

    def _summarize_text(self, prompt: str) -> str:
        parts = prompt.split(":", 1)
        text = parts[1].strip() if len(parts) > 1 else prompt
        words = text.split()

        if len(words) <= 40:
            return f"Short summary: {text}"

        first = " ".join(words[:20])
        middle = " ".join(words[len(words) // 2 - 10 : len(words) // 2 + 10])
        last = " ".join(words[-20:])

        return (
            "Summary:\n"
            f"- Opening: {first}...\n"
            f"- Core idea: {middle}...\n"
            f"- Closing: {last}..."
        )
