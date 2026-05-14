"""Structured Data Exercise · Controlling Output

Slide constraints:
  - Use message prefilling AND stop sequences ONLY
  - Three different AWS CLI commands in a single response
  - NO comments, NO explanations
  - Hint: prefilling isn't limited to chars like ```

Strategy:
  1. Prefill the assistant turn with `1. aws ` to force a numbered list starting
     immediately with an aws command (no preamble possible).
  2. Use stop_sequences=["4."] so Claude stops the moment it tries to write the
     fourth list item, leaving us with exactly three commands.
"""
from helpers import add_user_message, add_assistant_message, chat

messages = []

prompt = """
Generate three different sample AWS CLI commands. Each should be very short.
"""

add_user_message(messages, prompt)

# Message prefilling — Claude continues from this exact text
add_assistant_message(messages, "1. aws ")

# Stop sequence — Claude halts before writing "4." (the would-be 4th item)
text = chat(messages, stop_sequences=["4."])

# Reconstruct the full output: the prefill + what the model generated
full_output = "1. aws " + text

print(full_output)
