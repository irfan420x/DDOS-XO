# Path: agents/code_agent.py
import subprocess
import os
import tempfile
from typing import Dict, Any, Optional, List
from llm.router import LLMRouter

class CodeAgent:
    """
    LUNA-ULTRA Code Agent: Writes, executes, and self-heals code.
    """
    def __init__(self, config: Dict[str, Any], llm_router: LLMRouter):
        self.config = config
        self.llm_router = llm_router
        self.max_retries = config.get('max_retries', 5)
        self.sandbox_enabled = config.get('sandbox_enabled', True)

    async def execute_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Executes code and returns the result.
        """
        if language != "python":
            return {"success": False, "error": f"Language {language} not supported yet."}

        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
            tmp.write(code.encode('utf-8'))
            tmp_path = tmp.name

        try:
            # Execute in a subprocess
            result = subprocess.run(
                ["python3", tmp_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            success = result.returncode == 0
            return {
                "success": success,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Execution timed out (30s limit)."}
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    async def self_healing_loop(self, task_description: str, initial_code: str) -> Dict[str, Any]:
        """
        Implements the 6-step self-healing code loop.
        """
        current_code = initial_code
        attempts = 0
        
        while attempts < self.max_retries:
            attempts += 1
            print(f"LUNA Code Agent: Attempt {attempts}/{self.max_retries}")
            
            # 1. Execute code
            result = await self.execute_code(current_code)
            
            if result["success"]:
                print("LUNA Code Agent: Execution successful.")
                return {"success": True, "code": current_code, "output": result["stdout"]}
            
            # 2. Capture error
            error_msg = result.get("stderr") or result.get("error")
            print(f"LUNA Code Agent: Error detected: {error_msg}")
            
            # 3. Send error to LLM for fix
            fix_prompt = f"""
            Task: {task_description}
            Current Code:
            ```python
            {current_code}
            ```
            Error Output:
            {error_msg}
            
            Please fix the code and provide the full corrected version in a python code block.
            """
            
            fix_response = await self.llm_router.generate_response(fix_prompt)
            
            # 4. Extract fixed code
            import re
            pattern = r"```python\n(.*?)\n```"
            match = re.search(pattern, fix_response, re.DOTALL)
            
            if match:
                current_code = match.group(1)
            else:
                # If no code block found, use the whole response (risky)
                current_code = fix_response
                
        return {"success": False, "error": "Max retries reached without success.", "last_code": current_code}
