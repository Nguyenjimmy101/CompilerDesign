import sys

from LexicalAnalyzer.Tag import Tag
from LexicalAnalyzer.Token import Token
from LexicalAnalyzer.Word import Word, Words


class Lexer(object):
    line = 1
    peek = ' '
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
        while self._readch():
            if self.peek == '\n':
                self.line += 1
            elif self.peek != ' ' and self.peek != '\t':
                break

        # IDENTIFIERS
        if self.peek.isalpha():
            s = ''
            while True:
                s += self.peek
                self._readch()
                if not self.peek.isalnum():
                    break

            word = None
            try:
                word = getattr(Words, s.upper())
                if word:
                    return word
            except AttributeError:
                word = Word(s, Tag.ID)
                self.reserve(word)

                token = Token(self.peek)
                self.peek = ' '

                return token

        # OPERATORS
        if self.peek == '=':
            if self.readch('='):
                return Words.EQ
            else:
                return Token('=')
        elif self.peek == '!':
            if self.readch('='):
                return Words.NE
            else:
                return Token('!')
        elif self.peek == '<':
            if self.readch('='):
                return Words.LE
            else:
                return Token('<')
        elif self.peek == '>':
            if self.readch('='):
                return Words.GE
            else:
                return Token('>')
