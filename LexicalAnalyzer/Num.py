from LexicalAnalyzer.Token import Token
from LexicalAnalyzer.Tag import Tag


class Num(Token):
    value = None

    def __init__(self, value):
        super().__init__(Tag.NUM)

        self.value = value

    def __str__(self):
        return 'NUM: value is %s and tag is %s' % (self.value, self.tag)

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value
