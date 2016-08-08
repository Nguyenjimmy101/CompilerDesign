def switch_arith_token(token):
    if token == '+':
        return 'add'
    elif token == '-':
        return 'sub'
    elif token == '*':
        return 'mul'
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

    def exit(self):
        self.write('li $v0, 10')
        self.syscall()

    def section(self, name):
        self.sections.append(name)
        self.outfile.write('\n\t.%s\n' % name)

    def label(self, name):
        self.labels.append(name)
        self.outfile.write('%s:\n' % name)

    def sequence(self, seq):
        self.route(seq.stmt1)
        self.route(seq.stmt2)

    def assign(self, stmt):
        if stmt.expr.type == 'Type':
            t = self.new_t()
            self.write('li $t%s, %s' % (t, stmt.expr.value.value))
            self.variables[stmt.id._id.lexeme] = 't%s' % t
        elif stmt.expr.type == 'Paren':
            # arithmetic most likely
            expr = stmt.expr.expr
            if expr.type == 'Arithmetic':
                self.arithmetic(expr)
                
    def arithmetic(self, expr):
        var = self.new_t()
        expr1 = expr.expr1
        expr2 = expr.expr2
        
        op = switch_arith_token(expr.token.lexeme)
        # optype = op if expr1.type == 'Type' and expr2.type == 'Type' else '%si' % op
        
        if expr1.type == 'Type':
            self.write('li $t%s, %s' % (var, expr1.value.value))
            self.write('%s $t%s, $t%s, %s' % (op, var, var, expr2.value.value))
            return
        
        if expr2.type == 'Type':
            self.write('li $t%s, %s' % (var, expr2.value.value))
            self.write('%s $t%s, $t%s, %s' % (op, var, var, expr1.value.value))
            return
            
        print(expr1)
        
    def paren(self, paren):
        print('paren', paren)

    def print(self, stmt):
        self.write('li $v0, 1')
        self.write('la $a0, ($t0)')
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

            # Generate .data section
            self.section('data')
