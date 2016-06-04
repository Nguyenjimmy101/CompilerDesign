from LexicalAnalyzer.Tag import Tag
from LexicalAnalyzer.Token import Token


class Real(Token):
    value = 0

    def __init__(self, v):
        self.value = v

    def __str__(self):
        return 'REAL: Lexeme is %s and tag is %s' % (self.value, self.tag)
