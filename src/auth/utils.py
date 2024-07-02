from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from src.auth import consts, schemas
from src.config import settings
from src.users import models


def encode_jwt(
    payload: dict,
    private_key: str = settings.private_key_path.read_text(),
    algorithm: str = settings.algorithm,
    expire_minutes: int = settings.access_token_expire_minutes,
) -> str:
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.public_key_path.read_text(),
    algorithm: str = settings.algorithm,
) -> dict:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


def encode_password(raw_password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = raw_password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def check_password(raw_password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(
        password=raw_password.encode(),
        hashed_password=hashed_password,
    )


def create_access_token(user: models.User) -> str:
    payload = {
        "type": consts.JWTTokenType.ACCESS,
        "username": user.username,
        "sub": user.id,
    }
    return encode_jwt(payload=payload)


def create_refresh_token(user: models.User) -> str:
    payload = {
        "type": consts.JWTTokenType.REFRESH,
        "sub": user.id,
    }
    return encode_jwt(payload=payload)


async def create_auth_tokens(user: models.User) -> schemas.Token:
    return schemas.Token(access_token=create_access_token(user), refresh_token=create_refresh_token(user))
