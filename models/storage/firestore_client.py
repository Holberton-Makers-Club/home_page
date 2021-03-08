"""
database client for GCP firestore
"""
from google.cloud import firestore


class FirestoreClient():
    def __init__(self):
        self.db = firestore.Client()

    def connected(self):
        return True if self.db else False

    def get_by_class(self, classname: str):
        # return a list of dictionary representations of the found objects
        return [ref.to_dict() for ref in self.db.collection(classname).get()]
    
    def get_by_id(self, cls, id):
        # return a dictionary representation of the found object
        return self.db.collection(cls).document(id).get().to_dict()
    
    def get_by_attr(self, cls, attr, val):
        # return a list of dictionary representations of the found objects, or None
        matches = self.db.collection(cls).where(attr, u'==', val).get()
        return matches if len(matches) > 0 else None
    
    def save(self, obj):
        self.db.collection(obj.__class__.__name__).document(obj.id).set(obj.__dict__)
    
    def update_attr_by_id(self, cls, id, attr, value):
        ref = self.db.collection(cls.__name__).document(id)
        res = cls.get_by_attr('id', id)
        if not res:
            return False
        obj = res[0]
        if obj:
            if type(obj.get(attr)) == list:
                ref.update({attr: firestore.ArrayUnion([value])})
                return True
        ref.update({attr: value})
        return True
    
    def delete(self, obj):
        self.db.collection(obj.__class__.__name__).document(obj.id).delete()
    
    def delete_by_id(self, cls, id):
        self.db.collection(cls.__name__).document(id).delete()