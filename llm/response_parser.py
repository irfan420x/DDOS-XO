# Path: llm/response_parser.py
import re
from typing import Optional

class ResponseParser:
    """
    Parses LLM responses to extract structured data or code blocks.
    """
    @staticmethod
    def extract_code(text: str, language: str = "python") -> str:
        pattern = rf"```{language}\n(.*?)\n```"
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1) if match else ""

    @staticmethod
    def extract_json(text: str) -> Optional[str]:
        pattern = r"```json\n(.*?)\n```"
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1) if match else None
