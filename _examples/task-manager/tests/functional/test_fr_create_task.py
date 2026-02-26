"""
FR-001: Create a Task
=====================
Priority: P1

As a user, I want to POST a new task
so that I can track things I need to do.

Acceptance:
  - GIVEN a valid payload {title, description}
    WHEN POST /api/v1/tasks
    THEN 201 is returned with a task including a generated UUID
  - GIVEN a missing title
    WHEN POST /api/v1/tasks
    THEN 422 is returned
"""

import pytest
from httpx import ASGITransport, AsyncClient

from src.api.main import app


@pytest.fixture
def client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.functional
async def test_create_task_success(client):
    async with client as c:
        resp = await c.post("/api/v1/tasks", json={"title": "Buy milk", "description": "2%"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Buy milk"
    assert data["status"] == "todo"
    assert "id" in data


@pytest.mark.functional
async def test_create_task_missing_title(client):
    async with client as c:
        resp = await c.post("/api/v1/tasks", json={"description": "no title"})
    assert resp.status_code == 422
