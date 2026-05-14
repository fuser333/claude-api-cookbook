"""Helper functions with system prompt + stop_sequences support."""
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def add_user_message(messages: list, text: str) -> None:
    messages.append({"role": "user", "content": text})


def add_assistant_message(messages: list, text: str) -> None:
    """Append an assistant message · used here for message prefilling."""
    messages.append({"role": "assistant", "content": text})


def chat(
    messages: list,
    system: str | None = None,
    stop_sequences: list[str] | None = None,
    model: str = "claude-sonnet-4-5",
    max_tokens: int = 1024,
) -> str:
    """Call Claude with optional system prompt and stop sequences."""
    kwargs = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": messages,
    }
    if system:
        kwargs["system"] = system
    if stop_sequences:
        kwargs["stop_sequences"] = stop_sequences

    response = client.messages.create(**kwargs)
    return response.content[0].text
