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
        return len(self.keys)

    def add_key_to_node(self, key):
        index = self.find_index_to_insert(key)
        self.keys.insert(index, key)

    def get_mid_index(self):
        return len(self.keys) // 2

    def get_mid_key(self):
        return self.keys[self.get_mid_index()]

    def get_l_child(self):
        mid_index = self.get_mid_index()
        keys = self.keys[:mid_index]
        children = self.children[:mid_index + 1]
        return Node(keys, children)

    def get_r_child(self):
        mid_index = self.get_mid_index()
        keys = self.keys[mid_index+1:]
        children = self.children[mid_index + 1:]
        return Node(keys, children)

    def set_parent(self, parent):
        self.parent = parent

    def set_parent_for_children(self, parent):
        for child in self.children:
            child.set_parent(parent)


class BTree:

    def __init__(self, m=3):
        self.m = m
        self.root = Node()
        self.show_arr = []

    def show(self):
        self.get_all_nodes()
        tree = ''
        for level in self.show_arr:
            for node in level:
                tree += node.show_node()
            tree += '\n'
        print(tree)

    def show_complex(self):
        self.get_all_nodes()
        tree = ''
        for level in self.show_arr:
            for node in level:
                tree += str(node) + '\n'
            tree += '\n\n'
        print(tree)

    def get_all_nodes(self):
        self.show_arr = []
        self.get_all_nodes_util(self.root, 0)

    def get_all_nodes_util(self, node, level):
        if len(self.show_arr) <= level:
            self.show_arr.append([])
        self.show_arr[level].append(node)
        if not node.is_leaf():
            for child in node.children:
                self.get_all_nodes_util(child, level + 1)

    def add_key(self, key):
        node = self.find_node_to_insert(key)
        node.add_key_to_node(key)
        if self.is_full_node(node):
            self.split_node(node)

    def find_node_to_insert(self, key, node=None):
        if node is None:
            node = self.root
        if node.is_leaf():
            return node
        else:
            index = node.find_index_to_insert(key)
            return self.find_node_to_insert(key, node.children[index])

    def split_node(self, node):
        if self.is_it_root_node(node):
            self.split_root(node)
        else:
            self.split_branch_or_leaf(node)
        if self.is_full_node(node.parent):
            self.split_node(node.parent)

    def split_root(self, node):
        l_child = node.get_l_child()
        r_child = node.get_r_child()

        mid_key = node.get_mid_key()
        self.set_root(Node([mid_key], [l_child, r_child]))
        self.set_lr_child_parent(l_child, r_child, self.root)

    def is_it_root_node(self, node):
        return self.root == node

    def set_root(self, root):
        self.root = root

    def split_branch_or_leaf(self, node):
        l_child = node.get_l_child()
        r_child = node.get_r_child()

        parent = node.parent
        mid_key = node.get_mid_key()

        insert_index = parent.find_index_to_insert(mid_key)
        parent.add_key_to_node(mid_key)

        parent.children[insert_index:insert_index + 1] = [l_child, r_child]
        self.set_lr_child_parent(l_child, r_child, parent)

    @staticmethod
    def set_lr_child_parent(l_child, r_child, parent):
        l_child.set_parent(parent)
        r_child.set_parent(parent)

        l_child.set_parent_for_children(l_child)
        r_child.set_parent_for_children(r_child)

    def is_full_node(self, node):
        if node is None:
            return False
        return len(node.keys) >= self.m

    def search(self, key, node):
        for k, i in enumerate(node.keys):
            if k == key:
                return True
            elif k > key:
                if node.is_leaf:
                    return False
                return self.search(key, node.children[i])
        if node.is_leaf():
            return False
        return self.search(key, node.children[-1])


if __name__ == '__main__':
    print('siemaneczko')

    t = BTree()
    t.show()

    t.add_key(1)
    t.show()

    t.add_key(2)
    t.show()

    print(t.root.keys)

    t.add_key(3)
    t.show()

    t.add_key(4)
    t.show()

    t.add_key(5)
    t.show()

    t.add_key(6)
    # t.show()

    t.show_complex()

    t.add_key(7)
    # t.show()

    t.add_key(8)
    t.show()

    t.show_complex()

    t.add_key(9)
    t.show()
    print('Pass')

    t.show_complex()

    t.add_key(9)
    t.show()

    t.add_key(9)
    t.show()

    t.add_key(9)
    t.show()

    t.add_key(9)
    t.show()
    