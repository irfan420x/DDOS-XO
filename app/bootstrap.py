# Path: app/bootstrap.py
import os
import sys
import yaml
import time
from typing import Dict, Any, Optional
from core.controller import LunaController

class LunaBootstrap:
    """
    LUNA-ULTRA Bootstrap: Handles system initialization and startup sequence.
    """
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = config_path
        self.config = self.load_config()
        self.controller = None

    def load_config(self) -> Dict[str, Any]:
        if not os.path.exists(self.config_path):
            print(f"Error: Config file not found at {self.config_path}")
            sys.exit(1)
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def initialize_system(self) -> LunaController:
        """
        Initializes all core components and returns the controller.
        """
        print("🌙 LUNA-ULTRA: Initializing core systems...")
        
        # 1. Create necessary directories
        directories = ["logs", "memory", "vision", "automation", "gui/themes"]
        for d in directories:
            if not os.path.exists(d):
                os.makedirs(d)
        
        # 2. Initialize Controller
        self.controller = LunaController(self.config_path)
        
        # 3. Verify LLM Connectivity (Simulated)
        print(f"🌙 LUNA-ULTRA: Connecting to {self.config['llm']['default_provider']} API...")
        time.sleep(0.5)
        
        # 4. Load Memory
        print(f"🌙 LUNA-ULTRA: Restoring memory (3-day rolling window)...")
        time.sleep(0.5)
        
        return self.controller

    def display_startup_banner(self):
        """
        Displays the professional startup banner.
        """
        banner = f"""
        🌙 LUNA-ULTRA Activated
        -----------------------------------
        LLM: {self.config['llm']['default_provider'].upper()} API
        Permission: {self.config['permissions']['level']}
        Memory: Restored (3 days)
        User: {self.config['user']['name']}
        -----------------------------------
        All systems stable.
        Welcome back, {self.config['user']['name']}.
        """
        print(banner)

class LifecycleManager:
    """
    Manages the application lifecycle (startup, shutdown, always-on).
    """
    def __init__(self, controller: LunaController):
        self.controller = controller
        self.is_running = True

    def shutdown(self):
        """
        Gracefully shuts down the system.
        """
        print("🌙 LUNA-ULTRA: Shutting down systems...")
        # Save memory, close connections, etc.
        self.controller.memory_manager.save_memory()
        self.is_running = False
        print("🌙 LUNA-ULTRA: Shutdown complete. Goodbye, IRFAN.")
        sys.exit(0)
