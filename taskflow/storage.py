import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from taskflow.models import Priority, Task

class TaskStorage:
    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

    def load_tasks(self) -> List[Task]:
        if not self.storage_path.exists():
            return []

        with open(self.storage_path, "r") as f:
            data = json.load(f)

        return [Task.from_dict(item) for item in data]

    def save_tasks(self, tasks: List[Task]) -> None:
        with open(self.storage_path, "w") as f:
            json.dump([task.to_dict() for task in tasks], f, indent=2)

    def add_task(self, task: Task) -> None:
        tasks = self.load_tasks()
        tasks.append(task)
        self.save_tasks(tasks)

    def update_task(self, task_id: str, updates: dict) -> None:
        tasks = self.load_tasks()
        for task in tasks:
            if task.id == task_id:
                for key, value in updates.items():
                    if key == "priority" and isinstance(value, str):
                        value = Priority(value)
                    setattr(task, key, value)
                task.updated_at = datetime.now()
                break
        self.save_tasks(tasks)

    def delete_task(self, task_id: str) -> None:
        tasks = self.load_tasks()
        tasks = [task for task in tasks if task.id != task_id]
        self.save_tasks(tasks)

    def get_task(self, task_id: str) -> Optional[Task]:
        tasks = self.load_tasks()
        for task in tasks:
            if task.id == task_id:
                return task
        return None
