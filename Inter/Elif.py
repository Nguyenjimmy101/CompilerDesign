from .Stmt import Stmt


class Elif(Stmt):
    def __init__(self, operator, expr1, expr2, block):
        self.operator = operator
        self.expr1 = expr1
        self.expr2 = expr2
        self.block = block
        self.type = 'Elif'

    def gen(before, after):
        pass

    def __repr__(self):
        return str(self.__dict__)
