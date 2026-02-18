# Path: agents/code_agent.py
import subprocess
import os
import tempfile
import re
import logging
from typing import Dict, Any, Optional, List
from llm.router import LLMRouter

class CodeAgent:
    """
    LUNA-ULTRA Code Agent: Writes, executes, and self-heals code with a robust feedback loop.
    """
    def __init__(self, config: Dict[str, Any], llm_router: LLMRouter):
        self.config = config
        self.llm_router = llm_router
        self.max_retries = config.get('max_retries', 3) # Default to 3 for efficiency
        self.timeout = config.get('execution_timeout', 30)

    async def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if action == "write_and_run":
            return await self.self_healing_loop(params.get('task'), params.get('initial_code', ""))
        return {"error": f"Action {action} not supported"}

    def extract_code(self, text: str) -> str:
        """
        Extracts python code from markdown blocks or returns the text if no blocks found.
        """
        match = re.search(r"```python\n(.*?)\n```", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        # Fallback to general code block
        match = re.search(r"```\n(.*?)\n```", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text.strip()

    async def execute_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        if language != "python":
            return {"success": False, "error": f"Language {language} not supported."}

        # Clean code
        code = self.extract_code(code)
        if not code:
            return {"success": False, "error": "No valid code found to execute."}

        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
            tmp.write(code.encode('utf-8'))
            tmp_path = tmp.name

        try:
            result = subprocess.run(
                ["python3", tmp_path], 
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
            return {"success": False, "error": f"Code execution timed out after {self.timeout}s."}
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    async def self_healing_loop(self, task: str, initial_code: str) -> Dict[str, Any]:
        """
        The self-healing loop: Run -> Error -> LLM Fix -> Run again.
        """
        current_code = initial_code
        history = []

        for attempt in range(1, self.max_retries + 1):
            logging.info(f"LUNA Code Agent: Execution attempt {attempt}/{self.max_retries}")
            
            # If no code, ask LLM to generate it first
            if not current_code:
                gen_prompt = f"Task: {task}\nWrite a complete Python script to achieve this. Wrap the code in a ```python block."
                current_code = await self.llm_router.generate_response(gen_prompt)
                current_code = self.extract_code(current_code)

            result = await self.execute_code(current_code)
            
            if result["success"]:
                return {
                    "success": True, 
                    "attempt": attempt,
                    "code": current_code, 
                    "output": result["stdout"]
                }
            
            # Handle failure
            error_msg = result.get("stderr") or result.get("error")
            logging.warning(f"LUNA Code Agent: Attempt {attempt} failed: {error_msg}")
            
            history.append({"attempt": attempt, "error": error_msg})
            
            if attempt < self.max_retries:
                fix_prompt = (
                    f"Task: {task}\n"
                    f"Previous Code:\n```python\n{current_code}\n```\n"
                    f"Error encountered:\n{error_msg}\n"
                    f"Please fix the code. Ensure it is complete and runnable. Wrap in ```python code block."
                )
                fix_response = await self.llm_router.generate_response(fix_prompt)
                current_code = self.extract_code(fix_response)
            else:
                break
                
        return {
            "success": False, 
            "error": "Max retries reached without success.", 
            "history": history,
            "last_code": current_code
        }
