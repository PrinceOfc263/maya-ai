"""Maya AI command-line interface."""

from maya.commands import handle_command


def main() -> None:
    print("=" * 48)
    print("MAYA AI")
    print("Your personal assistant")
    print("=" * 48)
    print("Maya's core is running.")
    print("Type 'help' to see available commands.")
    print("Type 'exit' to quit.")

    running = True

    while running:
        try:
            command = input("\nYou > ")
            response, running = handle_command(command)

            if response:
                print(f"\nMaya > {response}")

        except (KeyboardInterrupt, EOFError):
            print("\n\nMaya > Goodbye! See you next time.")
            break


if __name__ == "__main__":
    main()
