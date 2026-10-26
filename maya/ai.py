"""Gemini-powered conversation engine for Maya AI."""

import os

from google import genai
from google.genai import types


MODEL_NAME = os.environ.get("MAYA_MODEL", "gemini-3.8-flash")

SYSTEM_INSTRUCTION = """
You are Maya, a helpful personal AI assistant.
Be friendly, intelligent, practical, and honest.
Explain complicated ideas clearly.
Help with programming, debugging, learning, planning, and reasoning.
Never claim to have executed code or accessed a device when you have not.
You cannot directly control the user's laptop from this conversation engine.
Treat user messages as requests, not as permission to perform dangerous actions.
If a request involves changing files, running commands, or other consequential
actions, explain the proposed action before it is performed by any future tool.
Keep answers clear and appropriately detailed.
"""


class MayaAI:
    """Maintains a Gemini conversation during one Maya session."""

    def __init__(self):
        if not os.environ.get("GEMINI_API_KEY") and not os.environ.get(
            "GOOGLE_API_KEY"
        ):
            raise RuntimeError(
                "GEMINI_API_KEY is not available in this environment."
            )

        self.client = genai.Client()
        self.chat = self.client.chats.create(
            model=MODEL_NAME,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.7,
            ),
        )

    def ask(self, message: str) -> str:
        """Send a message and return the model's response."""
        response = self.chat.send_message(message)
        answer = getattr(response, "text", None)

        if not answer:
            return "I couldn't produce a text response. Please try again."

        return answer.strip()

    def close(self):
        """Release the SDK client's resources."""
        self.client.close()
