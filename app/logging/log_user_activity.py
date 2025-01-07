from datetime import datetime
from typing import Annotated

from fastapi import Depends
from google.cloud import firestore
from sqlalchemy.orm import Session

from app.modassembly.authentication.authenticate import authenticate
from app.modassembly.database.nosql.get_firestore_client import get_firestore_client
from app.models.User import User


def log_user_activity(
    user: Annotated[User, Depends(authenticate)],
    endpoint: str,
) -> None:
    client: firestore.Client = get_firestore_client()
    activity_log = {
        "user_id": user.id.__str__(),
        "email": user.email.__str__(),
        "endpoint": endpoint,
        "timestamp": datetime.utcnow()
    }
    client.collection("user_activity_logs").add(activity_log)
