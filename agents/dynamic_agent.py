# Path: agents/dynamic_agent.py
import os
import re
import logging
from typing import Dict, Any, Optional
from llm.router import LLMRouter
from security.permission_engine import PermissionEngine
from security.sandbox_executor import SandboxExecutor

class DynamicAgent:
    """
    LUNA-ULTRA Dynamic Agent: Generates, executes, and manages code/commands on-the-fly.
    """
    def __init__(self, config: Dict[str, Any], llm_router: LLMRouter, permission_engine: PermissionEngine):
        self.config = config
        self.llm_router = llm_router
        self.permission_engine = permission_engine
        self.sandbox_executor = SandboxExecutor(config.get("security", {}))
        self.max_generation_retries = config.get("dynamic_agent", {}).get("max_generation_retries", 2)
        self.os_type = self._detect_os()
        logging.info(f"DynamicAgent initialized. Detected OS: {self.os_type}")

    def _detect_os(self) -> str:
        if os.name == "nt":
            return "windows"
        elif os.name == "posix":
            if "kali" in os.uname().version.lower() or "kali" in os.uname().release.lower():
                return "kali_linux"
            return "linux"
        return "unknown"

    def extract_code_block(self, text: str, language: str = "python") -> Optional[str]:
        """
        Extracts a code block for a specific language from a markdown string.
        """
        pattern = rf"```{{0,3}}{language}\n(.*?)\n```" # Handles ```python and ```
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return None

    def extract_bash_command(self, text: str) -> Optional[str]:
        """
        Extracts a bash command block from a markdown string.
        """
        pattern = r"```(?:bash|sh|zsh|shell)\n(.*?)\n```"
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return None

    async def generate_and_execute(self, task_description: str, available_tools: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates code/commands for a task and executes them in a sandbox.
        """
        logging.info(f"DynamicAgent: Attempting to generate and execute code for task: {task_description}")
        
        for attempt in range(self.max_generation_retries):
            generation_prompt = (
                f"You are LUNA-ULTRA, an autonomous AI agent running on {self.os_type}.\n"
                f"Your task is: {task_description}\n"
                f"You have access to the following tools: {available_tools}.\n"
                f"If the task requires Python, provide a complete Python script. If it requires a shell command, provide a bash/shell command.\n"
                f"Wrap Python code in ```python\n...\n```. Wrap shell commands in ```bash\n...\n```.\n"
                f"Only provide the code/command, no extra explanations unless within comments.\n"
                f"Attempt {attempt + 1}/{self.max_generation_retries}."
            )
            
            llm_response = await self.llm_router.generate_response(generation_prompt)
            logging.debug(f"LLM Response for code generation (Attempt {attempt + 1}):\n{llm_response}")

            python_code = self.extract_code_block(llm_response, "python")
            bash_command = self.extract_bash_command(llm_response)

            if python_code:
                logging.info("DynamicAgent: Python code generated. Executing in sandbox.")
                if not self.permission_engine.check_permission("shell_exec", f"Generated Python code: {python_code[:100]}..."):
                    return {"success": False, "error": "Permission denied for generated Python code."}
                
                result = await self.sandbox_executor.execute(python_code, language="python")
                if result.get("success"):
                    logging.info("DynamicAgent: Python code executed successfully.")
                    return {"success": True, "type": "python", "output": result.get("stdout"), "stderr": result.get("stderr")}
                else:
                    logging.warning("DynamicAgent: Python code execution failed: {}".format(result.get("stderr")))
                    # If execution fails, try to get LLM to fix it in the next retry
                    task_description += "\nPrevious Python code failed with error: {}. Please fix it or try a different approach.".format(result.get("stderr"))

            elif bash_command:
                logging.info("DynamicAgent: Bash command generated. Executing in sandbox.")
                if not self.permission_engine.check_permission("shell_exec", f"Generated Bash command: {bash_command[:100]}..."):
                    return {"success": False, "error": "Permission denied for generated Bash command."}
                
                result = await self.sandbox_executor.execute(bash_command, language="bash")
                if result.get("success"):
                    logging.info("DynamicAgent: Bash command executed successfully.")
                    return {"success": True, "type": "bash", "output": result.get("stdout"), "stderr": result.get("stderr")}
                else:
                    logging.warning("DynamicAgent: Bash command execution failed: {}".format(result.get("stderr")))
                    task_description += "\nPrevious Bash command failed with error: {}. Please fix it or try a different approach.".format(result.get("stderr"))
            else:
                logging.warning("DynamicAgent: No valid code or command block found in LLM response.")
                logging.warning(f"DynamicAgent: LLM did not provide a valid code or command block. Full LLM response: {llm_response}")
                task_description += "\nLLM did not provide a valid code or command block. Please provide one."

        return {"success": False, "error": "Failed to generate and execute code after multiple retries."}

    async def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if action == "generate_and_execute":
            return await self.generate_and_execute(params.get("task_description"), params.get("available_tools", {}))
        return {"error": f"Action {action} not supported by DynamicAgent."}
