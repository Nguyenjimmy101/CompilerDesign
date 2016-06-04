from LexicalAnalyzer.Token import Token


class Num(Token):
    value = None

    def __init__(self, value, tag):
        super().__init__(tag)

        self.value = value
