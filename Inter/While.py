from LexicalAnalyzer.Tag import Tag
from .Stmt import Stmt


class While(Stmt):
    def __init__(self, op, expr, block):
        super().__init__()
        self.op = op
        self.iterator = iterator
        self.block = block
        self.type = 'While'

    def gen(self, before, after):
        pass

    def __repr__(self):
        return str(self.__dict__)
