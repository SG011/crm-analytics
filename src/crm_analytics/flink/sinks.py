from pyflink.datastream.functions import SinkFunction
from crm_analytics.db.connection import get_connection
from datetime import datetime, timezone


class TimescaleDBSink(SinkFunction):
    def __init__(self):
        self._conn = None

    def invoke(self, value: dict, context) -> None:
        if self._conn is None or self._conn.closed:
            self._conn = get_connection()
        with self._conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO metrics (recorded_at, tenant_id, metric_name, metric_value, window_type)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    datetime.now(timezone.utc),
                    value["tenant_id"],
                    value["metric_name"],
                    float(value["count"]),
                    value.get("window_type", "1m"),
                )
            )
        self._conn.commit()
