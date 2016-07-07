from .Expr import Expr


class Id():
    def __init__(self, _id, _type):
        self._id = _id
        self.type = _type
        # self.offset = b

    def __repr__(self):
        return str(self.__dict__)
