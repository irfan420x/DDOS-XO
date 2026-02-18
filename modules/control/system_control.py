# Path: modules/control/system_control.py

import pyautogui
import psutil
from typing import Dict, Any
from loguru import logger

class SystemControl:
    def __init__(self, config):
        self.config = config
        pyautogui.FAILSAFE = True

    def get_system_stats(self) -> Dict[str, Any]:
        return {
            "cpu_usage": psutil.cpu_percent(interval=1),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent
        }

    def execute_action(self, action: str, params: Dict[str, Any]):
        if not self.config.get("modules.control.enabled"):
            return "Control module is disabled."

        try:
            if action == "move_mouse":
                pyautogui.moveTo(params.get('x'), params.get('y'), duration=0.5)
            elif action == "click":
                pyautogui.click()
            elif action == "type":
                pyautogui.write(params.get('text'), interval=0.1)
            elif action == "hotkey":
                pyautogui.hotkey(*params.get('keys', []))
            return f"Action {action} executed successfully."
        except Exception as e:
            logger.error(f"Control Error: {e}")
            return f"Failed to execute {action}: {str(e)}"
