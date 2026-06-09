import click

from taskflow.core import TaskFlow
from taskflow.models import Priority

@click.group()
def cli():
    pass

@cli.command()
@click.argument("title")
@click.option("--description", "-d", help="Task description")
@click.option("--priority", "-p", type=click.Choice([p.value for p in Priority]), default=Priority.MEDIUM.value, help="Task priority")
@click.option("--tags", "-t", help="Tags for the task (comma-separated list)")
def add(title, description, priority, tags):
    """Add a new task."""
    taskflow = TaskFlow()
    tag_list = [tag.strip() for tag in tags.split(",")] if tags else []
    task = taskflow.add_task(title, description, Priority(priority), tag_list)
    task_id_short = task.id[0:8]
    click.echo(f"Added task: {task_id_short}")
    click.echo(f"Title: {task.title}")
    click.echo(f"Priority: {task.priority}")
    if description:
        click.echo(f"Description: {description}")
    if tag_list:
        click.echo(f"Tags: {', '.join(tag_list)}")

@cli.command()
@click.option("--completed/--pending", "show_completed", default=None, help="Filter by completion status")
@click.option("--priority", "-p", type=click.Choice([p.value for p in Priority]), help="Filter by priority")
@click.option("--tag", "-t", help="Filter by tag")
@click.option("--all", "show_all", is_flag=True, help="Show all tasks (default)")
def list(show_completed, priority, tag, show_all):
    """List tasks."""
    taskflow = TaskFlow()
    tasks = taskflow.list_tasks(
        completed=show_completed if show_completed is not None else None,
        priority=Priority(priority) if priority else None,
        tag=tag if tag else None,
    )

    if not tasks:
        click.echo("No tasks found.")
        return

    for task in tasks:
        status = "✓" if task.completed else "○"
        priority_str = task.priority.value.upper()
        task_id_short = task.id[0:8]
        click.echo(f"{status} {task_id_short} - {task.title} ({priority_str})")
        if task.description:
            click.echo(f"    {task.description}")
        if task.tags:
            click.echo(f"    Tags: {', '.join(task.tags)}")

@cli.command()
@click.argument("task_id")
def complete(task_id):
    """Mark a task as completed."""
    taskflow = TaskFlow()
    task_id_short = task_id[0:8]
    try:
        taskflow.complete_task(task_id)
        click.echo(f"Marked task {task_id_short} as completed.")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

@cli.command()
@click.argument("task_id")
@click.option("--title", "-t", help="New title")
@click.option("--description", "-d", help="New description")
@click.option("--priority", "-p", type=click.Choice([p.value for p in Priority]), help="New priority")
@click.option("--completed/--incomplete", "completed", help="Set completion status")
def update(task_id, title, description, priority, completed):
    """Update a task."""
    taskflow = TaskFlow()
    task_id_short = task_id[0:8]
    updates = {}

    if title:
        updates["title"] = title
    if description:
        updates["description"] = description
    if priority:
        updates["priority"] = Priority(priority)
    if completed is not None:
        updates["completed"] = completed

    if not updates:
        click.echo("No updates provided.")
        return

    try:
        taskflow.update_task(task_id, **updates)
        click.echo(f"Updated task {task_id_short}.")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

@cli.command()
@click.argument("task_id")
def delete(task_id):
    """Delete a task."""
    taskflow = TaskFlow()
    task_id_short = task_id[0:8]
    try:
        taskflow.delete_task(task_id)
        click.echo(f"Deleted task {task_id_short}.")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

@cli.command()
@click.option("--completed/--pending", "show_completed", default=None, help="Filter by completion status")
@click.option("--priority", "-p", type=click.Choice([p.value for p in Priority]), help="Filter by priority")
@click.option("--tag", "-t", help="Filter by tag")
def stats(show_completed, priority, tag):
    """Show task statistics."""
    taskflow = TaskFlow()
    tasks = taskflow.list_tasks(
        completed=show_completed if show_completed is not None else None,
        priority=Priority(priority) if priority else None,
        tag=tag if tag else None,
    )

    total = len(tasks)
    completed = sum(1 for task in tasks if task.completed)
    pending = total - completed

    click.echo(f"Total tasks: {total}")
    click.echo(f"Completed: {completed}")
    click.echo(f"Pending: {pending}")

    if priority or tag or show_completed is not None:
        click.echo(f"\nFiltered tasks ({total}):")
        for task in tasks:
            status = "✓" if task.completed else "○"
            click.echo(f"  {status} {task.title}")

@cli.command()
def version():
    """Show version information."""
    from taskflow import __version__
    click.echo(f"TaskFlow version {__version__}")

def main():
    cli()
