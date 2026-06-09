"""Tests for TaskFlow CLI."""
import tempfile
from pathlib import Path
from taskflow.core import TaskFlow
from taskflow.models import Priority


def test_add_task():
    """Test adding a task."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "tasks.json"
        taskflow = TaskFlow(storage_path)

        task = taskflow.add_task(
            "Test Task",
            "This is a test task",
            Priority.HIGH,
            ["test", "important"]
        )

        assert task.id is not None
        assert task.title == "Test Task"
        assert task.description == "This is a test task"
        assert task.priority == Priority.HIGH
        assert task.completed is False
        assert task.tags == ["test", "important"]


def test_list_tasks():
    """Test listing tasks."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "tasks.json"
        taskflow = TaskFlow(storage_path)

        taskflow.add_task("Task 1", priority="low")
        taskflow.add_task("Task 2", priority="high")
        taskflow.add_task("Task 3", priority="medium")

        tasks = taskflow.list_tasks()
        assert len(tasks) == 3

        # Test filtering by priority
        high_tasks = taskflow.list_tasks(priority=Priority.HIGH)
        assert len(high_tasks) == 1
        assert high_tasks[0].title == "Task 2"


def test_complete_task():
    """Test completing a task."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "tasks.json"
        taskflow = TaskFlow(storage_path)

        task = taskflow.add_task("Test Task")
        assert task.completed is False

        taskflow.complete_task(task.id)

        updated_task = taskflow.get_task(task.id)
        assert updated_task is not None
        assert updated_task.completed is True


def test_update_task():
    """Test updating a task."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "tasks.json"
        taskflow = TaskFlow(storage_path)

        task = taskflow.add_task("Original Title")

        taskflow.update_task(
            task.id,
            title="Updated Title",
            description="Updated description",
            priority="critical",
            completed=True,
        )

        updated_task = taskflow.get_task(task.id)
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Updated description"
        assert updated_task.priority == Priority.CRITICAL
        assert updated_task.completed is True


def test_delete_task():
    """Test deleting a task."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "tasks.json"
        taskflow = TaskFlow(storage_path)

        task = taskflow.add_task("Task to delete")

        taskflow.delete_task(task.id)

        assert taskflow.get_task(task.id) is None


def test_get_stats():
    """Test getting task statistics."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_path = Path(tmpdir) / "tasks.json"
        taskflow = TaskFlow(storage_path)

        # Add some tasks
        taskflow.add_task("Task 1", priority="low")
        taskflow.add_task("Task 2", priority="high")
        taskflow.add_task("Task 3", priority="high")
        taskflow.add_task("Task 4", priority="medium")

        # Complete one task
        tasks = taskflow.list_tasks()
        taskflow.complete_task(tasks[0].id)

        stats = taskflow.get_stats()
        assert stats["total"] == 4
        assert stats["completed"] == 1
        assert stats["pending"] == 3
        assert stats["by_priority"][Priority.LOW.value] == 1
        assert stats["by_priority"][Priority.HIGH.value] == 2
        assert stats["by_priority"][Priority.MEDIUM.value] == 1


if __name__ == "__main__":
    test_add_task()
    print("test_add_task passed")

    test_list_tasks()
    print("test_list_tasks passed")

    test_complete_task()
    print("test_complete_task passed")

    test_update_task()
    print("test_update_task passed")

    test_delete_task()
    print("test_delete_task passed")

    test_get_stats()
    print("test_get_stats passed")

    print("\nAll tests passed!")
