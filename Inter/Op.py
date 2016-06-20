from .Expr import Expr

class Op(Expr):
    def __init__(self, tok, p):
        super().__init__(tok, p)

    def reduce(self):
        pass
