# Path: llm/providers/gemini.py
import os
import requests
from typing import Optional, Dict, Any

class GeminiProvider:
    """
    Gemini API Provider for LUNA-ULTRA.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        if not self.api_key:
            return "Error: Gemini API Key not found."
        
        url = f"{self.base_url}?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        data = {"contents": [{"parts": [{"text": full_prompt}]}]}
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            return f"Gemini API Error: {str(e)}"
