# TaskFlow

A modern command-line task management tool for organizing your workflow.

## Overview

TaskFlow is a simple yet powerful CLI tool for managing tasks efficiently. It helps you track tasks by title, description, priority, and tags. Tasks are stored locally in a JSON file for persistence.

## Features

- **Add tasks** with title, description, priority, and tags
- **List tasks** with filtering options (completed/pending, priority, tag)
- **Update tasks** (title, description, priority, completion status)
- **Delete tasks**
- **Show statistics** (total, completed, pending, filtered views)
- **View version** information

## Installation

Install TaskFlow globally:

```bash
uv pip install taskflow
```

Or install in development mode:

```bash
uv pip install -e .
```

## Usage

### Add a task

```bash
taskflow add "Finish report" --description "Complete the quarterly report" --priority high --tags "work,urgent"
```

### List tasks

```bash
taskflow list
```

Filter tasks:

```bash
taskflow list --completed
taskflow list --priority high
taskflow list --tag work
taskflow list --completed --priority high --tag urgent
```

### Mark a task as completed

```bash
taskflow complete <task-id>
```

### Update a task

```bash
taskflow update <task-id> --title "New title" --description "New description" --priority medium --completed
```

### Delete a task

```bash
taskflow delete <task-id>
```

### Show statistics

```bash
taskflow stats
```

### Show version

```bash
taskflow version
```

## Storage

Tasks are stored in `~/.config/taskflow/tasks.json` by default. You can change the storage location by setting the `TASKFLOW_STORAGE_PATH` environment variable.

## Development

To run tests:

```bash
uv run pytest
```

To run linting and type checking:

```bash
uv run ruff check
uv run mypy taskflow
```

## License

MIT

## Contributing

Feel free to contribute by opening issues or submitting pull requests. For major changes, please open an issue first to discuss what you would like to change.

## Author

Andrew Girgis
