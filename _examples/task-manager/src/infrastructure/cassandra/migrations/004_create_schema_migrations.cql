-- Migration: 004_create_schema_migrations
-- Description: Tracking table for applied migrations.
-- Idempotent: Yes

CREATE TABLE IF NOT EXISTS schema_migrations (
    name       text PRIMARY KEY,
    applied_at timestamp
);
