from .Node import Node


class Stmt(Node):
    after = 0

    def gen(self, before, after):
        pass


Stmt.null = Stmt()
Stmt.enclosing = Stmt.null
