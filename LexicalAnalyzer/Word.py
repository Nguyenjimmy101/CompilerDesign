from LexicalAnalyzer.Tag import Tag
from LexicalAnalyzer.Token import Token


class Word(Token):
    lexeme = ''

    def __init__(self, lexeme, tag):
        super().__init__(tag)
        self.lexeme = lexeme

    def __str__(self):
        return 'WORD: Lexeme is %s and tag is %s' % (self.lexeme, self.tag)
        
    def __repr__(self):
        return 'WORD: Lexeme is %s and tag is %s' % (self.lexeme, self.tag)


class Words(object):
    NONE = Word('', Tag.BASIC)
    EQ = Word('==', Tag.EQ)
    NE = Word('!=', Tag.NE)
    LE = Word('<=', Tag.LE)
    GE = Word('>=', Tag.GE)
    LT = Word('<', Tag.LT)
    GT = Word('>', Tag.GT)
    ASSIGN = Word('=', Tag.ASSIGN)
    IF = Word('if', Tag.IF)
    ELSE = Word('else', Tag.ELSE)
    ELIF = Word('elif', Tag.ELIF)
    PRINT = Word('print', Tag.PRINT)
    LIST = Word('list', Tag.LIST)
    APPEND = Word('append', Tag.APPEND)
    MAP = Word('map', Tag.MAP)
    WHILE = Word('while', Tag.WHILE)
    FOR = Word('for', Tag.FOR)
    RETURN = Word('return', Tag.RETURN)
    DEF = Word('def', Tag.DEF)
    FUN = Word('fun', Tag.FUN)
    PRINTERR = Word('printerr', Tag.PRINTERR)
    MINUS = Word('-', Tag.MINUS)
    ADD = Word('+', Tag.ADD)
    MULT = Word('*', Tag.MULT)
    DIV = Word('/', Tag.DIV)
    NEW_LINE = Word('NEW_LINE', Tag.NEW_LINE)
    BEGIN_PAREN = Word('BEGIN_PAREN', Tag.BEGIN_PAREN)
    END_PAREN = Word('END_PAREN', Tag.END_PAREN)
    EOF = Word('EOF', Tag.EOF)
