import sys

from .Tag import Tag
from .Token import Token
from .Word import Words


class Lexer(object):
    line = 1
    peek = " "
    words = {
        'if': Tag.IF,
        'else': Tag.ELSE,
        'while': Tag.WHILE,
    }

    def reserve(self, word):
        self.words[word.lexeme] = word

    def _readch(self):
        self.peek = sys.stdin.read(1)

    def readch(self, c):
        self._readch()

        if self.peek != c:
            return False
        self.peek = ' '
        return True

    def scan(self):
        # WHITESPACE
        while self.peek != ' ' and self.peek != '\t':
            if self.peek == '\n':
                self.line += 1

        # IDENTIFIERS

        # OPERATORS
        if self.peek == '=':
            if self.readch('='):
                return Words.eq
            else:
                return Token('=')
        elif self.peek == '!':
            if self.readch('='):
                return Words.ne
            else:
                return Token('!')
        elif self.peek == '<':
            if self.readch('='):
                return Words.le
            else:
                return Token('<')
        elif self.peek == '>':
            if self.readch('='):
                return Words.ge
            else:
                return Token('>')


if __name__ == '__main__':
    lexer = Lexer()
    while True:
        lexer.scan()
