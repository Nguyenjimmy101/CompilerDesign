from LexicalAnalyzer import Token
from LexicalAnalyzer.Lexer import Lexer
from LexicalAnalyzer.Tag import Tag


class Parser(object):
    lex = None
    look = None
    top = None
    used = 0

    def __init__(self, stream):
        self.lex = Lexer(stream)
        self.move()

    def move(self):
        self.look = self.lex.scan()

    def match(self, tag):
        if self.look.tag == tag:
            self.move()
        else:
            raise SyntaxError('Expected %s, got %s' % (tag, self.look))

    def block(self):
        indent = self.indent

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
        pass

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
        else:
            self.assign()

    def assign(self):
        self.match(Tag.ASSIGN)
        self.match(Tag.ID)
        self.expr()
