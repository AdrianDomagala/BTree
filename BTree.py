class Node:
    def __init__(self, keys=[], children=[], parent=None):
        self.keys = keys
        self.children = children
        self.parent = parent

    def __str__(self):
        return f'Id: {id(self)} \t ' \
               f'keys: {self.keys} \t ' \
               f'children: {[id(child) for child in self.children]} \t '\
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


class BTree:

    def __init__(self, m=3):
        self.m = m
        self.root = Node()
        self.show_arr = []

    def show(self):
        self.show_arr = []
        self.add_nodes_to_show(self.root, 0)
        tree = ''
        for level in self.show_arr:
            for node in level:
                tree += node
            tree += '\n'
        print(tree)

    def show_complex(self):
        self.show_arr = []
        self.add_nodes_to_show_complex(self.root, 0)
        tree = ''
        for level in self.show_arr:
            for node in level:
                tree += node + '\n'
            tree += '\n\n'
        print(tree)

    def add_nodes_to_show(self, node, level):
        if len(self.show_arr) <= level:
            self.show_arr.append([])
        self.show_arr[level].append(node.show_node())
        if not node.is_leaf():
            for child in node.children:
                self.add_nodes_to_show(child, level + 1)

    def add_nodes_to_show_complex(self, node, level):
        if len(self.show_arr) <= level:
            self.show_arr.append([])
        self.show_arr[level].append(str(node))
        if not node.is_leaf():
            for child in node.children:
                self.add_nodes_to_show_complex(child, level + 1)

    # # TODO refactoring coś mi się nie podoba
    # def search(self, key, node: Node):
    #     for k, i in enumerate(node.keys):
    #         if k == key:
    #             return True
    #         elif k > key:
    #             if node.is_leaf:
    #                 return False
    #             return self.search(key, node.children[i])
    #     else:
    #         if node.is_leaf():
    #             return False
    #         return self.search(key, node.children[-1])

    def make_new_root(self):
        pass

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
        if self.is_root(node):
            self.split_root(node)
        elif node.is_leaf():
            self.split_branch(node)

            # self.split_leaf(node)
        else:
            self.split_branch(node)
        if self.is_full_node(node.parent):
            self.split_node(node.parent)

    def split_root(self, node):
        mid_index = len(node.keys) // 2
        l_keys = node.keys[:mid_index]
        r_keys = node.keys[mid_index + 1:]

        l_children = node.children[:mid_index + 1]
        r_children = node.children[mid_index + 1:]

        l_child = Node(l_keys, l_children)
        r_child = Node(r_keys, r_children)  # cos z parent

        self.root = Node([node.keys[mid_index]], [l_child, r_child])

        l_child.parent = self.root
        r_child.parent = self.root

        for child in l_child.children:
            child.parent = l_child

        for child in r_child.children:
            child.parent = r_child

    def is_root(self, node):
        return self.root == node

    def split_leaf(self, node: Node):
        mid_index = len(node.keys) // 2
        l_keys = node.keys[:mid_index]
        r_keys = node.keys[mid_index + 1:]

        parent = node.parent
        insert_index = parent.find_index_to_insert(node.keys[mid_index])

        parent.add_key_to_node(node.keys[mid_index])
        node.keys = l_keys
        parent.children[insert_index] = node
        parent.children.insert(insert_index + 1, Node(r_keys, [], parent))

    def split_branch(self, node):
        mid_index = len(node.keys) // 2
        l_keys = node.keys[:mid_index]
        r_keys = node.keys[mid_index + 1:]

        l_children = node.children[:mid_index + 1]
        r_children = node.children[mid_index + 1:]

        parent = node.parent

        insert_index = parent.find_index_to_insert(node.keys[mid_index])

        l_child = Node(l_keys, l_children, parent)
        r_child = Node(r_keys, r_children, parent)

        parent.keys.insert(insert_index, node.keys[mid_index])
        # parent.add_key_to_node(node.keys[mid_index])

        parent.children[insert_index] = l_child
        parent.children.insert(insert_index + 1, r_child)

        print(' ')

    def is_full_node(self, node):
        if node is None:
            return False
        return len(node.keys) >= self.m


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

    t.add_key(9)
    t.show()

    t.add_key(9)
    t.show()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


# To setdefaulst parameter as self variable probably only way
# def lol(self, destination=None):
#     if destination in None:
#         destination = self.path
#     x = do_stuff(destination)


#
#
# n = Node()
#    n.children.append(Node())
#    n.keys.append(1)
#    nc = n.children[0]
#    nc.keys.append(2)
#    nc.parent = n
#    print(nc.parent.keys)
#    n.keys.append(3)
#    print(n.keys)
#    print(nc.parent.keys)
#    print(nc)
#    print('boot integer: ', bool(0))
#    x = 5
#    y = 6
#    print(x, y)
#    temp = y
#    y = x
#    x = temp
#    print(x, y, temp)
#
#    lst = []
#    print('bool list test ', bool(lst))
#    print(lst)
#    lst = [1,2,3,4]
#    print(lst)
#    lst.insert(len(lst), -1)
#    # lst.insert(-1, 5)
#
#    print(lst)
#
#    print(lst[8:])
#
#    nod = Node(keys=[1, 3, 5, 19])
#    print(nod.show_node())
#    print(bool(lst[9]))
