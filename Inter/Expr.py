from .Node import Node


class Expr(Node):
    def __init__(self, token, operator):
        super().__init__()
        self.token = token
        self.type = operator
        self.type = 'Expression'

    def gen(self):
        return self

    def reduce(self):
        return self

    def jumping(self, t, f):
        self.emitjumps(self.token, t, f)

    def emitjumps(self, test, t, f):
        if t != 0 and f != 0:
            self.emit('if %s goto L%s' % (test, t))
            self.emit('goto L%s' % f)
        elif t != 0:
            self.emit('if %s goto L%s' % (test, t))
        elif f != 0:
            self.emit('iffalse %s goto L%s' % (test, f))
        else:
            pass

    def __str__(self):
        str(self.__dict__)
