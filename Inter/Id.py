from .Expr import Expr

class Id(Expr):
    def __init__(self, _id, _type, b):
        super().__init__(_id, _type)
        self.offset = b
