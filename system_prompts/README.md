# System Prompts Exercise · Building with the Claude API

Demonstrates how the **system prompt** changes Claude's behavior on the same user message.

## Key concept

In the Anthropic Messages API, `system` is a **top-level parameter**, not part of the `messages` array. This is different from OpenAI's API where `system` is a role inside the messages list.

```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    system="You are a senior Python engineer...",   # ← top-level
    messages=[{"role": "user", "content": "Write a function..."}],
    max_tokens=1024,
)
```

## Files

- `helpers.py` — extended `chat()` helper that accepts an optional `system` argument
- `exercise.py` — runs the same user message 3 times: baseline / concise engineer / pirate teacher, to make the behavior shift visible

## Run

```bash
export ANTHROPIC_API_KEY="your-api-key"
uv sync
uv run exercise.py
```

Expected output: 3 sections showing very different formatting, tone and verbosity for the same user request.
