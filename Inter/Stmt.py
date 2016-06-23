from .Node import Node


class Null:
    def __init__(self):
        self.type = 'NULL'

    def __repr__(self):
        return 'NULL'


class Stmt(Node):
    null = Null()
    after = 0

    def gen(self, before, after):
        pass

# Stmt.null = Null()
# Stmt.enclosing = Stmt.null
