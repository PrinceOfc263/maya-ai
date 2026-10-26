"""Fast, streaming Gemini conversation engine for Maya AI."""

import os

from google import genai
from google.genai import types


MODEL_NAME = os.environ.get(
    "MAYA_MODEL",
    "gemini-3.5-flash-lite",
)

SYSTEM_INSTRUCTION = """
You are Maya, a friendly, intelligent personal AI assistant.
Be direct, useful, natural, and accurate.
Help with general questions, programming, debugging, learning, and planning.
Prefer concise answers unless the user asks for detail.
Never claim to have performed actions you did not perform.
You cannot directly control the user's computer from this chat engine.
Ask for clarification when a request is genuinely ambiguous.
"""


class MayaAI:
    """Maintains a conversation and streams responses as they arrive."""

    def __init__(self):
        if not (
            os.environ.get("GEMINI_API_KEY")
            or os.environ.get("GOOGLE_API_KEY")
        ):
            raise RuntimeError(
                "API key missing. Check GEMINI_API_KEY in Codespaces."
            )

        self.client = genai.Client()
        self.chat = self.client.chats.create(
            model=MODEL_NAME,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.5,
                max_output_tokens=1024,
            ),
        )

    def ask_stream(self, message: str):
        """Yield answer text progressively instead of waiting for completion."""
        for chunk in self.chat.send_message_stream(message):
            text = getattr(chunk, "text", None)
            if text:
                yield text

    def ask(self, message: str) -> str:
        """Return a complete answer when streaming output is not needed."""
        return "".join(self.ask_stream(message)).strip()

    def close(self):
        """Release the client's resources."""
        self.client.close()
