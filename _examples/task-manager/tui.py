#!/usr/bin/env python3
"""
Task Manager TUI — Interactive API Client
==========================================

A rich-powered terminal UI that lets you call every Task Manager endpoint
interactively. Responses are automatically chained: IDs returned from
create/list operations are stored in a context ring so subsequent calls
(get, update, delete) can reuse them with a single Enter press.

Usage:
    # Start the API server first:
    uv run uvicorn src.api.main:app --port 8000

    # Then in another terminal:
    uv run python tui.py
    uv run python tui.py --base-url http://localhost:8000  # (default)
"""

from __future__ import annotations

import sys
from collections import deque
from datetime import datetime

import httpx
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

theme = Theme({
    "menu.key": "bold cyan",
    "menu.label": "white",
    "success": "bold green",
    "error": "bold red",
    "info": "bold yellow",
    "muted": "dim white",
    "id": "bold magenta",
})

console = Console(theme=theme)

BASE_URL = "http://localhost:8000"

# ---------------------------------------------------------------------------
# Context ring — stores recently seen task IDs for easy reuse
# ---------------------------------------------------------------------------

MAX_CONTEXT = 20


class Context:
    """Tracks recently-seen task IDs so they can be offered as defaults."""

    def __init__(self) -> None:
        self._ids: deque[str] = deque(maxlen=MAX_CONTEXT)
        self._last_id: str | None = None

    @property
    def last_id(self) -> str | None:
        return self._last_id

    def push(self, task_id: str) -> None:
        if task_id in self._ids:
            self._ids.remove(task_id)
        self._ids.appendleft(task_id)
        self._last_id = task_id

    def push_many(self, task_ids: list[str]) -> None:
        for tid in reversed(task_ids):
            self.push(tid)
        # Keep the first one as "last"
        if task_ids:
            self._last_id = task_ids[0]

    @property
    def recent(self) -> list[str]:
        return list(self._ids)


ctx = Context()

# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------


def _client() -> httpx.Client:
    return httpx.Client(base_url=BASE_URL, timeout=10.0)


def _display_task(task: dict, *, label: str = "Task") -> None:
    """Pretty-print a single task response."""
    status_colors = {"todo": "yellow", "in_progress": "blue", "done": "green"}
    s = task.get("status", "?")
    color = status_colors.get(s, "white")

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Field", style="bold")
    table.add_column("Value")
    table.add_row("ID", f"[id]{task['id']}[/id]")
    table.add_row("Title", task["title"])
    table.add_row("Description", task.get("description") or "—")
    table.add_row("Status", f"[{color}]{s}[/{color}]")
    table.add_row("Created", task.get("created_at", ""))
    table.add_row("Updated", task.get("updated_at", ""))
    console.print(Panel(table, title=f"[success]{label}[/success]", border_style="green"))


def _display_error(resp: httpx.Response) -> None:
    try:
        detail = resp.json().get("detail", resp.text)
    except Exception:
        detail = resp.text
    console.print(f"[error]HTTP {resp.status_code}:[/error] {detail}")


# ---------------------------------------------------------------------------
# Prompt helpers with context awareness
# ---------------------------------------------------------------------------


def _prompt(label: str, *, default: str | None = None, required: bool = True) -> str:
    """Prompt for input, showing a default from context if available."""
    suffix = f" [muted]\\[{default}][/muted]" if default else ""
    while True:
        console.print(f"  {label}{suffix}: ", end="")
        value = input().strip()
        if not value and default:
            return default
        if value:
            return value
        if not required:
            return ""
        console.print("  [error]Required — please enter a value.[/error]")


def _prompt_task_id(label: str = "Task ID") -> str:
    """Prompt for a task ID, offering the last-used ID and a pick list."""
    default = ctx.last_id
    if ctx.recent:
        console.print()
        console.print("  [info]Recent task IDs:[/info]")
        for i, tid in enumerate(ctx.recent[:5], 1):
            marker = " [success]← last[/success]" if tid == default else ""
            console.print(f"    [menu.key]{i}[/menu.key]) [id]{tid}[/id]{marker}")
        console.print()

    raw = _prompt(label, default=default)

    # Allow picking by number
    if raw.isdigit() and 1 <= int(raw) <= len(ctx.recent):
        chosen = ctx.recent[int(raw) - 1]
        console.print(f"  [muted]→ Using {chosen}[/muted]")
        return chosen
    return raw


def _prompt_status(label: str = "Status", *, default: str | None = None) -> str:
    statuses = ["todo", "in_progress", "done"]
    console.print()
    for i, s in enumerate(statuses, 1):
        colors = {"todo": "yellow", "in_progress": "blue", "done": "green"}
        marker = " [success]← default[/success]" if s == default else ""
        console.print(f"    [menu.key]{i}[/menu.key]) [{colors[s]}]{s}[/{colors[s]}]{marker}")
    raw = _prompt(label, default=default, required=True)
    if raw.isdigit() and 1 <= int(raw) <= 3:
        return statuses[int(raw) - 1]
    if raw in statuses:
        return raw
    console.print(f"  [error]Invalid status. Choose from: {', '.join(statuses)}[/error]")
    return _prompt_status(label, default=default)


# ---------------------------------------------------------------------------
# Actions
# ---------------------------------------------------------------------------


def action_create() -> None:
    console.rule("[success]Create Task[/success]")
    title = _prompt("Title")
    description = _prompt("Description", required=False)
    with _client() as c:
        resp = c.post("/api/v1/tasks", json={"title": title, "description": description})
    if resp.status_code == 201:
        data = resp.json()
        ctx.push(data["id"])
        _display_task(data, label="Created")
    else:
        _display_error(resp)


