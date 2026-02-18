# Path: agents/code_agent.py
import subprocess
import os
import tempfile
import re
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

    async def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if action == "write_and_run":
            return await self.self_healing_loop(params.get('task'), params.get('initial_code', ""))
        return {"error": f"Action {action} not supported"}

    async def execute_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        if language != "python":
            return {"success": False, "error": f"Language {language} not supported."}

        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
            tmp.write(code.encode('utf-8'))
            tmp_path = tmp.name

        try:
            result = subprocess.run(["python3", tmp_path], capture_output=True, text=True, timeout=30)
            return {"success": result.returncode == 0, "stdout": result.stdout, "stderr": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    async def self_healing_loop(self, task: str, initial_code: str) -> Dict[str, Any]:
        current_code = initial_code
        for i in range(self.max_retries):
            result = await self.execute_code(current_code)
            if result["success"]:
                return {"success": True, "code": current_code, "output": result["stdout"]}
            
            error_msg = result.get("stderr") or result.get("error")
            fix_prompt = f"Task: {task}\nCode:\n{current_code}\nError: {error_msg}\nFix the code and provide the full version in a python code block."
            fix_response = await self.llm_router.generate_response(fix_prompt)
            match = re.search(r"```python\n(.*?)\n```", fix_response, re.DOTALL)
            current_code = match.group(1) if match else fix_response
                
        return {"success": False, "error": "Max retries reached.", "last_code": current_code}
