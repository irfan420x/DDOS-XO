# Path: llm/deepseek_brain.py

import openai
from typing import List, Dict, Any
from core.system_prompt import LUNA_PERSONALITY
from loguru import logger

class LunaBrain:
    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com"):
        self.client = openai.AsyncOpenAI(api_key=api_key, base_url=base_url)
        self.system_prompt = LUNA_PERSONALITY
        self.history: List[Dict[str, str]] = []

    async def chat(self, user_input: str, context: str = "") -> str:
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "system", "content": f"Current Context: {context}"}
        ]
        
        # Add history (last 10 messages for context)
        messages.extend(self.history[-10:])
        messages.append({"role": "user", "content": user_input})

        try:
            response = await self.client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                temperature=0.7
            )
            answer = response.choices[0].message.content
            
            # Update history
            self.history.append({"role": "user", "content": user_input})
            self.history.append({"role": "assistant", "content": answer})
            
            return answer
        except Exception as e:
            logger.error(f"DeepSeek API Error: {e}")
            return f"দুঃখিত, আমি এই মুহূর্তে কানেক্ট করতে পারছি না। এরর: {str(e)}"

    def clear_history(self):
        self.history = []
