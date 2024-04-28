from fastapi import Security, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session
from sqlmodel import select

from app.api.users.users_schema import User
from app.config import settings
from app.database import engine

auth_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_pwd_context() -> CryptContext:
    return pwd_context


def get_db_session() -> Session:
    """Dependency for getting a database session."""
    with Session(engine) as session:
        yield session


def get_current_user(
        db: Session = Depends(get_db_session),
        token: str = Security(auth_scheme)
) -> User:
    """Dependency for getting the current user."""
    token_data = decode_token(token)
    user = db.exec(select(User).where(User.email == token_data["sub"])).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def decode_token(token: str) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            key=settings.auth.secret_key.get_secret_value(),
            algorithms=[settings.auth.algorithm]
        )
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception
        return dict(sub=sub)
    except JWTError:
        raise credentials_exception
