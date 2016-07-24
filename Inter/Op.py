from Inter.Temp import Temp
from .Expr import Expr

class Op(Expr):
    def __init__(self, tok, p):
        super().__init__(tok, p)
        self.p = p

    def reduce(self):
        x = self.gen()
        t = Temp(self.p)
        self.emit(x + " = " + t)
        return t
