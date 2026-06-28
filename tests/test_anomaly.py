import pytest
from crm_analytics.flink.operators.anomaly import ZScoreAnomalyDetector

def test_normal_value_not_anomaly():
    detector = ZScoreAnomalyDetector(threshold=3.0)
    is_anomaly, z = detector.detect(value=105.0, mean=100.0, stddev=10.0)
    assert is_anomaly is False
    assert abs(z - 0.5) < 0.001

def test_extreme_value_is_anomaly():
    detector = ZScoreAnomalyDetector(threshold=3.0)
    is_anomaly, z = detector.detect(value=145.0, mean=100.0, stddev=10.0)
    assert is_anomaly is True
    assert z == pytest.approx(4.5)

def test_zero_stddev_not_anomaly():
    detector = ZScoreAnomalyDetector(threshold=3.0)
    is_anomaly, z = detector.detect(value=100.0, mean=100.0, stddev=0.0)
    assert is_anomaly is False
    assert z == 0.0
