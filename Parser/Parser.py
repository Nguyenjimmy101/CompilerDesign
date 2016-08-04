from Inter import *
from LexicalAnalyzer.Lexer import Lexer
from LexicalAnalyzer.Tag import Tag
from LexicalAnalyzer.Word import Word
from LexicalAnalyzer.Bool import Bool as LBool
from LexicalAnalyzer.Num import Num as LNum
from LexicalAnalyzer.Real import Real as LReal
from LexicalAnalyzer.String import String as LString
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
        begin = s.newlabel()
        after = s.newlabel()
        s.emitlabel(begin)
        s.gen(begin, after)
        s.emitlabel(after)
        # print(self.top.__dict__)
        # print(str(s.__dict__))

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
        if indent is None:
            indent = self.indent
        body = self.block_body(indent)
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
            expr = Integer()
            self.match(Tag.NUM)
        elif self.look.tag == Tag.REAL:
            expr = self.look
            expr = Float()
            self.match(Tag.REAL)
        elif self.look.tag == Tag.STRING:
            expr = self.look
            expr = String()
            self.match(Tag.STRING)
        elif self.look.tag == Tag.BOOL:
            expr = self.look
            expr = Bool()
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
        if not token:
            raise ValueError('Variable %s does not exist' % t)

        # if type is not None and token != type:
        #     raise TypeError('Variable %s expected to be %s' % (t, type))

        return Id(t, token)

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
        self.match(Tag.ID)
        expr = self.expr()
        type = self.expr_type(expr)
        self.top.put(_id.lexeme, type)
        self.move()
        return Assign(Id(_id, type), expr)

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

        func_env = [name.lexeme, FunctionType(type.lexeme)]
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
            wordtype = self.word_type(argType)
            _id = Id(argName, wordtype)
            args.append(_id)
            envs.append([argName.lexeme, wordtype])

        block = self.block(indent, envs)
        return Function(name, type, args, block)

    def expr_type(self, expr, expr2=None):
        if isinstance(expr, LNum):
            return Integer()
        elif isinstance(expr, LReal):
            return Float()
        elif isinstance(expr, LString):
            return String()
        elif isinstance(expr, LBool):
            return Bool()
        else:
            if isinstance(expr, Word):
                return self.word_type(expr)

        if expr.type == 'Paren':
            return self.expr_type(expr.expr)

        if expr.type == 'Arithmetic':
            type1 = self.expr_type(expr.expr1)
            type2 = self.expr_type(expr.expr2)
            return self.coerce_types(type1, type2)

        if isinstance(expr, Id):
            return expr.type

        if expr.type == 'FunctionCall':
            return expr.function_name.type
            
        if isinstance(expr, Type):
            return expr

    def word_type(self, word):
        if word.lexeme == 'int':
            return Integer()
        elif word.lexeme == 'string':
            return String()
        elif word.lexeme == 'void':
            return Void()
        elif word.lexeme == 'float':
            return Float()
        elif word.lexeme == 'bool':
            return Bool()
        else:
            raise TypeError('Unknown type %s' % word.lexeme)

    def coerce_types(self, type1, type2):
        if isinstance(type1, type(type2)):
            return type1

        if isinstance(type1, Integer) and isinstance(type2, Float):
            return Float()
        elif isinstance(type1, Float) and isinstance(type2, Integer):
            return Float()

        if isinstance(type1, String) and isinstance(type2, Integer):
            return String()
        elif isinstance(type1, Integer) and isinstance(type2, String):
            return String()

        if isinstance(type1, Bool) and isinstance(type2, Integer):
            return Integer()
        elif isinstance(type1, Integer) and isinstance(type2, Bool):
            return Integer()

        raise TypeError('Cannot coerce types %s and %s' % (type(type1), type(type2)))

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
