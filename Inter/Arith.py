from .Op import Op
from .Expr import Expr


class Arith(Op, Expr):
    def __init__(self, token, x1, x2):
        super().__init__(token, None)
        self.expr1 = x1
        self.expr2 = x2
        self.type = 'Arithmetic'

    def gen(self, before=None, after=None):
        return self.expr1.reduce(), self.expr2.reduce()

    def __repr__(self):
        return str(self.__dict__)
