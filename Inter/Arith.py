from .Op import Op

class Arith(Op):

    def __init__(self, token, x1, x2):
        super().__init__(token, None)
        self.expr1 = x1
        self.expr2 = x2
        self.type = 'Arithmetic'

    def gen(self):
        pass

    def __repr__(self):
        return str(self.__dict__)
