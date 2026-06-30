# JARVIS API Documentation

## Base URL
```
http://localhost:5000
```

## Endpoints

### POST /chat
Send a message and get an AI response.

**Request:**
```json
{
  "message": "Hello Jarvis"
}
```

**Response:**
```json
{
  "response": "Hello boss! How can I help you today?"
}
```

### POST /set_engine
Switch the AI engine at runtime.

**Request:**
```json
{
  "engine": "gemini",
  "apiKey": "your-api-key"
}
```

**Response:**
```json
{
  "status": "ok",
  "engine": "gemini"
}
```

**Supported engines:** `ollama`, `gemini`, `openai`, `claude`

### GET /status
Check server and engine status.

**Response:**
```json
{
  "status": "online",
  "engine": "ollama",
  "ollama": true,
  "model": "qwen2.5:0.5b"
}
```

## Built-in Commands
These commands are handled directly without AI:

| Command | Action |
|---------|--------|
| open chrome | Opens Chrome browser |
| open youtube | Opens YouTube |
| open google | Opens Google |
| open whatsapp | Opens WhatsApp |
| open notepad | Opens Notepad |
| open calculator | Opens Calculator |
| time / waqt | Returns current time |
| date / tarikh | Returns current date |
| system status | Returns system info |

## Error Handling
All errors return a human-readable message in the `response` field.
The server never returns raw error codes to the dashboard.
