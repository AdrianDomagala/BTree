from Node import *


class BTree:
    def __init__(self, m=3):
        self.m = m
        self.root = Node()
        self.show_arr = []

    def add_key(self, key):
        node = self.find_node_to_insert(key)
        node.add_key_to_node(key)
        if self.is_it_full_node(node):
            self.split_node(node)

    def find_node_to_insert(self, key, node=None):
        if node is None:
            node = self.root
        if node.is_leaf():
            return node
        else:
            index = node.find_index_to_insert(key)
            return self.find_node_to_insert(key, node.children[index])

    def is_it_full_node(self, node):
        if node is None:
            return False
        return node.number_of_keys() >= self.m

    def split_node(self, node):
        if self.is_it_root_node(node):
            self.split_root(node)
        else:
            self.split_branch_or_leaf(node)
        if self.is_it_full_node(node.parent):
            self.split_node(node.parent)

    def is_it_root_node(self, node):
        return self.root == node

    def split_root(self, node):
        l_child = node.create_l_child()
        r_child = node.create_r_child()

        mid_key = node.get_mid_key()

        self.set_root(Node([mid_key], [l_child, r_child]))
        self.set_lr_child_parent(l_child, r_child, self.root)

    def split_branch_or_leaf(self, node):
        l_child = node.create_l_child()
        r_child = node.create_r_child()

        parent = node.parent
        mid_key = node.get_mid_key()

        insert_index = parent.find_index_to_insert(mid_key)
        parent.add_key_to_node(mid_key)

        parent.children[insert_index:insert_index + 1] = [l_child, r_child]
        self.set_lr_child_parent(l_child, r_child, parent)

    def set_root(self, root):
        self.root = root

    @staticmethod
    def set_lr_child_parent(l_child, r_child, parent):
        l_child.set_parent(parent)
        r_child.set_parent(parent)

        l_child.set_parent_for_children(l_child)
        r_child.set_parent_for_children(r_child)

    def show(self):
        self.get_all_nodes()
        tree = ''
        for level in self.show_arr:
            for node in level:
                tree += node.show_node()
            tree += '\n'
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

    def show_complex(self):
        self.get_all_nodes()
        tree = ''
        for level in self.show_arr:
            for node in level:
                tree += str(node) + '\n'
            tree += '\n\n'
        print(tree)

    def search(self, key, node=None):
        if node is None:
            node = self.root
        for i, k in enumerate(node.keys):
            if k == key:
                return node, i
            elif k > key:
                if node.is_leaf():
                    return None, None
                return self.search(key, node.children[i])
        if node.is_leaf():
            return None, None
        return self.search(key, node.children[-1])

    def delete_key(self, key):
        node, index = self.search(key)
        if node is not None:
            if node.is_leaf():
                self.delete_key_form_leaf(node, index)
            else:
                self.delete_delimiter(node, index)

    def delete_key_form_leaf(self, node, index):
        node.keys.pop(index)
        if not self.is_node_have_enough_keys(node):
            self.supply_node(node)

    def delete_delimiter(self, node, index):
        pass

    def is_node_have_enough_keys(self, node):
        if self.is_it_root_node(node):
            if node.is_leaf():
                return True
            return node.keys >= 1
        return node.keys >= self.min_number_of_keys()

    def supply_node(self, node):
        pass

    def min_number_of_keys(self):
        return self.min_number_of_children() - 1

    def min_number_of_children(self):
        return self.m // 2


if __name__ == '__main__':
    tree = BTree(m=3)
    for i in range(17):
        tree.add_key(i)
        tree.show()
        if i % 4 == 0:
            tree.show_complex()
    tree.show_complex()

    n = tree.search(12)
    print(n[0], '\tindex: ', n[1])
