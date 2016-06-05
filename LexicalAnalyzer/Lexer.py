import sys

from LexicalAnalyzer.Bool import Bool
from LexicalAnalyzer.Num import Num
from LexicalAnalyzer.Real import Real
from LexicalAnalyzer.String import String
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

    def readch(self, char):
        self._readch()

        if self.peek != char:
            return False
        self.peek = ' '
        return True

    def scan(self):
        # WHITESPACE
        while True:
            self._readch()
            if self.peek == '\n':
                self.line += 1
            elif self.peek != ' ' and self.peek != '\t':
                break

        # IDENTIFIERS
        if self.peek.isalpha():
            identifier = ''
            while True:
                identifier += self.peek
                self._readch()
                if not self.peek.isalnum():
                    break

            try:
                word = getattr(Words, identifier.upper())
                if word:
                    return word
            except AttributeError:
                word = Word(identifier, Tag.ID)
                self.reserve(word)

                token = Token(self.peek)
                self.peek = ' '

                return token

        # NUMBERS
        if self.peek.isnumeric():
            number = 0
            while True:
                number = 10 * number + int(self.peek)
                self._readch()
                if not self.peek.isnumeric():
                    break

            if self.peek != '.':
                return Num(number)

            number = float(number)
            digit = 10

            while True:
                self._readch()
                if not self.peek.isnumeric():
                    break
                number += int(self.peek) / digit
                digit *= 10
            return Real(number)

        # STRINGS
        if self.peek in ('\'', '\"'):
            # save the quote type so we don't stop on a different quote
            quote = self.peek

            string = ''
            while True:
                self._readch()
                if self.peek == '\\':
                    # skip escape characters
                    string += self.peek
                    self._readch()
                    string += self.peek
                elif self.peek == quote:
                    break
                else:
                    string += self.peek

            return String(string)

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
