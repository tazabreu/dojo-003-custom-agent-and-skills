-- Migration: 003_create_tasks_by_status
-- Description: Materialised view to allow querying tasks by status.
-- Idempotent: Yes

CREATE TABLE IF NOT EXISTS tasks_by_status (
    status     text,
    created_at timestamp,
    id         uuid,
    title      text,
    PRIMARY KEY (status, created_at, id)
) WITH CLUSTERING ORDER BY (created_at DESC, id ASC)
  AND comment = 'Tasks partitioned by status, newest first';
