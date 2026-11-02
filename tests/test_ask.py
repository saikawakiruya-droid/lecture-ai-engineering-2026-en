from types import SimpleNamespace

from app.ask import DEFAULT_QUESTION, ask, interactive_chat


class FakeChat:
    def __init__(self):
        self.questions = []

    def send_message(self, question):
        self.questions.append(question)
        return SimpleNamespace(text=f"Answer to: {question}", usage_metadata=None)


def test_ask_sends_question_to_chat(capsys):
    chat = FakeChat()

    answer = ask(chat, "What is LoRA?")

    assert chat.questions == ["What is LoRA?"]
    assert answer == "Answer to: What is LoRA?"
    assert "[tokens] input=n/a output=n/a" in capsys.readouterr().out


def test_interactive_chat_keeps_history_for_follow_up(monkeypatch):
    chat = FakeChat()
    questions = iter(["Follow-up question", "/exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(questions))

    interactive_chat(chat)

    assert chat.questions == [DEFAULT_QUESTION, "Follow-up question"]
