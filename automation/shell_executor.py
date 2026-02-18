# Path: automation/shell_executor.py
import subprocess
from typing import Dict, Any

class ShellExecutor:
    """
    LUNA-ULTRA Shell Executor: Executes shell commands with permission gating.
    """
    def __init__(self, config: Dict[str, Any], permission_engine: Any):
        self.config = config
        self.permission_engine = permission_engine
        self.timeout = config.get('timeout', 60)

    async def execute(self, command: str) -> Dict[str, Any]:
        if not self.permission_engine.check_permission("shell_exec", command):
            return {"success": False, "error": "Permission Denied."}
        
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=self.timeout)
            return {"success": result.returncode == 0, "stdout": result.stdout, "stderr": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}
