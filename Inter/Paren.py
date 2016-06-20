from .Node import Node

class Paren(Node):
    def __init__(self, token, expr):
        self.token = token
        self.expr = expr
