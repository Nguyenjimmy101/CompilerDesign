from .Stmt import Stmt


class PrintErr(Stmt):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr
        self.type = 'PrintErr'

    def gen(self, before, after):
        pass

    def __repr__(self):
        return str(self.__dict__)
