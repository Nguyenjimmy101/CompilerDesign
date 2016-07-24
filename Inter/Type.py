from .Node import Node
from .Expr import Expr


class Type(Expr):
    def __init__(self, kind):
        super().__init__('', '')
        
        self.kind = kind
        self.type = 'Type'
        # self.offset = b

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


class Integer(Type):
    def __init__(self):
        super().__init__('int')


class Float(Type):
    def __init__(self):
        super().__init__('float')


class Bool(Type):
    def __init__(self):
        super().__init__('bool')


class String(Type):
    def __init__(self):
        super().__init__('string')


class Void(Type):
    def __init__(self):
        super().__init__('void')

class FunctionType(Type):
    def __init__(self, returnType):
        super().__init__('function')
        self.returnType = returnType

