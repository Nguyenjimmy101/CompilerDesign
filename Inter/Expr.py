from .Node import Node


class Expr(Node):

    def __init__(self, token, operator):
        super().__init__()
        self.token = token
        self.type = operator
        self.type = 'Expression'

    def gen(self, before=None, after=None):
        return self

    def reduce(self):
        return self

    def jumping(self, t, f):
        self.emitjumps(self.token, t, f)

    def emitjumps(self, test, t, f):
        if t and f:
            self.emit('if %s goto L%s' % (test, t))
            self.emit('goto L%s' % f)
        elif t:
            self.emit('if %s goto L%s' % (test, t))
        elif f:
            self.emit('if false %s goto L%s' % (test, f))
        else:
            pass

    def __str__(self):
        str(self.__dict__)
