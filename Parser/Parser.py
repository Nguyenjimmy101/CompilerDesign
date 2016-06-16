from LexicalAnalyzer import Token
from LexicalAnalyzer.Lexer import Lexer


class Parser(object):
    lex = None
    look = None
    top = None
    used = 0

    def __init__(self, stream):
        self.lex = Lexer(stream)

    def move(self):
        self.look = self.lex.scan()

    def error(self, s):
        print("Near Line " + self.lex.line + ": " + s)

    def match(self, tag):
        if self.look.tag == tag:
            self.move()
        else:
            raise SyntaxError('Expected %s, got %s' % (tag, self.look.tag))

    def block(self):
        #statements
        pass
