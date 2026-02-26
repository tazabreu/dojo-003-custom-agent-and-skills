#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

echo "==> Tearing down Cassandra (removing volumes)..."
docker compose down -v

echo "==> Starting fresh Cassandra..."
docker compose up -d cassandra

echo "==> Waiting for Cassandra..."
"$SCRIPT_DIR/wait-for-cassandra.sh"

echo "==> Running migrations..."
uv run python scripts/migrate.py

echo "==> Done! Cassandra is fresh and migrated."
