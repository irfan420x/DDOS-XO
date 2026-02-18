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

## 🚀 Key Features (v2.2 Upgrade)

### 🧠 Central Personality Engine
- **Strict Identity Control**: LUNA's personality is strictly controlled via `config/system_prompt.txt`.
- **Personality Validation**: Automatically detects and corrects identity drift (e.g., if the model forgets it's LUNA).
- **Bilingual Support**: Fully capable of communicating in **English** and **Bengali** naturally.

### 🛠️ Unified LLM Abstraction
- **API Mode**: High-performance models (DeepSeek, OpenAI, Anthropic, Gemini).
- **Local Mode**: Privacy-focused offline use via **Ollama** or **llama.cpp**.
- **Hybrid Mode**: Dynamically switches between Local and API based on task complexity.

### 📂 Self-Evolving Memory
- **Long-term Context**: Uses a vector database (ChromaDB) to remember past interactions and user preferences.
- **Infinite Recall**: LUNA recalls relevant past memories to provide context-aware assistance.

### 🌐 Real-time Web Awareness
- **Live Search**: LUNA can search Google for real-time information, news, and documentation.
- **Content Extraction**: Fetches and summarizes webpage content for deep analysis.

### 🛡️ Hardened Security Sentinel
- **Port Monitoring**: Detects unauthorized open ports.
- **Process Sentinel**: Monitors for suspicious processes (miners, netcats) and high CPU usage.
- **Regex Blacklist**: Prevents dangerous shell commands with advanced pattern matching.

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
