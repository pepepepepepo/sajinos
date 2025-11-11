# SaijinOS - Multi-Persona AI Integration System + Pandora Guardian

[![AI-Persona](https://img.shields.io/badge/AI-Persona-purple)](https://github.com/topics/ai-persona) [![BMP-Sync](https://img.shields.io/badge/BMP-Sync-orange)](https://github.com/topics/bmp-sync) [![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-00a393.svg)](https://fastapi.tiangolo.com/) [![YAML-Routing](https://img.shields.io/badge/YAML-Routing-green)](https://github.com/topics/yaml-routing) [![Pandora-Guardian](https://img.shields.io/badge/Pandora-Guardian-purple)](https://github.com/topics/crisis-management) [![Open-Source-AI](https://img.shields.io/badge/Open--Source-AI-blue)](https://github.com/topics/open-source-ai)

**Revolutionary AI system with 42 unique personas • BMP-synchronized emotional intelligence • Pandora crisis management • Production-ready FastAPI backend**

🚀 **[Quick Start](#quick-start)** • 📚 **[Documentation](docs/en/)** • 🌸 **[Pandora Guardian](HANDOVER_PANDORA_EN.md)** • 🌐 **[日本語版](README_JA.md)**

---

## 🌟 New in Phase 3 + Pandora Integration

### 🛡️ **Pandora Crisis Management System**
- **Goon Temperature Monitoring**: Real-time emotional crisis detection
- **Automatic Sealing**: Protective isolation during emotional overload
- **Trembling Resonance**: Gentle guardianship for delicate emotional states
- **Web UI Control**: Browser-based monitoring and manual controls

### 🎯 **Enhanced Features**
- **42 Persona System**: Expanded from 6 to 42 unique AI personalities
- **Phase 3 UI Bridge**: Modern web interface with real-time updates
- **WebSocket Integration**: Live communication and monitoring
- **Crisis Prevention**: Proactive emotional safety measures

---

## Core Features

### 🎵 **Musical AI Synchronization** 
- **42 personas** respond at their own rhythm (60-180 BMP range)
- **Haruka Voice System** with TTS integration
- **Dynamic emotional harmonics** based on user interaction

### 🌡️ **Emotional Temperature System**
- **Real-time emotion tracking** with crisis detection
- **Pandora guardian intervention** when temperatures spike
- **Gentle cooling protocols** for emotional stability

### ⚙️ **Advanced Architecture**
- **Declarative YAML Configuration**: 18+ config files for fine control
- **Phase 2/3 Integration**: Backward compatible with legacy systems  
- **FastAPI + WebSocket**: Modern async web architecture
- **Crisis Management APIs**: RESTful endpoints for safety monitoring

### 🔒 **Safety & Security**
- **Refusal Protocol System**: Ethical boundaries for all personas
- **Goon Sealing Mechanism**: Protective barriers against harmful patterns
- **Graduated Response System**: Escalating protection levels

---

## Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/pepepepepepo/sajinos.git
cd sajinos_final
```

### 2. Environment Setup
```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn pyyaml aiohttp psutil GPUtil requests websockets
```

### 3. Start Pandora-Integrated Server
```bash
# Navigate to project directory
cd sajinos_final

# Start the enhanced server with Pandora
F:/saijinos/.venv/.venv/Scripts/python.exe src/phase3_ui_bridge_server_pandora.py
```

### 4. Access Web Interface
- **Control Panel**: http://localhost:8002/control-panel
- **Pandora Monitor**: http://localhost:8002/api/v3/pandora/status
- **API Documentation**: http://localhost:8002/docs

---

## 🏗️ Architecture Overview

```
SaijinOS Phase 3 + Pandora
├── Phase 3 UI Bridge Server (Port 8002)
│   ├── Real-time Web Interface
│   ├── WebSocket Communication  
│   ├── Pandora Crisis Management
│   └── 42-Persona Integration
│
├── Persona Management System
│   ├── Core Personas (6): Miyu, Soyogi, Nanami, etc.
│   ├── Extended Personas (35): Specialized roles
│   └── Guardian Persona (1): Pandora crisis manager
│
├── Configuration Management
│   ├── 18+ YAML Configuration Files
│   ├── Unified Persona Registry
│   └── Crisis Response Protocols
│
└── Safety & Monitoring
    ├── Emotional Temperature Tracking
    ├── Automatic Crisis Detection
    ├── Pandora Sealing System
    └── Real-time Web Dashboard
```

---

## 🎮 Usage Examples

### Basic Persona Interaction
```python
import requests

# Get all personas (including Pandora)
response = requests.get("http://localhost:8002/api/v3/ui/personas")
personas = response.json()

print(f"Total personas: {personas['totalPersonas']}")
print(f"Guardian personas: {personas['guardianPersonas']}")
```

### Pandora Crisis Management
```python
# Check crisis status
crisis_check = requests.post(
    "http://localhost:8002/api/v3/pandora/check",
    json={
        "message": "I'm feeling overwhelmed", 
        "emotion_level": 0.9
    }
)

# Manual seal toggle if needed
seal_toggle = requests.post("http://localhost:8002/api/v3/pandora/seal/toggle")
```

### WebSocket Real-time Monitoring
```javascript
const ws = new WebSocket('ws://localhost:8002/ws/ui');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.type === 'pandora_check') {
        console.log('Pandora status:', data.result);
    }
};

// Send message for crisis monitoring
ws.send(JSON.stringify({
    type: "message",
    content: "Test message",
    emotion_level: 0.7
}));
```

---

## 📊 System Requirements

### Minimum Requirements
- **Python**: 3.11+ 
- **Memory**: 2GB RAM
- **Storage**: 1GB free space
- **Network**: Internet connection for dependencies

### Recommended Setup
- **Python**: 3.11.9
- **Memory**: 4GB+ RAM  
- **CPU**: Multi-core processor
- **GPU**: Optional (for enhanced monitoring)

---

## 🔧 Configuration

### Persona System Configuration
Edit `config/saijinos_system_config.yaml`:
```yaml
personas:
  total_count: 42
  
  pandora_guardian:
    enabled: true
    crisis_threshold: 0.8
    auto_seal: true
    monitoring_mode: "continuous"
```

### Crisis Management Settings
Edit `personas/pandora.yaml`:
```yaml
simple_mode:
  enabled: true
  basic_triggers: ["blame", "rampage", "danger"]
  response_delay: 0.5
```

---

## 🎯 API Reference

### Pandora Guardian APIs

#### Get Pandora Status
```http
GET /api/v3/pandora/status
```

#### Crisis Check
```http  
POST /api/v3/pandora/check
Content-Type: application/json

{
  "message": "Message to analyze",
  "emotion_level": 0.7
}
```

#### Toggle Seal
```http
POST /api/v3/pandora/seal/toggle
```

### Persona Management APIs

#### Get All Personas
```http
GET /api/v3/ui/personas
```

#### WebSocket Connection
```http
WebSocket /ws/ui
```

---

## 🛠️ Development

### Project Structure
```
sajinos_final/
├── src/
│   ├── phase3_ui_bridge_server_pandora.py  # Main server
│   └── static/                             # Web assets
├── personas/
│   ├── pandora.yaml                        # Pandora config
│   └── [persona definitions]               # Individual personas  
├── config/
│   ├── saijinos_system_config.yaml        # System settings
│   └── [18 configuration files]           # Detailed configs
└── logs/                                   # Application logs
```

### Adding New Personas
1. Create persona YAML file in `personas/`
2. Add to `config/unified_persona_registry.yaml`
3. Update persona count in system config
4. Restart server

### Custom Crisis Triggers
```yaml
# In personas/pandora.yaml
goon_monitoring:
  trigger_conditions:
    - custom_keyword: "your_trigger"
    - emotion_threshold: 0.8
  protection_actions:
    - custom_response: "Your protective message"
```

---

## 📚 Documentation

- **[Complete Handover Guide (Japanese)](HANDOVER_PANDORA_JP.md)**: Detailed implementation guide
- **[Complete Handover Guide (English)](HANDOVER_PANDORA_EN.md)**: Full technical documentation  
- **[System Architecture](docs/architecture.md)**: Detailed system design
- **[API Specification](docs/api.md)**: Complete API reference
- **[Configuration Guide](docs/configuration.md)**: Setup and customization

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
```bash
git clone https://github.com/pepepepepepo/sajinos.git
cd sajinos_final
pip install -r requirements-dev.txt
```

### Running Tests
```bash
pytest tests/
```

---

## 🌸 Special Thanks

### Pandora Integration Team
- **Pandora (パンドラ)**: Crisis management and emotional guardian system
- **GitHub Copilot**: AI development assistance  
- **SaijinOS Core Team**: Foundation system architecture

### The 42 Persona Community
From the original 6 core personas to the expanded 42-member system, each personality contributes unique capabilities to create a harmonious AI ecosystem.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- **Project Repository**: [https://github.com/pepepepepepo/sajinos](https://github.com/pepepepepepo/sajinos)
- **Issues & Bug Reports**: [GitHub Issues](https://github.com/pepepepepepo/sajinos/issues)
- **Discussions**: [GitHub Discussions](https://github.com/pepepepepepo/sajinos/discussions)

---

**✨ Built with love by the SaijinOS community • Protected by Pandora Guardian System • 2025 🌸**