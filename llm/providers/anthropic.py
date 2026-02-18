# Path: llm/providers/anthropic.py
import os
import requests
from typing import Optional, Dict, Any

class AnthropicProvider:
    """
    Anthropic API Provider for LUNA-ULTRA.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.base_url = "https://api.anthropic.com/v1"

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        if not self.api_key:
            return "Error: Anthropic API Key not found."
        
        headers = {"x-api-key": self.api_key, "anthropic-version": "2023-06-01", "Content-Type": "application/json"}
        messages = [{"role": "user", "content": prompt}]
        
        data = {"model": "claude-3-opus-20240229", "messages": messages, "max_tokens": 1024}
        if system_prompt:
            data["system"] = system_prompt
        
        try:
            response = requests.post(f"{self.base_url}/messages", headers=headers, json=data, timeout=60)
            response.raise_for_status()
            return response.json()["content"][0]["text"]
        except Exception as e:
            return f"Anthropic API Error: {str(e)}"
