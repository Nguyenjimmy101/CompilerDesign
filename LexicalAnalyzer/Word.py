from LexicalAnalyzer.Tag import Tag
from LexicalAnalyzer.Token import Token


class Word(Token):
    lexeme = ''

    def __init__(self, s, tag):
        super().__init__(tag)
        self.lexeme = s

    def __str__(self):
        return 'WORD: Lexeme is %s and tag is %s' % (self.lexeme, self.tag)


class Words(object):
    EQ = Word('==', Tag.EQ)
    NE = Word('!=', Tag.NE)
    LE = Word('<=', Tag.LE)
    GE = Word('>=', Tag.GE)
    IF = Word('if', Tag.IF)
    ELSE = Word('else', Tag.ELSE)
