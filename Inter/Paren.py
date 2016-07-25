from .Node import Node

class Paren(Node):

    def __init__(self, token, expr):
        super().__init__()
        self.token = token
        self.expr = expr
        self.type = 'Paren'
        
    def gen(self, before, after):
        return self

    def __repr__(self):
        return str(self.__dict__)
