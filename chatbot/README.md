# Chat Bot Exercise · Building with the Claude API

Implementation of the chat bot exercise from the Anthropic Academy course "Building with the Claude API".

## Files

- `helpers.py` — three helper functions:
  - `add_user_message(messages, text)` — append user turn
  - `add_assistant_message(messages, text)` — append assistant turn
  - `chat(messages, model, max_tokens)` — call Claude API and return text
- `chatbot.py` — main loop that ties the three helpers together
- `pyproject.toml` — dependencies (anthropic SDK)

## Setup

```bash
export ANTHROPIC_API_KEY="your-api-key"
uv sync
```

## Run

```bash
uv run chatbot.py
```

Type any message. Type `exit`, `quit` or `salir` to leave.

## Key concepts proven by this exercise

- **Stateless API** — Claude has no memory; the client sends the whole conversation history with each request.
- **Messages array** — alternating `user` / `assistant` turns build the context.
- **Multi-turn loop** — the chatbot pattern is just "append → call → append → print → repeat".
