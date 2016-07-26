from LexicalAnalyzer.Tag import Tag
from .Stmt import Stmt
from .Expr import Expr


class While(Stmt, Expr):
    def __init__(self, op, expr, block, iterator):
        super().__init__()
        self.op = op
        self.iterator = iterator
        self.block = block
        self.type = 'While'

    def gen(self, before, after):
        self.after = after
        self.jumping(0, after)
        label = self.newlabel()
        self.emitlabel(label)
        self.gen(label, before)
        self.emit('goto L%s' % after)

    def __repr__(self):
        return str(self.__dict__)
