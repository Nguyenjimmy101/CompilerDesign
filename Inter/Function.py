from .Node import Node


class Function(Node):

    def __init__(self, name, args, block):
        self.name = name
        self.args = args
        self.block = block
        self.type = 'Function'

    def __repr__(self):
        return str(self.__dict__)
