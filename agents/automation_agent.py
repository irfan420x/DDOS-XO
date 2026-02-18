# Path: agents/automation_agent.py
from typing import Dict, Any
from automation.shell_executor import ShellExecutor
from automation.mouse_controller import MouseController
from automation.keyboard_controller import KeyboardController
from automation.browser_controller import BrowserController

class AutomationAgent:
    """
    LUNA-ULTRA Automation Agent: Handles task automation with permission gating.
    """
    def __init__(self, config: Dict[str, Any], permission_engine: Any):
        self.config = config
        self.permission_engine = permission_engine
        self.shell = ShellExecutor(config.get('automation', {}), permission_engine)
        self.mouse = MouseController(config.get('automation', {}))
        self.keyboard = KeyboardController(config.get('automation', {}))
        self.browser = BrowserController(config.get('automation', {}))

    async def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes automation actions with explicit permission checks.
        """
        if action == "shell_exec":
            return await self.shell.execute(params.get('command'))
            
        elif action == "mouse_click":
            if self.permission_engine.check_permission("mouse_click", f"Click at {params.get('x')}, {params.get('y')}"):
                self.mouse.click(params.get('x'), params.get('y'))
                return {"success": True}
            return {"success": False, "error": "Permission Denied"}
            
        elif action == "keyboard_type":
            if self.permission_engine.check_permission("keyboard_type", "Typing text"):
                self.keyboard.type(params.get('text'))
                return {"success": True}
            return {"success": False, "error": "Permission Denied"}
            
        elif action == "browser_open":
            if self.permission_engine.check_permission("read_file", f"Open URL: {params.get('url')}"):
                self.browser.open_url(params.get('url'))
                return {"success": True}
            return {"success": False, "error": "Permission Denied"}
            
        return {"error": f"Action {action} not supported"}
