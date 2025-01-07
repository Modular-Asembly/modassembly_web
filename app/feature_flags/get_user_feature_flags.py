from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.UserFeatureFlag import UserFeatureFlag
from app.modassembly.database.sql.get_sql_session import get_sql_session
from app.modassembly.authentication.authenticate import authenticate
from pydantic import BaseModel

router = APIRouter()

class FeatureFlagResponse(BaseModel):
    feature_flag_id: int
    enabled: bool

@router.get("/user/feature-flags", response_model=List[FeatureFlagResponse])
def get_user_feature_flags(
    user: UserFeatureFlag = Depends(authenticate),
    session: Session = Depends(get_sql_session)
) -> List[FeatureFlagResponse]:
    """
    Retrieve feature flags for the authenticated user.

    - **user**: The authenticated user.
    - **session**: The database session.

    Returns a list of feature flags with their enabled status for the user.
    """
    user_feature_flags = session.query(UserFeatureFlag).filter(
        UserFeatureFlag.user_id == user.id
    ).all()

    return [
        FeatureFlagResponse(
            feature_flag_id=flag.feature_flag_id.__int__(),
            enabled=flag.enabled.__bool__()
        )
        for flag in user_feature_flags
    ]
