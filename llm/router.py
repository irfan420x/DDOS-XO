# Path: llm/router.py
import os
from typing import Dict, Any, Optional
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
            return f"Error: Provider {provider_name} not configured."

        import logging
        logging.info(f"LLMRouter: Sending prompt to {provider_name} with system prompt: {system_prompt}\nPrompt: {prompt}")
        try:
            response = await self.providers[provider_name].generate(prompt, system_prompt)
            logging.info(f"LLMRouter: Received response from {provider_name}: {response}")
            return response
        except Exception as e:
            logging.error(f"LLMRouter: Error from {provider_name}: {str(e)}")
            if self.fallback_enabled and provider_name != 'openai':
                logging.warning(f"LLMRouter: Falling back to OpenAI due to error from {provider_name}.")
                return await self.generate_response(prompt, system_prompt, provider='openai')
            return f"LLM Error ({provider_name}): {str(e)}"