def action_get() -> None:
    console.rule("[success]Get Task[/success]")
    task_id = _prompt_task_id()
    with _client() as c:
        resp = c.get(f"/api/v1/tasks/{task_id}")
    if resp.status_code == 200:
        data = resp.json()
        ctx.push(data["id"])
        _display_task(data)
    else:
        _display_error(resp)


def action_list() -> None:
    console.rule("[success]List Tasks[/success]")
    console.print("  Filter by status? (leave blank for all)")
    status_filter = _prompt("Status filter", required=False)
    params = {}
    if status_filter:
        if status_filter.isdigit():
            statuses = ["todo", "in_progress", "done"]
            idx = int(status_filter) - 1
            if 0 <= idx < 3:
                status_filter = statuses[idx]
        params["status"] = status_filter

    with _client() as c:
        resp = c.get("/api/v1/tasks", params=params)
    if resp.status_code != 200:
        _display_error(resp)
        return

    data = resp.json()
    tasks = data.get("tasks", [])
    if not tasks:
        console.print("  [muted]No tasks found.[/muted]")
        return

    # Push all IDs into context ring
    ctx.push_many([t["id"] for t in tasks])

    table = Table(title=f"Tasks ({data['count']})", show_lines=True)
    table.add_column("#", style="menu.key", width=3)
    table.add_column("ID", style="id", max_width=36)
    table.add_column("Title")
    table.add_column("Status")
    table.add_column("Created")

    status_colors = {"todo": "yellow", "in_progress": "blue", "done": "green"}
    for i, t in enumerate(tasks, 1):
        s = t["status"]
        color = status_colors.get(s, "white")
        table.add_row(
            str(i),
            t["id"],
            t["title"],
            f"[{color}]{s}[/{color}]",
            t.get("created_at", "")[:19],
        )
    console.print(table)
    console.print("  [info]All listed IDs are now in context for quick reuse.[/info]")


def action_update() -> None:
    console.rule("[success]Update Task Status[/success]")
    task_id = _prompt_task_id()

    # Fetch current status to show as default
    current_status = None
    with _client() as c:
        resp = c.get(f"/api/v1/tasks/{task_id}")
    if resp.status_code == 200:
        current_status = resp.json().get("status")
        console.print(f"  [muted]Current status: {current_status}[/muted]")

    new_status = _prompt_status("New status", default=current_status)

    with _client() as c:
        resp = c.patch(f"/api/v1/tasks/{task_id}", json={"status": new_status})
    if resp.status_code == 204:
        console.print(f"  [success]Task updated to '{new_status}'.[/success]")
        ctx.push(task_id)
    else:
        _display_error(resp)


def action_delete() -> None:
    console.rule("[success]Delete Task[/success]")
    task_id = _prompt_task_id()
    console.print(f"  [error]Delete task {task_id}?[/error] (y/N): ", end="")
    confirm = input().strip().lower()
    if confirm != "y":
        console.print("  [muted]Cancelled.[/muted]")
        return
    with _client() as c:
        resp = c.delete(f"/api/v1/tasks/{task_id}")
    if resp.status_code == 204:
        console.print("  [success]Task deleted.[/success]")
    else:
        _display_error(resp)


# ---------------------------------------------------------------------------
# Main menu
# ---------------------------------------------------------------------------

ACTIONS = {
    "1": ("Create Task", action_create),
    "2": ("Get Task by ID", action_get),
    "3": ("List Tasks", action_list),
    "4": ("Update Task Status", action_update),
    "5": ("Delete Task", action_delete),
}


def show_menu() -> None:
    console.print()
    panel_lines = []
    for key, (label, _) in ACTIONS.items():
        panel_lines.append(f"  [menu.key]{key}[/menu.key]  {label}")
    panel_lines.append(f"  [menu.key]q[/menu.key]  Quit")
    if ctx.last_id:
        panel_lines.append("")
        panel_lines.append(f"  [muted]Last ID: [id]{ctx.last_id}[/id][/muted]")
    console.print(Panel("\n".join(panel_lines), title="Task Manager", border_style="cyan"))


def main() -> None:
    # Allow overriding base URL via CLI arg
    global BASE_URL
    for arg in sys.argv[1:]:
        if arg.startswith("--base-url="):
            BASE_URL = arg.split("=", 1)[1]
        elif arg == "--base-url" and sys.argv.index(arg) + 1 < len(sys.argv):
            BASE_URL = sys.argv[sys.argv.index(arg) + 1]

    console.print(
        Panel(
            "[bold]Task Manager TUI[/bold]\n"
            f"[muted]Talking to {BASE_URL}[/muted]\n"
            "[muted]IDs from responses are auto-captured for reuse[/muted]",
            border_style="cyan",
        )
    )

    while True:
        show_menu()
        console.print("  Choose: ", end="")
        try:
            choice = input().strip().lower()
        except (KeyboardInterrupt, EOFError):
            console.print("\n  [muted]Bye![/muted]")
            break

        if choice == "q":
            console.print("  [muted]Bye![/muted]")
            break

        action = ACTIONS.get(choice)
        if action:
            try:
                action[1]()
            except httpx.ConnectError:
                console.print(
                    f"\n  [error]Cannot connect to {BASE_URL}.[/error]"
                    "\n  [muted]Is the API server running?  "
                    "Start it with: uv run uvicorn src.api.main:app --port 8000[/muted]"
                )
            except KeyboardInterrupt:
                console.print("\n  [muted]Action cancelled.[/muted]")
        else:
            console.print("  [error]Invalid choice.[/error]")


if __name__ == "__main__":
    main()
