class CheckpointStore:
    def __init__(self):
        self.storage = {}

    def save(self, task_id, state):
        self.storage[task_id] = state.copy()

    def load(self, task_id):
        return self.storage.get(task_id)

    def delete(self, task_id):
        self.storage.pop(task_id, None)
