from faststream.kafka import KafkaBroker
from app.core.config import settings


def create_kafka_broker() -> KafkaBroker:
    broker = KafkaBroker(
        bootstrap_servers=settings.kafka_bootstrap_servers,
        client_id=settings.kafka_client_id,
        enable_idempotence=settings.kafka_enable_idempotence,
        acks=settings.kafka_acks,
        request_timeout_ms=settings.kafka_request_timeout_ms,
        retry_backoff_ms=settings.kafka_retry_backoff,
        linger_ms=settings.kafka_linger_ms,
        metadata_max_age_ms=settings.kafka_max_age_metadata_ms,
    )
    return broker
