from LexicalAnalyzer.Tag import Tag
from LexicalAnalyzer.Token import Token


class Comment(Token):
    value = None

    def __init__(self, value):
        super().__init__(Tag.COMMENT)
        self.value = value

    def __str__(self):
        return 'COMMENT: value is %s and tag is %s' % (self.value, self.tag)
