#!/usr/bin/env bash
set -euo pipefail

CONTAINER="${CASSANDRA_CONTAINER:-ticker-cassandra}"
MAX_RETRIES="${CASSANDRA_MAX_RETRIES:-30}"
SLEEP_SECONDS="${CASSANDRA_SLEEP:-5}"

echo "Waiting for Cassandra ($CONTAINER) to be ready..."

for i in $(seq 1 "$MAX_RETRIES"); do
    if docker exec "$CONTAINER" cqlsh -e "SELECT now() FROM system.local" &>/dev/null; then
        echo "Cassandra is ready (attempt $i/$MAX_RETRIES)."
        exit 0
    fi
    echo "  Attempt $i/$MAX_RETRIES — not ready yet, sleeping ${SLEEP_SECONDS}s..."
    sleep "$SLEEP_SECONDS"
done

echo "ERROR: Cassandra did not become ready after $MAX_RETRIES attempts." >&2
exit 1
