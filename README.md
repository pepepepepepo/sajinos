<<<<<<< HEAD
# 🌸 SaijinOS - Multi-Persona AI Integration System

> **Revolutionary AI system evolving from 6 to 41 unique personas**  
> *Beautiful, intelligent, and reliable multi-persona management system*

[![AI-Persona](https://img.shields.io/badge/AI-Persona-purple)](https://github.com/topics/ai-persona) [![BMP-Sync](https://img.shields.io/badge/BMP-Sync-orange)](https://github.com/topics/bmp-sync) [![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-00a393.svg)](https://fastapi.tiangolo.com/) [![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org) [![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)]() [![Status](https://img.shields.io/badge/Status-Phase%203%20Complete-success.svg)]()

🚀 **[Quick Start](#quick-start)** • 📚 **[Phase 3 Features](#phase-3-features)** • 🌐 **[日本語版](README_JA.md)** • 📖 **[Documentation](docs/en/)**

---

## 🌟 **Project Evolution**

### **Phase 3 (Current)** - UI Bridge & Pandora Guardian System ✨
**SaijinOS Phase 3** は、41個の個性豊かなペルソナを管理する高度なWebシステムです。美しいUI、堅牢なバックエンド、そして強力なパンドラ・ガーディアンシステムによる危機管理機能を備えています。

### **Previous Phases**
- **Phase 1-2**: 6-persona BMP-synchronized emotional intelligence system
- **Foundation**: Musical AI synchronization, emotional temperature recording

## 🎯 **Phase 3 Features**

### **✨ Latest Innovations**
- 🎭 **41-Persona System**: Each with unique personality and specialized skills
- 🛡️ **Pandora Guardian**: Advanced crisis detection & management system
- 🎨 **Beautiful UI**: Responsive and interactive web interface  
- ⚡ **High-Speed API**: FastAPI-based optimized RESTful API
- 🧪 **Comprehensive Testing**: Automated test suites for quality assurance
- 📦 **Modular Architecture**: Maintainability and scalability focused structure

### **🌟 Core Capabilities**
- **Musical AI Synchronization**: BMP-synchronized emotional intelligence (Legacy)
- **Emotional Temperature Recording**: Conversation warmth tracking
- **Declarative YAML Routing**: Persona definitions via config files
- **Lightweight Deployment**: FastAPI + SQLite minimal setup

---

## 🚀 **Quick Start**

### **1. Clone Repository**
```bash
git clone https://github.com/pepepepepepo/sajinos.git
cd sajinos
```

### **2. Environment Setup**
```bash
# 仮想環境の作成と有効化
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Mac/Linux

# 依存関係のインストール
pip install -r requirements.txt
```

### **3. Configuration**
Copy `.env.example` to `.env` and customize (optional):
```env
API_PORT=8002
PERSONAS_DIR=./personas
```

### **4. Launch Phase 3 System**
```bash
# Phase 3 UI Bridge Server (Latest)
python src/phase3_ui_bridge_server_modular.py

# Quick Test
python quick_test.py
```

### **5. Access Points**

- **Phase 3 UI**: http://localhost:8002
- **API Documentation**: http://localhost:8002/docs  
- **Persona Management**: http://localhost:8002/admin
- **Pandora Guardian**: http://localhost:8002/api/v3/pandora/status

---

## 🏗️ **システム構造**

```
saijinos/
├── 📁 src/
│   ├── 📄 phase3_ui_bridge_server_modular.py  # メインサーバー (85行)
│   └── 📁 core/
│       ├── 📁 personas/
│       │   ├── 📄 __init__.py
│       │   └── 📄 persona_manager.py           # ペルソナ管理 (134行)
│       ├── 📁 ui/
│       │   ├── 📄 __init__.py  
│       │   └── 📄 ui_handler.py                # UI処理 (33行)
│       └── 📁 pandora/
│           ├── 📄 __init__.py
│           └── 📄 guardian_system.py           # パンドラシステム (200+行)
├── 📁 tests/
│   ├── 📄 test_persona_api.py                  # API テスト (270行)
│   └── 📄 test_module_integrity.py             # モジュールテスト
├── 📄 quick_test.py                            # クイックテスト (67行)
├── 📄 HANDOVER_20251110.md                     # 引継書
└── 📄 TOMORROW_SCHEDULE_20251111.md            # 作業予定表
```

---

## 🎭 **ペルソナシステム**

### **ペルソナカテゴリ**

| カテゴリ | 人数 | 特徴 | 代表例 |
|---------|------|------|--------|
| 🌸 **自然・花** | 8名 | 美しさ・癒し・成長 | 花詠🌺, 桜雅🌸 |
| ⭐ **宇宙・星** | 6名 | 神秘・知識・導き | ミレア💫, ステラ⭐ |  
| 🔥 **魔法・元素** | 9名 | 力・変化・創造 | 火鈴🔥, 継⚡ |
| 🏔️ **自然力** | 7名 | 安定・保護・純粋 | エルザ❄️, 翠嵐🌪️ |
| 🎄 **季節・祝祭** | 5名 | 喜び・祝福・絆 | ノエリ🎄, 恵🍂 |
| 💎 **宝石・輝き** | 6名 | 美・永続・価値 | ルミフィエ✨, 瑞希💎 |

### **ペルソナAPI例**

```python
# 全ペルソナ取得
GET /api/v3/personas/all

# 特定ペルソナ取得  
GET /api/v3/personas/{persona_name}

# ペルソナ検索
GET /api/v3/personas/search?category=自然
```

---

## 🛡️ **パンドラ・ガーディアンシステム**

### **危機管理機能**

- 🔍 **自動検出**: システム異常の自動検知
- 📊 **状態管理**: リアルタイム状態モニタリング  
- 🚨 **アラート**: 危機レベル別通知システム
- 🔧 **自動復旧**: 可能な問題の自動修復
- 📝 **ログ管理**: 詳細な活動履歴保存

### **パンドラAPI例**

```python
# パンドラ状態確認
GET /api/v3/pandora/status

# 危機検出実行
POST /api/v3/pandora/detect_crisis

# ガーディアン呼び出し
POST /api/v3/pandora/call_guardian
```

---

## 🧪 **テスト実行**

### **全テスト実行**

```bash
# APIテスト
python -m pytest tests/test_persona_api.py -v

# モジュール整合性テスト  
python tests/test_module_integrity.py

# クイックテスト
python quick_test.py
```

### **テストカバレッジ**

- ✅ **ペルソナAPI**: 全エンドポイント
- ✅ **パンドラシステム**: 危機検出・管理  
- ✅ **UI機能**: 基本表示・操作
- ✅ **モジュール整合性**: インポート・依存関係
- ✅ **エラーハンドリング**: 例外処理

---

## 🔧 **開発・運用**

### **設定**

```python
# config/settings.py
SERVER_HOST = "localhost"  
SERVER_PORT = 8002
DEBUG_MODE = True
LOG_LEVEL = "INFO"
```

### **ログ出力例**

```
2024-11-10 18:30:15 [INFO] Server starting on http://localhost:8002
2024-11-10 18:30:16 [INFO] Loaded 41 personas successfully
2024-11-10 18:30:16 [INFO] Pandora Guardian System initialized
2024-11-10 18:30:17 [INFO] All systems ready ✨
```

### **パフォーマンス**

- 🚀 **起動時間**: < 3秒
- ⚡ **API応答**: < 100ms (平均)
- 💾 **メモリ使用量**: < 200MB
- 📦 **ファイルサイズ**: 800+ 行 (8ファイル)

---

## 📈 **今後の予定**

### **Phase 3 完了項目** ✅
- [x] モジュラー化リファクタリング
- [x] パンドラシステム統合
- [x] 包括的テストスイート  
- [x] APIドキュメント整備
- [x] エラーハンドリング強化

### **次期計画** 🔮
- [ ] WebSocketリアルタイム機能
- [ ] Docker化・コンテナ対応
- [ ] セキュリティ強化 (認証・CORS)
- [ ] パフォーマンス最適化
- [ ] 国際化対応 (i18n)
- [ ] CI/CDパイプライン

---

## 🤝 **貢献・サポート**

### **開発チーム**

**明日の担当ペルソナ (2025/11/11):**
- 🌺 **花詠** (READMEアート・詩的表現)
- 💫 **ミレア** (宇宙規模設計・最適化)  
- ⚡ **継** (パフォーマンス・エネルギー効率)
- ❄️ **エルザ** (完璧テスト・品質保証)
- ✨ **ルミフィエ** (UI/UX・光る体験)
- 🎄 **ノエリ** (品質管理・幸福度向上)

### **お問い合わせ**

- 📧 **Email**: saijinos@example.com
- 📱 **Discord**: SaijinOS Community
- 🐙 **GitHub**: [saijinos/phase3](https://github.com/saijinos/phase3)

---

## 📜 **ライセンス**

```
MIT License - 自由に使用・改変・配布可能
Copyright (c) 2024 SaijinOS Project
```

---

## 🌈 **メッセージ**

> *「技術と美しさの調和を通じて、  
> より良いデジタル世界を創造します」*  
> 
> — **SaijinOS Development Team** 🌸✨

---

**🎯 最終更新**: 2024年11月10日  
**🔖 バージョン**: Phase 3.0 - Modular & Pandora Integration  
**👥 開発状況**: アクティブ開発中 🚀

**素晴らしい一日を！** 💖🌸✨
=======
﻿# SaijinOS - Multi-Persona AI Integration System

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
>>>>>>> 9732929528fa0ee2098912020cd38338e5907ca0
