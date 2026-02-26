# Dojo 003 — Custom Agents and Skills

This repository is a **dojo coding exercise** in which we build **GitHub Copilot custom agents** with specific, repeatable prompts defined at the team level, plus the ability to explicitly use **skills** to define exactly how certain commands should be implemented.

## What are Custom Agents?

Custom agents are Markdown-based profiles (`.agent.md`) that tailor Copilot's expertise for specific tasks. Each agent profile declares a name, description, available tools, and a detailed prompt that shapes the agent's behavior.

You can create agents at the **repository**, **organization**, or **personal** level, and they are available wherever Copilot coding agent runs — in your IDE, the GitHub CLI, or on github.com.

> **Reference:** [Creating custom agents for Copilot coding agent](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-custom-agents)

## What are Agent Skills?

Agent skills are folders of instructions, scripts, and resources that Copilot can load when relevant to improve its performance on specialized tasks. Skills live in your repository (`.github/skills` or `.claude/skills`) or in your home directory (`~/.copilot/skills` or `~/.claude/skills`).

Skills let you teach Copilot to perform tasks in a **specific, repeatable way** — for example, how to scaffold a new page, how to create a data pipeline with embedded tests, or how to wire up a new API endpoint.

> **Reference:** [About agent skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)

## Objectives

1. **Build custom agents** with team-level prompts that encode our conventions and standards.
2. **Create skills** that define exactly how recurring tasks should be implemented.
3. **Try agents locally** in the IDE (VS Code, JetBrains, etc.) and via the GitHub Copilot CLI.
4. **Try agents from GitHub** as a background coding agent that opens pull requests autonomously.

## Use Cases

We will exercise these custom agents on repeatable tasks such as:

- **A new page on a web portal** — scaffold a frontend page with routing, components, and tests following our conventions.
- **A new data pipeline with embedded automated tests** — generate ingestion, transformation, and validation steps with built-in test coverage.
- **A new API endpoint in an existing system** — add route, controller, service, and integration tests using our established patterns.

## Repository Structure

```
.
├── README.md
├── backend/              # API and backend services
├── frontend/             # Web portal / UI application
├── data-pipelines/       # Data ingestion and transformation pipelines
└── examples/
    └── clean-architecture-and-cassandra-expert/
        ├── .github/
        │   ├── agents/   # Custom agent profile (.agent.md)
        │   └── skills/   # Agent skills (e.g. cassandra-migrations)
        ├── src/           # FastAPI + Cassandra clean-architecture app
        ├── tests/
        │   ├── unit/      # Isolated domain & use-case tests
        │   └── functional/# FR tests with spec-as-docstring pattern
        ├── scripts/       # Migration runner, Cassandra reset helpers
        └── docker-compose.yml
```

## Examples

### `clean-architecture-and-cassandra-expert`

A complete working example that demonstrates:

- **Custom agent** (`.github/agents/clean-architecture-and-cassandra-expert.agent.md`) — encodes team conventions for building Python/FastAPI services backed by Cassandra with clean architecture layering.
- **Agent skill** (`.github/skills/cassandra-migrations/SKILL.md`) — teaches the agent how to create versioned CQL migrations, reset the Docker database, and redeploy Cassandra from scratch.
- **FR-as-docstring testing pattern** — functional requirements are written as concise Python docstrings (inspired by [spec-kit](https://github.com/github/spec-kit) and [OpenSpec](https://github.com/Fission-AI/OpenSpec)) directly inside `tests/functional/test_fr_*.py` files, making each test file the single source of truth for its requirement.
- **uv** for dependency management, **Docker Compose** for Cassandra, **pytest** for both unit and FR tests.

#### Quick start

```bash
cd examples/clean-architecture-and-cassandra-expert

# Set up the Python environment
uv sync --all-extras

# Start Cassandra and run migrations
scripts/reset-cassandra.sh

# Run unit tests (no Docker needed)
uv run pytest tests/unit -v

# Run functional requirement tests (requires Cassandra)
uv run pytest tests/functional -v

# Start the API server
uv run uvicorn src.api.main:app --reload
```

## Getting Started

> _More agent profiles and skills will be added as the dojo progresses._
