# Detailed Setup Guide

## Prerequisites

### Windows
1. **Python 3.11+** — Download from [python.org](https://python.org)
2. **Git Bash** — Download from [git-scm.com](https://git-scm.com)
3. **Chrome** — Required for voice features
4. **Ollama** (optional) — Download from [ollama.com](https://ollama.com)

### Mac/Linux
1. **Python 3.11+** — Usually pre-installed
2. **Chrome** — Required for voice features
3. **Ollama** (optional) — `curl -fsSL https://ollama.com/install.sh | sh`

---

## Installation

### Step 1: Clone the repo
```bash
git clone https://github.com/yourusername/jarvis-ai-assistant.git
cd jarvis-ai-assistant
```

### Step 2: Install Python dependencies
```bash
pip install -r requirements.txt
```

**Note for Windows:** If PyAudio fails, install it manually:
```bash
pip install pipwin
pipwin install pyaudio
```

### Step 3: Choose your AI engine

#### Option A: Ollama (Free, Local, Private)
```bash
# Install Ollama
# Windows: Download from ollama.com
# Mac/Linux: curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull qwen2.5:0.5b    # Small, fast (400MB)
ollama pull qwen2.5:1.5b    # Better quality (1GB)

# Start Ollama
ollama serve
```

#### Option B: Google Gemini (Free API, Cloud)
1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Click "Create API Key"
3. Copy the key
4. Edit `backend/server.py`:
```python
ENGINE = "gemini"
GEMINI_KEY = "your-key-here"
```

#### Option C: OpenAI GPT (Paid)
1. Get key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Edit `backend/server.py`:
```python
ENGINE = "openai"
OPENAI_KEY = "sk-your-key-here"
```

---

## Running

### Quick Start (Windows)
Double-click `scripts/start.bat` — everything starts automatically!

### Manual Start
```bash
# Terminal 1: Start backend
cd backend
python server.py

# Terminal 2: Start dashboard
cd frontend
python -m http.server 8080

# Open Chrome
# Go to: http://localhost:8080
```

### Voice Assistant Only (No Dashboard)
```bash
cd backend
python voice_assistant.py
```

---

## Troubleshooting

### Microphone not working in dashboard
1. Open Chrome Settings → Privacy → Microphone
2. Allow `localhost:8080`
3. Or click the lock icon in the address bar → Microphone → Allow

### Ollama CUDA errors
Run Ollama in CPU mode:
```bash
# Windows PowerShell (Admin)
$env:CUDA_VISIBLE_DEVICES="-1"
ollama serve

# Mac/Linux
CUDA_VISIBLE_DEVICES=-1 ollama serve
```

### Gemini rate limit
- Free tier: 15 requests/minute
- Wait 30-60 seconds between bursts
- Use different API keys for higher limits

### Port already in use
```bash
# Kill process on port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -i :5000
kill -9 <PID>
```
