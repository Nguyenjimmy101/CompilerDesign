from treelib import node, tree


# tree

class Env:
    def __init__(self, root, root_id):
        self.new_tree = tree()
        self.new_tree.create_node(root, root_id)

    def add_node(self, node, node_id, parent_id):
        self.new_tree.create_node(node, node_id, parent=parent_id)

    def show_tree(self):
        self.new_tree.show()
