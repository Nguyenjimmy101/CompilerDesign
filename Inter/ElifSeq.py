from .Stmt import Stmt


class ElifSeq(Stmt):
    def __init__(self, if1, if2):
        super().__init__()
        self.if1 = if1
        self.if2 = if2
        self.type = 'Elif Sequence'

    def gen(self, before, after):
        pass

    def __repr__(self):
        return str(self.__dict__)
