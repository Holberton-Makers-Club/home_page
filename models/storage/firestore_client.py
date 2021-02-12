"""
database client for GCP firestore
"""
from google.cloud import firestore


class FirestoreClient():
    def __init__(self):
        self.db = firestore.Client()
    def get_all_by_class(self, classname: str):
        return [ref.to_dict() for ref in self.db.collection(classname).get()]
