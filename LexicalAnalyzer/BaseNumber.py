from LexicalAnalyzer.Token import Token


class BaseNumber(Token):
    value = 0

    def __init__(self, value, tag):
        super().__init__(tag)
        self.value = value

    def __lt__(self, other):
        if isinstance(other, BaseNumber):
            return self.value < other.value
        return self.value < other

    def __gt__(self, other):
        if isinstance(other, BaseNumber):
            return self.value > other.value
        return self.value > other.value

    def __eq__(self, other):
        if isinstance(other, BaseNumber):
            return self.value == other.value
        return self.value == other
