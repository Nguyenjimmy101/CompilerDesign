from Inter import *
from LexicalAnalyzer.Lexer import Lexer
from LexicalAnalyzer.Tag import Tag
from LexicalAnalyzer.Word import Word
from symbols.Env import Env


class Parser(object):
    lex = None
    look = None
    top = Env(root=True)
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

    def block(self, indent=None, envs=None):
        saved = self.top
        self.top = Env(self.top)
        if envs:
            for env in envs:
                self.top.put(*env)
        body = self.block_body(indent or self.indent)
        block = Block(body, self.top)
        self.top = saved
        return block

    def block_body(self, oldindent):
        try:
            while self.look.tag == Tag.NEW_LINE:
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
            return self._id()
        elif self.look.tag == Tag.APPEND:
            self.match(Tag.APPEND)
            self.expr()

        return expr

    def stmt(self):
        if self.look.tag == Tag.NEW_LINE:
            self.match(Tag.NEW_LINE)

        if isinstance(self.look, str) and len(self.look) == 0:
            return Stmt.null

        if self.look.tag == Tag.IF:
            return self.if_stmt()
        elif self.look.tag == Tag.WHILE:
            return self.while_stmt()
        elif self.look.tag == Tag.FOR:
            return self.for_stmt()
        elif self.look.tag == Tag.ASSIGN:
            return self.assign()
        elif self.look.tag == Tag.DEF:
            return self.function()
        elif self.look.tag == Tag.RETURN:
            self.match(Tag.RETURN)
            return self.expr()
        elif self.look.tag == Tag.PRINT or self.look.tag == Tag.PRINTERR:
            return self.print()
        elif self.look.tag == Tag.FUN:
            self.lambd()
        elif self.look.tag == Tag.COMMENT:
            return self.comment()
        elif self.look.tag == Tag.APPEND:
            self.match(Tag.APPEND)
            self.expr()
        elif self.look.tag == Tag.EOF:
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
        _if = If(op, expr1, expr2, b)

        if self.look.tag == Tag.ELIF:
            return ElifSeq(_if, self.elif_stmt())
        elif self.look.tag == Tag.ELSE:
            return self.else_stmt(_if)
        return _if

    def elif_stmt(self):
        self.match(Tag.ELIF)
        indent = self.indent
        op = self.relop()
        expr1 = self.expr()
        expr2 = self.expr()
        if self.look.tag == Tag.NEW_LINE:
            self.match(Tag.NEW_LINE)

        b = self.block(indent)
        _elif = Elif(op, expr1, expr2, b)

        if self.look.tag == Tag.ELIF:
            return ElifSeq(_elif, self.elif_stmt())
        elif self.look.tag == Tag.ELSE:
            return self.else_stmt(_elif)
        return _elif

    def _id(self, type=None):
        t = self.look
        self.match(Tag.ID)
        token = self.top.get(t.lexeme)
        print(t.lexeme, self.top)
        if not token:
            raise ValueError('Variable %s does not exist' % t)

        if type is not None and token != type:
            raise TypeError('Variable %s expected to be %s' % (t, type))

        return Id(t, type)

    def else_stmt(self, if_stmt):
        self.match(Tag.ELSE)
        # ifstmt = self.if_stmt()
        indent = self.indent
        if self.look.tag == Tag.NEW_LINE:
            self.match(Tag.NEW_LINE)
        b = self.block(indent)
        return Else(if_stmt, b)

    def for_stmt(self):
        self.match(Tag.FOR)
        indent = self.indent
        var = self.look
        self.match(Tag.ID)
        expr = self.expr()
        return For(var, expr, self.block(indent, [[var.lexeme, None]]))

    def while_stmt(self):
        self.match(Tag.WHILE)
        indent = self.indent
        op = self.relop()
        expr = self.expr()
        return While(op, expr, self.block(indent))

    def assign(self):
        self.match(Tag.ASSIGN)
        _id = self.look
        self.top.put(_id.lexeme)
        self.match(Tag.ID)
        expr = self.expr()
        self.move()
        return Assign(Id(_id, None), expr)

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
        if self.is_arith(token):
            p = Paren(token, self.expr())
            self.match(Tag.END_PAREN)
            return p
        else:
            token = self._id()
            exprs = []
            while self.look.tag != Tag.END_PAREN:
                exprs.append(self.expr())
            self.match(Tag.END_PAREN)
            return FunctionCall(token, exprs)

    def print(self):
        if self.look.tag == Tag.PRINT:
            self.match(Tag.PRINT)
            return Print(self.expr())
        else:
            self.match(Tag.PRINTERR)
            return PrintErr(self.expr())

    def function(self):
        self.match(Tag.DEF)
        name = self.look
        self.match(Tag.ID)

        self.match(Tag.TYPE_SEPARATOR)
        type = self.look
        self.match(Tag.TYPE)

        func_env = [name.lexeme, '%sfunction' % type.lexeme]
        self.top.put(*func_env)

        envs = [func_env]

        indent = self.indent
        # Arguments
        args = []
        while self.look.tag != Tag.NEW_LINE:
            argName = self.look
            self.match(Tag.ID)
            self.match(Tag.TYPE_SEPARATOR)
            argType = self.look
            self.match(Tag.TYPE)
            _id = Id(argName, argType)
            args.append(_id)
            envs.append([argName.lexeme, argType.lexeme])

        block = self.block(indent, envs)
        return Function(name, type, args, block)

    def lambd(self):
        self.match(Tag.FUN)
        while self.look.tag != Tag.NEW_LINE:
            self.expr()
        self.block()

    def comment(self):
        self.match(Tag.COMMENT)
        if self.look.tag == Tag.COMMENT:
            self.comment()
        if self.look.tag == Tag.NEW_LINE:
            self.match(Tag.NEW_LINE)
            # self.stmt()
