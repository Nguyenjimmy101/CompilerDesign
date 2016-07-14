from .Node import Node

class Expr(Node):

    def __init__(self, token, operator):
        self.token = token
        self.type = operator
        self.type = 'Expression'

    def gen(self):
        return self

    def reduce(self):
        return self

    def jumping(self, t, f):
        pass
        #self.emitjumps(self.Op, t,f)

    def emitjumps(self, test, t, f):
        if t != 0 and f != 0:
            pass
        elif t != 0:
            pass
        elif f != 0:
            pass
        else:
            pass

    def __str__(self):
        pass