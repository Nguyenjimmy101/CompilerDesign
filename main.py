import sys

from Parser.Parser import Parser

def run_parser(parser):
    while True:
        parser.move()
        if isinstance(parser.look, bool) and parser.look == False:
            break
        print(parser.look)
    print('END ALL')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as fp:
            run_parser(Parser(fp))
    else:
        run_parser(Parser(sys.stdin))
