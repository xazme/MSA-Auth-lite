from .config import Config
from .components import ComponentsConfig


class ApplicationSettings(Config, ComponentsConfig): ...


settings = ApplicationSettings()

__all__ = [
    "settings",
]
