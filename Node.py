class Node:
    def __init__(self, keys=[], children=[], parent=None):
        self.keys = keys
        self.children = children
        self.parent = parent

    def __str__(self):
        return f'Id: {id(self)} \t ' \
               f'keys: {self.keys} \t ' \
               f'children: {[id(child) for child in self.children]} \t ' \
               f'parent id: {id(self.parent)}'

    def show_node(self):
        return '|\t' + '\t|\t'.join(str(k) for k in self.keys) + '\t|'

    def is_leaf(self):
        return not bool(self.children)

    def find_index_to_insert(self, key):
        for i, k in enumerate(self.keys):
            if k >= key:
                return i
        return self.number_of_keys()

    def add_key_to_node(self, key):
        index = self.find_index_to_insert(key)
        self.keys.insert(index, key)

    def get_mid_index(self):
        return self.number_of_keys() // 2

    def get_mid_key(self):
        return self.keys[self.get_mid_index()]

    def create_l_child(self):
        mid_index = self.get_mid_index()
        keys = self.keys[:mid_index]
        children = self.children[:mid_index + 1]
        return Node(keys, children)

    def create_r_child(self):
        mid_index = self.get_mid_index()
        keys = self.keys[mid_index + 1:]
        children = self.children[mid_index + 1:]
        return Node(keys, children)

    def set_parent(self, parent):
        self.parent = parent

    def set_parent_for_children(self, parent):
        for child in self.children:
            child.set_parent(parent)

    def number_of_keys(self):
        return len(self.keys)
