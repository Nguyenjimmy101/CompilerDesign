from LexicalAnalyzer.Tag import Tag
from LexicalAnalyzer.Token import Token


class Bool(Token):
    value = None

    def __init__(self, value):
        super().__init__(Tag.BOOL)
        self.value = value

    def __str__(self):
        return 'BOOL: value is %s and tag is %s' % (self.value, self.tag)

    def __eq__(self, other):
        return self.value == other.value
