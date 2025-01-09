import os

from google.cloud import firestore


_client = None
FIRESTORE_DB = os.environ["FIRESTORE_DB"]


def get_firestore_client() -> firestore.Client:
    global _client
    if _client is None:
        _client = firestore.Client(database=FIRESTORE_DB)
    return _client
