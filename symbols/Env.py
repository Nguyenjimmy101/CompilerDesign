from treelib import Node, Tree
from pprint import pformat


class Env:
    def __init__(self, prev=None, root=False):
        self.prev = prev
        self.table = dict()

        if root:
            self.table = {'root': {}}

    def put(self, token, _id):
        self.table[token] = _id

    def get(self, token):
        e = self
        while e != None:
            found = e.table.get(token)
            if found:
                return found
            e = e.prev

    def __str__(self):
        return pformat(self.table)
