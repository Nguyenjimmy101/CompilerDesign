from LexicalAnalyzer.Tag import Tag
from .Stmt import Stmt

class Else(Stmt):
    def __init__(self, if_stmt, block):
        self.if_stmt = if_stmt
        self.block = block
        self.type = 'Else'

    def gen(before, after):
        pass