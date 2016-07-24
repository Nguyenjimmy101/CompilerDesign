class UnknownType(object):
    def __init__(self):
        self.type = 'Unknown Type'

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)
