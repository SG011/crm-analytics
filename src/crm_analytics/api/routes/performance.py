from fastapi import APIRouter
from crm_analytics.db.connection import get_connection

router = APIRouter()

@router.get("/performance/{tenant_id}")
def get_performance(tenant_id: str):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT metric_name,
                   time_bucket('1 hour', recorded_at) AS bucket,
                   SUM(metric_value) AS total
            FROM metrics
            WHERE tenant_id = %s
              AND recorded_at > NOW() - INTERVAL '7 days'
            GROUP BY metric_name, bucket
            ORDER BY metric_name, bucket
            """,
            (tenant_id,)
        )
        rows = cur.fetchall()
    metrics: dict = {}
    for metric_name, bucket, total in rows:
        metrics.setdefault(metric_name, []).append({"bucket": bucket.isoformat(), "total": total})
    return metrics
