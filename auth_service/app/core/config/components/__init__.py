from .db_config import DataBaseConfig
from .jwt_config import JWTConfig
from .kafka_config import KafkaConfig
from .pg_admin_config import PGAdminConfig


class ComponentsConfig(
    DataBaseConfig,
    JWTConfig,
    KafkaConfig,
    PGAdminConfig,
): ...


__all__ = ["ComponentsConfig"]
