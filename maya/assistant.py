"""Interactive command-line interface for Maya AI."""

from maya.ai import MayaAI
from maya.commands import handle_command


BUILTIN_COMMANDS = {"help", "time", "date", "system", "hello", "exit"}


def is_builtin_command(command: str) -> bool:
    """Keep existing Maya commands separate from AI conversations."""
    normalized = command.strip().lower()

    return (
        normalized in BUILTIN_COMMANDS
        or normalized.startswith("search ")
        or normalized == "search"
        or normalized == "open browser"
    )


def main():
    print("=" * 48)
    print("MAYA AI")
    print("Your personal assistant")
    print("=" * 48)
    print("Maya's core is running.")
    print("Type 'help' to see available commands.")
    print("Ask a question naturally to talk to Maya's AI.")
    print("Type 'exit' to quit.")

    assistant = None

    try:
        while True:
            try:
                command = input("\nYou > ").strip()
            except EOFError:
                print("\nMaya > Goodbye!")
                break

            if not command:
                continue

            if is_builtin_command(command):
                response, should_exit = handle_command(command)
                print(f"\nMaya > {response}")

                if should_exit:
                    break

                continue

            if assistant is None:
                try:
                    print("\nMaya > Connecting to my AI brain...")
                    assistant = MayaAI()
                    print("Maya > I'm connected. What would you like to discuss?")
                except Exception as exc:
                    print(
                        "\nMaya > I couldn't initialize the AI connection. "
                        f"Error: {type(exc).__name__}: {exc}"
                    )
                    print(
                        "Check your API key, model availability, and "
                        "internet connection, then restart Maya."
                    )
                    continue

            try:
                print("\nMaya > Thinking...")
                answer = assistant.ask(command)
                print(f"\nMaya > {answer}")
            except Exception as exc:
                print(
                    "\nMaya > I couldn't complete that request. "
                    f"Error: {type(exc).__name__}: {exc}"
                )
                print(
                    "Check your connection, API quota, and model availability."
                )

    except KeyboardInterrupt:
        print("\nMaya > Stopping Maya. Goodbye!")

    finally:
        if assistant is not None:
            try:
                assistant.close()
            except Exception:
                pass


if __name__ == "__main__":
    main()
