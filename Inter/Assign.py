from .Stmt import Stmt

class Assign(Stmt):

    def __init__(self, _id, expr):
        self.id = _id
        self.expr = expr
        self.type = 'Assignment'

    def gen(self, before, after):
        pass

    def __repr__(self):
        return str(self.__dict__)
