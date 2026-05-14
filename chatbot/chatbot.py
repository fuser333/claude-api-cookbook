"""Chat Bot Exercise · Building with the Claude API.

Steps from the exercise slide:
  1. Prompt the user to enter some input using the built-in 'input' function
  2. Add it to a list of messages
  3. Call the API
  4. Add generated text to the list of messages
  5. Print the generated text
  6. Repeat from #1
"""
from helpers import add_user_message, add_assistant_message, chat


def main():
    messages = []
    print("Chat Bot ready · type 'exit' to quit.\n")

    while True:
        # 1. Prompt user input
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit", "salir"}:
            print("Bye.")
            break

        # 2. Add user message to list
        add_user_message(messages, user_input)

        # 3. Call API
        reply = chat(messages)

        # 4. Add generated text to list of messages
        add_assistant_message(messages, reply)

        # 5. Print the generated text
        print(f"Claude: {reply}\n")

        # 6. Repeat from #1 (the while loop handles this)


if __name__ == "__main__":
    main()
