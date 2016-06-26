from LexicalAnalyzer.Tag import Tag
from .Stmt import Stmt

class Else(Stmt):
    def __init__(self, if_stmt, block):
        super().__init__()
        self.if_stmt = if_stmt
        self.block = block
        self.type = 'Else'

    def gen(self, before, after):
        pass

    def __repr__(self):
        return str(self.__dict__)
