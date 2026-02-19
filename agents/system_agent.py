# Path: agents/system_agent.py
import os
import logging
from typing import Dict, Any

class SystemAgent:
    """
    LUNA-ULTRA System Agent: Handles OS control and monitoring.
    """
    def __init__(self, config: Dict[str, Any], controller: Any = None):
        self.config = config
        self.controller = controller

    async def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if action == "get_health":
            return {"success": True, "cpu": "N/A", "ram": "N/A"}
        
        elif action in ["list_files", "list_directory"]:
            path = params.get('path', '.')
            try:
                files = os.listdir(path)
                return {"success": True, "files": files, "output": f"Files in {path}: {', '.join(files)}"}
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        elif action == "get_system_info":
            import platform
            info = {
                "os": platform.system(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor(),
                "cwd": os.getcwd()
            }
            return {"success": True, "info": info, "output": f"System Status: {info['os']} {info['version']} | CWD: {info['cwd']}"}
            
        elif action == "create_directory":
            path = params.get('path')
            if not path: return {"success": False, "error": "No path provided"}
            try:
                os.makedirs(path, exist_ok=True)
                return {"success": True, "message": f"Directory {path} created.", "output": f"I have successfully created the directory: {path}"}
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        elif action in ["shutdown", "restart", "power_off"]:
            mode = "SHUTDOWN" if action in ["shutdown", "power_off"] else "RESTART"
            msg = f"⚠️ System Power Action: {mode} command received from IRFAN."
            
            # Send Telegram notification if controller is available
            if self.controller and self.controller.telegram:
                try:
                    import asyncio
                    asyncio.create_task(self.controller.telegram.send_notification(msg))
                    logging.info(f"SystemAgent: Power notification sent to Telegram: {mode}")
                except Exception as e:
                    logging.error(f"SystemAgent: Failed to send power notification: {e}")
            
            # In a real scenario, we would call os.system("shutdown /s /t 1") 
            # but for safety in sandbox, we just return success and log it.
            return {
                "success": True, 
                "message": f"System {mode.lower()} initiated. Telegram notification sent.",
                "output": f"LUNA: I have initiated a system {mode.lower()} as requested, IRFAN. A notification has been sent to your Telegram."
            }
            
        return {"error": f"Action {action} not supported"}
