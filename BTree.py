from Node import *


class BTree:
    def __init__(self, m=3, root=None):
        if root is None:
            root = Node()
        self.m = m
        self.root = root
        self.all_nodes_arr = []

    def __eq__(self, other):
        if isinstance(other, BTree):
            return self.m == other.m and self.root == other.root

    def add_key_in_range(self, start=0, end=16, step=1):
        for i in range(start, end, step):
            self.add_key(i)

    def add_key(self, key):
        if isinstance(key, int):
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
        return node.number_of_keys() > self.max_number_of_keys()

    def split_node(self, node):
        if self.is_it_root_node(node):
            self.split_root()
        else:
            self.split_branch_or_leaf(node)
        if self.is_it_full_node(node.parent):
            self.split_node(node.parent)

    def is_it_root_node(self, node):
        return self.root is node

    def split_root(self):
        l_child = self.root.create_l_part()
        r_child = self.root.create_r_part()

        mid_key = self.root.get_mid_key()

        self.set_root(Node([mid_key], [l_child, r_child]))
        self.set_lr_child_parent(l_child, r_child, self.root)

    def split_branch_or_leaf(self, node):
        l_child = node.create_l_part()
        r_child = node.create_r_part()

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
        tree_text = ''
        for level in self.all_nodes_arr:
            for node in level:
                tree_text += node.show_node()
            tree_text += '\n'
        print(tree_text)

    def get_all_nodes(self):
        self.all_nodes_arr = []
        self.get_all_nodes_util(self.root, 0)

    def get_all_nodes_util(self, node, level):
        if len(self.all_nodes_arr) <= level:
            self.all_nodes_arr.append([])
        self.all_nodes_arr[level].append(node)
        if not node.is_leaf():
            for child in node.children:
                self.get_all_nodes_util(child, level + 1)

    def show_complex(self):
        self.get_all_nodes()
        tree_text = ''
        for level in self.all_nodes_arr:
            for node in level:
                tree_text += str(node) + '\n'
            tree_text += '\n\n'
        print(str(id(self)) + '\n' + tree_text)

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

            self.delete_key(key)

    def delete_key_form_leaf(self, node, index):
        node.keys.pop(index)
        if not self.is_node_have_enough_keys(node):
            self.supply_leaf(node)

    def delete_delimiter(self, node, index):
        pass

    def is_node_have_enough_keys(self, node):
        if self.is_it_root_node(node):
            if node.is_leaf():
                return True
            return node.number_of_keys() >= 1
        return node.number_of_keys() >= self.min_number_of_keys()

    def supply_leaf(self, node: Node):
        if node.is_extreme_left_child():
            return self.supply_leaf_by_r_neighbour(node)
        elif node.is_extreme_right_child():
            return self.supply_leaf_by_l_neighbour(node)
        else:
            return self.supply_leaf_by_neighbours(node)

    def min_number_of_keys(self):
        return self.min_number_of_children() - 1

    def min_number_of_children(self):
        return self.m // 2 if self.m > 3 else 2
        # tak mi się wydaje żeby nie było sytuacji gdy przy m=3 minimalna ilość kluczy to 0

    def max_number_of_keys(self):
        return self.m - 1

    def is_node_can_be_merge(self, node):
        return node.number_of_keys() <= self.min_number_of_keys()

    def can_take_key_from_node(self, node):
        return node.number_of_keys() >= self.min_number_of_keys() + 1

    def supply_leaf_by_r_neighbour(self, node):
        r_neighbour = node.get_right_neighbour()
        if self.can_take_key_from_node(r_neighbour):
            self.move_key_form_r_neighbour(node, r_neighbour)
        else:
            self.merge_nodes(node, r_neighbour)

    def supply_leaf_by_l_neighbour(self, node):
        l_neighbour = node.get_left_neighbour()
        if self.can_take_key_from_node(l_neighbour):
            self.move_key_form_l_neighbour(node, l_neighbour)
        else:
            self.merge_nodes(node, l_neighbour)

    def supply_leaf_by_neighbours(self, node):
        r_neighbour = node.get_right_neighbour()
        if self.can_take_key_from_node(r_neighbour):
            return self.move_key_form_r_neighbour(node, r_neighbour)

        l_neighbour = node.get_left_neighbour()
        if self.can_take_key_from_node(l_neighbour):
            return self.move_key_form_l_neighbour(node, l_neighbour)

        # na tym mergowaniem trzeba się zastanowić (aktualnie dwa przypadki dla równowagi, żeby nie mergować tylko w jedną stronę
        if node.at_left_from_parent():
            self.merge_nodes(node, l_neighbour)
        else:
            self.merge_nodes(node, r_neighbour)

    @staticmethod
    def move_key_form_r_neighbour(node, r_neighbour):
        key = r_neighbour.keys.pop(0)
        index = node.find_position_in_parent()
        node.keys.append(node.parent.keys[index])
        node.parent.keys[index] = key

    @staticmethod
    def move_key_form_l_neighbour(node, l_neighbour):
        key = l_neighbour.keys.pop()
        index = l_neighbour.find_position_in_parent()
        node.keys.insert(0, node.parent.keys[index])
        node.parent.keys[index] = key

    def merge_nodes(self, node, other_node):
        if node.is_left_neighbour(other_node):
            self.merge_nodes_util(other_node, node)
        elif node.is_right_neighbour(other_node):
            self.merge_nodes_util(node, other_node)

    def merge_nodes_util(self, l_node, r_node):
        parent = l_node.parent
        index = l_node.find_position_in_parent()
        keys = l_node.keys + [parent.keys[index]] + r_node.keys
        children = l_node.children + r_node.children
        node = Node(keys, children, l_node.parent)

        parent.keys.pop(index)
        parent.children[index:index+2] = [node]

        if not self.is_node_have_enough_keys(parent):
            self.supply_node(parent)

    def supply_node(self, node):
        pass


if __name__ == '__main__':
    tree = BTree(m=3)
    for i in range(16):
        tree.add_key(i)
        tree.show()
        if i % 4 == 0:
            tree.show_complex()

    # tree.add_key('l')
    tree.show_complex()
    print('tree 1' + 24*'*')
    tree.show()
    #
    tree2 = BTree()
    tree2.add_key_in_range(16, 0, -1)
    tree.show()
    tree2.show()
    tree2.show_complex()

    tree2.delete_key(16)
    tree2.show_complex()

    print(tree == tree2)
    #
    # # tree3 = BTree.btree_in_range(n=16, m=3)
    # # tree3.show()
    #
    # # tree.add_key(14)
    # # tree.delete_key(17)
    # # tree.delete_key(16)
    # # tree.show_complex()
    # # # extreme right bez merge check
    # #
    # # tree.add_key(2)
    # # tree.delete_key(0)
    # # tree.show_complex()
    # # # extreme left bez merge check/
    #




    # n = tree.search(7)
    # print(n[0], '\tindex: ', n[1])

    # l = [i for i in range(5)]
    # print(l)
    # o = l.pop(0)
    # print(o)
    # print(l)

# usuwa wszystkie
