"""
JARVIS Voice Assistant — Standalone Terminal Version
=====================================================
Wake word activated voice assistant with Ollama AI.

Usage:
    python voice_assistant.py

Say "Hi Jarvis" to activate, then speak your command.
Say "sleep" to go standby, "exit" to quit.
"""

import speech_recognition as sr
import pyttsx3
import requests
import os
import webbrowser
import datetime

# ===== CONFIG =====
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:0.5b"

SYSTEM_PROMPT = """You are Jarvis, an Iron Man style premium AI assistant.
RULES: Never say you are Qwen or any AI model. You are ONLY Jarvis.
Call the user 'boss'. Be confident, smart, short replies.
Sound like Iron Man's Jarvis — premium and professional."""


def create_engine():
    """Create a fresh TTS engine (avoids conflicts)."""
    engine = pyttsx3.init(driverName='sapi5')
    engine.setProperty('rate', 160)
    engine.setProperty('volume', 1.0)
    return engine


def speak(text):
    """Speak text aloud using Windows TTS."""
    print(f"\n🤖 Jarvis: {text}")
    engine = create_engine()
    engine.say(text[:500])
    engine.runAndWait()
    engine.stop()


def listen():
    """Listen for voice input and return text."""
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.pause_threshold = 0.6
    recognizer.dynamic_energy_threshold = True

    with sr.Microphone() as source:
        print("\n🎤 Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)
        except sr.WaitTimeoutError:
            return ""

    try:
        text = recognizer.recognize_google(audio)
        print(f"👤 You: {text}")
        return text.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        print("⚠️ Speech recognition service unavailable")
        return ""


def ask_ollama(prompt):
    """Get AI response from Ollama."""
    payload = {
        "model": MODEL,
        "prompt": f"{SYSTEM_PROMPT}\n\nBoss says: {prompt}\n\nJarvis:",
        "stream": False
    }
    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=60)
        return r.json().get("response", "Sorry boss, no reply.")
    except requests.exceptions.ConnectionError:
        return "Ollama offline hai boss. 'ollama serve' run karo."
    except Exception as e:
        return f"Error: {str(e)}"


def handle_command(command):
    """Handle built-in commands or route to AI."""
    if "open chrome" in command:
        speak("Opening Chrome boss.")
        os.system("start chrome")
        return True

    elif "open youtube" in command:
        speak("Opening YouTube boss.")
        webbrowser.open("https://www.youtube.com")
        return True

    elif "open google" in command:
        speak("Opening Google boss.")
        webbrowser.open("https://www.google.com")
        return True

    elif "open whatsapp" in command:
        speak("Opening WhatsApp boss.")
        os.system("start whatsapp")
        return True

    elif "open notepad" in command:
        speak("Opening Notepad boss.")
        os.system("start notepad")
        return True

    elif any(w in command for w in ["time", "waqt", "baj"]):
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"Boss, abhi {now} baj rahe hain.")
        return True

    elif any(w in command for w in ["date", "tarikh"]):
        today = datetime.datetime.now().strftime("%d %B %Y")
        speak(f"Aaj {today} hai boss.")
        return True

    return False


def main():
    """Main assistant loop."""
    print("=" * 50)
    print("  🤖 JARVIS VOICE ASSISTANT")
    print("  Say 'Hi Jarvis' to wake me up!")
    print("=" * 50)

    speak("Jarvis system online. Say Hi Jarvis to wake me up boss.")

    active_mode = False

    while True:
        if not active_mode:
            # Standby — waiting for wake word
            wake = listen()
            if any(w in wake for w in ["hi jarvis", "hey jarvis", "hello jarvis"]):
                speak("Yes boss, I am listening.")
                active_mode = True
        else:
            # Active — listening for commands
            command = listen()

            if not command:
                continue

            # Mode commands
            if "sleep" in command or "standby" in command:
                speak("Going to standby mode boss. Say Hi Jarvis to wake me.")
                active_mode = False
                continue

            if "exit" in command or "stop" in command or "shutdown" in command:
                speak("Goodbye boss. Jarvis shutting down.")
                break

            # Try built-in commands first
            if handle_command(command):
                continue

            # AI response
            reply = ask_ollama(command)
            speak(reply)


if __name__ == '__main__':
    main()
