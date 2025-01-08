from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.User import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_user(email: str, password: str, session: Session) -> User:
    user = session.query(User).filter(User.email == email).first()
    if not user:
        raise ValueError(f"User not found for email :: {email}")
    if not pwd_context.verify(password, str(user.hashed_password)):
        raise ValueError(f"Invalid password for email :: {email}")
    return user

