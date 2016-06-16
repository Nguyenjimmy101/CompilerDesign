import sys

from LexicalAnalyzer.Lexer import Lexer

def run_lexer(lexer):
    while True:
        out = lexer.scan()
        if isinstance(out, bool) and out == False:
            print('END')
            break
        print(out)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as fp:
            run_lexer(Lexer(fp))
    else:
        run_lexer(Lexer(sys.stdin))
