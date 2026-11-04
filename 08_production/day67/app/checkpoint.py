import json
import os

from pathlib import Path


class CheckpointStore:
    def __init__(self, directory="checkpoint"):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def _get_path(self, task_id: str):
        return self.directory / f"{task_id}.json"

    def save(self, task_id: str, state: dict):
        path = self._get_path(task_id)
        temp_path = path.with_suffix(".tmp")

        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

            f.flush()
            os.fsync(f.fileno())

        os.replace(temp_path, path)

    def load(self, task_id: str):
        path = self._get_path(task_id)

        if not path.exists():
            return None

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
