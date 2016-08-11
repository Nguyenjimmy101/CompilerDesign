from .Expr import Expr


class Rel(Expr):

    def __init__(self, operator, expr1, expr2):
        super().__init__(operator, '')
        self.expr1 = expr1
        self.expr2 = expr2
        self.type = 'Rel'

    def jumping(self, true, false):
        a = self.expr1.reduce()
        b = self.expr2.reduce()

        test = '%s %s %s' % (str(a), str(self.token), str(b))
        self.emitjumps(test, true, false)

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)
