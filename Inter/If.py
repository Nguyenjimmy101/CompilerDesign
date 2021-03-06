from LexicalAnalyzer.Tag import Tag
from .Stmt import Stmt


class If(Stmt):
    def __init__(self, rel, block):
        super().__init__()
        self.rel = rel
        self.block = block
        self.type = 'If'

    def gen(self, before, after):
        label = self.newlabel()
        self.rel.jumping(0, after)
        self.emitlabel(label)
        self.block.gen(label, after)

    def gen_two(self, label, after):
        self.block.gen(label, after)

    def __repr__(self):
        return str(self.__dict__)
