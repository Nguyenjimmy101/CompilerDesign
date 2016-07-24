from .Node import Node

class Block(Node):

    def __init__(self, stmts, env):
        super().__init__()
        self.stmts = stmts
        self.env = env
        self.type = 'Block'

    def __repr__(self):
        return str(self.__dict__)
        
    def gen(self, before, after):
        label = self.newlabel()
        self.stmts.gen(label, after)
        self.emitlabel(label)
