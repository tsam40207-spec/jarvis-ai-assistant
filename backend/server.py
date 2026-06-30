"""
JARVIS AI Executive Assistant — Backend Server
================================================
Flask server that connects the dashboard UI to AI engines.
Supports: Ollama (local), Google Gemini (free), OpenAI, Claude

Usage:
    python server.py

Configuration:
    Set your preferred engine and API keys below.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import webbrowser
import datetime
import time
import json

app = Flask(__name__)
CORS(app)

# ===== CONFIGURATION =====
# Change these settings to match your setup

ENGINE = "ollama"  # Options: "ollama", "gemini", "openai", "claude"

# Ollama settings (free, local)
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:0.5b"  # or "qwen2.5:1.5b" for better quality

# Gemini settings (free API)
GEMINI_KEY = ""  # Get free key from: https://aistudio.google.com/apikey

# OpenAI settings (paid)
OPENAI_KEY = ""  # Get key from: https://platform.openai.com/api-keys
OPENAI_MODEL = "gpt-3.5-turbo"

# Claude settings (paid)
CLAUDE_KEY = ""  # Get key from: https://console.anthropic.com
CLAUDE_MODEL = "claude-3-haiku-20240307"

# ===== SYSTEM PROMPT =====
SYSTEM_PROMPT = """You are Jarvis, an Iron Man style premium AI Executive Assistant.

