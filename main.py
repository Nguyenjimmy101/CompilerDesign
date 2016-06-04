import sys

from LexicalAnalyzer.Lexer import Lexer

if __name__ == '__main__':
    lexer = Lexer()
    while True:
        print(lexer.scan())
