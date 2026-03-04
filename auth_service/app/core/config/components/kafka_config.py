from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from ..constans import ENV_FILE_PATH


class KafkaConfig(BaseSettings):
    kafka_client_id: str = Field(default="Nameless Broker")
    kafka_bootstrap_servers: str = Field(default="putyourserver:port")
    kafka_enable_idempotence: bool = Field(default=True)

    kafka_acks: str | int = Field(default="all")
    kafka_retries: int = Field(default=2147483647)
    kafka_max_in_flight_requests_per_connection: int = Field(default=5)

    kafka_request_timeout_ms: int = Field(default=30000)
    kafka_retry_backoff: int = Field(default=100)
    kafka_linger_ms: int = Field(default=50)
    kafka_max_age_metadata_ms: int = Field(default=5000)

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
    )
