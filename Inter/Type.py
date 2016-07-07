from .Node import Node


class Type():
    def __init__(self, kind):
        self.kind = kind
        self.type = 'Type'
        # self.offset = b

    def __repr__(self):
        return str(self.__dict__)
