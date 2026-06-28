from dataclasses import dataclass
from pyflink.datastream.functions import AggregateFunction


@dataclass
class MetricAccumulator:
    tenant_id: str = ""
    metric_name: str = ""
    count: int = 0


class CountAggregator(AggregateFunction):
    def create_accumulator(self) -> MetricAccumulator:
        return MetricAccumulator()

    def add(self, value: dict, accumulator: MetricAccumulator) -> MetricAccumulator:
        accumulator.tenant_id = value.get("tenant_id", "")
        accumulator.metric_name = value.get("event_type", "unknown")
        accumulator.count += 1
        return accumulator

    def get_result(self, accumulator: MetricAccumulator) -> dict:
        return {
            "tenant_id": accumulator.tenant_id,
            "metric_name": accumulator.metric_name,
            "count": accumulator.count,
        }

    def merge(self, a: MetricAccumulator, b: MetricAccumulator) -> MetricAccumulator:
        return MetricAccumulator(
            tenant_id=a.tenant_id,
            metric_name=a.metric_name,
            count=a.count + b.count,
        )
