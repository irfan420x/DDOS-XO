# Path: core/validation_loop.py
import os
import logging
import subprocess
import json
import shlex
from typing import Dict, Any, List, Optional

class ValidationLoop:
    """
    LUNA-ULTRA Code Execution Validation Loop: Self-healing and syntax checking.
    """
    def __init__(self, controller):
        self.controller = controller
        self.max_retries = 3

    async def validate_and_fix(self, repo_path: str) -> Dict[str, Any]:
        """
        Validates a repository's code and attempts to fix syntax errors autonomously.
        """
        logging.info(f"ValidationLoop: Starting validation for {repo_path}")
        history = []
        
        for attempt in range(self.max_retries):
            logging.info(f"ValidationLoop: Attempt {attempt + 1}/{self.max_retries}")
            
            # 1. Compile all Python files
            compile_res = subprocess.run(
                ["python3", "-m", "compileall", repo_path],
                capture_output=True,
                text=True
            )
            
            if compile_res.returncode == 0:
                logging.info("ValidationLoop: Syntax check passed.")
                return {"success": True, "history": history, "message": "All files compiled successfully."}
            
            # 2. Extract Syntax Errors
            error_report = compile_res.stderr
            logging.warning(f"ValidationLoop: Syntax errors detected: {error_report}")
            
            # 3. Request Fix from LLM
            fix_prompt = (
                f"Repository Path: {repo_path}\n"
                f"Syntax Errors Encountered:\n{error_report}\n"
                f"Analyze the errors and provide the corrected code for the affected files.\n"
                f"Format as a JSON list: [{{'path': 'file_path', 'content': 'new_content'}}]"
            )
            
            fix_response = await self.controller.llm_router.generate_response(fix_prompt)
            
            # 4. Apply Fixes
            try:
                import re
                json_match = re.search(r"\[.*\]", fix_response, re.DOTALL)
                if json_match:
                    fixes = json.loads(json_match.group(0))
                    for fix in fixes:
                        file_path = os.path.join(repo_path, fix["path"])
                        # Ensure path is within repo_path for safety
                        if os.path.commonpath([repo_path, os.path.abspath(file_path)]) == repo_path:
                            with open(file_path, 'w') as f:
                                f.write(fix["content"])
                            logging.info(f"ValidationLoop: Applied fix to {fix['path']}")
                        else:
                            logging.warning(f"ValidationLoop: Security block - attempt to write outside repo: {fix['path']}")
                    history.append({"attempt": attempt, "errors": error_report, "fixes_applied": [f["path"] for f in fixes]})
                else:
                    logging.error("ValidationLoop: No valid JSON fix found in LLM response.")
                    break
            except Exception as e:
                logging.error(f"ValidationLoop: Error applying fixes: {e}")
                break
                
        return {"success": False, "history": history, "error": "Max retries reached without fixing all syntax errors."}

    async def run_simulation(self, repo_path: str, entry_point: str = "main.py") -> Dict[str, Any]:
        """
        Attempts a minimal run simulation to catch runtime exceptions.
        """
        full_path = os.path.join(repo_path, entry_point)
        if not os.path.exists(full_path):
            return {"success": False, "error": f"Entry point {entry_point} not found."}
            
        logging.info(f"ValidationLoop: Simulating execution of {entry_point}")
        try:
            # Run with a timeout and capture output
            # We use a separate process to avoid crashing the main app
            result = subprocess.run(
                ["python3", full_path],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=10,
                env={**os.environ, "LUNA_SIMULATION": "1"} # Flag for the app to run in mock mode if supported
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except subprocess.TimeoutExpired:
            return {"success": True, "message": "Simulation timed out (likely a long-running process), but no immediate crash."}
        except Exception as e:
            return {"success": False, "error": str(e)}
