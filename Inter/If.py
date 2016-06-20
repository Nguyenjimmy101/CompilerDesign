from LexicalAnalyzer.Tag import Tag
from .Stmt import Stmt

class If(Stmt):
    def __init__(self, expr, stmt):
        self.expr = expr
        self.stmt = stmt

    def gen(before, after):
        pass
