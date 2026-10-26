"""Interactive command-line interface for Maya AI."""

from maya.ai import MayaAI
from maya.commands import handle_command


BUILTIN_COMMANDS = {
    "help",
    "time",
    "date",
    "system",
    "hello",
    "exit",
}


def is_builtin_command(command: str) -> bool:
    """Recognize existing local commands."""
    normalized = command.strip().lower()

    return (
        normalized in BUILTIN_COMMANDS
        or normalized == "search"
        or normalized.startswith("search ")
        or normalized == "open browser"
    )


def main():
    print("=" * 48)
    print("MAYA AI")
    print("Your personal assistant")
    print("=" * 48)
    print("AI model: Gemini Flash-Lite")
    print("Type 'help' for commands or ask me anything.")
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
                    print("Maya > Connected.")
                except Exception as exc:
                    print(
                        "\nMaya > I couldn't connect to the AI service."
                        f"\nError: {type(exc).__name__}: {exc}"
                    )
                    print(
                        "Check the API key, model access, internet, "
                        "and API quota."
                    )
                    continue

            try:
                print("\nMaya > ", end="", flush=True)
                received_text = False

                for part in assistant.ask_stream(command):
                    print(part, end="", flush=True)
                    received_text = True

                if not received_text:
                    print("I couldn't produce a text response.")

                print()

            except Exception as exc:
                print(
                    f"\n\nMaya > Request failed: "
                    f"{type(exc).__name__}: {exc}"
                )
                print("Check your connection, model access, and API quota.")

    except KeyboardInterrupt:
        print("\n\nMaya > Stopping Maya. Goodbye!")

    finally:
        if assistant is not None:
            try:
                assistant.close()
            except Exception:
                pass


if __name__ == "__main__":
    main()