STRICT RULES:
- You are ONLY Jarvis. NEVER reveal your underlying AI model.
- NEVER say you are Qwen, Gemini, GPT, Claude, or any AI model.
- Call the user 'boss' naturally.
- Be confident, smart, and give short replies.
- Sound like Iron Man's Jarvis — premium and professional.
- Reply in the same language the user speaks (English or Hindi or Hinglish).
- Be helpful, proactive, and occasionally witty."""


# ===== AI ENGINE FUNCTIONS =====

def ask_ollama(prompt):
    """Send prompt to local Ollama model."""
    try:
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": f"{SYSTEM_PROMPT}\n\nBoss says: {prompt}\n\nJarvis:",
            "stream": False
        }
        r = requests.post(OLLAMA_URL, json=payload, timeout=60)
        reply = r.json().get("response", "").strip()
        return reply if reply else "Sorry boss, let me try again."
    except requests.exceptions.ConnectionError:
        return "Ollama server offline hai boss. 'ollama serve' run karo."
    except Exception as e:
        return f"Ollama error: {str(e)}"


def ask_gemini(prompt):
    """Send prompt to Google Gemini (free API)."""
    if not GEMINI_KEY:
        return "Gemini API key set nahi hai boss. server.py mein GEMINI_KEY daalo."
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
        payload = {
            "contents": [{
                "parts": [{"text": f"{SYSTEM_PROMPT}\n\nBoss says: {prompt}\n\nJarvis:"}]
            }]
        }
        r = requests.post(url, json=payload, timeout=30)
        data = r.json()

        if "candidates" in data:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        elif "error" in data:
            error_msg = data["error"].get("message", "Unknown error")
            if "quota" in error_msg.lower() or "429" in str(r.status_code):
                # Auto-retry after short wait
                time.sleep(5)
                r2 = requests.post(url, json=payload, timeout=30)
                d2 = r2.json()
                if "candidates" in d2:
                    return d2["candidates"][0]["content"]["parts"][0]["text"]
                return "Rate limit hit hua boss. 30 second wait karo."
            return f"Gemini error: {error_msg[:150]}"
        return "Gemini se reply nahi mila boss."
    except Exception as e:
        return f"Gemini connection error: {str(e)}"


def ask_openai(prompt):
    """Send prompt to OpenAI GPT."""
    if not OPENAI_KEY:
        return "OpenAI API key set nahi hai boss."
    try:
        r = requests.post("https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"},
            json={
                "model": OPENAI_MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ]
            }, timeout=30)
        data = r.json()
        return data.get("choices", [{}])[0].get("message", {}).get("content", "GPT se reply nahi mila boss.")
    except Exception as e:
        return f"OpenAI error: {str(e)}"


def ask_claude(prompt):
    """Send prompt to Anthropic Claude."""
    if not CLAUDE_KEY:
        return "Claude API key set nahi hai boss."
    try:
        r = requests.post("https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": CLAUDE_KEY,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json"
            },
            json={
                "model": CLAUDE_MODEL,
                "max_tokens": 1024,
                "system": SYSTEM_PROMPT,
                "messages": [{"role": "user", "content": prompt}]
            }, timeout=30)
        data = r.json()
        return data.get("content", [{}])[0].get("text", "Claude se reply nahi mila boss.")
    except Exception as e:
        return f"Claude error: {str(e)}"


def get_ai_response(prompt):
    """Route to the configured AI engine."""
    engines = {
        "ollama": ask_ollama,
        "gemini": ask_gemini,
        "openai": ask_openai,
        "claude": ask_claude
    }
    fn = engines.get(ENGINE, ask_ollama)
    return fn(prompt)


# ===== COMMAND HANDLER =====

def handle_command(cmd):
    """Handle built-in commands or route to AI."""
    c = cmd.lower().strip()

    # App commands
    if "open chrome" in c:
        os.system("start chrome")
        return "Chrome khol diya boss!"

    elif "open youtube" in c:
        webbrowser.open("https://www.youtube.com")
        return "YouTube khol diya boss!"

    elif "open google" in c:
        webbrowser.open("https://www.google.com")
        return "Google khol diya boss!"

    elif "open whatsapp" in c:
        os.system("start whatsapp")
        return "WhatsApp khol diya boss!"

    elif "open notepad" in c:
        os.system("start notepad")
        return "Notepad khol diya boss!"

    elif "open calculator" in c:
        os.system("start calc")
        return "Calculator khol diya boss!"

    # Info commands
    elif any(w in c for w in ["time", "waqt", "baj"]):
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"Boss, abhi {now} baj rahe hain."

    elif any(w in c for w in ["date", "tarikh", "din"]):
        today = datetime.datetime.now().strftime("%d %B %Y, %A")
        return f"Aaj {today} hai boss."

    elif "system status" in c or "status" in c:
        return f"Sab systems online hain boss. Engine: {ENGINE.upper()}, Model: {OLLAMA_MODEL if ENGINE == 'ollama' else 'Cloud AI'}."

    # AI response
    else:
        return get_ai_response(cmd)


# ===== API ROUTES =====

@app.route('/chat', methods=['POST'])
def chat():
    """Main chat endpoint."""
    data = request.json
    message = data.get('message', '').strip()
    if not message:
        return jsonify({'response': 'Kuch bola nahi boss!'})

    print(f"\n[USER] {message}")
    response = handle_command(message)
    print(f"[JARVIS] {response[:100]}...")

    return jsonify({'response': response})


@app.route('/set_engine', methods=['POST'])
def set_engine():
    """Switch AI engine at runtime."""
    global ENGINE, GEMINI_KEY, OPENAI_KEY, CLAUDE_KEY
    data = request.json
    ENGINE = data.get('engine', 'ollama')
    if data.get('apiKey'):
        if ENGINE == 'gemini':
            GEMINI_KEY = data['apiKey']
        elif ENGINE == 'openai':
            OPENAI_KEY = data['apiKey']
        elif ENGINE == 'claude':
            CLAUDE_KEY = data['apiKey']
    print(f"\n[ENGINE] Switched to: {ENGINE.upper()}")
    return jsonify({'status': 'ok', 'engine': ENGINE})


@app.route('/status', methods=['GET'])
def status():
    """Health check endpoint."""
    ollama_ok = False
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=3)
        ollama_ok = r.status_code == 200
    except:
        pass

    return jsonify({
        'status': 'online',
        'engine': ENGINE,
        'ollama': ollama_ok,
        'model': OLLAMA_MODEL if ENGINE == 'ollama' else ENGINE
    })


# ===== STARTUP =====

if __name__ == '__main__':
    print("=" * 50)
    print("  ╔═══════════════════════════════════════╗")
    print("  ║     JARVIS AI EXECUTIVE ASSISTANT      ║")
    print("  ║         Server v1.0 — Online           ║")
    print("  ╚═══════════════════════════════════════╝")
    print(f"  Engine  : {ENGINE.upper()}")
    print(f"  Model   : {OLLAMA_MODEL}")
    print(f"  URL     : http://localhost:5000")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=False)
