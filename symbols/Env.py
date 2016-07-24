# from treelib import Node, Tree
from pprint import pformat
from Inter.UnknownType import UnknownType


class Env:
    def __init__(self, prev=None, root=False):
        self.prev = prev
        self.table = dict()

    def put(self, token, type=UnknownType()):
        self.table[token] = type

    def get(self, token):
        e = self
        while e != None:
            found = e.table.get(token)
            if found:
                return found
            e = e.prev
        return None

    def __str__(self):
        return str(self.table)

    def __repr__(self):
        return str(self.table)
