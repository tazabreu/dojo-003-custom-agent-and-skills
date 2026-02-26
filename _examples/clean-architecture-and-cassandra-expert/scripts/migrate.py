"""Cassandra migration runner.

Reads .cql files from src/infrastructure/cassandra/migrations/, applies them
in order, and tracks applied migrations in a schema_migrations table.
"""

import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from cassandra.cluster import Cluster


CONTACT_POINTS = os.getenv("CASSANDRA_CONTACT_POINTS", "127.0.0.1").split(",")
KEYSPACE = os.getenv("CASSANDRA_KEYSPACE", "ticker_data")
MIGRATIONS_DIR = Path(__file__).resolve().parent.parent / "src/infrastructure/cassandra/migrations"


def run_migrations() -> None:
    cluster = Cluster(CONTACT_POINTS)
    session = cluster.connect()

    migration_files = sorted(MIGRATIONS_DIR.glob("*.cql"))
    if not migration_files:
        print("No migration files found.")
        return

    keyspace_migration = migration_files[0]
    print(f"Applying bootstrap: {keyspace_migration.name}")
    for statement in _split_statements(keyspace_migration.read_text()):
        session.execute(statement)

    session.set_keyspace(KEYSPACE)

    tracking_migration = [f for f in migration_files if "schema_migrations" in f.name]
    if tracking_migration:
        print(f"Ensuring tracking table: {tracking_migration[0].name}")
        for statement in _split_statements(tracking_migration[0].read_text()):
            session.execute(statement)

    applied = _get_applied(session)
    print(f"Already applied: {len(applied)} migration(s)")

    for mf in migration_files:
        if mf.name in applied:
            continue
        print(f"Applying: {mf.name} ... ", end="")
        for statement in _split_statements(mf.read_text()):
            session.execute(statement)
        session.execute(
            "INSERT INTO schema_migrations (name, applied_at) VALUES (%s, %s)",
            (mf.name, datetime.now(timezone.utc)),
        )
        print("OK")

    print("All migrations applied.")
    cluster.shutdown()


def _get_applied(session) -> set[str]:
    try:
        rows = session.execute("SELECT name FROM schema_migrations")
        return {row.name for row in rows}
    except Exception:
        return set()


def _split_statements(cql_text: str) -> list[str]:
    statements = []
    for raw in cql_text.split(";"):
        stripped = raw.strip()
        if stripped and not stripped.startswith("--"):
            statements.append(stripped)
    return statements


if __name__ == "__main__":
    try:
        run_migrations()
    except Exception as exc:
        print(f"Migration failed: {exc}", file=sys.stderr)
        sys.exit(1)
