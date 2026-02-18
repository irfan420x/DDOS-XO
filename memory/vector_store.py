# Path: memory/vector_store.py
import json
import os
from typing import Dict, Any, List
import logging

# Placeholder for sentence_transformers import
try:
    from sentence_transformers import SentenceTransformer
    _GLOBAL_HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    logging.warning("sentence-transformers not found. Vector embeddings will be simulated.")
    _GLOBAL_HAS_SENTENCE_TRANSFORMERS = False

class VectorStore:
    """
    LUNA-ULTRA Vector Store: Stores and retrieves vectorized memories for RAG.
    """
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.vector_file = "memory/vector_store.json"
        self.data = self._load_data()
        self.model = None
        self.has_sentence_transformers = _GLOBAL_HAS_SENTENCE_TRANSFORMERS

        if self.has_sentence_transformers:
            try:
                self.model = SentenceTransformer("all-MiniLM-L6-v2")
                logging.info("SentenceTransformer model loaded for vector embeddings.")
            except Exception as e:
                logging.error(f"Failed to load SentenceTransformer model: {e}")
                self.model = None
                self.has_sentence_transformers = False # Disable if model loading fails
        logging.info("VectorStore initialized.")

    def _load_data(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.vector_file):
            try:
                with open(self.vector_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logging.warning(f"Vector store file {self.vector_file} is corrupted. Starting fresh.")
                return []
        return []

    def _save_data(self):
        if not os.path.exists("memory"):
            os.makedirs("memory")
        with open(self.vector_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def add_entry(self, entry: Dict[str, Any]):
        """
        Adds a new memory entry to the vector store.
        If sentence-transformers is available, it will vectorize the content.
        """
        if self.has_sentence_transformers and self.model:
            text_to_embed = "User: {}\nLUNA: {}".format(entry.get("user", ""), entry.get("luna", ""))
            entry["embedding"] = self.model.encode(text_to_embed).tolist()
        self.data.append(entry)
        self._save_data()
        logging.debug("Added entry to vector store: {}".format(entry.get("user")))

    def get_relevant_entries(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieves relevant entries based on a query.
        If sentence-transformers is available, it performs similarity search.
        Otherwise, it falls back to a simple keyword search.
        """
        if self.has_sentence_transformers and self.model and self.data:
            query_embedding = self.model.encode(query).tolist()
            
            # Calculate cosine similarity (simplified for demonstration)
            similarities = []
            for i, entry in enumerate(self.data):
                if "embedding" in entry:
                    # Simple dot product for similarity
                    similarity = sum(a*b for a,b in zip(query_embedding, entry["embedding"]))
                    similarities.append((similarity, i))
            
            similarities.sort(key=lambda x: x[0], reverse=True)
            relevant_entries = [self.data[i] for _, i in similarities[:top_k]]
            return relevant_entries
        else:
            # Fallback to simple keyword search
            relevant_entries = []
            query_lower = query.lower()
            for entry in self.data:
                if query_lower in entry.get("user", "").lower() or query_lower in entry.get("luna", "").lower():
                    relevant_entries.append(entry)
            
            # For now, just return the most recent matching entries from keyword search
            return relevant_entries[-top_k:]
