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
    indent = 0
    finished_indent = False
    words = {
        'if': Tag.IF,
        'else': Tag.ELSE,
        'while': Tag.WHILE,
        'elif': Tag.ELIF,
    }

    def __init__(self, stream):
        self.stream = stream

    def reserve(self, word):
        self.words[word.lexeme] = word

    def _readch(self):
        try:
            self.peek = self.stream.read(1)
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
        # WHITESPACE
        while True:
            if not self._skip:
                self._readch()
            self._skip = False

            if self.peek == '\n':
                # import ipdb; ipdb.set_trace()
                self.line += 1
                self.indent = 0
                self.finished_indent = False
                return Words.NEW_LINE
            elif self.peek == ' ' and self.finished_indent == False:
                self.indent += 1
            elif self.peek != ' ' and self.peek != '\t':
                self.finished_indent = True
                break
            elif self.peek == '':
                return Words.EOF

        if self.peek == '#':
            comment = ''
            while self.peek != '\n':
                comment += self.peek
                self._readch()
            self.skip()
            return Comment(comment)

        # PARENTHESES
        if self.peek == ')':
            return Words.END_PAREN

        if self.peek == '(':
            return Words.BEGIN_PAREN

        # IDENTIFIERS
        if self.peek.isalpha() or self.peek == '_':
            identifier = ''
            while True:
                if self.peek.isalnum() or self.peek == '_':
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

                return word

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
                    break

            if self.peek != '.':
                self.skip()
                return Num(number)

            number = float(number)
            digit = 10

            while True:
                self._readch()
                if self.peek.isnumeric():
                    number += int(self.peek) / digit
                    digit *= 10
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
