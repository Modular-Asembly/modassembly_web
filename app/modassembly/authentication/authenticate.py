from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.modassembly.authentication.create_access_token import (
    ALGORITHM,
    SECRET_KEY,
)
from app.modassembly.database.sql.get_sql_session import get_sql_session
from app.models.User import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def authenticate(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[Session, Depends(get_sql_session)],
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credential :: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = session.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User :: {email} not found",
        )
    return user
