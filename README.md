# 🌙 DDOS-XO: Autonomous Architect & OS Agent (v2.0 Upgrade)

<p align="center">
  <img src="https://img.shields.io/badge/LUNA--ULTRA-v2.0--Upgrade-blueviolet?style=for-the-badge&logo=moon" alt="LUNA-ULTRA">
  <img src="https://img.shields.io/badge/Architecture-Single%20LLM-blue?style=for-the-badge" alt="Architecture">
  <img src="https://img.shields.io/badge/Main%20Brain-DeepSeek-green?style=for-the-badge" alt="Main Brain">
  <img src="https://img.shields.io/badge/Security-Hardened%20OS-red?style=for-the-badge" alt="Security">
</p>

LUNA-ULTRA is a next-generation autonomous agent designed for full OS control and project architecture. This v2.0 upgrade transforms LUNA into a modern AI Control Center with a PyQt6 dashboard, hardened security, and natural voice interaction.

## 🚀 Key Features (v2.0)
- **Modern 3-Panel Dashboard**: Redesigned PyQt6 GUI with real-time system monitoring (CPU/RAM), LLM status, and permission indicators.
- **Dynamic Configuration**: Update LLM providers, API keys, and permission levels directly from the GUI without restarting.
- **Hardened Security**: 
    - **Regex-based Blacklist**: Prevents dangerous commands with advanced pattern matching.
    - **Secure ShellExecutor**: No `shell=True` fallback, shlex-based command splitting, and dry-run mode.
    - **Audit Logging**: Detailed security logs for all sensitive actions.
- **Natural Voice Control**: 
    - **Wake Word**: Responds to "LUNA".
    - **Natural TTS**: Human-like reactions using gTTS.
    - **STT Integration**: Speech-to-text for hands-free operation.
- **Reasoning View**: Dedicated panel to see LUNA's internal thought process and planning.
- **Self-Healing Code Loop**: Automatically detects and fixes errors in generated code.

## 🛠️ Installation & Run
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Irfan430/DDOS-XO.git
   cd DDOS-XO
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install PyQt6 qtawesome psutil sounddevice soundfile SpeechRecognition gTTS pygame
   ```
3. **Run LUNA-ULTRA**:
   ```bash
   python -m app.main
   ```
   *Use `python -m app.main --cli` for terminal mode.*

## 🏗 Project Structure
```text
DDOS-XO/
├── app/            # Application lifecycle and startup
├── core/           # Orchestrator and dynamic controller
├── agents/         # Specialized agents (Architect, Code, Security)
├── llm/            # Single LLM Router (DeepSeek default)
├── memory/         # Session state and rolling memory
├── automation/     # Hardened Shell, Mouse, Keyboard control
├── vision/         # Screen awareness and OCR
├── security/       # Regex-based Permission & Audit engines
├── gui/            # PyQt6 3-Panel Dashboard & Voice Engine
└── config/         # Modular YAML configurations
```

## 🔐 Security Levels
- **SAFE**: Read-only access.
- **STANDARD**: File and application level access.
- **ADVANCED**: Shell and Docker execution allowed.
- **ROOT**: Full system control.

---
<p align="center">
  <i>"LUNA is fully operational. Welcome back, IRFAN."</i>
</p>

<p align="center">
  <b>Author: IRFAN</b>
</p>
