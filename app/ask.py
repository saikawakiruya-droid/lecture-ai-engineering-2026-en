"""Lecture 01: ask an LLM questions in a conversation.

Usage:
    uv run python -m app.ask "What is LoRA?"
    uv run python -m app.ask            # Start a conversation with a course-specific question

Without a question argument, the script starts a chat with the default question and
keeps its history for follow-up questions until you enter /exit or /quit.
"""

import argparse

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# A course-specific question. The correct answer is in homework-levels in data/glossary.json
DEFAULT_QUESTION = "What are the 3 homework levels in the AIE2026 course?"


def ask(chat: genai.chats.Chat, question: str) -> str:
    response = chat.send_message(question)

    usage = response.usage_metadata
    input_tokens = usage.prompt_token_count if usage else None
    output_tokens = usage.candidates_token_count if usage else None
    print(f"[tokens] input={input_tokens if input_tokens is not None else 'n/a'} "
          f"output={output_tokens if output_tokens is not None else 'n/a'}")

    return response.text


def interactive_chat(chat: genai.chats.Chat) -> None:
    print(f"[question] {DEFAULT_QUESTION}\n")
    print(ask(chat, DEFAULT_QUESTION))
    print("\nAsk a follow-up question, or enter /exit to finish.")

    while True:
        try:
            question = input("You> ").strip()
        except EOFError:
            print()
            return

        if question.lower() in {"/exit", "/quit"}:
            return
        if not question:
            continue

        print(f"\n[question] {question}\n")
        print(ask(chat, question))


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask an LLM questions in a conversation")
    parser.add_argument("question", nargs="?", help="Ask one question and exit")
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    try:
        client = genai.Client(api_key=get_api_key())
        chat = client.chats.create(model=MODEL)
        if args.question:
            print(f"[question] {args.question}\n")
            print(ask(chat, args.question))
        else:
            interactive_chat(chat)
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
