from typing import List

from google.cloud import firestore

from app.modassembly.database.nosql.get_firestore_client import get_firestore_client


def get_user_activity_logs(username: str, label: str) -> List:
    client: firestore.Client = get_firestore_client()
    logs_ref = client.collection("user_activity_logs")
    query = logs_ref.where("username", "==", username).where("label", "==", label)
    logs = query.stream()
    return list(logs)
