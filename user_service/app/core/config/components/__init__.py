from .db_config import DataBaseConfig
from .kafka_config import KafkaConfig
from .pg_admin_config import PGAdminConfig


class ComponentsConfig(
    DataBaseConfig,
    KafkaConfig,
    PGAdminConfig,
): ...


__all__ = ["ComponentsConfig"]
