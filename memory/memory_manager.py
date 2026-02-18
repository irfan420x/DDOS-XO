import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from .vector_store import VectorStore
import logging

class MemoryManager:
    """
    LUNA-ULTRA Memory System: 3-day rolling memory with vector store support for RAG.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.rolling_days = config.get("rolling_days", 3)
        self.memory_file = "memory/short_term_memory.json"
        self.vector_store = VectorStore(config) # Initialize VectorStore
        self.memory_data = self.load_memory()
        self.cleanup_old_memory()
        logging.info("MemoryManager initialized.")

    def load_memory(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logging.warning(f"Short-term memory file {self.memory_file} is corrupted. Starting fresh.")
                return []
        return []

    def save_memory(self):
        if not os.path.exists("memory"):
            os.makedirs("memory")
        with open(self.memory_file, "w") as f:
            json.dump(self.memory_data, f, indent=4)

    def store_interaction(self, user_input: str, response: str, tags: List[str] = []):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "luna": response,
            "tags": tags
        }
        self.memory_data.append(entry)
        self.vector_store.add_entry(entry) # Add to vector store as well
        self.save_memory()
        logging.debug(f"Stored interaction: {user_input}")

    def get_context(self, current_input: str, limit: int = 5) -> str:
        """
        Retrieves context from both rolling memory and vector store.
        """
        context_parts = []

        # Get recent interactions from rolling memory
        recent = self.memory_data[-limit:]
        for entry in recent:
            context_parts.append("User: {}\nLUNA: {}".format(entry.get("user", ""), entry.get("luna", "")))
        
        # Get relevant entries from vector store (RAG simulation)
        relevant_vector_entries = self.vector_store.get_relevant_entries(current_input, top_k=2)
        for entry in relevant_vector_entries:
            context_parts.append("Relevant Memory: User: {}\nLUNA: {}".format(entry.get("user", ""), entry.get("luna", "")))

        return "\n".join(context_parts)

    def cleanup_old_memory(self):
        cutoff_date = datetime.now() - timedelta(days=self.rolling_days)
        self.memory_data = [
            entry for entry in self.memory_data 
            if datetime.fromisoformat(entry["timestamp"]) > cutoff_date
        ]
        self.save_memory()
        logging.info(f"Cleaned up old memory. Remaining entries: {len(self.memory_data)}")
