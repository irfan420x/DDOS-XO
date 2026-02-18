# Path: llm/router.py

import asyncio
from typing import Optional, List, Dict, Any
from loguru import logger
import ollama
import openai

class LLMRouter:
    def __init__(self, config_manager):
        self.config = config_manager
        self.history: List[Dict[str, str]] = []
        self._api_key: Optional[str] = None

    def set_api_key(self, key: str):
        self._api_key = key # Memory only

    async def generate(self, prompt: str, system_message: Optional[str] = None) -> str:
        backend = self.config.get("llm.active_backend", "ollama")
        logger.info(f"Routing request to {backend}")

        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        # Add history for context
        messages.extend(self.history[-5:]) # Last 5 turns
        messages.append({"role": "user", "content": prompt})

        try:
            if backend == "ollama":
                response = await self._call_ollama(messages)
            elif backend == "openai":
                response = await self._call_openai(messages)
            else:
                response = "Error: Unsupported LLM backend."
            
            # Update history
            self.history.append({"role": "user", "content": prompt})
            self.history.append({"role": "assistant", "content": response})
            return response

        except Exception as e:
            logger.error(f"LLM Error ({backend}): {e}")
            if self.config.get("llm.fallback_enabled"):
                logger.info("Attempting fallback...")
                # Fallback logic could go here
            return f"I encountered an error: {str(e)}"

    async def _call_ollama(self, messages: List[Dict[str, str]]) -> str:
        url = self.config.get("llm.backends.ollama.url")
        model = self.config.get("llm.backends.ollama.model")
        client = ollama.AsyncClient(host=url)
        resp = await client.chat(model=model, messages=messages)
        return resp['message']['content']

    async def _call_openai(self, messages: List[Dict[str, str]]) -> str:
        if not self._api_key:
            raise ValueError("OpenAI API Key not set in memory.")
        
        client = openai.AsyncOpenAI(api_key=self._api_key)
        resp = await client.chat.completions.create(
            model=self.config.get("llm.backends.openai.model"),
            messages=messages
        )
        return resp.choices[0].message.content
