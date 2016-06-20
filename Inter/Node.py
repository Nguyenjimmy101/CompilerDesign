from LexicalAnalyzer.Lexer import Lexer

class Node(object):
    lexline = 0

    def __init__(self):
        self.lexline = Lexer.line
