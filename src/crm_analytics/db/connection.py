# src/crm_analytics/db/connection.py
import os
import psycopg2

def get_connection():
    return psycopg2.connect(
        host=os.getenv("TIMESCALEDB_HOST", "localhost"),
        port=int(os.getenv("TIMESCALEDB_PORT", "5432")),
        dbname=os.getenv("TIMESCALEDB_DB", "crm_analytics"),
        user=os.getenv("TIMESCALEDB_USER", "analytics"),
        password=os.getenv("TIMESCALEDB_PASSWORD", "analytics_pass"),
    )
