# Path: agents/code_agent.py
import subprocess
from typing import Dict, Any

class CodeAgent:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.max_retries = 5

    def execute_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        if language == "python":
            try:
                result = subprocess.run(["python3", "-c", code], capture_output=True, text=True, timeout=30)
                return {
                    "success": result.returncode == 0,
                    "stdout": result.stdout,
                    "stderr": result.stderr
                }
            except Exception as e:
                return {"success": False, "error": str(e)}
        return {"success": False, "error": f"Language {language} not supported"}
