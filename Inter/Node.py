from LexicalAnalyzer.Lexer import Lexer


global labels
labels = 0

class Node(object):
    lexline = 0

    def __init__(self):
        self.lexline = Lexer.line

    def error(self, s):
        raise SyntaxError('near line %s, : %s' % (self.lexline, s))

    def newlabel(self):
        global labels
        labels += 1
        return labels

    def emit(self, s):
        print('\t%s' % s)

    def emitlabel(self, i):
        print("L%s:" % i)
