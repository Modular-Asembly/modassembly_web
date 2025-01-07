from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.models.UserFeatureFlag import UserFeatureFlag
from app.modassembly.database.sql.get_sql_session import get_sql_session
from app.modassembly.authentication.authenticate import authenticate
from app.models.User import User

router = APIRouter()

class UpdateFeatureFlagRequest(BaseModel):
    feature_flag_id: int
    enabled: bool

class UpdateFeatureFlagResponse(BaseModel):
    user_id: int
    feature_flag_id: int
    enabled: bool

@router.put("/user-feature-flag", response_model=UpdateFeatureFlagResponse)
def update_user_feature_flag(
    request: UpdateFeatureFlagRequest,
    current_user: User = Depends(authenticate),
    session: Session = Depends(get_sql_session)
) -> UpdateFeatureFlagResponse:
    """
    Update the status of a feature flag for a specific user.

    - **feature_flag_id**: ID of the feature flag to update.
    - **enabled**: Boolean indicating if the feature flag should be enabled for the user.
    """
    user_feature_flag = session.query(UserFeatureFlag).filter(
        UserFeatureFlag.user_id == current_user.id,
        UserFeatureFlag.feature_flag_id == request.feature_flag_id
    ).first()

    if not user_feature_flag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feature flag for user not found"
        )

    # Use setattr to assign the boolean value
    setattr(user_feature_flag, 'enabled', request.enabled)

    session.commit()

    return UpdateFeatureFlagResponse(
        user_id=user_feature_flag.user_id.__int__(),
        feature_flag_id=user_feature_flag.feature_flag_id.__int__(),
        enabled=user_feature_flag.enabled.__bool__()
    )
