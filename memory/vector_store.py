# Path: memory/vector_store.py
import json
import os
from typing import List, Dict, Any

class VectorStore:
    """
    LUNA-ULTRA Vector Store: Simulated vector storage for long-term memory.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.store_file = "memory/vector_store.json"
        self.data = self.load_store()

    def load_store(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.store_file):
            with open(self.store_file, 'r') as f:
                return json.load(f)
        return []

    def save_store(self):
        with open(self.store_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def add_entry(self, entry: Dict[str, Any]):
        self.data.append(entry)
        self.save_store()

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        # Simple keyword-based search for simulation
        results = [e for e in self.data if query.lower() in e['user'].lower()]
        return results[:limit]
