class Compiler(object):

    def __init__(self, env_table, tree, outfile_name='out.asm'):
        self.outfile_name = outfile_name
        self.env_table = env_table
        self.tree = tree

        self.variables = {}
        self.sections = []
        self.labels = []

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
        print('assignment!')
        
    def route(self, element):
        print('router', element)
        if element.type == 'Assignment':
            self.assign(element)

    def compile(self):
        with open(self.outfile_name, 'w') as outfile:
            self.outfile = outfile
            
            self.section('text')
            self.section('globl main')
            self.label('main')
            
            self.sequence(self.tree)
            
            # Generate .data section
            self.section('data')
