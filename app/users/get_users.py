from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.modassembly.authentication.authenticate import authenticate
from app.modassembly.database.sql.get_sql_session import get_sql_session
from app.models.User import User

router = APIRouter()

class UserResponse(BaseModel):
    id: int
    email: str
    username: str

    class Config:
        orm_mode = True

@router.get("/users", response_model=List[UserResponse], summary="Retrieve all users", tags=["users"])
def get_users(
    session: Session = Depends(get_sql_session),
    current_user: User = Depends(authenticate)
) -> List[UserResponse]:
    """
    Retrieve all users.

    This endpoint retrieves all users from the database.
    It requires authentication and returns a list of users.
    """
    users = session.query(User).all()
    return [
        UserResponse(
            id=user.id,  # Directly access the integer value
            email=user.email,  # Directly access the string value
            username=user.username  # Directly access the string value
        )
        for user in users
    ]
