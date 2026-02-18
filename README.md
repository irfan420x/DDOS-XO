# 🌙 LUNA-ULTRA: The Ultimate AI Companion

<p align="center">
  <img src="https://img.shields.io/badge/LUNA--ULTRA-vFinal-blueviolet?style=for-the-badge&logo=moon" alt="LUNA-ULTRA">
  <img src="https://img.shields.io/badge/Architecture-Single%20LLM-blue?style=for-the-badge" alt="Architecture">
  <img src="https://img.shields.io/badge/Main%20Brain-DeepSeek-green?style=for-the-badge" alt="Main Brain">
  <img src="https://img.shields.io/badge/Security-Gated%20OS-red?style=for-the-badge" alt="Security">
</p>

---

## 🧠 **Core Architecture**
**LUNA-ULTRA** is a professional-grade AI agent system designed for **IRFAN**. It features a unified brain architecture, advanced security gating, and a self-healing code execution loop.

### 🚀 **Key Features**
- **Single LLM Brain**: Unified intelligence using **DeepSeek API** for stable and consistent behavior.
- **Self-Healing Code Loop**: Automatically detects and fixes errors in generated code (up to 5 retries).
- **Strict Permission System**: Multi-level security (**SAFE, STANDARD, ADVANCED, ROOT**) to protect your system.
- **3-Day Rolling Memory**: Context-aware memory with vector storage and auto-summarization.
- **Modern Dark GUI**: A beautiful, professional interface for seamless interaction.
- **Vision & Emotion**: On-demand screen capture and emotion detection capabilities.

---

## 🏗 **Project Structure**
```text
luna-ultra/
├── app/            # Application lifecycle and startup
│   ├── main.py             # Main entry point
│   ├── bootstrap.py        # System initialization
│   ├── startup_banner.py   # Professional banner
│   └── lifecycle.py        # Shutdown and always-on
├── core/           # Orchestrator and state management
│   ├── controller.py       # Central brain
│   ├── orchestrator.py     # Multi-agent coordinator
│   ├── cognitive_mode.py   # Mode detection
│   └── state_manager.py    # System state
├── agents/         # Specialized agents
│   ├── code_agent.py       # Self-healing code agent
│   ├── screen_agent.py     # Vision agent
│   ├── emotion_agent.py    # Emotion detection
│   ├── automation_agent.py # Task automation
│   ├── system_agent.py     # OS control
│   └── security_agent.py   # Risk analysis
├── llm/            # LLM Router and API providers
│   ├── router.py           # Single brain router
│   ├── providers/          # API providers (DeepSeek, OpenAI, etc.)
│   └── response_parser.py  # Structured data parsing
├── memory/         # Vector store and memory management
│   ├── vector_store.py     # Long-term memory
│   ├── memory_manager.py   # 3-day rolling memory
│   └── summarizer.py       # Auto-summarization
├── automation/     # Shell, Mouse, Keyboard, Browser control
│   ├── shell_executor.py   # Gated shell execution
│   ├── mouse_controller.py # GUI automation
│   ├── keyboard_controller.py # Input automation
│   └── browser_controller.py # Web automation
├── vision/         # Screen capture and OCR
│   ├── screen_capture.py   # On-demand capture
│   ├── ocr_engine.py       # Text extraction
│   └── emotion_detector.py # Expression analysis
├── security/       # Permission and policy engines
│   ├── permission_engine.py # Gated OS control
│   ├── policy_engine.py    # Command blacklist
│   ├── sandbox_executor.py # Isolated execution
│   └── audit_logger.py     # Security logging
├── gui/            # Modern Dark UI
│   ├── main_window.py      # Main GUI window
│   ├── panels/             # UI panels
│   ├── widgets/            # Custom widgets
│   └── themes/             # Dark themes
└── config/         # Configuration and system prompts
    ├── config.yaml         # Main configuration
    └── system_prompt.txt   # LUNA's personality
```

---

## 🛠 **Installation & Setup**

### **Prerequisites**
- Python 3.10+
- DeepSeek API Key (or OpenAI/Anthropic)

### **Quick Start**
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Irfan430/DDOS-XO.git
   cd DDOS-XO
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure your API keys**:
   Edit `config/config.yaml` and add your DeepSeek API key.
4. **Run LUNA-ULTRA**:
   ```bash
   python app/main.py
   ```

---

## 🔐 **Security Levels**
- **SAFE**: Read-only access. No system changes allowed.
- **STANDARD**: File and application level access.
- **ADVANCED**: Shell and Docker execution allowed.
- **ROOT**: Full system control. Use with caution.

---

## 🐳 **Docker Support**
Build and run LUNA-ULTRA in a containerized environment:
```bash
docker build -t luna-ultra .
docker run -d luna-ultra
```

---

<p align="center">
  <i>"LUNA is fully operational. Welcome back, IRFAN."</i>
</p>

<p align="center">
  <b>Author: IRFAN</b>
</p>
