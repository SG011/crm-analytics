import pytest
from crm_analytics.flink.operators.aggregation import CountAggregator, MetricAccumulator

def test_add_increments_count():
    agg = CountAggregator()
    acc = agg.create_accumulator()
    acc = agg.add({"tenant_id": "t1", "event_type": "ContactCreated"}, acc)
    acc = agg.add({"tenant_id": "t1", "event_type": "ContactCreated"}, acc)
    result = agg.get_result(acc)
    assert result["count"] == 2

def test_merge_combines_accumulators():
    agg = CountAggregator()
    acc1 = MetricAccumulator(tenant_id="t1", metric_name="ContactCreated", count=3)
    acc2 = MetricAccumulator(tenant_id="t1", metric_name="ContactCreated", count=5)
    merged = agg.merge(acc1, acc2)
    assert merged.count == 8

def test_get_result_returns_dict_with_expected_keys():
    agg = CountAggregator()
    acc = agg.create_accumulator()
    acc = agg.add({"tenant_id": "t1", "event_type": "DealCreated"}, acc)
    result = agg.get_result(acc)
    assert "tenant_id" in result
    assert "metric_name" in result
    assert "count" in result
