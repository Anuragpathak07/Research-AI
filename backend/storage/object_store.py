# storage/object_store.py
import os
import json

class ObjectStore:
    def __init__(self, base_path="object_store"):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def save_json(self, name, data):
        path = os.path.join(self.base_path, f"{name}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return path

    def load_json(self, name):
        path = os.path.join(self.base_path, f"{name}.json")
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
