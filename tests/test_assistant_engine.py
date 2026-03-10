from ai_assistant import AssistantEngine


def test_empty_prompt():
    engine = AssistantEngine()
    assert "Please type" in engine.ask("   ")


def test_python_prompt_returns_code_block():
    engine = AssistantEngine()
    reply = engine.ask("write python code to reverse a string")
    assert "```python" in reply


def test_clear_history():
    engine = AssistantEngine()
    engine.ask("hello")
    assert engine.history
    engine.clear()
    assert engine.history == []
