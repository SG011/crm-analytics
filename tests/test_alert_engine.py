import pytest
from unittest.mock import MagicMock, patch
from crm_analytics.alert.alert_engine import AlertEngine

def test_no_anomaly_no_alert():
    engine = AlertEngine(webhook_url="http://fake-webhook/")
    fired = engine.check_and_alert("t1", "deals_closed", value=105.0, mean=100.0, stddev=10.0)
    assert fired is False

def test_anomaly_fires_alert():
    engine = AlertEngine(webhook_url="http://fake-webhook/")
    with patch("httpx.post") as mock_post:
        mock_post.return_value = MagicMock(status_code=200)
        fired = engine.check_and_alert("t1", "deals_closed", value=200.0, mean=100.0, stddev=10.0)
    assert fired is True
    mock_post.assert_called_once()

def test_alert_payload_contains_tenant_and_metric():
    engine = AlertEngine(webhook_url="http://fake-webhook/")
    with patch("httpx.post") as mock_post:
        mock_post.return_value = MagicMock(status_code=200)
        engine.check_and_alert("tenant-abc", "contacts_created", value=5000.0, mean=100.0, stddev=50.0)
    payload = mock_post.call_args.kwargs.get("json", {})
    assert "tenant-abc" in str(payload)
    assert "contacts_created" in str(payload)
