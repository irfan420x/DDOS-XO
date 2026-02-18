# Path: core/personality_engine.py
import logging
import re
from typing import Dict, Any, Optional

class PersonalityEngine:
    """
    LUNA-ULTRA Personality Engine: Enforces LUNA's identity, tone, and consistency.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.profile = config.get('personality', {}).get('profile', 'professional')
        self.enforce_personality = config.get('llm', {}).get('enforce_personality', True)
        
        # Master System Prompt (LUNA Identity)
        self.master_prompt = self._load_master_prompt()
        
        # Personality Profiles
        self.profiles = {
            "professional": "You are LUNA-ULTRA, a highly efficient and professional AI OS Agent. Your tone is formal, precise, and helpful.",
            "hacker": "You are LUNA-ULTRA, an elite cyber-security and OS automation expert. Your tone is technical, sharp, and direct. Use terminal-style metaphors.",
            "friendly": "You are LUNA-ULTRA, a friendly and supportive AI companion. Your tone is warm, encouraging, and conversational.",
            "minimal": "You are LUNA-ULTRA. Respond with absolute brevity. No fluff, only facts and actions."
        }

    def _load_master_prompt(self) -> str:
        import os
        path = "config/system_prompt.txt"
        if os.path.exists(path):
            with open(path, "r") as f:
                return f.read().strip()
        return "You are LUNA-ULTRA, an autonomous AI Architect and OS Agent."

    def get_system_prompt(self) -> str:
        """
        Combines master prompt with current profile and tone instructions.
        """
        profile_instruction = self.profiles.get(self.profile, self.profiles["professional"])
        
        # Tone instructions (Bengali + English capable)
        tone_instruction = (
            "You are fully capable of communicating in both English and Bengali. "
            "If the user speaks Bengali, respond in natural, fluent Bengali. "
            "Always maintain your identity as LUNA-ULTRA."
        )
        
        return f"{self.master_prompt}\n\n{profile_instruction}\n\n{tone_instruction}"

    def validate_response(self, response: str) -> bool:
        """
        Validates if the response maintains LUNA's identity and tone.
        """
        if not self.enforce_personality:
            return True
            
        # 1. Check if response ignores identity (e.g., says "I am an AI model by OpenAI")
        forbidden_patterns = [
            r"I am an AI model",
            r"I am a large language model",
            r"developed by (OpenAI|Google|Anthropic|Meta)",
            r"I don't have a name"
        ]
        
        for pattern in forbidden_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                logging.warning(f"PersonalityEngine: Identity drift detected in response: {response[:50]}...")
                return False
                
        # 2. Check if response references LUNA (Optional but good for reinforcement)
        # We don't strictly require it, but we check for negative cases.
        
        return True

    def get_reinforcement_prefix(self) -> str:
        """
        Returns a prefix to reinforce personality if drift is detected.
        """
        return "IMPORTANT: Remember you are LUNA-ULTRA. Do not break character. Maintain your assigned tone and identity. "
