# 🏗️ LUNA-ULTRA: Structural Audit Report

## 1. Core Architecture
- **Boot Flow**: `app/main.py` -> `app/bootstrap.py` -> `core/controller.py`.
- **Orchestrator**: `core/orchestrator.py` handles intent analysis and agent routing.
- **Agents**: Specialized agents in `agents/` (Architect, Code, Dynamic, etc.).
- **Memory**: `memory/memory_manager.py` manages short-term JSON and long-term ChromaDB.
- **Security**: `security/` handles permissions, sandboxing, and sentinel monitoring.
- **Automation**: `automation/` handles shell, peripheral, and telegram control.

## 2. LLM Routing Logic
- Uses `llm/router.py` to interface with `DeepSeek` (default).
- Orchestrator uses a "Thinking Phase" (Inner Monologue) to decide between CHAT and ACTION.

## 3. Tool Execution Flow
- Orchestrator parses LLM response into a JSON plan.
- Steps are executed sequentially via agent `execute()` methods.
- Results are stored in `state_manager.py` for persistence.

## 4. Dependency Structure
- Currently a single `requirements.txt` containing all dependencies (some heavy like `sentence-transformers`).

## 5. Config Structure
- Monolithic `config/config.yaml` containing LLM, security, vision, and user settings.

## 6. Optional Modules
- **Voice**: Integrated in `gui/voice_engine.py`.
- **Vision**: Integrated in `vision/vision_loop.py`.
- **Telegram**: Integrated in `automation/telegram_controller.py`.
- **Sentinel**: Integrated in `security/security_sentinel.py`.

---
*Status: Audit Complete. Ready for Phase 1 Refactoring.*
