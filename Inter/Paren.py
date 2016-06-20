from .Node import Node

class Paren(Node):

    def __init__(self, token, expr):
        self.token = token
        self.expr = expr
        self.type = 'Paren'

    def __repr__(self):
        return str(self.__dict__)
