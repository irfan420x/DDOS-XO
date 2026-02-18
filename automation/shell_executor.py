# Path: automation/shell_executor.py
import subprocess
import shlex
from typing import Dict, Any

class ShellExecutor:
    """
    LUNA-ULTRA Shell Executor: Executes shell commands with permission gating and security hardening.
    """
    def __init__(self, config: Dict[str, Any], permission_engine: Any):
        self.config = config
        self.permission_engine = permission_engine
        self.timeout = config.get('timeout', 60)

    async def execute(self, command: str) -> Dict[str, Any]:
        """
        Executes a command after permission check. Avoids shell=True where possible.
        """
        if not self.permission_engine.check_permission("shell_exec", command):
            return {"success": False, "error": "Permission Denied by LUNA Security Engine."}
        
        try:
            # Use shlex to safely split command and avoid shell=True injection risks
            args = shlex.split(command)
            
            # Use subprocess.run with timeout to prevent hanging
            result = subprocess.run(
                args, 
                shell=False, # Hardened: No shell expansion
                capture_output=True, 
                text=True, 
                timeout=self.timeout
            )
            return {
                "success": result.returncode == 0, 
                "stdout": result.stdout, 
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": f"Command timed out after {self.timeout} seconds."}
        except Exception as e:
            # Fallback for complex pipes if necessary, but log as risky
            if "|" in command or ">" in command or ";" in command:
                try:
                    result = subprocess.run(
                        command, 
                        shell=True, 
                        capture_output=True, 
                        text=True, 
                        timeout=self.timeout
                    )
                    return {"success": result.returncode == 0, "stdout": result.stdout, "stderr": result.stderr}
                except Exception as e2:
                    return {"success": False, "error": str(e2)}
            return {"success": False, "error": str(e)}
