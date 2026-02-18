# Path: llm/router.py
import os
import logging
from typing import Dict, Any, Optional
from .providers.deepseek import DeepSeekProvider
from .providers.openai import OpenAIProvider
from .providers.anthropic import AnthropicProvider
from .providers.gemini import GeminiProvider
from .providers.local_provider import LocalProvider
from core.personality_engine import PersonalityEngine

class LLMRouter:
    """
    Unified LLM Router: Supports API, Local, and Hybrid modes with Personality Enforcement.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.mode = config.get('mode', 'api') # api | local | hybrid
        self.default_provider = config.get('default_provider', 'deepseek')
        self.fallback_enabled = config.get('fallback_enabled', True)
        self.enforce_personality = config.get('enforce_personality', True)
        
        # Initialize Personality Engine
        self.personality_engine = PersonalityEngine(config)
        
        # Initialize Providers
        api_keys = config.get('api_keys', {})
        self.providers = {
            'deepseek': DeepSeekProvider(api_keys.get('deepseek')),
            'openai': OpenAIProvider(api_keys.get('openai')),
            'anthropic': AnthropicProvider(api_keys.get('anthropic')),
            'gemini': GeminiProvider(api_keys.get('gemini')),
            'local': LocalProvider(config.get('local', {}))
        }

    async def generate_response(self, prompt: str, system_prompt: Optional[str] = None, provider: Optional[str] = None) -> str:
        """
        Unified entry point for all LLM calls. Ensures personality consistency.
        """
        # 1. Determine Provider based on Mode
        provider_name = provider or self.default_provider
        if self.mode == 'local':
            provider_name = 'local'
        elif self.mode == 'hybrid':
            # Hybrid logic: Use local for simple tasks, API for complex (simplified for now)
            provider_name = provider or self.default_provider
            
        if provider_name not in self.providers:
            return f"Error: Provider {provider_name} not configured."

        # 2. Inject System Prompt (Personality Enforcement)
        # Always prepend LUNA's identity if not explicitly provided
        final_system_prompt = system_prompt or self.personality_engine.get_system_prompt()
        
        # 3. Generate Response
        logging.info(f"LLMRouter: Mode: {self.mode} | Provider: {provider_name}")
        try:
            response = await self.providers[provider_name].generate(prompt, final_system_prompt)
            
            # 4. Personality Validation Layer
            if self.enforce_personality:
                if not self.personality_engine.validate_response(response):
                    logging.warning("LLMRouter: Personality drift detected. Regenerating with reinforcement...")
                    # Regenerate once with stricter instruction
                    reinforcement = self.personality_engine.get_reinforcement_prefix()
                    response = await self.providers[provider_name].generate(f"{reinforcement}\n\n{prompt}", final_system_prompt)
            
            return response
            
        except Exception as e:
            logging.error(f"LLMRouter: Error from {provider_name}: {str(e)}")
            
            # 5. Fallback Logic
            if self.fallback_enabled:
                if self.mode == 'local' or provider_name == 'local':
                    logging.warning("LLMRouter: Local LLM failed. Falling back to API (DeepSeek)...")
                    return await self.generate_response(prompt, system_prompt, provider='deepseek')
                elif provider_name != 'openai':
                    logging.warning(f"LLMRouter: Falling back to OpenAI due to error from {provider_name}.")
                    return await self.generate_response(prompt, system_prompt, provider='openai')
                    
            return f"LLM Error ({provider_name}): {str(e)}"
