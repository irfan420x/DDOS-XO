# 🌙 LUNA-ULTRA (DDOS-XO) - v2.5
### The Ultimate Autonomous AI Architect & OS Control Center

<p align="center">
  <img src="https://img.shields.io/badge/Version-2.5-blueviolet?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/Main_Brain-DeepSeek-blue?style=for-the-badge" alt="Brain">
  <img src="https://img.shields.io/badge/GUI-PyQt6-orange?style=for-the-badge" alt="GUI">
  <img src="https://img.shields.io/badge/Security-Hardened-red?style=for-the-badge" alt="Security">
</p>

**LUNA-ULTRA** is a state-of-the-art autonomous agent designed for **Full OS Control**, **Project Architecture**, and **System Automation**. This version elevates LUNA into a sophisticated AI Control Center with a sleek PyQt6 dashboard, hardened security protocols, and natural voice interaction, now featuring a Manus AI-style **Resume Engine** for unparalleled reliability.

---

## 🚀 Key Features (v2.5 Advanced Upgrade)

### 🧠 **Central Personality Engine & Voice Emotion**
- **Strict Identity Control**: LUNA's personality is meticulously managed via `config/system_prompt.txt`, ensuring consistent and predictable interactions.
- **Voice Emotion Analysis**: LUNA intelligently analyzes user tone and adapts its response style, seamlessly switching between Bengali and English.
- **Personality Validation**: The system automatically detects and corrects any identity drift, maintaining its core persona.

### 🛠️ **Unified LLM & Self-Reflective Debugging**
- **Thought Loop**: LUNA employs a self-reflective loop to autonomously fix its own code and planning errors, ensuring robust and continuous operation.
- **Multi-Agent Collaboration**: Internal agents (Architect, Coder, Security) collaborate on complex tasks, simulating a team of experts.
- **Unified LLM**: Supports API, Local (Ollama), and Hybrid modes, providing flexibility and control over LLM usage.

### 📂 **Self-Evolving Memory & Skill Acquisition**
- **Infinite Memory**: Utilizes ChromaDB for long-term context and recall of past interactions, enabling it to learn and grow over time.
- **Autonomous Skill Acquisition**: LUNA can autonomously search for, write, and install its own "Skills" (plugins) to handle new and unforeseen tasks.

### 🔄 **NEW: State Persistence & Auto-Resume Engine**
- **Automatic State Saving**: In case of an LLM token limit error or other interruptions, LUNA automatically saves the complete execution state.
- **Seamless Resumption**: Simply type `resume` to continue the task from the exact point of interruption, ensuring no loss of progress.
- **Context Compression**: Intelligently compresses the context before resuming to avoid repeated token limit errors.

---

## 🛠️ Installation & Setup

### 1. System Requirements
- **Python**: 3.11+ recommended
- **Operating System**: Linux (Ubuntu/Debian), macOS, or Windows (with WSL)
- **RAM**: Minimum 4GB (8GB+ recommended for vision features)

### 2. Manual System Dependencies
Some features require system-level packages that cannot be installed via pip. Please run the following commands based on your OS:

#### Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install -y tesseract-ocr tesseract-ocr-eng tesseract-ocr-ben portaudio19-dev python3-pyaudio python3-pyqt6
```

#### macOS:
```bash
brew install tesseract tesseract-lang portaudio
```

### 3. Python Dependencies Installation
```bash
# Clone the repository
git clone https://github.com/Irfan430/DDOS-XO.git
cd DDOS-XO

# Install all Python dependencies
pip install -r requirements.txt
```

### 4. Configuration
- **API Keys**: Launch the GUI and enter your API keys in the Settings panel, or edit `config/llm.yaml` directly.
- **System Prompt**: Customize LUNA's personality in `config/system_prompt.txt`.

---

## 🎮 Running LUNA-ULTRA

### GUI Mode (Default):
```bash
python -m app.main
```

### CLI Mode:
```bash
python -m app.main --cli
```

---

## 📂 Project Structure

```
DDOS-XO/
├── app/                    # Application lifecycle and startup
├── core/                   # Orchestrator, Personality Engine, State Management, Resume Engine
├── agents/                 # Specialized agents (Architect, Code, System, etc.)
├── llm/                    # Unified Router and Provider implementations
├── gui/                    # PyQt6 Dashboard and Voice Engine
├── security/               # Permission Engine and Security Sentinel
├── memory/                 # Short-term and Long-term (ChromaDB) memory
├── config/                 # Configuration files (YAML, system prompt)
├── requirements.txt        # Complete Python dependencies
└── README.md               # This file
```

---

## 📜 License
This project is open-source and available under the **MIT License**.

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

---

**Created by IRFAN** | *LUNA is always learning.*
