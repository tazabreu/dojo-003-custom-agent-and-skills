# Clean Architecture & Cassandra Expert — Example

This example demonstrates a **GitHub Copilot custom agent** and **skill** for building Python APIs with FastAPI and Apache Cassandra using clean architecture.

## What's Included

| Path | Purpose |
|------|---------|
| `.github/agents/clean-architecture-and-cassandra-expert.agent.md` | Custom agent profile — defines behavior, architecture rules, and testing strategy |
| `.github/skills/cassandra-migrations/SKILL.md` | Skill — versioned CQL migration management and Docker lifecycle |
| `src/` | Clean architecture source code (domain → application → infrastructure → api) |
| `tests/unit/` | Unit tests — mocked, no I/O |
| `tests/functional/` | FR tests — spec-as-docstring pattern, run against real Cassandra |
| `scripts/` | Migration runner, Cassandra wait/reset helpers |
| `docker-compose.yml` | Local Cassandra 4.1 with health check |

## FR-as-Docstring Pattern

Functional requirements live as module-level docstrings in `tests/functional/test_fr_*.py` files, blending [spec-kit](https://github.com/github/spec-kit)'s Given/When/Then acceptance scenarios with [OpenSpec](https://github.com/Fission-AI/OpenSpec)'s concise proposal style:

```python
"""
FR-001: Insert Ticker Price Data
=================================
Priority: P1

As a data consumer, I want to POST ticker price records
so that historical stock prices are persisted for analysis.

Acceptance:
  - GIVEN a valid payload {ticker, price, timestamp}
    WHEN  POST /api/v1/ticker-prices
    THEN  201 Created is returned with the persisted record
  ...
"""
```

This keeps the spec co-located with its validation — no separate document to keep in sync.

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- Docker and Docker Compose

## Quick Start

```bash
# Install dependencies
uv sync --all-extras

# Start Cassandra & run migrations
scripts/reset-cassandra.sh

# Unit tests (no Docker needed)
uv run pytest tests/unit -v

# FR tests (requires running Cassandra)
uv run pytest tests/functional -v

# Start the API
uv run uvicorn src.api.main:app --reload
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/ticker-prices` | Insert a ticker price record |
| `GET` | `/api/v1/ticker-prices/{ticker}` | Query price history (optional `start`/`end` params) |
