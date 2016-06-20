from .Stmt import Stmt

class Assign(Stmt):
    def __init__(self, _id, expr):
        self.id = _id
        self.expr = expr

    def gen(self, before, after):
        pass
