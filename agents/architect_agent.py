# Path: agents/architect_agent.py
import os
import logging
from typing import Dict, Any, List
from llm.router import LLMRouter

class ArchitectAgent:
    """
    LUNA-ULTRA Architect Agent: Plans and builds multi-file projects.
    """
    def __init__(self, config: Dict[str, Any], llm_router: LLMRouter):
        self.config = config
        self.llm_router = llm_router

    async def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if action == "plan_project":
            return await self.plan_project(params.get("description"))
        elif action == "create_structure":
            return await self.create_structure(params.get("structure"))
        elif action == "write_file":
            return await self.write_file(params.get("path"), params.get("content"))
        return {"success": False, "error": f"Action {action} not supported by ArchitectAgent"}

    async def plan_project(self, description: str) -> Dict[str, Any]:
        prompt = (
            f"Plan a multi-file project based on this description: {description}\n"
            f"Provide a JSON list of files and folders to create.\n"
            f"Example: {{\"structure\": [\"src/\", \"src/main.py\", \"requirements.txt\"]}}"
        )
        response = await self.llm_router.generate_response(prompt)
        # Simplified extraction for now
        return {"success": True, "plan": response}

    async def create_structure(self, structure: List[str]) -> Dict[str, Any]:
        try:
            for item in structure:
                if item.endswith("/"):
                    os.makedirs(item, exist_ok=True)
                else:
                    dir_name = os.path.dirname(item)
                    if dir_name:
                        os.makedirs(dir_name, exist_ok=True)
                    with open(item, 'w') as f:
                        pass
            return {"success": True, "output": f"Created structure: {structure}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def write_file(self, path: str, content: str) -> Dict[str, Any]:
        try:
            dir_name = os.path.dirname(path)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
            with open(path, 'w') as f:
                f.write(content)
            return {"success": True, "output": f"Successfully wrote to {path}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
