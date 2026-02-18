# Path: modules/execution/executor.py

import subprocess
import os
from typing import Dict, Any
from loguru import logger

class AutonomousExecutor:
    def __init__(self, config):
        self.config = config
        self.sandbox_path = "data/sandbox"
        os.makedirs(self.sandbox_path, exist_ok=True)

    async def run_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        logger.info(f"Executing {language} code in sandbox...")
        
        file_ext = ".py" if language == "python" else ".js"
        temp_file = os.path.join(self.sandbox_path, f"temp_script{file_ext}")
        
        with open(temp_file, "w") as f:
            f.write(code)

        try:
            if language == "python":
                result = subprocess.run(["python3", temp_file], capture_output=True, text=True, timeout=30)
            else:
                result = subprocess.run(["node", temp_file], capture_output=True, text=True, timeout=30)
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except Exception as e:
            return {"success": False, "stderr": str(e)}

    async def push_to_github(self, repo: str, message: str):
        logger.info(f"Pushing changes to {repo}...")
        try:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", message], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            return "Successfully pushed to GitHub."
        except Exception as e:
            return f"GitHub Push Failed: {str(e)}"
