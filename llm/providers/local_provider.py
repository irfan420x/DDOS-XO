# Path: llm/providers/local_provider.py
import requests
import json
import logging
from typing import Optional, Dict, Any

class LocalProvider:
    """
    LUNA-ULTRA Local LLM Provider: Supports Ollama and llama.cpp (OpenAI-compatible API).
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.base_url = config.get('base_url', 'http://localhost:11434/v1')
        self.model = config.get('model', 'deepseek-r1:1.5b')
        self.timeout = config.get('timeout', 60)

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generates a response from the local LLM provider.
        """
        logging.info(f"LocalProvider: Sending prompt to {self.model} at {self.base_url}")
        
        # 1. Prepare messages (OpenAI-compatible format)
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        # 2. Prepare payload
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.config.get('temperature', 0.7),
            "max_tokens": self.config.get('max_tokens', 2048),
            "stream": False
        }
        
        # 3. Send request
        try:
            # Use requests for simplicity (can be replaced with httpx for async)
            import asyncio
            response = await asyncio.to_thread(
                requests.post,
                f"{self.base_url}/chat/completions",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                content = data['choices'][0]['message']['content']
                
                # 4. Normalize response (Remove hallucinated system resets)
                content = self._normalize_response(content)
                return content
            else:
                error_msg = f"Local LLM Error: {response.status_code} - {response.text}"
                logging.error(error_msg)
                return error_msg
                
        except Exception as e:
            error_msg = f"Local LLM Connection Error: {str(e)}"
            logging.error(error_msg)
            return error_msg

    def _normalize_response(self, content: str) -> str:
        """
        Removes hallucinated system resets or common local LLM artifacts.
        """
        # Remove common artifacts like "System: ", "User: ", etc.
        content = re.sub(r"^(System|User|Assistant):\s*", "", content, flags=re.IGNORECASE)
        
        # Remove hallucinated system instructions
        content = re.sub(r"\[INST\].*?\[/INST\]", "", content, flags=re.DOTALL)
        
        return content.strip()

import re
