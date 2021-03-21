from uuid import uuid4
from models.base import Base

class Quotes(Base):
    """ Quotes class """
    def __init__(self, *args, **kwargs):
        """ init """
        self.author = ''
        self.text = ''
        super().__init__(*args, **kwargs)
    