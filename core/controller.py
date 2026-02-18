# Path: core/controller.py
import asyncio
from typing import Dict, Any
from llm.router import LLMRouter

class LunaController:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.llm_router = LLMRouter(config.get('llm', {}))
        self.state = "idle"
        self.permission_level = config.get('permissions', {}).get('level', 'SAFE')

    async def process_input(self, user_input: str) -> str:
        self.state = "thinking"
        response = await self.llm_router.get_response(user_input)
        self.state = "idle"
        return response

    def get_status(self) -> Dict[str, Any]:
        return {
            "state": self.state,
            "permission": self.permission_level,
            "provider": self.llm_router.default_provider
        }
