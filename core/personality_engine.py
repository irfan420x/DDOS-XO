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
        self.enforce_personality = config.get('llm', {}).get('enforce_personality', True)
        self.prompt_path = "config/system_prompt.txt"

    def _load_master_prompt(self) -> str:
        import os
        if os.path.exists(self.prompt_path):
            with open(self.prompt_path, "r") as f:
                content = f.read().strip()
                # Remove path comment if present
                if content.startswith("# Path:"):
                    content = "\n".join(content.split("\n")[1:]).strip()
                return content
        return "You are LUNA-ULTRA, an autonomous AI Architect and OS Agent."

    def get_system_prompt(self) -> str:
        """
        Strictly loads the system prompt from system_prompt.txt.
        """
        master_prompt = self._load_master_prompt()
        
        # Always ensure bilingual capability is mentioned if not in the file
        if "Bengali" not in master_prompt:
            master_prompt += "\n\nYou are fully capable of communicating in both English and Bengali. If the user speaks Bengali, respond in natural, fluent Bengali."
            
        return master_prompt

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
