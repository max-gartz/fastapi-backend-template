from sqlmodel import Session
from sqlmodel import select

from app.api.users.users_schema import User


def get_user_by_email(db: Session, email: str) -> User | None:
    """Get a user."""
    return db.exec(select(User).where(User.email == email)).first()
