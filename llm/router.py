# Path: llm/router.py
import os
from typing import Dict, Any
from .providers.deepseek import DeepSeekProvider
from .providers.openai import OpenAIProvider

class LLMRouter:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.default_provider = config.get('default_provider', 'deepseek')
        self.providers = {
            'deepseek': DeepSeekProvider(config.get('api_keys', {}).get('deepseek')),
            'openai': OpenAIProvider(config.get('api_keys', {}).get('openai'))
        }

    async def get_response(self, prompt: str, provider: str = None) -> str:
        provider_name = provider or self.default_provider
        if provider_name not in self.providers:
            raise ValueError(f"Provider {provider_name} not supported")
        return await self.providers[provider_name].generate(prompt)
