def switch_arith_token(token):
    if token == '+':
        return 'add'
    elif token == '-':
        return 'sub'
    elif token == '*':
        return 'mult'
    elif token == '/':
        return 'div'
    else:
        raise SyntaxError('"%s" is not a valid arithmetic token' % token)


class Compiler(object):

    def __init__(self, env_table, tree, outfile_name='out.asm'):
        self.outfile_name = outfile_name
        self.env_table = env_table
        self.tree = tree

        self.sections = []
        self.labels = []

        # 0 - 9
        self.t_var = []

        # ex: t4, t0, t1
        # does not include dollar signs
        self.variables = {}

    def new_t(self):
        if len(self.t_var) == 10:
            print('t vars full, using 0')
            return 0
        else:
            if len(self.t_var) == 0:
                self.t_var.append(0)
                return 0
            m = max(self.t_var)
            self.t_var.append(m + 1)
            return m + 1

    def new_label(self):
        if len(self.labels) == 0:
            self.labels.append(1)
            return 1
        m = max(self.labels)
        self.labels.append(m + 1)
        return m + 1

    def tab(self):
        self.outfile.write('\t')

    def nl(self):
        self.outfile.write('\n')

    def write(self, data):
        self.tab()
        self.outfile.write(data)
        self.nl()

    def syscall(self):
        self.write('syscall')
        self.nl()

    def exit(self):
        self.write('li $v0, 10')
        self.syscall()

    def section(self, name):
        self.sections.append(name)
        self.outfile.write('\n\t.%s\n' % name)

    def label(self, name):
        self.outfile.write('%s:\n' % name)

    def sequence(self, seq):
        self.route(seq.stmt1)
        self.route(seq.stmt2)

    def assign(self, stmt):
        # variable id name
        varid = stmt.id._id.lexeme
        if stmt.expr.type == 'Type':
            t = self.new_t()
            self.write('li $t%s, %s' % (t, stmt.expr.value.value))
            if varid not in self.variables:
                self.variables[varid] = 't%s' % t
        elif stmt.expr.type == 'Paren':
            # arithmetic most likely
            expr = stmt.expr.expr
            if expr.type == 'Arithmetic':
                t = self.arithmetic(expr)
                if varid not in self.variables:
                    self.variables[varid] = 't%s' % t

    def arithmetic(self, expr):
        var = self.new_t()
        expr1 = expr.expr1
        expr2 = expr.expr2

        op = switch_arith_token(expr.token.lexeme)

        if expr1.type == 'Type' and expr2.type == 'Type':
            self.write('li $t%s, %s' % (var, expr1.value.value))
            self.write('%s $t%s, $t%s, %s' % (op, var, var, expr2.value.value))
        elif expr1.type == 'Type' and expr2.type != 'Type':
            exprvar = self.variables[expr2._id.lexeme]
            self.write('li $t%s, %s' % (var, expr1.value.value))
            self.write('%s $%s, $t%s, $%s' % (op, exprvar, var, exprvar))
        elif expr2.type == 'Type' and expr1.type != 'Type':
            exprvar = self.variables[expr1._id.lexeme]
            self.write('li $t%s, %s' % (var, expr2.value.value))
            self.write('%s $%s, $t%s, $%s' % (op, exprvar, var, exprvar))
        elif expr1.type != 'Type' and expr2.type != 'Type':
            expr1var = self.variables[expr1._id.lexeme]
            expr2var = self.variables[expr2._id.lexeme]
            self.write('%s $t%s, $%s, $%s' % (op, var, expr1var, expr2var))
        # self.nl()
        return var

    def _if(self, stmt):
        rel = stmt.rel

        endif = self.new_label()
        a = ''
        b = ''

        if hasattr(rel.expr1, '_id'):
            # expr1 is an ID, should be in the variables table
            a = self.variables[rel.expr1._id.lexeme]
        else:
            a_t = self.new_t()
            self.write('li $t%s, %s' % (a_t, rel.expr1.value.value))
            a = 't%s' % a_t

        if hasattr(rel.expr2, '_id'):
            # expr1 is an ID, should be in the variables table
            b = self.variables[rel.expr2._id.lexeme]
        else:
            b_t = self.new_t()
            self.write('li $t%s, %s' % (b_t, rel.expr2.value.value))
            b = 't%s' % b_t

        if rel.token.lexeme == '==':
            self.write('bne $%s, $%s, L%s' % (a, b, endif))
        elif rel.token.lexeme == '!=':
            self.write('beq $%s, $%s, L%s' % (a, b, endif))
        elif rel.token.lexeme == '<':
            self.write('bge $%s, $%s, L%s' % (a, b, endif))
        elif rel.token.lexeme == '>':
            self.write('ble $%s, $%s, L%s' % (a, b, endif))
        elif rel.token.lexeme == '<=':
            self.write('bgt $%s, $%s, L%s' % (a, b, endif))
        elif rel.token.lexeme == '>=':
            self.write('blt $%s, $%s, L%s' % (a, b, endif))

        self.route(stmt.block)
        self.label('L%s' % endif)

    def _else(self, stmt):
        if_stmt = stmt.if_stmt
        rel = if_stmt.rel

        else_lbl = self.new_label()
        endif = self.new_label()
        a = ''
        b = ''

        if hasattr(rel.expr1, '_id'):
            # expr1 is an ID, should be in the variables table
            a = self.variables[rel.expr1._id.lexeme]
        else:
            a_t = self.new_t()
            self.write('li $t%s, %s' % (a_t, rel.expr1.value.value))
            a = 't%s' % a_t

        if hasattr(rel.expr2, '_id'):
            # expr1 is an ID, should be in the variables table
            b = self.variables[rel.expr2._id.lexeme]
        else:
            b_t = self.new_t()
            self.write('li $t%s, %s' % (b_t, rel.expr2.value.value))
            b = 't%s' % b_t

        if rel.token.lexeme == '==':
            self.write('bne $%s, $%s, L%s' % (a, b, else_lbl))
        elif rel.token.lexeme == '!=':
            self.write('beq $%s, $%s, L%s' % (a, b, else_lbl))
        elif rel.token.lexeme == '<':
            self.write('bge $%s, $%s, L%s' % (a, b, else_lbl))
        elif rel.token.lexeme == '>':
            self.write('ble $%s, $%s, L%s' % (a, b, else_lbl))
        elif rel.token.lexeme == '<=':
            self.write('bgt $%s, $%s, L%s' % (a, b, else_lbl))
        elif rel.token.lexeme == '>=':
            self.write('blt $%s, $%s, L%s' % (a, b, else_lbl))

        self.route(if_stmt.block)
        self.write('j L%s' % endif)
        self.label('L%s' % else_lbl)
        self.route(stmt.block)
        self.label('L%s' % endif)

    def paren(self, paren):
        print('paren', paren)

    def print(self, stmt):
        self.write('li $v0, 1')
        self.write('la $a0, ($%s)' % self.variables[stmt.expr._id.lexeme])
        self.syscall()

    def route(self, element):
        print('routing', element.type)
        if element.type == 'Assignment':
            self.assign(element)
        elif element.type == 'Sequence':
            self.sequence(element)
        elif element.type == 'Print':
            self.print(element)
        elif element.type == 'Paren':
            self.paren(element)
        elif element.type == 'If':
            self._if(element)
        elif element.type == 'Else':
            self._else(element)
        elif element.type == 'Block':
            self.route(element.stmts)
        else:
            print('Null statement')

    def compile(self):
        with open(self.outfile_name, 'w') as outfile:
            self.outfile = outfile

            self.section('text')
            self.section('globl main')
            self.label('main')

            self.sequence(self.tree)
            self.exit()

            print('VARIABLES', self.variables)

            # Generate .data section
            self.section('data')
