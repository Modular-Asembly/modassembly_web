from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.models.UserFeatureFlag import UserFeatureFlag
from app.modassembly.authentication.authenticate import authenticate
from app.modassembly.database.sql.get_sql_session import get_sql_session
from app.models.User import User

router = APIRouter()

class FeatureFlagUpdateRequest(BaseModel):
    feature_flag_id: int
    enabled: bool

class FeatureFlagUpdateResponse(BaseModel):
    user_id: int
    feature_flag_id: int
    enabled: bool

@router.put("/user-feature-flag", response_model=FeatureFlagUpdateResponse)
def update_user_feature_flag(
    request: FeatureFlagUpdateRequest,
    current_user: User = Depends(authenticate),
    session: Session = Depends(get_sql_session)
) -> FeatureFlagUpdateResponse:
    """
    Update the status of a feature flag for a specific user.

    - **feature_flag_id**: The ID of the feature flag to update.
    - **enabled**: The new status of the feature flag (True or False).
    """
    user_feature_flag = session.query(UserFeatureFlag).filter(
        UserFeatureFlag.user_id == current_user.id,
        UserFeatureFlag.feature_flag_id == request.feature_flag_id
    ).first()

    if not user_feature_flag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User feature flag not found"
        )

    # Assign the new enabled status directly
    user_feature_flag.enabled = request.enabled
    session.commit()

    return FeatureFlagUpdateResponse(
        user_id=user_feature_flag.user_id.__int__(),
        feature_flag_id=user_feature_flag.feature_flag_id.__int__(),
        enabled=user_feature_flag.enabled.__bool__()
    )
