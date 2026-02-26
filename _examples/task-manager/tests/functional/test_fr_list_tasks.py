"""
FR-002: List and Filter Tasks
==============================
Priority: P1

As a user, I want to list all tasks and optionally filter by status
so that I can see what needs attention.

Acceptance:
  - GIVEN existing tasks
    WHEN GET /api/v1/tasks
    THEN all tasks are returned
  - GIVEN existing tasks with mixed statuses
    WHEN GET /api/v1/tasks?status=todo
    THEN only "todo" tasks are returned
"""

import pytest
from httpx import ASGITransport, AsyncClient

from src.api.main import app


@pytest.fixture
def client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.functional
async def test_list_tasks(client):
    async with client as c:
        await c.post("/api/v1/tasks", json={"title": "Task A"})
        await c.post("/api/v1/tasks", json={"title": "Task B"})
        resp = await c.get("/api/v1/tasks")
    assert resp.status_code == 200
    data = resp.json()
    assert data["count"] >= 2
