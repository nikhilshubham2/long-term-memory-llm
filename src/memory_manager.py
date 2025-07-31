# src/memory_manager.py
import json
from typing import List, Dict

class MemoryManager:
    def __init__(self, file_path: str = "memory.json"):
        self.file_path = file_path
        self._load_memories()

    def _load_memories(self):
        try:
            with open(self.file_path, 'r') as f:
                self.memories = json.load(f)
        except FileNotFoundError:
            self.memories = []

    def _save_memories(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.memories, f, indent=4)

    def add_memory(self, content: str):
        self.memories.append({"content": content})
        self._save_memories()

    def get_all_memories(self) -> List[Dict[str, str]]:
        return self.memories

    def delete_memory(self, content_to_delete: str):
        initial_count = len(self.memories)
        self.memories = [
            mem for mem in self.memories if content_to_delete.lower() not in mem.get("content", "").lower()
        ]
        if len(self.memories) < initial_count:
            self._save_memories()