from datetime import datetime
from typing import Dict, Optional

from google.cloud import firestore
from sqlalchemy.orm import Session

from app.modassembly.database.nosql.get_firestore_client import get_firestore_client
from app.models.User import User
from app.modassembly.database.sql.get_sql_session import get_sql_session


def log_user_activity(user_id: int, session: Session, endpoint: str, extra_data: Dict[str, str]) -> None:
    # Retrieve the Firestore client
    client: firestore.Client = get_firestore_client()

    # Retrieve the user from the user id
    user: Optional[User] = session.query(User).filter(User.id == user_id).first()
    if user is None:
        raise ValueError(f"User with id {user_id} not found")

    # Log the user_id, endpoint, and extra data
    activity_log = {
        "user_id": user.id.__int__(),
        "email": user.email.__str__(),
        "endpoint": endpoint,
        "timestamp": datetime.utcnow().isoformat(),
        **extra_data
    }
    client.collection("user_activity_logs").add(activity_log)
