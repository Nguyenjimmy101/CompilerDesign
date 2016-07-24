from .Expr import Expr


class Temp(Expr):
    count = 0
    number = 0

    def __init__(self, p):
        super().__init__(self, p)
        self.number = self.count + 1

    def __repr__(self):
        return str(self.__dict__)
