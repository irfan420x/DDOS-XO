# Path: llm/router.py
import yaml
import os
from typing import Dict, Any, List, Optional
from .providers.deepseek import DeepSeekProvider
from .providers.openai import OpenAIProvider
from .providers.anthropic import AnthropicProvider
from .providers.gemini import GeminiProvider

class LLMRouter:
    """
    Single brain architecture: Routes all agent requests to the selected LLM provider.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.default_provider = config.get('default_provider', 'deepseek')
        self.fallback_enabled = config.get('fallback_enabled', False)
        
        api_keys = config.get('api_keys', {})
        self.providers = {
            'deepseek': DeepSeekProvider(api_keys.get('deepseek')),
            'openai': OpenAIProvider(api_keys.get('openai')),
            'anthropic': AnthropicProvider(api_keys.get('anthropic')),
            'gemini': GeminiProvider(api_keys.get('gemini'))
        }

    async def generate_response(self, prompt: str, system_prompt: Optional[str] = None, provider: Optional[str] = None) -> str:
        provider_name = provider or self.default_provider
        
        if provider_name not in self.providers:
            if self.fallback_enabled:
                provider_name = 'openai' # Default fallback
            else:
                return f"Error: Provider {provider_name} not configured."

        try:
            response = await self.providers[provider_name].generate(prompt, system_prompt)
            return response
        except Exception as e:
            if self.fallback_enabled and provider_name != 'openai':
                return await self.generate_response(prompt, system_prompt, provider='openai')
            return f"LLM Error ({provider_name}): {str(e)}"

class ResponseParser:
    """
    Parses LLM responses to extract structured data or code blocks.
    """
    @staticmethod
    def extract_code(text: str, language: str = "python") -> str:
        import re
        pattern = rf"```{language}\n(.*?)\n```"
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1) if match else ""
