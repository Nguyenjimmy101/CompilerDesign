class Compiler(object):

    def __init__(self, env_table, tree, outfile_name='out.asm'):
        self.outfile_name = outfile_name
        self.env_table = env_table
        self.tree = tree

        self.variables = {}
        self.sections = []
        self.labels = []

    def tab(self):
        self.outfile.write('\t')

    def nl(self):
        self.outfile.write('\n')

    def write(self, data):
        self.outfile.write(data)
        self.nl()

    def syscall(self):
        self.tab()
        self.write('syscall')
    
    def exit(self):
        self.tab()
        self.write('li $v0, 10')
        self.syscall()

    def section(self, name):
        self.sections.append(name)
        self.write('\n\t.%s' % name)

    def label(self, name):
        self.labels.append(name)
        self.write('%s:' % name)

    def sequence(self, seq):
        self.route(seq.stmt1)
        self.route(seq.stmt2)

    def assign(self, stmt):
        self.tab()
        if stmt.expr.type == 'Type':
            self.write('li $t2, %s' % stmt.expr.value.value)
            self.nl()

    def print(self, stmt):
        self.tab()
        self.write('li $v0, 1')
        self.tab()
        self.write('la $a0, ($t2)')
        self.syscall()

    def route(self, element):
        print('routing', element.type)
        if element.type == 'Assignment':
            self.assign(element)
        elif element.type == 'Sequence':
            self.sequence(element)
        elif element.type == 'Print':
            self.print(element)
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
