# Path: core/controller.py
import asyncio
import yaml
import os
import logging
from typing import Dict, Any, Optional, List
from llm.router import LLMRouter
from security.permission_engine import PermissionEngine
from memory.memory_manager import MemoryManager
from core.orchestrator import Orchestrator
from core.state_manager import StateManager
from core.cognitive_mode import CognitiveMode
from security.sandbox_executor import SandboxExecutor
from automation.telegram_controller import TelegramController
from vision.vision_loop import VisionLoop

class LunaController:
    """
    The central brain of LUNA-ULTRA. Coordinates all modules and agents.
    """
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = config_path
        self.config = self.load_config()
        self.llm_router = LLMRouter(self.config.get("llm", {}))
        self.permission_engine = PermissionEngine(self.config.get("permissions", {}))
        self.sandbox_executor = SandboxExecutor(self.config.get("security", {}), self.permission_engine) # Pass permission_engine
        self.memory_manager = MemoryManager(self.config.get("memory", {}))
        self.state_manager = StateManager()
        self.cognitive_mode = CognitiveMode()
        self.orchestrator = Orchestrator(self)
        self.telegram = TelegramController(self.config, self)
        self.vision_loop = VisionLoop(self)
        self.system_prompt = self.load_system_prompt()
        logging.info("LunaController initialized.")

    async def start_services(self):
        """Starts background services like Telegram Bot and Vision Loop."""
        if self.telegram.enabled:
            asyncio.create_task(self.telegram.run_bot())
            await self.telegram.send_notification("System Online and Ready.")
        
        if self.vision_loop.enabled:
            asyncio.create_task(self.vision_loop.start())

    async def shutdown_services(self):
        """Shuts down background services."""
        if self.telegram.enabled:
            await self.telegram.stop_bot()
        
        if self.vision_loop.running:
            await self.vision_loop.stop()

    def load_config(self) -> Dict[str, Any]:
        try:
            with open(self.config_path, "r") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logging.error(f"Config file not found at {self.config_path}")
            return {}

    def load_system_prompt(self) -> str:
        prompt_path = "config/system_prompt.txt"
        if os.path.exists(prompt_path):
            with open(prompt_path, "r") as f:
                return f.read()
        return "You are LUNA-ULTRA, a professional AI agent."

    async def process_input(self, user_input: str) -> str:
        """
        Main entry point for user interaction. Now uses Orchestrator to handle tasks.
        """
        self.state_manager.set_state("thinking")
        logging.info(f"Processing user input: {user_input}")
        
        # 1. Detect Cognitive Mode
        mode = self.cognitive_mode.detect_mode(user_input)
        self.state_manager.set_mode(mode)
        
        # 2. Orchestrate the task
        response = await self.orchestrator.handle_task(user_input) # Delegate to orchestrator
        
        # 3. Store interaction in memory
        self.memory_manager.store_interaction(user_input, str(response)) # Store full response
        
        self.state_manager.set_state("idle")
        logging.info("Task processing complete.")
        return str(response) # Return string representation of the response

    def get_status(self) -> Dict[str, Any]:
        return {
            "state": self.state_manager.get_state(),
            "mode": self.state_manager.get_mode(),
            "permission": self.permission_engine.current_level.name,
            "provider": self.llm_router.default_provider,
            "user": self.config.get("user", {}).get("name", "IRFAN"),
            "os_type": self.orchestrator.agents.get("dynamic").os_type if "dynamic" in self.orchestrator.agents else "N/A"
        }
