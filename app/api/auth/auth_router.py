import logging
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.api.auth.auth_schema import Token, TokenData
from app.api.auth.auth_utils import create_access_token
from app.api.dependencies import get_pwd_context, get_db_session
from app.api.users.users_utils import get_user_by_email
from app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

logger = logging.getLogger(__name__)


@router.post("/token", response_model=Token, description="Login with username and password.")
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db_session),
        pwd_context: CryptContext = Depends(get_pwd_context)
) -> Token:
    user = get_user_by_email(db, email=form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if not pwd_context.verify(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data=TokenData(sub=user.email).model_dump(mode="json"),
        secret_key=settings.auth.secret_key.get_secret_value(),
        algorithm=settings.auth.algorithm,
        expires_delta=timedelta(minutes=settings.auth.access_token_expire_minutes)
    )
    return Token(access_token=access_token, token_type="bearer")  # nosec
