from enum import Enum


class TokenType(str, Enum):
    ACCESS = "Access"
    REFRESH = "Refresh"
