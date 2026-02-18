# 🌙 LUNA-ULTRA

<p align="center">
  <img src="https://img.shields.io/badge/LUNA--ULTRA-vFinal-blueviolet?style=for-the-badge&logo=moon" alt="LUNA-ULTRA">
  <img src="https://img.shields.io/badge/Architecture-Single%20LLM-blue?style=for-the-badge" alt="Architecture">
  <img src="https://img.shields.io/badge/Main%20Brain-DeepSeek-green?style=for-the-badge" alt="Main Brain">
</p>

---

## 🧠 Overview
**LUNA-ULTRA** is a next-generation AI agent system designed for power, security, and elegance. Built with a single LLM architecture (defaulting to DeepSeek), it provides a unified brain for all agentic tasks including coding, automation, vision, and system control.

### 🚀 Key Features
- **Single LLM Brain**: Unified intelligence using DeepSeek API for stable and consistent behavior.
- **Hybrid Ultra Architecture**: Combines local execution with cloud-based intelligence.
- **Modern Dark GUI**: A beautiful, professional interface for seamless interaction.
- **Strict Permission System**: Multi-level security (SAFE, STANDARD, ADVANCED, ROOT) to protect your system.
- **Self-Healing Code Loop**: Automatically detects and fixes errors in generated code.
- **3-Day Rolling Memory**: Context-aware memory with vector storage and auto-summarization.
- **Vision & Emotion**: On-demand screen capture and emotion detection capabilities.

---

## 🏗 Project Structure
```text
luna-ultra/
├── app/            # Application lifecycle and startup
├── core/           # Orchestrator and state management
├── agents/         # Specialized agents (Code, Screen, Emotion, etc.)
├── llm/            # LLM Router and API providers
├── memory/         # Vector store and memory management
├── automation/     # Shell, Mouse, Keyboard, Browser control
├── vision/         # Screen capture and OCR
├── security/       # Permission and policy engines
├── gui/            # Modern Dark UI panels and widgets
└── config/         # Configuration and system prompts
```

---

## 🛠 Installation & Setup

### Prerequisites
- Python 3.10+
- DeepSeek API Key (or OpenAI/Anthropic)

### Quick Start
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

## 🔐 Security Levels
- **SAFE**: Read-only access. No system changes allowed.
- **STANDARD**: File and application level access.
- **ADVANCED**: Shell and Docker execution allowed.
- **ROOT**: Full system control. Use with caution.

---

## 🐳 Docker Support
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
