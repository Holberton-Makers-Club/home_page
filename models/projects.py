from models.base import Base

class Project(Base):
    """ Project class """
    def __init__(self, *args, **kwargs):
        """ init """
        super().__init__(*args, **kwargs)

