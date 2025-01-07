from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.modassembly.authentication.create_access_token import (
    create_access_token,
)
from app.modassembly.authentication.verify_user import verify_user
from app.modassembly.database.sql.get_sql_session import get_sql_session


router = APIRouter()


ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/login")
def login_api(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_sql_session),
) -> Token:
    try:
        user = verify_user(form_data.username, form_data.password, session)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        email=str(user.email), expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
