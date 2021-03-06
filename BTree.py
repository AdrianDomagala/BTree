from __future__ import annotations
from typing import Optional
from BTreeNode import *
from copy import deepcopy
from math import ceil


class BTree:
    def __init__(self, m=3, root=None):
        if root is None:
            root = BTreeNode()
        self.m = m
        self.root = root
        self.all_nodes_arr = []
        self.searching_path = None
        self.delete_steps = []
        self.last_used_node = None
        self.last_used_node_key_num = None

    def __eq__(self, other):
        if isinstance(other, BTree):
            return self.m == other.m and self.root == other.root
        else:
            return NotImplemented

    def add_key_in_range(self, start=0, end=16, step=1):
        for i in range(start, end, step):
            self.add_key(i)

    def add_key(self, key: int) -> list:
        if isinstance(key, int):
            node = self.find_node_to_insert(key)

            self.set_last_used_node(node, key)

            node.add_key_to_node(key)
            path = [deepcopy(self)]

            if self.is_it_full_node(node):
                path += self.split_node(node)
            return path

    def find_node_to_insert(self, key: int, node: BTreeNode = None) -> BTreeNode:
        if node is None:
            node = self.root
        self.searching_path = []
        return self.find_node_to_insert_util(key, node)

    def set_last_used_node(self, node, key_num):
        self.last_used_node = node
        self.last_used_node_key_num = node.find_index_to_insert(key_num)

    def get_last_used_node(self):
        return self.last_used_node, self.last_used_node_key_num

    def find_node_to_insert_util(self, key: int, node: BTreeNode) -> BTreeNode:
        self.searching_path.append(node)
        if node.is_leaf():
            return node
        else:
            index = node.find_index_to_insert(key)
            return self.find_node_to_insert_util(key, node.children[index])

    def is_it_full_node(self, node: BTreeNode) -> bool:
        if node is None:
            return False
        return node.number_of_keys() > self.max_number_of_keys()

    def max_number_of_keys(self):
        return self.m - 1

    def split_node(self, node: BTreeNode) -> list:
        l_child = node.create_l_part()
        r_child = node.create_r_part()
        mid_key = node.get_mid_key()

        if self.is_it_root_node(node):
            self.set_root(BTreeNode([mid_key], [l_child, r_child]))
        else:
            node.get_parent().insert_children(mid_key, [l_child, r_child])
        path = [deepcopy(self)]

        if self.is_it_full_node(node.get_parent()):
            path += self.split_node(node.get_parent())
        return path

    def is_it_root_node(self, node: BTreeNode) -> bool:
        return self.root is node

    def split_root(self):
        return self.split_node(self.root)

    def set_root(self, root: BTreeNode):
        self.root = root

    def show(self):
        self.get_all_nodes()
        tree_text = ''
        for level in self.all_nodes_arr:
            for node in level:
                tree_text += node.show_node()
            tree_text += '\n'
        print(tree_text)
        return tree_text

    def get_all_nodes(self):
        self.all_nodes_arr = []
        self.get_all_nodes_util(self.root)
        return self.all_nodes_arr

    def get_all_nodes_util(self, node: BTreeNode, level: int = 0):
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
        return str(id(self)) + '\n' + tree_text

    def show_complex_with_coordinates(self):
        self.get_all_nodes()
        tree_text = ''
        for level in self.all_nodes_arr:
            for node in level:
                tree_text += str(node) + str(node.get_coordinates().values()) + '\n'
            tree_text += '\n\n'
        print(str(id(self)) + '\n' + tree_text)
        return str(id(self)) + '\n' + tree_text

    def search(self, key: int, node: BTreeNode = None):
        if node is None:
            node = self.root
        self.searching_path = []
        return self.search_util(key, node)

    def search_util(self, key: int, node: BTreeNode) -> (BTreeNode, int):
        self.searching_path.append(node)
        for i, k in enumerate(node.keys):
            if k == key:
                return node, i
            elif key < k:
                if node.is_leaf():
                    return None, None
                return self.search_util(key, node.children[i])
        if node.is_leaf():
            return None, None
        return self.search_util(key, node.children[-1])

    def get_searching_path(self):
        return self.searching_path

    def delete_all_keys(self, key: int):
        node, index = self.search(key)
        if node is not None:
            self.delete_key_util(index, node)
            self.delete_all_keys(key)

    def delete_key(self, key: int):
        node, index = self.search(key)
        if node is not None:
            self.delete_key_util(index, node)

    def delete_key_util(self, index: int, node: BTreeNode):
        if node.is_leaf():
            self.delete_key_form_leaf(node, index)
        else:
            self.delete_delimiter(node, index)

    def delete_key_form_leaf(self, node, index):
        node.keys.pop(index)
        self.delete_steps.append(deepcopy(self))
        self.supply_node_if_it_needs(node)

    def supply_node_if_it_needs(self, node):
        if not self.is_node_have_enough_keys(node):
            if self.is_it_root_node(node) and not self.root.is_leaf():
                self.delete_root()
            else:
                self.supply_node(node)
                self.delete_steps.append(deepcopy(self))

    def delete_delimiter(self, node, index):
        if self.key_can_be_swap(node, index):
            leaf = self.swap_key_in_delimiter(node, index)
            self.delete_steps.append(deepcopy(self))
            self.supply_node_if_it_needs(leaf)
        else:
            self.delete_by_merge(node, index)

    def key_can_be_swap(self, node: BTreeNode, index: int) -> bool:
        return self.key_can_be_swap_by_left_descendant(node, index) \
               or self.key_can_be_swap_by_right_descendant(node, index)

    def key_can_be_swap_by_left_descendant(self, node, index):
        if child := node.get_child_at(index):
            return child.number_of_keys() > self.min_number_of_keys()
        return False

    def key_can_be_swap_by_right_descendant(self, node, index):
        if child := node.get_child_at(index + 1):
            return child.number_of_keys() > self.min_number_of_keys()
        return False

    def swap_key_in_delimiter(self, node, index):
        if self.key_can_be_swap_by_left_descendant(node, index):
            return node.swap_key_from_extreme_right_leaf(index)
        else:
            return node.swap_key_from_extreme_left_leaf(index)

    def delete_by_merge(self, node, index):
        if left_child := node.get_child_at(index):
            left_child.merge_with_right_neighbour(index)
            self.delete_steps.append(deepcopy(self))
            self.supply_node_if_it_needs(node)
            self.delete_key_util(self.min_number_of_keys(), node.get_child_at(index))

    def is_node_have_enough_keys(self, node):
        if self.is_it_root_node(node):
            if node.is_leaf():
                return True
            return node.number_of_keys() >= 1
        return node.number_of_keys() >= self.min_number_of_keys()

    def min_number_of_keys(self):
        return self.min_number_of_children() - 1

    def min_number_of_children(self):
        return ceil(self.m / 2)

    def supply_node(self, node: BTreeNode):
        if self.can_be_supply_by_left_neighbour(node):
            return node.move_key_form_left_neighbour()
        elif self.can_be_supply_by_right_neighbour(node):
            return node.move_key_form_right_neighbour()
        elif self.can_be_merge_with_left_neighbour(node):
            return self.merge_node_with_left_neighbour(node)
        elif self.can_be_merge_with_right_neighbour(node):
            return self.merge_node_with_right_neighbour(node)

    def can_be_supply_by_left_neighbour(self, node):
        if left_neighbour := node.get_left_neighbour():
            return self.can_take_key_from_node(left_neighbour)

    def can_take_key_from_node(self, node):
        return node.number_of_keys() > self.min_number_of_keys()

    def can_be_supply_by_right_neighbour(self, node):
        if right_neighbour := node.get_right_neighbour():
            return self.can_take_key_from_node(right_neighbour)

    def can_be_merge_with_left_neighbour(self, node):
        if left_neighbour := node.get_left_neighbour():
            return self.is_node_can_be_merge(left_neighbour)

    def is_node_can_be_merge(self, node):
        return node.number_of_keys() <= self.min_number_of_keys()

    def can_be_merge_with_right_neighbour(self, node):
        if right_neighbour := node.get_right_neighbour():
            return self.is_node_can_be_merge(right_neighbour)

    def merge_node_with_left_neighbour(self, node):
        node.merge_with_left_neighbour()
        self.delete_steps.append(deepcopy(self))
        return self.supply_node_if_it_needs(node.get_parent())

    def merge_node_with_right_neighbour(self, node):
        node.merge_with_right_neighbour()
        self.delete_steps.append(deepcopy(self))
        return self.supply_node_if_it_needs(node.get_parent())

    def delete_root(self):
        new_root = self.root.children[0]
        self.root = new_root
        self.delete_steps.append(deepcopy(self))

    def get_root(self):
        return self.root

    def get_height(self):
        return self.root.get_height()

    def get_deleting_path(self):
        return self.delete_steps if self.delete_steps is not None else []

    def set_deleting_path(self, delete_path):
        self.delete_steps = delete_path


if __name__ == '__main__':
    tree = BTree(m=3)
