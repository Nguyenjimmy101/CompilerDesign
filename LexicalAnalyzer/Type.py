import null as null

from LexicalAnalyzer.Token import Token
from LexicalAnalyzer.Word import Word, Words
from LexicalAnalyzer.Tag import Tag


def numeric(p):
    return p == Type.Char or p == Type.Int or p == Type.Float


# ignore built in method max
def max(p1, p2):
    if not (numeric(p1)) or not (numeric(p2)):
        return null
    elif __eq__(p1, p2, Type.Float):
        return Type.Float
    elif __eq__(p1, p2, Type.Int):
        return Type.Int
    else:
        return Type.Char


class Type(Token):
    width = 0

    def __init__(self, w, tag):
        super().__init__(tag)
        self.width = w

    def __str__(self):
        return 'TYPE: Lexeme is %s tag is %s Width is %s' % (self.lexeme, self.tag, self.width)

    def __eq__(self, p, type):
        return self == type or p == type


class Type(object):
    Int = Word('int', Tag.BASIC, 4)
    Float = Word('float', Tag.BASIC, 8)
    Char = Word('char', Tag.BASIC, 1)
    Bool = Word('bool', Tag.BASIC, 1)
