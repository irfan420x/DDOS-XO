# Path: core/controller.py
import asyncio
import yaml
import os
from typing import Dict, Any, Optional, List
from llm.router import LLMRouter
from security.permission_engine import PermissionEngine
from memory.memory_manager import MemoryManager
from core.orchestrator import Orchestrator
from core.state_manager import StateManager
from core.cognitive_mode import CognitiveMode

class LunaController:
    """
    The central brain of LUNA-ULTRA. Coordinates all modules and agents.
    """
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = config_path
        self.config = self.load_config()
        self.llm_router = LLMRouter(self.config.get('llm', {}))
        self.permission_engine = PermissionEngine(self.config.get('permissions', {}))
        self.memory_manager = MemoryManager(self.config.get('memory', {}))
        self.state_manager = StateManager()
        self.cognitive_mode = CognitiveMode()
        self.orchestrator = Orchestrator(self)
        self.system_prompt = self.load_system_prompt()

    def load_config(self) -> Dict[str, Any]:
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return {}

    def load_system_prompt(self) -> str:
        prompt_path = "config/system_prompt.txt"
        if os.path.exists(prompt_path):
            with open(prompt_path, 'r') as f:
                return f.read()
        return "You are LUNA-ULTRA, a professional AI agent."

    async def process_input(self, user_input: str) -> str:
        """
        Main entry point for user interaction.
        """
        self.state_manager.set_state("thinking")
        
        # 1. Detect Cognitive Mode
        mode = self.cognitive_mode.detect_mode(user_input)
        self.state_manager.set_mode(mode)
        
        # 2. Retrieve context from memory
        context = self.memory_manager.get_context(user_input)
        
        # 3. Build full prompt
        full_prompt = f"Context: {context}\nMode: {mode}\nUser: {user_input}"
        
        # 4. Get response from LLM
        response = await self.llm_router.generate_response(full_prompt, self.system_prompt)
        
        # 5. Store interaction in memory
        self.memory_manager.store_interaction(user_input, response)
        
        self.state_manager.set_state("idle")
        return response

    def get_status(self) -> Dict[str, Any]:
        return {
            "state": self.state_manager.get_state(),
            "mode": self.state_manager.get_mode(),
            "permission": self.permission_engine.current_level.name,
            "provider": self.llm_router.default_provider,
            "user": self.config.get('user', {}).get('name', 'IRFAN')
        }
