from LexicalAnalyzer.Tag import Tag
from LexicalAnalyzer.Token import Token
from LexicalAnalyzer.Word import Words

symbol_dict = {':': Tag.KEY_SEPARATOR,
               ')': Tag.END_PAREN,
               '(': Tag.BEGIN_PAREN,
               '+': Words.ADD,
               '-': Words.MINUS,
               '*': Words.MULT,
               '/': Words.DIV,
               }


def symbol_scanner(self):
    if self.peek in self.symbol_dict:
        return self.symbol_dict[self.peek]

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
