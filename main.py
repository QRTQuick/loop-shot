"""
Simple 'brain' that can listen and speak.

- Listens using the microphone (SpeechRecognition + Google Web Speech by default)
- Speaks responses using pyttsx3 (offline TTS)
- Optionally uses OpenAI (set OPENAI_API_KEY) to generate smarter answers

If microphone or TTS isn't available, it falls back to typed input and console output.
"""

from time import sleep
import os
import sys

try:
    import speech_recognition as sr
except Exception:
    sr = None

try:
    import pyttsx3
except Exception:
    pyttsx3 = None

try:
    import openai
except Exception:
    openai = None


def init_tts():
    if not pyttsx3:
        return None
    engine = pyttsx3.init()
    engine.setProperty("rate", 175)
    return engine


def speak(text, engine=None):
    """Speak text using pyttsx3 if available, otherwise print."""
    if engine:
        engine.say(text)
        engine.runAndWait()
    else:
        print("[TTS]", text)


def listen(timeout=5, phrase_time_limit=15):
    """Listen from the default microphone and return transcribed text.

    Falls back to console input if SpeechRecognition or microphone isn't available.
    """
    if not sr:
        return input("Type your question (microphone not available): ")

    r = sr.Recognizer()
    try:
        mic = sr.Microphone()
    except Exception as e:
        print("Microphone not available:", e)
        return input("Type your question: ")

    with mic as source:
        print("Listening... (speak now)")
        r.adjust_for_ambient_noise(source, duration=0.6)
        try:
            audio = r.listen(
                source, timeout=timeout, phrase_time_limit=phrase_time_limit
            )
        except sr.WaitTimeoutError:
            print("No speech detected (timeout).")
            return ""

    try:
        text = r.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""
    except sr.RequestError as e:
        print("Speech recognition error:", e)
        return ""


def get_answer(prompt):
    """Get an answer for the prompt.

    If OpenAI is installed and OPENAI_API_KEY is set, use the ChatCompletion API.
    Otherwise, return a simple fallback response.
    """
    prompt = prompt.strip()
    if not prompt:
        return "Sorry, I didn't hear anything. Try again."

    if openai and os.getenv("OPENAI_API_KEY"):
        try:
            openai.api_key = os.getenv("OPENAI_API_KEY")
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            print("OpenAI error:", e)
            # fall through to simple reply

    # Simple fallback responder
    low = prompt.lower()
    if any(greet in low for greet in ("hello", "hi", "hey")):
        return (
            "Hello! I can listen to your voice and speak answers. Say 'quit' to exit."
        )
    if "your name" in low:
        return "I am your brain assistant. You can call me Brain."
    if low.endswith("?"):
        return f"I heard your question: '{prompt}'. I'm not connected to a knowledge engine, but I can echo and help set up AI integration."
    return "I heard: " + prompt


def main():
    engine = init_tts()
    speak("Hello! I can speak. Ask me something or say quit to exit.", engine)

    while True:
        q = listen()
        if not q:
            # when listening returns empty string, allow re-trying
            continue
        if q.lower() in ("quit", "exit", "stop"):
            speak("Goodbye!", engine)
            break

        ans = get_answer(q)
        print("Answer:", ans)
        speak(ans, engine)
        sleep(0.5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted. Exiting.")
        try:
            speak("Goodbye!")
        except Exception:
            pass
        sys.exit(0)
