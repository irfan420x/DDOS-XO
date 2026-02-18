# Path: core/cognitive_mode.py
from typing import Dict, Any

class CognitiveMode:
    """
    LUNA-ULTRA Cognitive Mode: Detects and adapts to user intent.
    """
    def __init__(self):
        self.modes = ["coding", "research", "idle", "automation"]

    def detect_mode(self, user_input: str) -> str:
        """
        Simple keyword-based mode detection.
        """
        user_input = user_input.lower()
        if any(kw in user_input for kw in ["code", "python", "script", "debug"]):
            return "coding"
        elif any(kw in user_input for kw in ["search", "find", "research", "info"]):
            return "research"
        elif any(kw in user_input for kw in ["automate", "run", "execute", "shell"]):
            return "automation"
        return "idle"
