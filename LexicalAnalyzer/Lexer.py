import sys

from LexicalAnalyzer.Bool import Bool
from LexicalAnalyzer.Comment import Comment
from LexicalAnalyzer.Num import Num
from LexicalAnalyzer.Real import Real
from LexicalAnalyzer.String import String
from LexicalAnalyzer.Tag import Tag
from LexicalAnalyzer.Token import Token
from LexicalAnalyzer.Word import Word, Words


class Lexer(object):
    line = 1
    peek = ' '
    _skip = False
    words = {
        'if': Tag.IF,
        'else': Tag.ELSE,
        'while': Tag.WHILE,
    }

    def __init__(self):
        pass

    def reserve(self, word):
        self.words[word.lexeme] = word

    def _readch(self):
        try:
            self.peek = sys.stdin.read(1)
        except EOFError:
            print('eof error')


    def readch(self, char):
        self._readch()

        if self.peek != char:
            return False
        self.peek = ' '
        return True

    def skip(self):
        self._skip = True

    def scan(self):
        if self.peek == '#':
            comment = ''
            while self.peek != '\n':
                comment += self.peek
                self._readch()
            self.skip()
            return Comment(comment)

        if self._skip:
            self._skip = False
        else:
            # WHITESPACE
            while True:
                self._readch()
                if self.peek == '':
                    return False
                if self.peek == '\n':
                    self.line += 1
                    print('NEW LINE')
                elif self.peek != ' ' and self.peek != '\t':
                    break

        # PARENTHESES
        if self.peek == ')':
            return Tag.END_PAREN

        if self.peek == '(':
            return Tag.BEGIN_PAREN

        # IDENTIFIERS
        if self.peek.isalpha():
            identifier = ''
            while True:
                if self.peek.isalnum():
                    identifier += self.peek
                    self._readch()
                else:
                    self.skip()
                    break

            if identifier in ('true', 'false'):
                return Bool(identifier)

            try:
                word = getattr(Words, identifier.upper())
                if word:
                    return word
            except AttributeError:
                word = Word(identifier, Tag.ID)
                self.reserve(word)

                token = Token(identifier)
                self.peek = ' '

                return token

        # MAP KEY SEPARATOR
        if self.peek == ':':
            return Tag.KEY_SEPARATOR

        # NUMBERS
        if self.peek.isnumeric():
            number = 0
            while True:
                if self.peek.isnumeric():
                    number = 10 * number + int(self.peek)
                    self._readch()
                else:
                    self.skip()
                    break

            if self.peek != '.':
                return Num(number)

            number = float(number)
            digit = 10

            while True:
                if self.peek.isnumeric():
                    number += int(self.peek) / digit
                    digit *= 10
                    self._readch()
                else:
                    self.skip()
                    break
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
        if self.peek == '+':
            return Words.ADD
        elif self.peek == '-':
            return Words.MINUS
        elif self.peek == '*':
            return Words.MULT
        elif self.peek == '/':
            return Words.DIV

        # COMPARISON
        if self.peek == '=':
            if self.readch('='):
                return Words.EQ
            else:
                return Words.ASSIGN
        elif self.peek == '!':
            if self.readch('='):
                return Words.NE
            else:
                return Token('!')
        elif self.peek == '<':
            if self.readch('='):
                return Words.LE
            else:
                return Words.LT
        elif self.peek == '>':
            if self.readch('='):
                return Words.GE
            else:
                return Words.GT

        return ''
