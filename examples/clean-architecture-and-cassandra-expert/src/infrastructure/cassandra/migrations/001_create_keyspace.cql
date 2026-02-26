-- Migration: 001_create_keyspace
-- Description: Creates the ticker_data keyspace for local development.
-- Idempotent: Yes

CREATE KEYSPACE IF NOT EXISTS ticker_data
  WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
