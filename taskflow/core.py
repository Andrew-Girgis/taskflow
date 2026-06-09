import uuid
from pathlib import Path
from typing import List, Optional, Union

from taskflow.models import Priority, Task
from taskflow.storage import TaskStorage

class TaskFlow:
    def __init__(self, storage_path: Path = Path("~/.config/taskflow/tasks.json")):
        self.storage = TaskStorage(storage_path.expanduser())

    def add_task(self, title: str, description: str = "", priority: Union[Priority, str] = Priority.MEDIUM, tags: Optional[List[str]] = None) -> Task:
        if isinstance(priority, str):
            priority = Priority(priority)
        task = Task(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            priority=priority,
            tags=tags or [],
        )
        self.storage.add_task(task)
        return task

    def list_tasks(self, completed: Optional[bool] = None, priority: Optional[Union[Priority, str]] = None, tag: Optional[str] = None) -> List[Task]:
        tasks = self.storage.load_tasks()

        if completed is not None:
            tasks = [task for task in tasks if task.completed == completed]

        if priority:
            if isinstance(priority, str):
                priority = Priority(priority)
            tasks = [task for task in tasks if task.priority == priority]

        if tag:
            tasks = [task for task in tasks if tag in task.tags]

        return tasks

    def complete_task(self, task_id: str) -> None:
        self.storage.update_task(task_id, {"completed": True})

    def update_task(self, task_id: str, **kwargs) -> None:
        updates = {}
        for k, v in kwargs.items():
            if k in Task.__dataclass_fields__:
                if k == "priority" and isinstance(v, str):
                    v = Priority(v)
                updates[k] = v
        self.storage.update_task(task_id, updates)

    def delete_task(self, task_id: str) -> None:
        self.storage.delete_task(task_id)

    def get_task(self, task_id: str) -> Optional[Task]:
        return self.storage.get_task(task_id)

    def get_stats(self) -> dict:
        tasks = self.storage.load_tasks()
        total = len(tasks)
        completed = sum(1 for task in tasks if task.completed)
        pending = total - completed

        priority_counts = {priority: 0 for priority in Priority}
        for task in tasks:
            priority_counts[task.priority] += 1

        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "by_priority": {p.value: count for p, count in priority_counts.items()},
        }
