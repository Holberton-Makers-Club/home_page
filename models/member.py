from uuid import uuid4

class Member():
    """ Member class """
    def __init__(self, name):
        """ __init__ method """
        self.name = str(name)
        self.id = str(uuid4())
        self.githublink = ""
        self.linkedin = ""
        self.twitter = ""
        self.seeking = ""
