import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from sqlmodel import Session, select

from app.api.dependencies import get_pwd_context, get_db_session, get_current_user
from app.api.users.users_schema import User, UserRead, UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])

logger = logging.getLogger(__name__)


@router.post("", response_model=UserRead)
def create_user(
        user_data: UserCreate,
        db: Session = Depends(get_db_session),
        pwd_context: CryptContext = Depends(get_pwd_context)
) -> UserRead:
    """Create a user."""
    user = User(
        **user_data.model_dump(),
        password_hash=pwd_context.hash(user_data.password.get_secret_value())
    )

    existing_user = db.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        logger.error("Failed to create user: Email already exists")
        raise HTTPException(status_code=400, detail="Email already exists")

    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info("Created user with id: %s", user.id)
    return UserRead(**user.model_dump())


@router.get("", response_model=List[UserRead])
def get_users(
        db: Session = Depends(get_db_session),
        current_user: User = Depends(get_current_user)
) -> List[UserRead]:
    """Get users."""
    if not current_user.is_admin:
        logger.error("User not authorized to list all users")
        raise HTTPException(status_code=403, detail="Not authorized to access users")
    results = db.exec(select(User)).all()
    logger.info(f"Users retrieved. Count: {len(results)}")
    return [UserRead(**user.model_dump()) for user in results]


@router.get("/current", response_model=UserRead)
def get_current(
        current_user: User = Depends(get_current_user)
) -> UserRead:
    """Get the current user."""
    return UserRead(**current_user.model_dump())


@router.get("/{user_id}", response_model=UserRead)
def get_user(
        user_id: int,
        db: Session = Depends(get_db_session),
        current_user: User = Depends(get_current_user)
) -> UserRead:
    """Get a user by id."""
    if not current_user.is_admin and current_user.id != user_id:
        logger.error("User not authorized to access user: %s", user_id)
        raise HTTPException(status_code=403, detail="Not authorized to access user")
    user = db.exec(select(User).where(User.id == user_id)).first()
    if not user:
        logger.error("User not found: %s", user_id)
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"Retrieved User with id: {user_id}")
    return UserRead(**user.model_dump())


@router.put("/{user_id}", response_model=UserRead)
def update_user(
        user_id: int,
        user_data: UserUpdate,
        db: Session = Depends(get_db_session),
        current_user: User = Depends(get_current_user),
        pwd_context: CryptContext = Depends(get_pwd_context)
) -> UserRead:
    """Update a user by id."""
    if not current_user.is_admin and current_user.id != user_id:
        logger.error("User not authorized to update user: %s", user_id)
        raise HTTPException(status_code=403, detail="Not authorized to update user")
    user = db.exec(select(User).where(User.id == user_id)).first()
    if not user:
        logger.error("User not found: %s", user_id)
        raise HTTPException(status_code=404, detail="User not found")

    user_data_dict = user_data.model_dump(exclude_unset=True)
    if user_data.password:
        user_data_dict["password_hash"] = pwd_context.hash(user_data.password.get_secret_value())
    if user_data.email:
        existing_user = db.exec(select(User).where(User.email == user_data.email)).first()
        if existing_user and existing_user.id != user_id:
            logger.error("Failed to update user: Email already exists")
            raise HTTPException(status_code=400, detail="Email already exists")
    user.sqlmodel_update(user_data_dict)
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info(f"Updated user with id: {user.id}")
    return UserRead(**user.model_dump())


@router.delete("/{user_id}", response_model=UserRead)
def delete_user(
        user_id: int,
        db: Session = Depends(get_db_session),
        current_user: User = Depends(get_current_user)
) -> UserRead:
    """Delete a user by id."""
    if not current_user.is_admin and current_user.id != user_id:
        logger.error("User not authorized to delete user: %s", user_id)
        raise HTTPException(status_code=403, detail="Not authorized to delete user")
    user = db.exec(select(User).where(User.id == user_id)).first()
    if not user:
        logger.error("User not found: %s", user_id)
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    logger.info("Deleted user with id: %s", user_id)
    return UserRead(**user.model_dump())
