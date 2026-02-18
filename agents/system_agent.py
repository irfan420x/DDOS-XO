# Path: agents/system_agent.py
import os
# import psutil
from typing import Dict, Any

class SystemAgent:
    """
    LUNA-ULTRA System Agent: Handles OS control and monitoring.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    async def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if action == "get_health":
            # cpu = psutil.cpu_percent()
            # ram = psutil.virtual_memory().percent
            return {"success": True, "cpu": "N/A", "ram": "N/A"}
        elif action == "list_files":
            path = params.get('path', '.')
            files = os.listdir(path)
            return {"success": True, "files": files}
        return {"error": f"Action {action} not supported"}
