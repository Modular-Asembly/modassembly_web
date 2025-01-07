from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.models.FeatureFlag import FeatureFlag
from app.modassembly.database.sql.get_sql_session import get_sql_session
from app.modassembly.authentication.authenticate import authenticate
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
    db_feature_flag = FeatureFlag(name=feature_flag.name, enabled=feature_flag.enabled)
    session.add(db_feature_flag)
    session.commit()
    session.refresh(db_feature_flag)
    
    return FeatureFlagResponse(
        id=db_feature_flag.id.__int__(),
        name=db_feature_flag.name.__str__(),
        enabled=db_feature_flag.enabled.__bool__()
    )
