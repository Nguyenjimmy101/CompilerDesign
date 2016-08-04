from .Stmt import Stmt


class Elif(Stmt):
    def __init__(self, rel, block):
        super().__init__()
        self.rel = rel
        # self.operator = operator
        # self.expr1 = expr1
        # self.expr2 = expr2
        self.block = block
        self.type = 'Elif'

    def gen(self, before, after):
        pass

    def __repr__(self):
        return str(self.__dict__)
