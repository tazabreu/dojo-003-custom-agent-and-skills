-- Migration: 003_create_schema_migrations
-- Description: Tracking table for applied migrations.
-- Idempotent: Yes

CREATE TABLE IF NOT EXISTS ticker_data.schema_migrations (
    name       text PRIMARY KEY,
    applied_at timestamp
);
