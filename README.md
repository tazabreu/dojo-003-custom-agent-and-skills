# Dojo 003 — Custom Agents, Skills & Background Agents

This repo is a dojo to experiment with how **instructions**, **custom agents**, and **skills** improve the quality and reliability of work done by **background agents**.

The canonical “what are we doing today?” brief is in [INSTRUCTIONS.html](INSTRUCTIONS.html).

## Goals (from INSTRUCTIONS.html)

1. Experiment with key primitives: **instructions**, **custom agents**, and **skills**.
2. Automate a recurring task (e.g., scaffolding web pages, API endpoints, or data-pipeline test structures).
3. Validate how these primitives improve **background agents** capabilities.

## Agenda

- Watch a quick demo of the expected output (5 min)
- Breakout sessions (40 min)
  - Pick a recurring task from your team’s workflow.
  - Build a small **agent** (standards/guidelines to reach a goal) paired with a **skill** (concrete, repeatable implementation steps).
  - If time permits, run it from **GitHub.com** using background-agent capabilities.
- Regroup and share insights (10 min)

## How to Use This Repo

### 1) Start from instructions (not from example code)

- Repo-level guardrails live in `.github/copilot-instructions.md`.
- Skills live under `.github/skills/<skill-name>/SKILL.md`.
- Agent profiles (if used) live under `.github/agents/*.agent.md`.

The intent is: encode conventions once, then let background agents apply them consistently.

### 2) Pick one “recurring task” and make it reproducible

Good candidates usually have:

- Clear inputs/outputs (e.g., “add an endpoint + tests + docs”)
- A stable structure (folders, naming, architectural boundaries)
- Easy verification (tests, linters, or a “definition of done” checklist)

### 3) Validate the impact

Compare outcomes with and without the instructions/agent/skill:

- Fewer back-and-forth clarifications
- More consistent structure and naming
- Better test coverage and edge-case handling
- Higher success rate for background-agent PRs

## About `_examples/`

`_examples/` contains generated apps used to exercise the dojo concepts. They are **not the goal** of this repository; they’re just convenient sandboxes for testing instructions, agents, and skills.

## References

- Creating custom agents: https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-custom-agents
- About agent skills: https://docs.github.com/en/copilot/concepts/agents/about-agent-skills
