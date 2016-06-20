from .Node import Node

class Expr(Node):
    def __init__(self, token, operator):
        self.token = token
        self.type = operator

    def gen(self):
        return self

    def reduce(self):
        return self
