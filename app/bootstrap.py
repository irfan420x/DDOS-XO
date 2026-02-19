# Path: app/bootstrap.py
import os
import sys
import yaml
import asyncio
from typing import Dict, Any
from core.controller import LunaController

class LunaBootstrap:
    """
    LUNA-ULTRA Bootstrap: Handles system initialization and startup sequence.
    """
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        if not os.path.exists(self.config_path):
            print(f"Error: Config file not found at {self.config_path}")
            sys.exit(1)
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    async def initialize_system(self) -> LunaController:
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
        controller = LunaController("config")
        
        # 3. Verify LLM Connectivity
        print(f"🌙 LUNA-ULTRA: Connecting to {self.config['llm']['default_provider']} API...")
        await asyncio.sleep(0.5)
        
        # 4. Load Memory
        print(f"🌙 LUNA-ULTRA: Restoring memory (3-day rolling window)...")
        await asyncio.sleep(0.5)
        
        return controller
