from .Stmt import Stmt

class Assign(Stmt):

    def __init__(self, _id, expr):
        super().__init__()
        self.id = _id
        self.expr = expr
        self.type = 'Assignment'

    def gen(self, before, after):
        self.emit('%s = %s' % (self.id, self.expr.gen(before, after)))

    def __repr__(self):
        return str(self.__dict__)
