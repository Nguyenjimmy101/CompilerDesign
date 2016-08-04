from .Stmt import Stmt


class Elif(Stmt):
    def __init__(self, rel, block):
        super().__init__()
        self.rel = rel
        self.block = block
        self.type = 'Elif'

    def gen(self, before, after):
        pass

    def __repr__(self):
        return str(self.__dict__)
