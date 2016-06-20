from .Node import Node

class Expr(Node):

    def __init__(self, token, operator):
        self.token = token
        self.type = operator
        self.type = 'Expression'

    def gen(self):
        return self

    def reduce(self):
        return self
