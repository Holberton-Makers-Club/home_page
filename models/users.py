from uuid import uuid4
from models.base import Base

class User(Base):
    """ User class """
    def __init__(self, *args, **kwargs):
        """ init """
        self.firstname = kwargs.get('firstname')
        self.interested = []
        super().__init__(*args, **kwargs)
        # Google handles encryption and decryption of all data automatically.
        # That's why we don't have to hash the password.
    
    def validate_password(self, password):
        # Google handles encryption and decryption of all data automatically.
        return password == self.password
