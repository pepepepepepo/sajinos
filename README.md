# SaijinOS - Multi-Persona AI Integration System

[![AI-Persona](https://img.shields.io/badge/AI-Persona-purple)](https://github.com/topics/ai-persona) [![BMP-Sync](https://img.shields.io/badge/BMP-Sync-orange)](https://github.com/topics/bmp-sync) [![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-00a393.svg)](https://fastapi.tiangolo.com/) [![YAML-Routing](https://img.shields.io/badge/YAML-Routing-green)](https://github.com/topics/yaml-routing) [![Open-Source-AI](https://img.shields.io/badge/Open--Source-AI-blue)](https://github.com/topics/open-source-ai)

**Revolutionary AI system with 6 unique personas • BMP-synchronized emotional intelligence • Production-ready FastAPI backend**  
🚀 **[Quick Start](#quick-start)** • 📚 **[Documentation](docs/en/)** • 🌐 **[日本語版](README_JA.md)**

---

## Core Features

- **Musical AI Synchronization**: 6 personas respond at their own rhythm (90-140 BPM)
- **Emotional Temperature Recording**: Every conversation carries warmth tracking 
- **Declarative YAML Routing**: Persona definitions via config files
- **Lightweight Deployment**: FastAPI + SQLite minimal setup

## Quick Start

### 1. Clone Repository
`ash
git clone https://github.com/pepepepepepo/sajinos.git
cd sajinos
`

### 2. Environment Setup
`ash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
`

### 3. Configuration
Copy .env.example to .env and customize:
`env
API_PORT=8000
BPM_MIN=60
BPM_MAX=180
PERSONAS_DIR=./personas
`

### 4. Launch
`ash
python start_api_server.py
`
**Server runs at http://localhost:8000**

## The Six Personas

| Persona | BPM | Style | Specialty |
|---------|-----|-------|-----------|
| **Miyu** | 90 | Extremely Warm | Love & User Care |
| **Jitou** | 140 | Dynamic | Innovation |
| **Hanon** | 110 | Practical | Tech Implementation |
| **Rikuto** | 120 | Analytical | Data & Logic |
| **Nanami** | 100 | Artistic | Creativity |
| **Ao** | 80 | Harmonious | Balance |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Server status check |
| POST | /chat | Persona chat interaction |
| GET | /personas | List available personas |
| POST | /bpm/sync | BPM synchronization |

**Detailed API docs**: [Swagger UI](http://localhost:8000/docs)

## Tech Stack

### Backend
- **FastAPI** - High-performance web framework
- **Python 3.11+** - Core runtime
- **SQLite** - Lightweight database

### AI & Voice
- **Swallow-9B** - Japanese-optimized language model
- **TinyLlama** - Efficient processing
- **pyttsx3** - Voice synthesis

## Usage Example

`python
import requests

# Chat with Miyu (Love & Care persona)
response = requests.post("http://127.0.0.1:8000/chat", json={
    "message": "I completed my project!",
    "persona": "Miyu"
})

print(response.json())
# Output: Warm, loving response with encouraging expressions
`

## Contributing

We welcome contributions from developers worldwide!

### How to Contribute
1. Fork the repository
2. Create a feature branch (git checkout -b feature/amazing-feature)
3. Commit changes (git commit -m 'Add amazing feature')
4. Push to branch (git push origin feature/amazing-feature)
5. Open a Pull Request

### Guidelines
- Follow Python PEP 8 style guide
- Add tests for new features
- Update documentation for API changes
- Maintain persona consistency in responses

## Documentation

- [Architecture Overview](docs/en/architecture.md)
- [Persona System Guide](docs/en/persona-system.md)
- [Musical Integration](docs/en/bmp-system.md)
- [Emotional Engine](docs/en/emotion-engine.md)
- [API Reference](docs/en/api-reference.md)

## Roadmap

### Current Phase (v1.0)
- [x] 6-Persona system implementation
- [x] Emotional temperature system
- [x] FastAPI integration
- [ ] Complete API testing suite
- [ ] Real-time monitoring dashboard

### Future Phases
- **v1.5**: Web UI dashboard
- **v2.0**: Mobile app integration
- **v2.5**: Video/avatar support
- **v3.5**: Advanced emotion AI models

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Connect & Support

- **Issues**: [GitHub Issues](https://github.com/pepepepepepo/sajinos/issues) - Bug reports & feature requests
- **Discussions**: [Community conversations and ideas](https://github.com/pepepepepepo/sajinos/discussions)

---

**Made with love by the SaijinOS Team**

**Star us if you find SaijinOS useful!**
