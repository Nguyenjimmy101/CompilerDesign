from LexicalAnalyzer.Tag import Tag
from .Stmt import Stmt


class For(Stmt):
    def __init__(self, var, iterator, block):
        super().__init__()
        self.var = var
        self.iterator = iterator
        self.block = block
        self.type = 'For'

    def gen(self, before, after):
        pass

    def __repr__(self):
        return str(self.__dict__)
