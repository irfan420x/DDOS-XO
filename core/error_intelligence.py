# Path: core/error_intelligence.py
import logging
from typing import Dict, Any, List, Optional

class ErrorIntelligence:
    """
    LUNA-ULTRA Error Intelligence Layer: Analyzes failures and suggests recovery.
    """
    def __init__(self, controller):
        self.controller = controller

    async def analyze_failure(self, task: str, error: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyzes a task failure to find the root cause and suggest steps.
        """
        logging.info(f"ErrorIntelligence: Analyzing failure for task: {task}")
        
        prompt = (
            f"Task: {task}\n"
            f"Error Message: {error}\n"
            f"Context: {context}\n\n"
            f"As LUNA-ULTRA, analyze this failure and provide:\n"
            f"1. Root Cause: Why did it fail technically?\n"
            f"2. Recovery Steps: Actionable step-by-step guidance to fix it.\n"
            f"3. Alternative Options: If multiple solutions exist, present them.\n\n"
            f"Respond in a professional, human-like tone."
        )
        
        analysis = await self.controller.llm_router.generate_response(prompt)
        
        return {
            "task": task,
            "error": error,
            "analysis": analysis,
            "root_cause": self._extract_section(analysis, "Root Cause"),
            "recovery_steps": self._extract_section(analysis, "Recovery Steps")
        }

    def _extract_section(self, text: str, section_name: str) -> str:
        import re
        pattern = rf"{section_name}:(.*?)(?=\n\d\.|\n[A-Z]|$)"
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return ""
