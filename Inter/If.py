from LexicalAnalyzer.Tag import Tag
from .Stmt import Stmt


class If(Stmt):
    def __init__(self, operator, expr1, expr2, block):
        super().__init__()
        self.operator = operator
        self.expr1 = expr1
        self.expr2 = expr2
        self.block = block
        self.type = 'If'

    def gen(self, before, after):
        pass

    def __repr__(self):
        return str(self.__dict__)
