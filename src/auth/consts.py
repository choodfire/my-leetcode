import enum


class JWTTokenType(str, enum.Enum):
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"
