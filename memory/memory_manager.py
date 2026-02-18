# Path: memory/memory_manager.py
import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from .vector_store import VectorStore

class MemoryManager:
    """
    LUNA-ULTRA Memory System: 3-day rolling memory with vector store support.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.rolling_days = config.get('rolling_days', 3)
        self.memory_file = "memory/short_term_memory.json"
        self.vector_store = VectorStore(config)
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
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "luna": response,
            "tags": tags
        }
        self.memory_data.append(entry)
        self.vector_store.add_entry(entry)
        self.save_memory()

    def get_context(self, current_input: str, limit: int = 5) -> str:
        recent = self.memory_data[-limit:]
        context = ""
        for entry in recent:
            context += f"User: {entry['user']}\nLUNA: {entry['luna']}\n"
        return context

    def cleanup_old_memory(self):
        cutoff_date = datetime.now() - timedelta(days=self.rolling_days)
        self.memory_data = [
            entry for entry in self.memory_data 
            if datetime.fromisoformat(entry['timestamp']) > cutoff_date
        ]
        self.save_memory()
