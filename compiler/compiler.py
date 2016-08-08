class Compiler(object):

    def __init__(self, env_table, tree, outfile_name='out.asm'):
        self.outfile_name = outfile_name
        self.env_table = env_table
        self.tree = tree

    def section(self, name):
        self.outfile.write('\t.%s\n' % name)

    def compile(self):
        with open(self.outfile_name, 'w') as outfile:
            self.outfile = outfile
            self.section('text')
            self.section('globl main')
            outfile.write('main:')

            # Generate .data section
            outfile.write('\t.data\n')
