from datetime import datetime, timedelta, timezone

from jose import jwt


def create_access_token(
        data: dict,
        secret_key: str,
        algorithm: str,
        expires_delta: timedelta | None = None
) -> str:
    claims = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    claims.update({"exp": expire})
    return jwt.encode(claims=claims, key=secret_key, algorithm=algorithm)
