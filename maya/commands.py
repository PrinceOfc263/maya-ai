"""Safe, basic commands supported by Maya AI."""

from datetime import datetime
from urllib.parse import quote_plus
import platform
import os
import sys


def get_help() -> str:
    return """
Here is what I can do right now:

  help                 Show available commands
  time                 Tell you the current time
  date                 Tell you today's date
  system               Show system information
  search <query>       Prepare a web search
  open browser         Open a browser when running locally
  hello                Say hello
  exit                 Shut down Maya

My AI reasoning, voice recognition, and desktop automation
will be added in later development steps.
""".strip()


def handle_command(command: str) -> tuple[str, bool]:
    """Return (response, keep_running) for a user command."""
    command = command.strip()
    lowered = command.lower()

    if not command:
        return "", True

    if lowered in {"exit", "quit", "goodbye"}:
        return "Goodbye! I'll be here when you need me.", False

    if lowered in {"help", "commands"}:
        return get_help(), True

    if lowered in {"hello", "hi", "hey maya"}:
        return "Hello! I'm Maya, your personal AI assistant.", True

    if lowered == "time":
        current_time = datetime.now().astimezone().strftime("%I:%M %p")
        return f"The current time is {current_time}.", True

    if lowered == "date":
        current_date = datetime.now().astimezone().strftime(
            "%A, %d %B %Y"
        )
        return f"Today is {current_date}.", True

    if lowered == "system":
        details = [
            f"Operating system: {platform.system()}",
            f"Platform: {platform.platform()}",
            f"Python: {sys.version.split()[0]}",
            f"Machine: {platform.machine()}",
        ]

        if os.environ.get("CODESPACES") == "true":
            details.append(
                "Environment: GitHub Codespaces (cloud)"
            )

        return "\n".join(details), True

    if lowered.startswith("search "):
        query = command[7:].strip()

        if not query:
            return "Tell me what you want to search for.", True

        url = "https://www.google.com/search?q=" + quote_plus(query)

        # Codespaces cannot open a browser on your physical laptop.
        if os.environ.get("CODESPACES") == "true":
            return (
                "Your search link is ready:\n"
                f"{url}\n"
                "Open this link in your laptop's browser."
            ), True

        return (
            "Your search link is ready:\n"
            f"{url}\n"
            "Use this link to open the search in your browser."
        ), True

    if lowered == "open browser":
        if os.environ.get("CODESPACES") == "true":
            return (
                "I'm running in the cloud right now, so I cannot "
                "open a browser window on your HP laptop yet. "
                "We'll add local desktop control later."
            ), True

        import webbrowser

        opened = webbrowser.open("https://www.google.com")
        if opened:
            return "I've requested that your default browser open.", True

        return (
            "I couldn't open the browser automatically. "
            "Please open your browser manually."
        ), True

    return (
        "I don't know how to do that yet. Type 'help' to see "
        "my current commands. We'll add more abilities gradually."
    ), True
