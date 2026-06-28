import httpx
from crm_analytics.flink.operators.anomaly import ZScoreAnomalyDetector

class AlertEngine:
    def __init__(self, webhook_url: str, threshold: float = 3.0):
        self._detector = ZScoreAnomalyDetector(threshold=threshold)
        self._webhook_url = webhook_url

    def check_and_alert(
        self,
        tenant_id: str,
        metric_name: str,
        value: float,
        mean: float,
        stddev: float,
    ) -> bool:
        is_anomaly, z_score = self._detector.detect(value, mean, stddev)
        if not is_anomaly:
            return False
        try:
            httpx.post(
                self._webhook_url,
                json={
                    "tenant_id": tenant_id,
                    "metric_name": metric_name,
                    "value": value,
                    "z_score": round(z_score, 2),
                    "message": f"Anomaly detected: {metric_name} for {tenant_id} = {value} (z={z_score:.2f})",
                },
                timeout=5,
            )
        except Exception:
            pass  # alert delivery failure must not crash the pipeline
        return True
