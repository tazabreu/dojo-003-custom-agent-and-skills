#!/usr/bin/env bash
set -euo pipefail

echo "Waiting for Cassandra to be ready..."

MAX_RETRIES=30
RETRY_INTERVAL=5

for i in $(seq 1 "$MAX_RETRIES"); do
    if docker compose exec cassandra cqlsh -e "SELECT now() FROM system.local" > /dev/null 2>&1; then
        echo "Cassandra is ready!"
        exit 0
    fi
    echo "  Attempt $i/$MAX_RETRIES — not ready yet, retrying in ${RETRY_INTERVAL}s..."
    sleep "$RETRY_INTERVAL"
done

echo "Cassandra did not become ready in time." >&2
exit 1
