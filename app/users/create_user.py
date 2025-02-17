from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.modassembly.authentication.authenticate import authenticate
from app.modassembly.database.sql.get_sql_session import get_sql_session
from app.models.User import User
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    session: Session = Depends(get_sql_session),
    current_user: User = Depends(authenticate)
) -> UserResponse:
    """
    Create a new user.

    - **email**: Email of the user
    - **username**: Username of the user
    - **password**: Password of the user
    """
    # Check if the email or username already exists
    existing_user = session.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already registered"
        )

    # Hash the password
    hashed_password = pwd_context.hash(user_data.password)

    # Create a new user instance
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password
    )

    # Add the new user to the session and commit
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return UserResponse(
        id=new_user.id.__int__(),
        email=new_user.email.__str__(),
        username=new_user.username.__str__()
    )
