import Expr

class Op(object):
    def __init__(self, tok, p):
        self.tok = tok
        self.p = p

    def reduce(self):
        self.x = gen()
        self.t = Temp(type)
        emit(str(t) + " = " + str(x))
        return t
