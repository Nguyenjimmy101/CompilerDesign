from LexicalAnalyzer.Tag import Tag
from LexicalAnalyzer.Token import Token


class Real(Token):
    value = 0

    def __init__(self, value):
        super().__init__(Tag.REAL)
        self.value = value

    def __str__(self):
        return 'REAL: value is %s and tag is %s' % (self.value, self.tag)

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value
