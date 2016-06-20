from .Expr import Expr

class Op(object):
    def __init__(self, tok, p):
        self.tok = tok
        self.p = p

    def reduce(self):
        pass
