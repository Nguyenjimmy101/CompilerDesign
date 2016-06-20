from LexicalAnalyzer.Tag import Tag
from .Stmt import Stmt

class Else(Stmt):
    def __init__(self, expr, stmt1, stmt2):
        self.expr = expr
        self.stmt1 = stmt1
        self.stmt2 = stmt2

    def gen(before, after):
        pass
