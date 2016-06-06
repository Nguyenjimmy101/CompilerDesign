from LexicalAnalyzer.BaseNumber import BaseNumber
from LexicalAnalyzer.Tag import Tag


class Num(BaseNumber):

    def __init__(self, value):
        super().__init__(value, Tag.NUM)

    def __str__(self):
        return 'NUM: value is %s and tag is %s' % (self.value, self.tag)
