from .Stmt import Stmt


class FunctionCall(Stmt):
    def __init__(self, function, arguments):
        super().__init__()
        self.function_name = function
        self.arguments = arguments
        self.type = 'FunctionCall'

    def gen(self, before, after):
        pass

    def __repr__(self):
        return str(self.__dict__)
