from LexicalAnalyzer.Token import Token
from LexicalAnalyzer.Tag import Tag


class Real(Token):
    value = None

    def __init__(self, value):
        super().__init__(Tag.REAL)

        self.value = value

    def __str__(self):
        return 'REAL: value is %s and tag is %s' % (self.value, self.tag)
