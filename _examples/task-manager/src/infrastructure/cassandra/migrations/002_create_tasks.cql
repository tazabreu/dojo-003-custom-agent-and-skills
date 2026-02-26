-- Migration: 002_create_tasks
-- Description: Creates the tasks table for storing task records.
-- Idempotent: Yes

CREATE TABLE IF NOT EXISTS tasks (
    id        uuid,
    title     text,
    description text,
    status    text,
    created_at timestamp,
    updated_at timestamp,
    PRIMARY KEY (id)
) WITH comment = 'Task records keyed by UUID';
