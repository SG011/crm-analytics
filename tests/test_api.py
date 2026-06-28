import pytest
import fakeredis
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from crm_analytics.api.app import app

@pytest.fixture
def client():
    return TestClient(app)

def test_health_returns_ok(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

def test_dashboard_returns_list(client):
    mock_rows = [("deals_closed", 42.0, "1d"), ("contacts_created", 100.0, "1d")]
    with patch("crm_analytics.api.routes.dashboard.query_metrics", return_value=mock_rows):
        resp = client.get("/dashboard/tenant-1")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert data[0]["metric_name"] == "deals_closed"

def test_dashboard_404_for_unknown_tenant(client):
    with patch("crm_analytics.api.routes.dashboard.query_metrics", return_value=[]):
        resp = client.get("/dashboard/nonexistent-tenant")
    assert resp.status_code == 404
