"""Helper functions with system prompt support."""
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def add_user_message(messages: list, text: str) -> None:
    """Append a user message to the conversation list."""
    messages.append({"role": "user", "content": text})


def add_assistant_message(messages: list, text: str) -> None:
    """Append an assistant message to the conversation list."""
    messages.append({"role": "assistant", "content": text})


def chat(
    messages: list,
    system: str | None = None,
    model: str = "claude-sonnet-4-5",
    max_tokens: int = 1024,
) -> str:
    """Call Claude API with optional system prompt and return generated text.

    Note: in the Anthropic Messages API the `system` is a TOP-LEVEL parameter,
    not part of the messages array.
    """
    kwargs = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": messages,
    }
    if system:
        kwargs["system"] = system

    response = client.messages.create(**kwargs)
    return response.content[0].text
