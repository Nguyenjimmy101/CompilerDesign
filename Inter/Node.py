from LexicalAnalyzer.Lexer import Lexer


class Node(object):
    lexline = 0

    def __init__(self):
        self.lexline = Lexer.line

    def error(self, s):
        raise SyntaxError('near line %s, : %s' % (self.lexline, s))

    labels = 0

    def newlabel(self):
        return self.labels

    def emitlabel(self, i):
        print("L %s :" % i)
