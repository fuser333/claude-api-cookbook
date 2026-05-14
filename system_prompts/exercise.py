"""System Prompts Exercise · Building with the Claude API.

Reference from the course slide:

    messages = []
    add_user_message(
        messages,
        "Write a Python function that checks a string for duplicate characters.",
    )
    answer = chat(messages)
    answer

The exercise extends this baseline by adding a `system` parameter to the chat
helper so the same user message produces a very different style of answer
depending on the persona we give Claude.
"""
from helpers import add_user_message, chat


# ---------------------------------------------------------------------------
# 1. Baseline · no system prompt
# ---------------------------------------------------------------------------
messages = []
add_user_message(
    messages,
    "Write a Python function that checks a string for duplicate characters.",
)
answer = chat(messages)
print("=" * 60)
print("BASELINE (no system prompt)")
print("=" * 60)
print(answer)


# ---------------------------------------------------------------------------
# 2. With a 'concise senior engineer' system prompt
# ---------------------------------------------------------------------------
messages = []
add_user_message(
    messages,
    "Write a Python function that checks a string for duplicate characters.",
)
answer = chat(
    messages,
    system=(
        "You are a senior Python engineer. Reply with the minimal idiomatic "
        "function only · no preamble · no explanatory text · use type hints "
        "and a one-line docstring."
    ),
)
print("\n" + "=" * 60)
print("WITH SYSTEM PROMPT (concise senior engineer)")
print("=" * 60)
print(answer)


# ---------------------------------------------------------------------------
# 3. With a 'pirate teacher' system prompt to prove behavior changes
# ---------------------------------------------------------------------------
messages = []
add_user_message(
    messages,
    "Write a Python function that checks a string for duplicate characters.",
)
answer = chat(
    messages,
    system=(
        "You are a pirate Python tutor. Explain the code in pirate dialect, "
        "then give the function in a code block, then end with 'Arrr.'"
    ),
)
print("\n" + "=" * 60)
print("WITH SYSTEM PROMPT (pirate teacher · proves behavior changes)")
print("=" * 60)
print(answer)
