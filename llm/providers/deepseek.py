# Path: llm/providers/deepseek.py
import os
import requests
from typing import Optional, Dict, Any

class DeepSeekProvider:
    """
    DeepSeek API Provider for LUNA-ULTRA.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.base_url = "https://api.deepseek.com/v1"

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        if not self.api_key:
            return "Error: DeepSeek API Key not found in config or environment."
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": "deepseek-chat",
            "messages": messages,
            "stream": False,
            "temperature": 0.7,
            "max_tokens": 2048
        }
        
        try:
            response = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            return f"DeepSeek API Error: {str(e)}"
        except (KeyError, IndexError) as e:
            return f"DeepSeek Response Parsing Error: {str(e)}"
