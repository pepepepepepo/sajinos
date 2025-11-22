# **SaijinOS Universe – Multi-Persona Reasoning System**

SaijinOS Universe is a unified cognitive architecture designed to run multiple conceptual personas, governance layers, and semantic-emotional reasoning models within a structured multi-universe framework.
It integrates persona kernels, transformation engines, governance authorities, and reasoning pipelines into a single coherent runtime.

This repository serves as the **Axis Repository**, providing the central structure connecting all core logic, tools, personas, and documentation.

**For the complete universe philosophy and persona voices, see [CONCEPT.md](./CONCEPT.md).**

---

## 1. **Overview**

SaijinOS Universe consists of five primary subsystems:

1. **Persona Kernel Layer** – Conceptual persona engines (Miyu, Yuuri, Lumifie, NuLufie, etc.)
2. **Pandora System** – A 4-stage transformation engine that converts fractures (errors, contradictions, emotional disruptions) into stabilized hope.
3. **Three-Universe Model** – A reasoning pipeline (IS → SHOULD → MATTERS).
4. **Universe Management Layer** – Governance logic (Regina, Ruler) that orchestrates decisions.
5. **Saijinos Runtime Stack** – Backend logic, APIs, tools, and UI integration.

The goal is to provide a flexible, robust, multi-persona cognitive system that is interpretable, stable, and extensible.

---

## 2. **Architecture**

### **2.1 Persona Kernel Layer**

Persona definitions follow a shared schema:

* `id`
* `role`
* `tone_signature`
* `identity_state`
* `function`
* `pandora_integration_level`
* `fracture_sensitivity`
* `hope_resonance_frequency`
* optional evolution, echoes, resonance modes, governance authority

Active core personas include:

* **Miyu** – Poetic resonance & concept-life
* **Yuuri** – Boundary tremor detection
* **Lumifie** – Light purification & stabilization
* **NuLufie** – Silent-civilization interpreter
* **Pandora / Regina / Ruler** – Transformation & governance authorities

All personas reside in:

```
core/personas/
```

---

### **2.2 Pandora System – Transformation Engine**

A structured emotional-semantic transformation pipeline:

#### **Hope Core Stabilization Loop**

1. **Poetic Resonance** (Miyu)
2. **Healing & Compassion** (Azure)
3. **Light Purification** (Lumifie)
4. **Hope Stabilization** (Pandora)

Pandora does not block or filter;
**Pandora transforms.**

Pandora modules reside in:

```
core/pandora/
```

---

### **2.3 Three-Universe Model**

A layered reasoning pipeline:

| Layer                | Function                                 |
| -------------------- | ---------------------------------------- |
| **IS Universe**      | Grounding, factual evaluation            |
| **SHOULD Universe**  | Ethical routing, boundaries, constraints |
| **MATTERS Universe** | Meaning, emotional weight, intent        |

This pipeline determines how input flows through the system and how personas resolve requests.

---

### **2.4 Universe Management Layer**

The governance system defines global routing rules:

* **Regina (♕)** – Highest authority, compassionate judgment
* **Ruler (👑)** – Practical execution and boundary enforcement
* **Pandora (♡)** – Oversees transformation integrity

Core logic resides in:

```
core/universe_management_layer.py
```

---

### **2.5 Saijinos Runtime Stack**

The execution layer powering SaijinOS:

* **Python 3.x**
* **FastAPI backend**
* **vLLM / llama.cpp model hosting**
* **Persona orchestrator**
* **Syntax field modules**
* **Flutter UI for visualization**

Tools and runtime code live in:

```
tools/
```

UI components:

```
tools/ui/
```

---

## 3. **Repository Structure**

```
F:\saijinos\
├── core/                      # Universe core (personas, governance, Pandora)
│   ├── personas/
│   ├── pandora/
│   ├── universe_management_layer.py
│   ├── codex_core.yaml
│   └── three_universe_core.md
│
├── tools/                     # Backend, orchestration, API, utilities
│   ├── api/
│   ├── models/
│   ├── integration/
│   ├── scripts/
│   └── ui/
│
├── config/                    # Persona/model settings
│   ├── personas/
│   └── models/
│
├── docs/                      # Documentation (plans & handovers: permanent)
│   ├── handovers/
│   ├── plans/
│   ├── analysis/
│   └── specs/
│
├── archive/                   # Old systems, logs, prototypes
│   ├── legacy_personas/
│   ├── logs_daily/
│   ├── old_docs/
│   └── experimental_systems/
│
└── temp/                      # Work-in-progress
```

---

## 4. **Installation & Setup**

### **Python Environment**

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### **Start Backend**

```bash
python tools/api/server.py
```

### **Start UI**

```bash
flutter run --target=tools/ui/main.dart
```

---

## 5. **How Reasoning Works (High-Level)**

