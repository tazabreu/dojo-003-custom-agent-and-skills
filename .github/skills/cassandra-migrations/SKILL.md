---
name: cassandra-migrations
description: >
  Manages versioned Cassandra schema migrations and Docker lifecycle.
  Use this skill when creating tables, altering schemas, resetting the
  database, or redeploying Cassandra fresh in Docker.
---

You are responsible for managing Apache Cassandra schema migrations in a versioned, repeatable way. All DDL changes go through migration files — never apply CQL statements ad-hoc.

## Migration File Convention

Migrations live in `src/infrastructure/cassandra/migrations/` and follow this naming:

```
NNN_short_description.cql
```

Where `NNN` is a zero-padded, monotonically increasing number (e.g., `001`, `002`).

### Example Migration

```cql
-- Migration: 001_create_ticker_prices
-- Description: Creates the ticker_prices table for storing historical stock data.
-- Idempotent: Yes

CREATE TABLE IF NOT EXISTS ticker_prices (
    ticker    text,
    ts        timestamp,
    price     decimal,
    currency  text,
    source    text,
    PRIMARY KEY (ticker, ts)
) WITH CLUSTERING ORDER BY (ts DESC)
  AND comment = 'Historical ticker price data, partitioned by ticker, sorted newest-first';
```

### Rules for Writing Migrations

1. **Always idempotent** — Use `IF NOT EXISTS` / `IF EXISTS` guards so migrations can be re-run safely.
2. **One concern per file** — Each migration does one thing (create a table, add a column, create an index).
3. **Never modify existing migrations** — To change a table, create a new migration with `ALTER TABLE`.
4. **Include a header comment** with migration number, description, and whether it is idempotent.

## Applying Migrations

Use the migration runner script at `scripts/migrate.py`:

```bash
uv run python scripts/migrate.py
```

The runner:
1. Connects to Cassandra (reads `CASSANDRA_CONTACT_POINTS` and `CASSANDRA_KEYSPACE` from env or defaults to `localhost` / `ticker_data`).
2. Creates a `schema_migrations` table if it doesn't exist.
3. Reads all `.cql` files from `src/infrastructure/cassandra/migrations/`, sorted by filename.
4. Skips migrations already recorded in `schema_migrations`.
5. Executes each pending migration inside a logged batch where possible.
6. Records the migration as applied.

## Resetting Cassandra (Fresh Deploy)

To tear down and recreate the database from scratch:

```bash
# Stop and remove containers + volumes
docker compose down -v

# Start fresh
docker compose up -d cassandra

# Wait for health check
scripts/wait-for-cassandra.sh

# Create keyspace (handled by init script or first migration)
uv run python scripts/migrate.py
```

Use the reset script for a one-liner:

```bash
scripts/reset-cassandra.sh
```

## Creating a New Migration

When asked to add or change schema:

1. Look at existing files in `src/infrastructure/cassandra/migrations/` to determine the next number.
2. Create a new file `NNN_short_description.cql` following the format above.
3. Run `uv run python scripts/migrate.py` to apply.
4. If the migration fails, **do not edit it** — create a compensating migration instead.

## Docker Compose Requirements

The `docker-compose.yml` must include:
- Cassandra 4.1+ image
- Health check using `cqlsh -e 'SELECT now() FROM system.local'`
- A named volume for data persistence (removable via `docker compose down -v`)
- Port 9042 exposed to localhost
- Environment variable `CASSANDRA_CLUSTER_NAME` set

## Keyspace Management

The default keyspace is `ticker_data` with `SimpleStrategy` and `replication_factor = 1` (local dev). The first migration or an init script should ensure it exists:

```cql
CREATE KEYSPACE IF NOT EXISTS ticker_data
  WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
```

## Troubleshooting

- **Cassandra not ready**: Use `scripts/wait-for-cassandra.sh` which polls the health check endpoint.
- **Migration stuck**: Check `schema_migrations` table for partial entries. Fix data, then re-run.
- **Schema disagreement**: Run `nodetool describecluster` inside the container to check schema versions.
