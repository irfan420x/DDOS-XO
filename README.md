# 🌙 LUNA-ULTRA (DDOS-XO) - v2.2+
### The Ultimate Autonomous AI Architect & OS Control Center

<p align="center">
  <img src="https://img.shields.io/badge/Version-2.2-blueviolet?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/Main_Brain-DeepSeek-blue?style=for-the-badge" alt="Brain">
  <img src="https://img.shields.io/badge/GUI-PyQt6-orange?style=for-the-badge" alt="GUI">
  <img src="https://img.shields.io/badge/Security-Hardened-red?style=for-the-badge" alt="Security">
</p>

LUNA-ULTRA is a next-generation autonomous agent designed for **Full OS Control**, **Project Architecture**, and **System Automation**. This version transforms LUNA into a modern AI Control Center with a PyQt6 dashboard, hardened security, and natural voice interaction.

---

## 🚀 Key Features (v2.3 Advanced Upgrade)

### 🧠 Central Personality Engine & Voice Emotion
- **Strict Identity Control**: LUNA's personality is strictly controlled via `config/system_prompt.txt`.
- **Voice Emotion Analysis**: LUNA can analyze user tone and adapt its response style (Bengali/English).
- **Personality Validation**: Automatically detects and corrects identity drift.

### 🛠️ Unified LLM & Self-Reflective Debugging
- **Thought Loop**: LUNA enters a self-reflective loop to fix its own code and plan errors autonomously.
- **Multi-Agent Collaboration**: Internal agents (Architect, Coder, Security) collaborate on complex tasks.
- **Unified LLM**: Supports API, Local (Ollama), and Hybrid modes.

### 📂 Self-Evolving Memory & Skill Acquisition
- **Infinite Memory**: Uses ChromaDB for long-term context and past interaction recall.
- **Autonomous Skill Acquisition**: LUNA can search for, write, and install its own "Skills" (plugins) to handle new tasks.

### 🌐 Web Awareness & Predictive Maintenance
- **Live Web Search**: Real-time Google search and content extraction.
- **System Health Sentinel**: Monitors CPU, RAM, Temp, and Disk health. Provides predictive maintenance alerts.

### 🛡️ Hardened Security & HUD Overlay
- **Security Sentinel**: Monitors ports, suspicious processes, and high resource usage.
- **HUD Overlay**: A transparent status indicator for real-time system and LUNA activity.
- **Regex Blacklist**: Advanced pattern matching for shell command safety.

---

## 🛠️ How to Use LUNA-ULTRA

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/Irfan430/DDOS-XO.git
cd DDOS-XO

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
- **API Keys**: Open the GUI and enter your API keys in the left panel, or edit `config/config.yaml`.
- **System Prompt**: Customize LUNA's personality in `config/system_prompt.txt`.
- **Local LLM**: Ensure Ollama is running if using Local Mode.

### 3. Running the Agent
```bash
python -m app.main
```

---

## 🎮 Feature Usage Guide

### 💬 Chat & Interaction
- Simply type in the chat box or speak after saying the wake word **"LUNA"**.
- LUNA will respond in the language you use (English/Bengali).

### 🏗️ Project Architect Mode
- **Command**: "Plan and build a Python Flask web app with a login page."
- **Action**: LUNA will create the folder structure, write all necessary files, and even generate a `requirements.txt`.

### 🌐 Web Search
- **Command**: "What is the latest version of Python and what are its new features?"
- **Action**: LUNA will search the web, visit relevant pages, and provide a summarized report.

### 🛡️ Security Monitoring
- The **Security Sentinel** runs in the background.
- If a new port is opened or a suspicious process starts, an alert will appear in the **Activity Feed**.

### ⚙️ Dynamic Mode Switching
- Use the **LLM Mode** dropdown in the GUI to switch between **API**, **Local**, and **Hybrid** modes on the fly.
- Change the **Personality Profile** to adjust LUNA's tone (Professional, Hacker, Friendly, Minimal).

---

## 📂 Project Structure
- `app/`: Application lifecycle and startup.
- `core/`: Orchestrator, Personality Engine, and State Management.
- `agents/`: Specialized agents (Architect, Code, System, etc.).
- `llm/`: Unified Router and Provider implementations.
- `gui/`: PyQt6 Dashboard and Voice Engine.
- `automation/`: Shell, Browser, and System control.
- `security/`: Permission Engine and Security Sentinel.
- `memory/`: Short-term and Long-term (ChromaDB) memory.

---

## 🌟 Proposed Future Features
1. **Telegram/Discord Remote Control**: Control LUNA from anywhere via chat bots.
2. **Autonomous Task Chaining**: Break down complex goals into multi-step autonomous plans.
3. **Multi-Modal Vision**: Real-time screen understanding and OCR for visual help.
4. **Auto-Security Sentinel Expansion**: Automatic firewall rules and threat mitigation.

---
**Created by IRFAN** | *LUNA is always learning.*
