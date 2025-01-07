from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.User import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_user(username: str, password: str, session: Session) -> User:
    user = session.query(User).filter(User.username == username).first()
    if not user:
        raise ValueError(f"User not found for username :: {username}")
    if not pwd_context.verify(password, str(user.hashed_password)):
        raise ValueError(f"Invalid password for username :: {username}")
    return user
