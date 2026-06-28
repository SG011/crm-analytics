import os
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaOffsetResetStrategy
from pyflink.common.serialization import SimpleStringSchema


def build_kafka_source() -> KafkaSource:
    return (
        KafkaSource.builder()
        .set_bootstrap_servers(os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"))
        .set_topics("crm-events")
        .set_group_id("crm-analytics-flink")
        .set_starting_offsets(KafkaOffsetResetStrategy.EARLIEST)
        .set_value_only_deserializer(SimpleStringSchema())
        .build()
    )
