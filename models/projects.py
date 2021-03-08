class Project():
    """ Project class """
    def __init__(self, name):
        """ __init__ method """
        self.name = str(name)
        self.description = ""
        self.members = []
        self.link = ""
