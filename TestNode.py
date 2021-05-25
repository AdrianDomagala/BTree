from Node import *
import pytest


class TestNode:
    @pytest.fixture
    def children(self):
        return [Node([j for j in range(i + 1)]) for i in range(5)]

    def test_compare_node(self):
        empty_node = Node()
        empty_node_1 = Node([], [])
        assert empty_node == empty_node_1

        node1 = Node([1, 2, 3], [empty_node])
        node2 = Node([1, 2, 3], [empty_node_1])
        assert node1 == node2

        node3 = Node([4, 5], [node1, empty_node])
        node4 = Node([4, 5], [node2, empty_node_1])
        assert node3 == node4

        node5 = Node([4, 5, 5], [node2, empty_node_1])
        assert node3 != node5

        node6 = Node()
        node7 = Node([1, 2, 3], [empty_node_1, node6])
        node8 = Node([4, 5], [node7, empty_node_1])
        assert node8 != node3

    def test_add_key(self):
        lst_start = [1, 2, 4, 5]
        lst1 = [1, 2, 4, 5, 6]
        lst2 = [1, 2, 3, 4, 5, 6]
        lst3 = [-2, 1, 2, 3, 4, 5, 6]
        lst4 = [-2, 1, 2, 3, 3, 4, 5, 6]

        node = Node(lst_start)
        node.add_key_to_node(6)
        assert node.keys == lst1

        node.add_key_to_node(3)
        assert node.keys == lst2

        node.add_key_to_node(-2)
        assert node.keys == lst3

        node.add_key_to_node(3)
        assert node.keys == lst4

    def test_get_mid_index(self):
        assert Node([i for i in range(15)]).get_mid_index() == 7
        assert Node([i for i in range(22)]).get_mid_index() == 11

    def test_set_parent_for_children(self, children):
        child1, child2, child3 = children[:3]
        parent = Node([0, 5], [child1, child2, child3])
        parent.set_parent_for_children(parent)
        assert all(child.parent is parent for child in parent.children)

    def test_create_left_part(self, children):
        child1, child2, child3, child4, child5 = children

        no_child_odd_keys = Node([0, 5, 8])
        no_child_even_keys = Node([1, 21, 26, 37])
        assert no_child_odd_keys.create_l_part() == Node([0])
        assert no_child_even_keys.create_l_part() == Node([1, 21])

        parent1 = Node([2, 5, 8], [child1, child2, child3, child4])
        parent2 = Node([1, 21, 26, 37], [child1, child2, child3, child4, child5])
        assert parent1.create_l_part() == Node([2], [child1, child2])
        assert parent2.create_l_part() == Node([1, 21], [child1, child2, child3])

    def test_create_right_part(self, children):
        child1, child2, child3, child4, child5 = children

        no_child_odd_keys = Node([0, 5, 8])
        no_child_even_keys = Node([1, 21, 26, 37])
        assert no_child_odd_keys.create_r_part() == Node([8])
        assert no_child_even_keys.create_r_part() == Node([37])

        parent1 = Node([2, 5, 8], [child1, child2, child3, child4])
        parent2 = Node([1, 21, 26, 37], [child1, child2, child3, child4, child5])
        assert parent1.create_r_part() == Node([8], [child3, child4])
        assert parent2.create_r_part() == Node([37], [child4, child5])

    def test_get_left_neighbour(self, children):
        child1, child2, child3, child4, child5 = children

        parent1 = Node([2, 5, 8], [child1, child2, child3, child4])
        parent1.set_parent_for_children(parent1)

        assert child4.get_left_neighbour() == child3
        assert child1.get_left_neighbour() is None

    def test_get_right_neighbour(self, children):
        child1, child2, child3, child4, child5 = children
        assert child1.get_right_neighbour() is None

        parent1 = Node([2, 5, 8], [child2, child3, child4])
        parent1.set_parent_for_children(parent1)

        assert child3.get_right_neighbour() == child4
        assert child4.get_right_neighbour() is None

    def test_find_position_in_parent(self, children):
        parent = Node([i for i in range(5)], children[:4])
        parent.set_parent_for_children(parent)
        assert children[3].find_position_in_parent() == 3
        assert children[4].find_position_in_parent() is None

    def test_is_extreme_left_child(self, children):
        parent = Node([i for i in range(5)], children[:4])
        parent.set_parent_for_children(parent)
        assert not children[3].is_extreme_left_child()
        assert children[0].is_extreme_left_child()
        assert not children[4].is_extreme_left_child()

    def test_is_extreme_right_child(self, children):
        parent = Node([i for i in range(5)], children[:4])
        parent.set_parent_for_children(parent)
        assert children[3].is_extreme_right_child()
        assert not children[0].is_extreme_right_child()
        assert not children[4].is_extreme_right_child()
