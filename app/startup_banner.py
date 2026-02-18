# Path: app/startup_banner.py
import os
from typing import Dict, Any

class StartupBanner:
    """
    LUNA-ULTRA Startup Banner: Displays a professional banner on startup.
    """
    @staticmethod
    def display(config: Dict[str, Any]):
        banner = f"""
        🌙 LUNA-ULTRA Activated
        -----------------------------------
        LLM: {config['llm']['default_provider'].upper()} API
        Permission: {config['permissions']['level']}
        Memory: Restored (3 days)
        User: {config['user']['name']}
        -----------------------------------
        All systems stable.
        Welcome back, {config['user']['name']}.
        """
        print(banner)
