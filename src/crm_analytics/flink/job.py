import json
import os
from pyflink.datastream import StreamExecutionEnvironment, CheckpointingMode
from pyflink.common import WatermarkStrategy, Time
from pyflink.datastream.window import TumblingEventTimeWindows
from crm_analytics.flink.sources import build_kafka_source
from crm_analytics.flink.operators.aggregation import CountAggregator
from crm_analytics.flink.sinks import TimescaleDBSink


def run():
    env = StreamExecutionEnvironment.get_execution_environment()

    # Exactly-once checkpointing every 10 seconds
    env.enable_checkpointing(10_000, CheckpointingMode.EXACTLY_ONCE)
    env.get_checkpoint_config().set_checkpoint_storage_uri(
        os.getenv("FLINK_CHECKPOINT_DIR", "file:///tmp/flink-checkpoints")
    )

    source = build_kafka_source()
    stream = env.from_source(source, WatermarkStrategy.no_watermarks(), "crm-events-source")

    # Parse JSON → dict
    parsed = stream.map(lambda raw: json.loads(raw))

    # Key by tenant_id, count events in 1-minute tumbling windows
    result = (
        parsed
        .key_by(lambda e: e.get("tenant_id", "unknown"))
        .window(TumblingEventTimeWindows.of(Time.minutes(1)))
        .aggregate(CountAggregator())
        .map(lambda r: {**r, "window_type": "1m"})
    )

    result.add_sink(TimescaleDBSink())

    env.execute("crm-analytics-pipeline")


if __name__ == "__main__":
    run()
