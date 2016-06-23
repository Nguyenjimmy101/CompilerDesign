from Inter import *
from LexicalAnalyzer.Lexer import Lexer
from LexicalAnalyzer.Tag import Tag
from LexicalAnalyzer.Word import Word
from symbols.Env import Env


class Parser(object):
    lex = None
    look = None
    top = None
    indent = 0
    used = 0
    table = {}

    def __init__(self, stream):
        self.top = Env(root=True)
        self.lex = Lexer(stream)
        self.move()

    def start(self):
        # print(self.stmts().stmt1.block)
        s = self.stmts()
        print(str(s.__dict__))

    def stmts(self):
        if isinstance(self.look, str) and len(self.look) == 0:
            return Stmt.null

        if self.look.tag != Tag.EOF:
            s = self.stmt()

            if isinstance(s, Word) and s.tag == Tag.EOF:
                return Stmt.null

            return Seq(s, self.stmts())
        else:
            print('eof')
            return Stmt.null

    def move(self):
        self.look = self.lex.scan()
        self.indent = self.lex.indent

    def match(self, tag):
        if self.look.tag == tag:
            # print(self.indent, self.look)
            self.move()
        else:
            raise SyntaxError('Expected %s, got %s' % (tag, self.look))

    def block(self, indent=None):
        # self.match(Tag.NEW_LINE)

        # if self.indent != oldindent + 2:
        # raise SyntaxError('Indent is not correct')

        if indent is not None:
            return self.block_body(indent)
        else:
            return self.block_body(self.indent)

    def block_body(self, oldindent):
        # import ipdb; ipdb.set_trace()
        # print(self.indent, oldindent)
        try:
            while self.look.tag == Tag.NEW_LINE:
                # if self.look.tag == Tag.NEW_LINE:
                self.match(Tag.NEW_LINE)
        except:
            print('error', self.look)
            self.move()

        if isinstance(self.look, str) and len(self.look) == 0:
            return Stmt.null

        if self.indent > oldindent:
            s = self.stmt()
            seq = Seq(s, self.block_body(oldindent))
            return seq
        else:
            # s = self.stmt()
            # seq = Seq(s, Stmt.null)
            # print(seq)
            return Stmt.null

    def relop(self):
        op = self.look
        if self.look.tag == Tag.LT:
            self.match(Tag.LT)
        elif self.look.tag == Tag.GT:
            self.match(Tag.GT)
        elif self.look.tag == Tag.GE:
            self.match(Tag.GE)
        elif self.look.tag == Tag.LE:
            self.match(Tag.LE)
        elif self.look.tag == Tag.EQ:
            self.match(Tag.EQ)
        elif self.look.tag == Tag.NE:
            self.match(Tag.NE)
        else:
            raise SyntaxError('Invalid conditional operator: %s' % self.look)

        return op

    def mathop(self):
        token = self.look
        self.move()
        return Arith(token, self.expr(), self.expr())

    def expr(self):
        if self.look.tag == Tag.NEW_LINE:
            self.match(Tag.NEW_LINE)

        expr = None

        if self.look.tag == Tag.NUM:
            expr = self.look
            self.match(Tag.NUM)
        elif self.look.tag == Tag.REAL:
            expr = self.look
            self.match(Tag.REAL)
        elif self.look.tag == Tag.STRING:
            expr = self.look
            self.match(Tag.STRING)
        elif self.look.tag == Tag.BOOL:
            expr = self.look
            self.match(Tag.BOOL)
        elif self.look.tag == Tag.ADD or self.look.tag == Tag.MINUS:
            return self.mathop()
        elif self.look.tag == Tag.MULT or self.look.tag == Tag.DIV:
            return self.mathop()
            # self.stmt()
        elif self.look.tag == Tag.BEGIN_PAREN:
            return self.parens()
        elif self.look.tag == Tag.LIST:
            self.match(Tag.LIST)
            self.expr()
        elif self.look.tag == Tag.ID:
            expr = self.look
            self.match(Tag.ID)
        elif self.look.tag == Tag.APPEND:
            self.match(Tag.APPEND)
            self.expr()

        return expr

    def stmt(self):
        if self.look.tag == Tag.NEW_LINE:
            self.match(Tag.NEW_LINE)

        if self.look.tag == Tag.IF:
            return self.if_stmt()
        elif self.look.tag == Tag.WHILE:
            self.match(Tag.WHILE)
            self.expr()
            self.block()
        elif self.look.tag == Tag.FOR:
            self.match(Tag.FOR)
            self.match(Tag.ID)
            self.expr()
            self.block()
        elif self.look.tag == Tag.ASSIGN:
            return self.assign()
        elif self.look.tag == Tag.DEF:
            return self.function()
        elif self.look.tag == Tag.RETURN:
            self.match(Tag.RETURN)
            self.expr()
        elif self.look.tag == Tag.PRINT or self.look.tag == Tag.PRINTERR:
            self.print()
        elif self.look.tag == Tag.FUN:
            self.lambd()
        elif self.look.tag == Tag.COMMENT:
            self.match(Tag.COMMENT)
            # self.stmt()
        elif self.look.tag == Tag.APPEND:
            self.match(Tag.APPEND)
            self.expr()
        elif self.look.tag == Tag.EOF:
            # Exit on EOF
            # print("End of the file")
            # raise SystemExit(0)
            self.match(Tag.EOF)
            return self.look
        else:
            self.match(Tag.ID)
            return self.look

    def if_stmt(self):
        self.match(Tag.IF)
        indent = self.indent
        op = self.relop()
        expr1 = self.expr()
        expr2 = self.expr()
        if self.look.tag == Tag.NEW_LINE:
            self.match(Tag.NEW_LINE)
        b = self.block(indent)
        return If(op, expr1, expr2, b)

    def assign(self):
        self.match(Tag.ASSIGN)
        _id = self.look
        self.match(Tag.ID)
        expr = self.expr()
        self.move()
        return Assign(_id, expr)

    def is_arith(self, token):
        return self.look.tag in (
            Tag.ADD,
            Tag.MINUS,
            Tag.MULT,
            Tag.DIV
        )

    def parens(self):
        self.match(Tag.BEGIN_PAREN)
        token = self.look
        # self.move()
        p = Paren(token, self.expr())
        self.match(Tag.END_PAREN)
        return p

    def print(self):
        if self.look.tag == Tag.PRINT:
            self.match(Tag.PRINT)
            self.expr()
            #self.stmt()
        else:
            self.match(Tag.PRINTERR)
            self.expr()
            #self.stmt()

    def function(self):
        self.match(Tag.DEF)
        name = self.look
        self.match(Tag.ID)

        indent = self.indent
        args = []
        # Arguments
        while self.look.tag != Tag.NEW_LINE:
            args.append(self.look)
            self.match(Tag.ID)
        self.match(Tag.NEW_LINE)
        block = self.block(indent)
        # print(block)
        return Function(name, args, block)

    def lambd(self):
        self.match(Tag.FUN)
        while self.look.tag != Tag.NEW_LINE:
            self.expr()
        self.block()
