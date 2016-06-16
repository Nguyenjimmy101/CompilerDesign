from LexicalAnalyzer import Token
from LexicalAnalyzer.Lexer import Lexer
from LexicalAnalyzer.Tag import Tag


class Parser(object):
    lex = None
    look = None
    top = None
    indent = 0
    used = 0

    def __init__(self, stream):
        self.lex = Lexer(stream)
        self.move()

    def move(self):
        # if isinstance(self.look, bool) and self.look == False:
            # return False
        self.look = self.lex.scan()

    def match(self, tag):
        if self.look.tag == tag:
            self.move()
            # print(self.look)
            self.indent = self.lex.indent
        else:
            raise SyntaxError('Expected %s, got %s' % (tag, self.look))

    def block(self):
        indent = self.indent
        # TODO handle newline
        self.match(Tag.NEW_LINE)
        self.stmt()
        while self.indent != indent:
            self.stmt()

    def relop(self):
        if self.look.tag == Tag.LT:
            self.match(Tag.LT)
        elif self.look.tag == Tag.GT:
            self.match(Tag.GT)
        elif self.look.tag == Tag.GE:
            self.match(Tag.GE)
        elif self.look.tag == Tag.LE:
            self.match(Tag.LE)
        elif self.look.tag == Tag.EQ:
            self.match(Tag.EQ)
        elif self.look.tag == Tag.NE:
            self.match(Tag.NE)

    def expr(self):
        if self.look.tag == Tag.NUM:
            self.match(Tag.NUM)
        elif self.look.tag == Tag.REAL:
            self.match(Tag.REAL)
        elif self.look.tag == Tag.STRING:
            self.match(Tag.STRING)
        elif self.look.tag == Tag.BOOL:
            self.match(Tag.BOOL)
        elif self.look.tag == Tag.ADD:
            self.add()
        elif self.look.tag == Tag.MINUS:
            self.subtract()
        elif self.look.tag == Tag.MULT:
            self.multiply()
        elif self.look.tag == Tag.DIV:
            self.divide()
        else:
            self.match(Tag.ID)

    def stmt(self):
        if self.look.tag == Tag.IF:
            self.match(Tag.IF)
            self.relop()
            self.expr()
            self.expr()
            self.block()
        elif self.look.tag == Tag.ELSE:
            self.match(Tag.ELSE)
            self.block()
        elif self.look.tag == Tag.ELIF:
            self.match(Tag.ELIF)
            self.relop()
            self.expr()
            self.expr()
            self.block()
        elif self.look.tag == Tag.WHILE:
            self.match(Tag.WHILE)
            self.expr()
            self.block()
        elif self.look.tag == Tag.FOR:
            self.match(Tag.FOR)
            self.match(Tag.ID)
            self.expr()
            self.block()
        elif self.look.tag == Tag.ASSIGN:
            self.assign()

    def assign(self):
        self.match(Tag.ASSIGN)
        self.match(Tag.ID)
        self.expr()

