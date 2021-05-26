from BTree import *
from Node import *
import copy
import pytest


class TestBTree:
    # exemplary btree
    #             |       5       |       12      |
    #         /                   |                   \
    #       | 2 |               | 10 |            | 17 | 22 |
    #      /     \            /        \         /     |      \
    #      1     4            7      11, 12   15, 17   18   27, 32

    @pytest.fixture
    def list_of_elements(self):
        return [5, 22, 2, 27, 15, 12, 7, 17, 18, 17, 10, 4, 32, 20, 1, 11, 12]

    @pytest.fixture
    def node1(self):
        child1 = Node([1])
        child2 = Node([4])
        node = Node([2], [child1, child2])
        node.set_parent_for_children()
        return node

    @pytest.fixture
    def node2(self):
        child1 = Node([7])
        child2 = Node([11, 12])
        node = Node([10], [child1, child2])
        node.set_parent_for_children()
        return node

    @pytest.fixture
    def node3(self):
        child1 = Node([15, 17])
        child2 = Node([18])
        child3 = Node([27, 32])
        node = Node([17, 22], [child1, child2, child3])
        node.set_parent_for_children()
        return node

    @pytest.fixture
    def root(self, node1, node2, node3):
        root = Node([5, 12], [node1, node2, node3])
        root.set_parent_for_children()
        return root

    @pytest.fixture
    def btree(self, root):
        return BTree(3, root)

    def test_create_btree(self, node1):
        tree1 = BTree(5)
        assert tree1.m == 5
        assert tree1.root == Node()
        assert not tree1.all_nodes_arr
        assert BTree(4, node1).root == node1

    def test_find_node_to_insert(self, btree):
        assert btree.find_node_to_insert(0) is btree.root.children[0].children[0]
        assert btree.find_node_to_insert(12) is btree.root.children[1].children[1]
        assert btree.find_node_to_insert(14) is btree.root.children[2].children[0]
        assert btree.find_node_to_insert(-1) is btree.root.children[0].children[0]
        assert btree.find_node_to_insert(213) is btree.root.children[2].children[2]

    def test_is_it_full_node(self):
        node1 = Node([1, 2])
        node2 = Node([1, 2, 3, 4])
        node3 = Node([1, 2, 2, 4, 5, 6, 7])
        btree4 = BTree(4)
        btree8 = BTree(8)
        assert not btree4.is_it_full_node(node1)
        assert btree4.is_it_full_node(node2)
        assert btree4.is_it_full_node(node3)
        assert not btree8.is_it_full_node(node3)

    def test_is_it_root_node(self):
        root = Node([1, 2])
        btree = BTree(3, root)
        assert btree.is_it_root_node(root)
        assert not btree.is_it_root_node(Node([1, 2]))

    def test_split_root(self):
        root = Node([4, 5, 7], [Node([1]), Node([5]), Node([6]), Node([9])])
        mid = len(root.keys) // 2
        l_node = Node(root.keys[:mid], root.children[:mid + 1])
        r_node = Node(root.keys[mid + 1:], root.children[mid + 1:])
        root_after_split = Node([5], [l_node, r_node])
        btree = BTree(3, root)
        btree.split_root()
        assert btree.root == root_after_split
        assert all(child.parent == btree.root for child in btree.root.children)

    def test_split_branch_or_leaf(self):
        pass  # TODO

    def test_add_key(self):
        pass  # TODO

    def test_search(self):
        pass  # TODO

    def test_delete_form_leaf(self):
        pass  # TODO
