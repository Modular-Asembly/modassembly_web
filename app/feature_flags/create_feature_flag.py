from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.modassembly.authentication.authenticate import authenticate
from app.modassembly.database.sql.get_sql_session import get_sql_session
from app.models.FeatureFlag import FeatureFlag
from app.models.User import User

router = APIRouter()

class FeatureFlagCreate(BaseModel):
    name: str
    enabled: bool

class FeatureFlagResponse(BaseModel):
    id: int
    name: str
    enabled: bool

@router.post("/feature_flags", response_model=FeatureFlagResponse, status_code=status.HTTP_201_CREATED)
def create_feature_flag(
    feature_flag: FeatureFlagCreate,
    session: Session = Depends(get_sql_session),
    current_user: User = Depends(authenticate)
) -> FeatureFlagResponse:
    """
    Create a new feature flag.

    - **name**: The name of the feature flag.
    - **enabled**: Boolean indicating if the feature flag is globally enabled.
    """
    # Check if the feature flag already exists
    existing_flag = session.query(FeatureFlag).filter(FeatureFlag.name == feature_flag.name).first()
    if existing_flag:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Feature flag with name '{feature_flag.name}' already exists."
        )

    # Create a new feature flag
    new_feature_flag = FeatureFlag(name=feature_flag.name, enabled=feature_flag.enabled)
    session.add(new_feature_flag)
    session.commit()
    session.refresh(new_feature_flag)

    return FeatureFlagResponse(
        id=new_feature_flag.id.__int__(),
        name=new_feature_flag.name.__str__(),
        enabled=new_feature_flag.enabled.__bool__()
    )
