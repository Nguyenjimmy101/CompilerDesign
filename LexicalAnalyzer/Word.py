from .Tag import Tag
from .Token import Token


class Word(Token):
    lexeme = ''

    def __init__(self, s, tag):
        super().__init__(tag)
        self.lexeme = s

    def __str__(self):
        return 'WORD: Lexeme is %s and tag is %s' % (self.lexeme, self.tag)


class Words(object):
    eq = Word('==', Tag.EQ)
    ne = Word('!=', Tag.NE)
    le = Word('<=', Tag.LE)
    ge = Word('>=', Tag.GE)
