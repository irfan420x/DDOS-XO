# Path: README.md

# JARVIS-CORE v2.0.0-PRO
**Author:** IRFAN  
**Status:** Production-Grade AI Control System

JARVIS-CORE is a highly advanced, modular AI desktop agent designed for total system control, automation, and intelligent assistance. Version 2.0.0-PRO introduces a refined architecture focused on performance, security, and scalability.

## 🚀 Key Features
- **Advanced Core Engine:** Asynchronous, event-driven architecture with multi-threading support.
- **Pro Security Framework:** Granular permission levels (SAFE to ROOT) with real-time safety filtering.
- **Intelligent LLM Routing:** Dynamic switching between local (Ollama) and cloud (OpenAI) backends.
- **Modular Ecosystem:** Isolated components for Vision, Voice, Shell, and System Control.
- **Offline-First:** Designed to run entirely locally for maximum privacy.
- **Vector Memory:** Long-term context retention using vector database integration.

## 📂 Project Structure
```text
jarvis-v2/
├── main.py             # Entry point
├── core/               # Engine & Config Management
├── security/           # Permission & Safety Framework
├── llm/                # LLM Routing & History
├── modules/            # Functional Modules (Vision, Voice, etc.)
├── gui/                # PyQt6 Pro Dashboard
├── config/             # YAML Configuration
├── data/               # Persistent Memory & Vector DB
└── logs/               # Audit Logs & Session Data
```

## 🛠 Installation
1. **Clone & Setup:**
   ```bash
   git clone https://github.com/Irfan430/DDOS-XO.git
   cd DDOS-XO
   pip install -r requirements.txt
   ```
2. **Configure:**
   Edit `config/config.yaml` to set your preferred backends and security levels.
3. **Run:**
   ```bash
   python main.py
   ```

## 🔒 Security Policy
JARVIS-CORE implements a strict "Safe-by-Default" policy. All actions are audited and passed through a multi-stage safety filter before execution. ROOT access requires explicit token validation.

---
*Built with ❤️ by IRFAN*
