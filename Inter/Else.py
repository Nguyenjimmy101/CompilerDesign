from LexicalAnalyzer.Tag import Tag
from .Stmt import Stmt


class Else(Stmt):

    def __init__(self, if_stmt, block):
        super().__init__()
        self.if_stmt = if_stmt
        self.block = block
        self.type = 'Else'

    def gen(self, before, after):
        label1 = self.newlabel()
        label2 = self.newlabel()
        
        self.if_stmt.rel.jumping(0, label2)

        self.emitlabel(label1)

        self.if_stmt.gen_two(label1, after)
        self.emit('goto L%s' % after)
        
        self.emitlabel(label2)
        self.block.gen(label2, after)

    def __repr__(self):
        return str(self.__dict__)
