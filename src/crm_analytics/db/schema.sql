-- src/crm_analytics/db/schema.sql
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Core metrics table: one row per (tenant, metric_name, window)
CREATE TABLE IF NOT EXISTS metrics (
    recorded_at   TIMESTAMPTZ NOT NULL,
    tenant_id     TEXT        NOT NULL,
    metric_name   TEXT        NOT NULL,  -- e.g. 'deals_closed', 'contacts_created', 'activities_logged'
    metric_value  DOUBLE PRECISION NOT NULL,
    window_type   TEXT        NOT NULL   -- '1m', '1h', '1d', '7d'
);

-- Convert to hypertable partitioned by time (1-day chunks)
SELECT create_hypertable('metrics', 'recorded_at', if_not_exists => TRUE);

-- Index for fast per-tenant queries
CREATE INDEX IF NOT EXISTS idx_metrics_tenant ON metrics (tenant_id, metric_name, recorded_at DESC);

-- Anomalies table
CREATE TABLE IF NOT EXISTS anomalies (
    detected_at   TIMESTAMPTZ NOT NULL,
    tenant_id     TEXT        NOT NULL,
    metric_name   TEXT        NOT NULL,
    metric_value  DOUBLE PRECISION NOT NULL,
    z_score       DOUBLE PRECISION NOT NULL,
    PRIMARY KEY (tenant_id, metric_name, detected_at)
);
