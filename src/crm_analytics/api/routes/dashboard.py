from fastapi import APIRouter, HTTPException
from crm_analytics.db.connection import get_connection

router = APIRouter()

def query_metrics(tenant_id: str) -> list[tuple]:
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT metric_name, SUM(metric_value) as total, window_type
            FROM metrics
            WHERE tenant_id = %s
              AND recorded_at > NOW() - INTERVAL '1 day'
            GROUP BY metric_name, window_type
            ORDER BY metric_name
            """,
            (tenant_id,)
        )
        return cur.fetchall()

@router.get("/dashboard/{tenant_id}")
def get_dashboard(tenant_id: str):
    rows = query_metrics(tenant_id)
    if not rows:
        raise HTTPException(status_code=404, detail=f"No metrics found for tenant {tenant_id}")
    return [{"metric_name": r[0], "total": r[1], "window": r[2]} for r in rows]
