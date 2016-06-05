from LexicalAnalyzer.Tag import Tag
from LexicalAnalyzer.Token import Token
from LexicalAnalyzer.Word import Word


def numeric(p):
    return p in (Types.INT, Types.FLOAT)


class Type(Token):
    width = 0

    def __init__(self, width, tag):
        super().__init__(tag)
        self.width = width

    def __str__(self):
        return 'TYPE: Lexeme is %s tag is %s width is %s' % (self.lexeme, self.tag, self.width)

    def __eq__(self, p, types):
        return self == types or p == types


class Types(object):
    INT = Word('int', Tag.BASIC)
    FLOAT = Word('float', Tag.BASIC)
    STRING = Word('string', Tag.BASIC)
    BOOL = Word('bool', Tag.BASIC)
