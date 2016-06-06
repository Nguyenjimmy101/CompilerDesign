import sys

from LexicalAnalyzer.Lexer import Lexer

if __name__ == '__main__':
    lexer = Lexer()
    while True:
        out = lexer.scan()
        if isinstance(out, bool) and out == False:
            print('END')
            break
        print(out)
