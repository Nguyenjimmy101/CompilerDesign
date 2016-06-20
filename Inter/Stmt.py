from .Node import Node


class Stmt(Node):
    after = 0

    def gen(self, before, after):
        pass


class Null(Stmt):
    def __init__(self):
        self.type = 'NULL'

    def __repr__(self):
        return 'NULL'

Stmt.null = Null()
Stmt.enclosing = Stmt.null
