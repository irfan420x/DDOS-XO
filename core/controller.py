# Path: core/controller.py
import os
import yaml
import logging
import asyncio
from typing import Dict, Any

from llm.router import LLMRouter
from security.permission_engine import PermissionEngine
from memory.memory_manager import MemoryManager
from core.orchestrator import Orchestrator
from core.state_manager import StateManager
from core.cognitive_mode import CognitiveMode
from security.sandbox_executor import SandboxExecutor
from core.skill_manager import SkillManager
from core.module_loader import ModuleLoader

class LunaController:
    """
    The central brain of LUNA-ULTRA. Coordinates all modules and agents.
    """
    def __init__(self, config_dir: str = "config"):
        self.config_dir = config_dir
        self.config = self.load_modular_configs()
        
        # Core Components
        self.llm_router = LLMRouter(self.config.get("llm", {}))
        from core.personality_engine import PersonalityEngine
        self.personality_engine = PersonalityEngine(self.config)
        self.permission_engine = PermissionEngine(self.config.get("security", {}))
        self.sandbox_executor = SandboxExecutor(self.config.get("security", {}), self.permission_engine)
        self.memory_manager = MemoryManager(self.config.get("features", {}).get("memory", {}))
        self.state_manager = StateManager()
        self.cognitive_mode = CognitiveMode()
        self.skill_manager = SkillManager()
        self.orchestrator = Orchestrator(self)
        
        # Optional Modules (Loaded Safely)
        self.telegram = self.init_optional_module("automation.telegram_controller", "TelegramController", self)
        self.vision_loop = self.init_optional_module("vision.vision_loop", "VisionLoop", self)
        self.security_sentinel = self.init_optional_module("security.security_sentinel", "SecuritySentinel", self)
        
        self.system_prompt = self.load_system_prompt()
        logging.info("LunaController: Modular initialization complete.")

    def load_modular_configs(self) -> Dict[str, Any]:
        combined_config = {}
        config_files = ["core.yaml", "llm.yaml", "security.yaml", "automation.yaml", "features.yaml"]
        for cf in config_files:
            path = os.path.join(self.config_dir, cf)
            if os.path.exists(path):
                with open(path, "r") as f:
                    combined_config.update(yaml.safe_load(f) or {})
            else:
                logging.warning(f"LunaController: Config file {cf} missing.")
        return combined_config

    def init_optional_module(self, module_path: str, class_name: str, *args):
        module_class = ModuleLoader.safe_import(module_path, class_name)
        if module_class:
            try:
                return module_class(*args)
            except Exception as e:
                logging.error(f"LunaController: Failed to initialize {class_name}: {e}")
        return None

    async def start_services(self):
        """Starts background services safely."""
        if self.telegram and self.config.get("automation", {}).get("telegram", {}).get("enabled"):
            asyncio.create_task(self.telegram.run_bot())
            await self.telegram.send_notification("System Online and Ready.")
        
        if self.vision_loop and self.config.get("features", {}).get("vision", {}).get("enabled"):
            asyncio.create_task(self.vision_loop.start())
        
        if self.security_sentinel and self.config.get("security", {}).get("sentinel_enabled"):
            asyncio.create_task(self.security_sentinel.start())

    async def shutdown_services(self):
        """Shuts down background services safely."""
        if self.telegram:
            await self.telegram.stop_bot()
        if self.vision_loop and hasattr(self.vision_loop, 'running') and self.vision_loop.running:
            await self.vision_loop.stop()
        if self.security_sentinel and hasattr(self.security_sentinel, 'running') and self.security_sentinel.running:
            await self.security_sentinel.stop()

    def load_system_prompt(self) -> str:
        path = "config/system_prompt.txt"
        if os.path.exists(path):
            with open(path, "r") as f:
                return f.read()
        return "You are LUNA-ULTRA, a professional AI assistant."

    async def process_input(self, user_input: str) -> str:
        """Central entry point for user input."""
        response_data = await self.orchestrator.handle_task(user_input)
        
        if response_data.get("type") == "chat":
            response = response_data.get("response")
        else:
            # Handle tool execution results
            results = response_data.get("results", [])
            if results:
                last_res = results[-1].get("result", {})
                response = f"Task completed: {last_res.get('output', 'Success')}"
            else:
                response = "Action performed."
        
        # Store in memory
        self.memory_manager.store_interaction(user_input, response)
        return response

    def update_config(self, new_config: Dict[str, Any]):
        """
        Updates the system configuration dynamically and reloads affected modules.
        """
        logging.info(f"LunaController: Updating configuration: {new_config}")
        
        # 1. Update internal config dictionary
        for section, values in new_config.items():
            if section not in self.config:
                self.config[section] = {}
            self.config[section].update(values)
            
        # 2. Update LLM Router if needed
        if "llm" in new_config:
            self.llm_router.mode = self.config["llm"].get("mode", "api")
            self.llm_router.default_provider = self.config["llm"].get("default_provider", "deepseek")
            self.llm_router.enforce_personality = self.config["llm"].get("enforce_personality", True)
            if "api_keys" in new_config["llm"]:
                for provider, key in new_config["llm"]["api_keys"].items():
                    if provider in self.llm_router.providers:
                        self.llm_router.providers[provider].api_key = key
        
        # 2.1 Update Personality Engine if needed
        if "personality" in new_config:
            self.personality_engine.profile = self.config["personality"].get("profile", "professional")
            self.llm_router.personality_engine.profile = self.personality_engine.profile
        
        # 3. Update Permission Engine if needed
        if "permissions" in new_config or "security" in new_config:
            from security.permission_engine import PermissionLevel
            level_str = self.config.get("permissions", {}).get("level") or self.config.get("security", {}).get("level", "SAFE")
            self.permission_engine.current_level = PermissionLevel[level_str]
            
        # 4. Update Voice Engine via GUI if available
        if "gui" in new_config and hasattr(self, 'gui') and self.gui:
            if "voice_mode" in new_config["gui"]:
                self.gui.voice_engine.toggle(new_config["gui"]["voice_mode"])

    def get_status(self) -> Dict[str, Any]:
        return {
            "state": "IDLE",
            "mode": "COGNITIVE",
            "permission": self.config.get("permissions", {}).get("level") or self.config.get("security", {}).get("level", "STANDARD"),
            "provider": self.config.get("llm", {}).get("default_provider", "deepseek")
        }
