from .Stmt import Stmt


class Print(Stmt):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr
        self.type = 'Print'

    def gen(self, before, after):
        pass

    def __repr__(self):
        return str(self.__dict__)
