from .Stmt import Stmt


class Seq(Stmt):
    def __init__(self, s1, s2):
        super().__init__()
        self.stmt1 = s1
        self.stmt2 = s2
        self.type = 'Sequence'

    def gen(self, before, after):
        if self.stmt1 == Stmt.null:
            self.stmt2.gen(before, after)
        elif self.stmt2 == Stmt.null:
            self.stmt1.gen(before, after)
        else:
            pass

    def __repr__(self):
        return str(self.__dict__)
