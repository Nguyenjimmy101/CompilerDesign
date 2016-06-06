from LexicalAnalyzer.Token import Token
from LexicalAnalyzer.Tag import Tag


class String(Token):
    value = None

    def __init__(self, value):
        super().__init__(Tag.STRING)
        self.value = value

    def __str__(self):
        return 'STRING: value is |%s| and tag is %s' % (self.value, self.tag)

    def __lt__(self, other):
        if isinstance(other, String):
            return self.value < other.value
        return self.value < other.value

    def __gt__(self, other):
        if isinstance(other, String):
            return self.value > other.value
        return self.value > other.value

    def __eq__(self, other):
        if isinstance(other, String):
            return self.value == other.value
        return self.value == other
