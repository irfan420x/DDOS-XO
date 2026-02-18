# Path: llm/providers/openai.py
import os
import requests
from typing import Optional, Dict, Any

class OpenAIProvider:
    """
    OpenAI API Provider for LUNA-ULTRA.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = "https://api.openai.com/v1"

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        if not self.api_key:
            return "Error: OpenAI API Key not found."
        
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        data = {"model": "gpt-4", "messages": messages, "stream": False}
        
        try:
            response = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=data, timeout=60)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"OpenAI API Error: {str(e)}"