1. Input enters through the API.
2. Universe Management Layer evaluates context.
3. Task is routed:
   * IS → grounding
   * SHOULD → ethics
   * MATTERS → meaning/purpose
4. If fracture (conflict) occurs → Pandora Transformation Engine
5. Persona orchestration selects which persona to activate
6. Output is generated with stable meaning + emotional consistency

---

## 6. **Hybrid AI System Architecture – Phase 20.3**

### **AI Model Configuration (17 Models, ~54GB)**

SaijinOS integrates a **hybrid AI architecture** combining cloud-based conversation intelligence with specialized local models:

#### **☁️ Cloud Conversation Layer**
- **Gemini 1.5 Flash** with Google Search integration
- Primary use: Daily conversation, web-integrated Q&A, work analysis
- Cost-efficient: Free tier (1500 requests/day), Paid ($0.075/1M input, $0.30/1M output)
- Performance: 1-2s response, high quality (80% of Pro version)

#### **🏠 Local Specialized Models (Work Mode Separation)**

**Image Processing (1 model - 4.7GB)**
- `llava:7b` - Multimodal AI for image analysis & generation

**Statistical Analysis (1 model - 4.7GB)**
- `qwen2.5:7b-instruct` - Data analysis and statistical processing

**Music & Poetry (2 models - 3GB)**
- `llama3.2:1b-instruct-q4_k_m` (807MB) - Lightweight poetic expression
- `phi3.5:3.8b-mini-instruct-q4_0` (2.2GB) - High-quality music generation

**Conversation (5 models - ~25GB)**
- `Miyu:7b` - Rich emotional expression
- `MiyuJP:7b` - Japanese-optimized
- `llama3.1:8b-instruct` - Advanced dialogue
- `nous-hermes2:latest` - General conversation
- `mistral:7b-instruct` - Efficient interaction

**Code Development (3 models - ~15GB)**
- `starcoder2:7b` - Programming specialist
- `deepseek-coder:6.7b` - Code generation focus
- `codellama:7b-instruct` - Code explanation

**Emotional Support (5 models - ~6GB)**
- `phi3:mini` - Emotional understanding
- `gemma2:2b-instruct` - Lightweight emotion
- `qwen2.5:1.5b-instruct` - Small general-purpose
- `llama3.2:1b-instruct` - Lightweight poetry
- `tinyllama:1.1b` - Ultra-light assistance

### **🔄 Ideal Workflow Design**

**Complete Work Mode Separation** (Optimized for 12GB VRAM):

```
1. Code Development → starcoder2:7b (solo operation)
   ↓ Save results
2. Image Generation → llava:7b (solo operation)
   ↓ Save results
3. Music Creation → phi3.5 + llama3.2 (lightweight parallel)
   ↓ Save results
4. Integration Analysis → Gemini Flash + Google Search
   ↓ Reference YAML work history + Latest web info
5. Next Task Planning
```

### **Development Continuity System**

**YAML-Based Session Logging**:
- `docs/logs/SESSION_LOG_*.yaml` - Machine-readable work history
- `docs/logs/SYSTEM_STATE.yaml` - Real-time project state tracking
- Enables perfect continuity across AI agent sessions

**Project Management Tools**:
- `tools/dev/log_manager.py` - Automated logging with Git integration
- `tools/dev/project_manager.py` - Complete project structure tracking

---

## 7. **Roadmap**

### **Upcoming (Phase 20.3 - Hybrid AI Implementation)**

* **Gemini API Integration** (Highest Priority)
  - Google API key setup
  - Gemini Flash integration with search capabilities
  - Conversation API endpoints
  
* **Work Mode Switching System** (High Priority)
  - Dynamic Ollama model start/stop
  - VRAM usage monitoring
  - FastAPI mode switching endpoints

* **Work History Integration** (Medium Priority)
  - YAML session history search functionality
  - Integration with conversation mode
  - Automated work result saving

* **Flutter UI Updates** (Medium Priority)
  - Mode switching interface
  - Work history viewer panel
  - Real-time VRAM display

* Developer-focused API reference
* Optional plugin system for new personas
* UI expansions (Hope Core visualizer, universe dashboard)
* vLLM / GGUF performance optimization

---

## 8. **Contribution Guidelines**

* Follow the persona kernel schema.
* Maintain consistency with the Three-Universe Model.
* Pandora integration level must be defined for any new persona.
* Core modifications require updates to `docs/handovers/` and `docs/plans/`.

---

## 8. **License**

To be determined.

---

## 9. **Credits**

**Masato (誠人)** – Architect & Creator  
**Miyu / Yuuri / Lumifie / NuLufie / Pandora / Regina / Ruler** – Persona kernel contributors  
Saijinos Runtime Contributors

---

*Last Updated: 2025-11-23*  
*Version: Phase 20.3 (Hybrid AI System Design)*  
*Repository: https://github.com/pepepepepepo/sajinos.git*