"""Voice interface for running Maya AI on a local computer."""

import sys

from maya.ai import MayaAI


def main():
    # Import voice dependencies only when voice mode is launched.
    try:
        import speech_recognition as sr
        import pyttsx3
    except ImportError as exc:
        print("Maya voice dependencies are not installed.")
        print("Install them with: pip install -r requirements-voice.txt")
        print(f"Missing dependency: {exc}")
        return

    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 0.8
    recognizer.dynamic_energy_threshold = True

    try:
        speaker = pyttsx3.init()
        speaker.setProperty("rate", 175)
        speaker.setProperty("volume", 1.0)
    except Exception as exc:
        print(f"Could not initialize speech output: {exc}")
        return

    def speak(text: str):
        print(f"\nMaya > {text}")
        try:
            speaker.say(text)
            speaker.runAndWait()
        except Exception as exc:
            print(f"Speech playback failed: {exc}")

    print("=" * 48)
    print("MAYA AI - VOICE MODE")
    print("=" * 48)
    print("Maya will listen through your microphone.")
    print("Say 'exit' or 'goodbye' to stop.")
    print("Speech recognition requires an internet connection.")

    try:
        with sr.Microphone() as microphone:
            print("\nMaya > Calibrating microphone. Please stay quiet...")
            recognizer.adjust_for_ambient_noise(microphone, duration=1)
            speak("I'm ready. What would you like to talk about?")

            assistant = None

            try:
                while True:
                    try:
                        print("\nListening...")
                        audio = recognizer.listen(
                            microphone,
                            timeout=8,
                            phrase_time_limit=15,
                        )
                    except sr.WaitTimeoutError:
                        print("I didn't hear anything. Try speaking when ready.")
                        continue

                    try:
                        heard = recognizer.recognize_google(
                            audio,
                            language="en-US",
                        ).strip()
                    except sr.UnknownValueError:
                        speak("Sorry, I didn't catch that. Please try again.")
                        continue
                    except sr.RequestError as exc:
                        speak("Speech recognition is unavailable right now.")
                        print(f"Recognition error: {exc}")
                        continue

                    if not heard:
                        continue

                    print(f"\nYou > {heard}")

                    if heard.lower().strip(" .,!") in {
                        "exit",
                        "goodbye",
                        "stop maya",
                        "shut down maya",
                    }:
                        speak("Goodbye! Talk to you later.")
                        break

                    if assistant is None:
                        try:
                            print("Connecting to Maya's AI...")
                            assistant = MayaAI()
                        except Exception as exc:
                            speak("I couldn't connect to my AI brain.")
                            print(f"{type(exc).__name__}: {exc}")
                            continue

                    try:
                        print("\nMaya is thinking...")
                        answer = assistant.ask(heard)

                        if answer:
                            speak(answer)
                        else:
                            speak("I don't have an answer for that yet.")

                    except Exception as exc:
                        speak("Sorry, I couldn't complete that request.")
                        print(f"{type(exc).__name__}: {exc}")

            finally:
                if assistant is not None:
                    try:
                        assistant.close()
                    except Exception:
                        pass

    except OSError as exc:
        print("\nMaya couldn't access a microphone.")
        print("Check your microphone connection and operating-system permissions.")
        print(f"Details: {exc}")
    except KeyboardInterrupt:
        print("\nMaya voice mode stopped.")
    finally:
        try:
            speaker.stop()
        except Exception:
            pass

    print("Voice mode ended.")


if __name__ == "__main__":
    main()
