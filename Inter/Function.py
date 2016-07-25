from .Node import Node


class Function(Node):
    def __init__(self, name, type, args, block):
        super().__init__()
        self.name = name
        self.type = type
        self.args = args
        self.block = block
        self.type = 'Function'

    def __repr__(self):
        return str(self.__dict__)
        
    def gen(self, before, after):
        pass
