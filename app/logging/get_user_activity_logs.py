from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from google.cloud import firestore

from app.modassembly.authentication.authenticate import authenticate
from app.modassembly.database.nosql.get_firestore_client import get_firestore_client
from app.models.User import User

router = APIRouter()

class ActivityLogResponse(BaseModel):
    user_id: int
    email: str
    endpoint: str
    timestamp: str

@router.get("/user/activity-logs", response_model=List[ActivityLogResponse])
def get_user_activity_logs(
    user: User = Depends(authenticate),
    endpoint: str = ""
) -> List[ActivityLogResponse]:
    """
    Retrieve usage logs for the authenticated user and a specific endpoint.

    - **user**: The authenticated user.
    - **endpoint**: The specific endpoint to filter logs by (optional).

    Returns a list of activity logs for the user.
    """
    client: firestore.Client = get_firestore_client()
    logs_ref = client.collection("user_activity_logs")
    query = logs_ref.where("user_id", "==", user.id.__int__())

    if endpoint:
        query = query.where("endpoint", "==", endpoint)

    logs = query.stream()

    return [
        ActivityLogResponse(
            user_id=log.get("user_id").__int__(),
            email=log.get("email").__str__(),
            endpoint=log.get("endpoint").__str__(),
            timestamp=log.get("timestamp").isoformat()
        )
        for log in logs
    ]
