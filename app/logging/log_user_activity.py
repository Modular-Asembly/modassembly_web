from typing import Dict

from google.cloud import firestore

from app.modassembly.database.nosql.get_firestore_client import get_firestore_client


def log_user_activity(username: int, label: str, extra_data: Dict[str, str]) -> None:
    client: firestore.Client = get_firestore_client()
    activity_log = {
        "username": username,
        "label": label,
        "timestamp": firestore.SERVER_TIMESTAMP,
        **extra_data,
    }
    client.collection("user_activity_logs").add(activity_log)
