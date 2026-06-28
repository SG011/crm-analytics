# crm-analytics

Real-time CRM analytics pipeline — Python 3.12, Apache Flink 1.19, TimescaleDB, FastAPI. Processes 10M TPS of CRM events into live dashboards with z-score anomaly detection.

## Architecture

```
CRM Events (Kafka) → Flink JobManager → CountAggregator (keyed by tenant_id)
                                      → WindowOperator (1-min tumbling)
                                      → TimescaleDB (metrics hypertable)
                                      → AnomalyDetector → AlertEngine (webhook)

Dashboard queries: FastAPI → Redis cache (5s TTL) → TimescaleDB
```

## Running Locally

```bash
docker-compose up -d          # Flink, Kafka, TimescaleDB, Redis
python -m crm_analytics.flink.job   # start Flink pipeline
uvicorn crm_analytics.api.app:app --reload --port 9000  # query API

# Query dashboard
curl http://localhost:9000/dashboard/{tenant_id}
curl http://localhost:9000/performance/{tenant_id}
```

## Features
- Exactly-once Flink stream processing (10s checkpoint interval)
- Tumbling 1-minute windows keyed by `tenant_id`
- TimescaleDB hypertable with automatic time-based compression
- Z-score anomaly detection (threshold: z > 3.0)
- HTTP webhook alerts on anomaly detection
- Redis query cache (5s TTL) for dashboard endpoints

## Tech Stack
Python 3.12 · Apache Flink 1.19 (PyFlink) · Apache Kafka · TimescaleDB (Postgres 16) · Redis 7 · FastAPI · Testcontainers
