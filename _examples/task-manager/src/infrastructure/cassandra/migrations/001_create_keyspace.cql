-- Migration: 001_create_keyspace
-- Description: Creates the task_manager keyspace.
-- Idempotent: Yes

CREATE KEYSPACE IF NOT EXISTS task_manager
WITH replication = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
};
