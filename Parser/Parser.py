import null

from LexicalAnalyzer import Token
from LexicalAnalyzer.Lexer import Lexer


class Parser:
    lex = Lexer()
    look = Token
    top = null
    used = 0

    def move(self):
        self.look = self.lex.scan()

    def error(self, s):
        print("Near Line " + self.Lexer.line + ": " + s)

    def match(self, t):
        if self.look.tag == t:
            self.move()
        else:
            self.error("Syntax Error")


    #def block(self):
    #statements

