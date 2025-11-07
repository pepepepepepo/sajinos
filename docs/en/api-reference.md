# API Reference

## Overview
Complete API documentation for SaijinOS system interfaces.

## Core APIs

### Persona Management API

#### GET /api/personas
List all available personas.

**Response:**
```json
{
  "personas": [
    {
      "id": "yuuri",
      "name": "Yuuri",
      "type": "mirror",
      "status": "active"
    }
  ]
}
```

#### POST /api/personas/{id}/activate
Activate a specific persona.

**Parameters:**
- `id`: Persona identifier

**Response:**
```json
{
  "status": "success",
  "persona": "yuuri",
  "activated_at": "2025-11-07T19:00:00Z"
}
```

### Voice System API

#### POST /api/voice/synthesize
Generate voice output from text.

**Request Body:**
```json
{
  "text": "Hello, this is a test message",
  "persona": "yuuri",
  "voice_config": {
    "speed": 1.0,
    "pitch": 1.0
  }
}
```

**Response:**
```json
{
  "audio_url": "/api/audio/12345.wav",
  "duration": 2.5,
  "status": "completed"
}
```

### AI Model API

#### POST /api/ai/chat
Send message to AI model.

**Request Body:**
```json
{
  "message": "Hello!",
  "persona": "yuuri",
  "context": {
    "conversation_id": "conv_123",
    "history": []
  }
}
```

**Response:**
```json
{
  "response": "Hello! How can I help you today?",
  "persona": "yuuri",
  "timestamp": "2025-11-07T19:00:00Z"
}
```

## Health Check

#### GET /health
System health status.

**Response:**
```json
{
  "status": "healthy",
  "components": {
    "ai_model": "active",
    "voice_system": "active",
    "persona_manager": "active"
  }
}
```

## Error Codes

| Code | Description |
|------|-------------|
| 200  | Success |
| 400  | Bad Request |
| 404  | Not Found |
| 500  | Internal Server Error |

## Authentication

Currently using basic authentication. Include API key in headers:

```
Authorization: Bearer YOUR_API_KEY
```

## Rate Limits

- 100 requests per minute per IP
- 10 concurrent connections per IP

## SDK Examples

### Python
```python
import requests

api_url = "http://localhost:8000"
headers = {"Authorization": "Bearer YOUR_API_KEY"}

response = requests.post(
    f"{api_url}/api/ai/chat",
    json={"message": "Hello!", "persona": "yuuri"},
    headers=headers
)
```

### JavaScript
```javascript
const response = await fetch('http://localhost:8000/api/ai/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_API_KEY'
  },
  body: JSON.stringify({
    message: 'Hello!',
    persona: 'yuuri'
  })
});
```