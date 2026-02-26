# Task Manager — Cassandra + Clean Architecture + TUI

A minimal task management API backed by Apache Cassandra, following strict clean architecture, with
an interactive **TUI** (terminal UI) for calling every endpoint without leaving the terminal.

## Quick Start

```bash
cd _examples/task-manager

# 1. Start Cassandra
docker compose up -d cassandra
scripts/wait-for-cassandra.sh

# 2. Install deps & run migrations
uv sync
uv run python scripts/migrate.py

# 3. Start the API
uv run uvicorn src.api.main:app --port 8000

# 4. In another terminal — launch the TUI
uv run python tui.py
```

## TUI Features

| Key | Action             | Context Chaining                                    |
|-----|--------------------|-----------------------------------------------------|
| 1   | Create Task        | Returned ID is auto-captured                        |
| 2   | Get Task by ID     | Defaults to last-used ID; pick from recent list     |
| 3   | List Tasks         | All listed IDs pushed to context ring               |
| 4   | Update Task Status | Fetches current status, offers as default           |
| 5   | Delete Task        | Defaults to last-used ID; confirms before deleting  |
| q   | Quit               |                                                     |

**Response chaining** — every ID that appears in a response is pushed into a context ring.
When a subsequent operation asks for a task ID, the last-seen ID is offered as the default
and the most recent IDs are displayed as a numbered pick-list. Just press Enter or type a number.

## API Endpoints

| Method  | Path                    | Description           |
|---------|-------------------------|-----------------------|
| POST    | `/api/v1/tasks`         | Create a task         |
| GET     | `/api/v1/tasks/{id}`    | Get task by UUID      |
| GET     | `/api/v1/tasks`         | List tasks (`?status=todo\|in_progress\|done`) |
| PATCH   | `/api/v1/tasks/{id}`    | Update task status    |
| DELETE  | `/api/v1/tasks/{id}`    | Delete a task         |

## Architecture

```
src/
  domain/entities/task.py              # Pure dataclass, no framework deps
  domain/repositories/task_repository.py  # Protocol (interface)
  application/use_cases/               # Business logic
  infrastructure/cassandra/            # Cassandra session + concrete repo
  api/                                 # FastAPI routes, schemas, DI
```

## Testing

```bash
uv run pytest tests/unit/                       # unit (no Docker needed)
uv run pytest tests/functional/ -m functional    # FR tests (needs Cassandra)
```
