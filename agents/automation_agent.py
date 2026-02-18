# Path: agents/automation_agent.py
from typing import Dict, Any
from automation.shell_executor import ShellExecutor
from automation.mouse_controller import MouseController
from automation.keyboard_controller import KeyboardController
from automation.browser_controller import BrowserController

class AutomationAgent:
    """
    LUNA-ULTRA Automation Agent: Handles task automation.
    """
    def __init__(self, config: Dict[str, Any], permission_engine: Any):
        self.config = config
        self.shell = ShellExecutor(config.get('automation', {}), permission_engine)
        self.mouse = MouseController(config.get('automation', {}))
        self.keyboard = KeyboardController(config.get('automation', {}))
        self.browser = BrowserController(config.get('automation', {}))

    async def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if action == "shell_exec":
            return await self.shell.execute(params.get('command'))
        elif action == "mouse_click":
            self.mouse.click(params.get('x'), params.get('y'))
            return {"success": True}
        elif action == "keyboard_type":
            self.keyboard.type(params.get('text'))
            return {"success": True}
        elif action == "browser_open":
            self.browser.open_url(params.get('url'))
            return {"success": True}
        return {"error": f"Action {action} not supported"}
