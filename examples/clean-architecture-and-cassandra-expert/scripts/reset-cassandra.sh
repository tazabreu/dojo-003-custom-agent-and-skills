#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "==> Tearing down Cassandra (removing volumes)..."
docker compose -f "$PROJECT_DIR/docker-compose.yml" down -v

echo "==> Starting fresh Cassandra..."
docker compose -f "$PROJECT_DIR/docker-compose.yml" up -d cassandra

echo "==> Waiting for Cassandra to be healthy..."
"$SCRIPT_DIR/wait-for-cassandra.sh"

echo "==> Running migrations..."
cd "$PROJECT_DIR"
uv run python scripts/migrate.py

echo "==> Done. Cassandra is fresh and migrated."
