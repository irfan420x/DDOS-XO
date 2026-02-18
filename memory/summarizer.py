# Path: memory/summarizer.py
from typing import List, Dict, Any

class Summarizer:
    """
    Auto-summarizes long memory entries to save context window.
    """
    def __init__(self, llm_router: Any):
        self.llm_router = llm_router

    async def summarize_memory(self, memory_entries: List[Dict[str, Any]]) -> str:
        text_to_summarize = "\n".join([f"User: {e['user']}\nLUNA: {e['luna']}" for e in memory_entries])
        prompt = f"Summarize the following conversation history concisely:\n\n{text_to_summarize}"
        summary = await self.llm_router.generate_response(prompt)
        return summary
