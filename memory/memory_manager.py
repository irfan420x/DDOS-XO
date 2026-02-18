# Path: memory/memory_manager.py
import json
import os
import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

class MemoryManager:
    """
    LUNA-ULTRA Memory System: 3-day rolling memory with vector store support.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.rolling_days = config.get('rolling_days', 3)
        self.memory_file = "memory/short_term_memory.json"
        self.vector_store_enabled = config.get('vector_store', True)
        self.memory_data = self.load_memory()
        self.cleanup_old_memory()

    def load_memory(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def save_memory(self):
        if not os.path.exists("memory"):
            os.makedirs("memory")
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory_data, f, indent=4)

    def store_interaction(self, user_input: str, response: str, tags: List[str] = []):
        """
        Stores a new interaction with timestamp and tags.
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "luna": response,
            "tags": tags
        }
        self.memory_data.append(entry)
        self.save_memory()
        
        # If vector store is enabled, we would index it here
        if self.vector_store_enabled:
            self.index_in_vector_store(entry)

    def get_context(self, current_input: str, limit: int = 5) -> str:
        """
        Retrieves relevant context for the current input.
        """
        # Simple recent context retrieval
        recent = self.memory_data[-limit:]
        context = ""
        for entry in recent:
            context += f"User: {entry['user']}\nLUNA: {entry['luna']}\n"
        return context

    def cleanup_old_memory(self):
        """
        Enforces the 3-day rolling memory policy.
        """
        cutoff_date = datetime.now() - timedelta(days=self.rolling_days)
        self.memory_data = [
            entry for entry in self.memory_data 
            if datetime.fromisoformat(entry['timestamp']) > cutoff_date
        ]
        self.save_memory()

    def index_in_vector_store(self, entry: Dict[str, Any]):
        """
        Simulated vector store indexing.
        """
        # In a real implementation, this would use a library like FAISS or ChromaDB
        pass

class Summarizer:
    """
    Auto-summarizes long memory entries to save context window.
    """
    def __init__(self, llm_router: Any):
        self.llm_router = llm_router

    async def summarize_memory(self, memory_entries: List[Dict[str, Any]]) -> str:
        """
        Uses LLM to summarize a list of memory entries.
        """
        text_to_summarize = "\n".join([f"User: {e['user']}\nLUNA: {e['luna']}" for e in memory_entries])
        prompt = f"Summarize the following conversation history concisely:\n\n{text_to_summarize}"
        summary = await self.llm_router.generate_response(prompt)
        return summary
