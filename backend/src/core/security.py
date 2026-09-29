from datetime import datetime, timedelta, timezone

import bcrypt
from jose import jwt

from src.core.config import settings


def gerar_hash_senha(senha_pura: str) -> str:
    senha_bytes = senha_pura.encode("utf-8")
    hash_bytes = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())

    return hash_bytes.decode("utf-8")


def verificar_senha(
    senha_pura: str,
    senha_hash: str,
) -> bool:
    senha_bytes = senha_pura.encode("utf-8")
    hash_bytes = senha_hash.encode("utf-8")

    return bcrypt.checkpw(senha_bytes, hash_bytes)


def criar_token_acesso(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )