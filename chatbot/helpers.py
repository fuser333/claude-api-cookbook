"""Three helper functions for working with Claude messages API."""
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def add_user_message(messages: list, text: str) -> None:
    """Append a user message to the conversation list."""
    messages.append({"role": "user", "content": text})


def add_assistant_message(messages: list, text: str) -> None:
    """Append an assistant message to the conversation list."""
    messages.append({"role": "assistant", "content": text})


def chat(messages: list, model: str = "claude-sonnet-4-5", max_tokens: int = 1024) -> str:
    """Call Claude API with the message history and return the generated text."""
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=messages,
    )
    return response.content[0].text
