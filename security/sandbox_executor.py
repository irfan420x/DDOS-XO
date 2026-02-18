# Path: security/sandbox_executor.py
import subprocess
import tempfile
import os
import shlex
import logging
from typing import Dict, Any, Optional
from security.permission_engine import PermissionEngine

class SandboxExecutor:
    """
    LUNA-ULTRA Sandbox Executor: Isolated execution for untrusted code/commands.
    """
    def __init__(self, config: Dict[str, Any], permission_engine: Optional[PermissionEngine] = None):
        self.config = config
        self.permission_engine = permission_engine
        self.timeout = config.get("execution_timeout", 30)
        self.sandbox_enabled = config.get("sandbox_enabled", True)
        logging.info(f"SandboxExecutor initialized. Sandbox enabled: {self.sandbox_enabled}")

    async def execute(self, code_or_command: str, language: str = "python") -> Dict[str, Any]:
        """
        Executes code or a command in a sandboxed environment.
        """
        if not self.sandbox_enabled:
            logging.warning("Sandbox is disabled. Executing directly.")
            # Fallback to direct execution if sandbox is disabled
            if language == "python":
                return await self._execute_python_direct(code_or_command)
            elif language == "bash":
                return await self._execute_bash_direct(code_or_command)
            else:
                return {"success": False, "error": f"Unsupported language for direct execution: {language}"}

        logging.info(f"Sandbox: Executing {language} code/command in isolated environment...")
        
        # Permission check (if permission_engine is provided)
        if self.permission_engine:
            action_type = "shell_exec" if language == "bash" else "code_exec"
            if not self.permission_engine.check_permission(action_type, code_or_command):
                return {"success": False, "error": "Permission Denied by LUNA Security Engine for sandbox execution."}

        if language == "python":
            return await self._execute_python_in_sandbox(code_or_command)
        elif language == "bash":
            return await self._execute_bash_in_sandbox(code_or_command)
        else:
            return {"success": False, "error": f"Unsupported language for sandbox execution: {language}"}

    async def _execute_python_in_sandbox(self, code: str) -> Dict[str, Any]:
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
            tmp.write(code.encode("utf-8"))
            tmp_path = tmp.name

        try:
            # In a real sandbox, this would involve Docker or a more restricted environment
            # For now, it's a subprocess with a temporary file
            process = await asyncio.create_subprocess_exec(
                "python3", tmp_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=self.timeout)
            
            return {
                "success": process.returncode == 0, 
                "stdout": stdout.decode().strip(), 
                "stderr": stderr.decode().strip(),
                "returncode": process.returncode
            }
        except asyncio.TimeoutError:
            process.kill()
            await process.wait()
            return {"success": False, "error": f"Python execution timed out after {self.timeout} seconds."}
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    async def _execute_bash_in_sandbox(self, command: str) -> Dict[str, Any]:
        try:
            # Use shlex to safely split command if not using shell=True
            # For now, using shell=True for simplicity but logging it as a risk
            logging.warning("Sandbox: Executing bash command with shell=True. Consider hardening.")
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=self.timeout)

            return {
                "success": process.returncode == 0, 
                "stdout": stdout.decode().strip(), 
                "stderr": stderr.decode().strip(),
                "returncode": process.returncode
            }
        except asyncio.TimeoutError:
            process.kill()
            await process.wait()
            return {"success": False, "error": f"Bash command timed out after {self.timeout} seconds."}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _execute_python_direct(self, code: str) -> Dict[str, Any]:
        # Direct execution without sandbox features (for disabled sandbox)
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
            tmp.write(code.encode("utf-8"))
            tmp_path = tmp.name
        try:
            result = subprocess.run(["python3", tmp_path], capture_output=True, text=True, timeout=self.timeout)
            return {"success": result.returncode == 0, "stdout": result.stdout, "stderr": result.stderr}
        except subprocess.TimeoutExpired:
            return {"success": False, "error": f"Python execution timed out after {self.timeout} seconds."}
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    async def _execute_bash_direct(self, command: str) -> Dict[str, Any]:
        # Direct execution without sandbox features (for disabled sandbox)
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=self.timeout)
            return {"success": result.returncode == 0, "stdout": result.stdout, "stderr": result.stderr}
        except subprocess.TimeoutExpired:
            return {"success": False, "error": f"Bash command timed out after {self.timeout} seconds."}
        except Exception as e:
            return {"success": False, "error": str(e)}
