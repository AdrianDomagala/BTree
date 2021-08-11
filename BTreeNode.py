from __future__ import annotations
from typing import Optional


class BTreeNode:
    """
    The BTreeNode object contains list of keys, list of children and reference to parent node.

    Args:
        keys (list): list of keys where any key is a integer number
        children (list): list of children any child is a another Node object
        parent (BTreeNode): reference to another Node object

    Attributes:
        keys (list): sorted list of keys where any key is a integer number
        children (list): list of children any child is a another Node object
        parent (BTreeNode): reference to another Node object
    """

    def __init__(self, keys: list = None, children: list = None, parent: BTreeNode = None):
        if keys is None:
            keys = []

        if children is None:
            children = []
        else:
            for child in children:
                if isinstance(child, BTreeNode):
                    child.set_parent(self)
                else:
                    children.remove(child)

        self.keys = keys
        self.children = children
        self.parent = parent
        self.x_up_l = None
        self.y_up_l = None
        self.x_d_r = None
        self.y_d_r = None

    def __str__(self):
        """Return string representation of Node object."""
        return f'Id: {id(self)} \t ' \
               f'keys: {self.keys} \t ' \
               f'children: {[id(child) for child in self.children]} \t ' \
               f'parent id: {id(self.parent)}'

    def __eq__(self, other: BTreeNode):
        """Return True if both node object are equal else return False."""
        if isinstance(other, BTreeNode):
            if self.is_leaf() and other.is_leaf():
                return self.keys == other.keys
            return self.keys == other.keys \
                   and self.number_of_children() == other.number_of_children() \
                   and self.all_children_are_equal(other)

    def all_children_are_equal(self, other: BTreeNode):
        """
        Function to compare two Node object.
        Args:
            other (BTreeNode): Node object to compare with self
        Returns:
            bool: True if all children of compared nodes are equal else False
        """
        for child, other_child in zip(self.children, other.children):
            if not child == other_child:
                return False
        return True

    def show_node(self):
        """
        Build str showing all node keys.
        Returns:
            string: str
        """
        return '|\t' + '\t|\t'.join(str(k) for k in self.keys) + '\t|'

    def is_leaf(self):
        """
        Check if node is leaf (have no child).
        Returns:
            bool: True if node has no child else False
        """
        return not bool(self.children)

    def find_index_to_insert(self, key: int) -> int:
        """
        Finds specific index to insert key to the node so as keys stay in order.
        Args:
            key (int): element to insert
        Returns:
            int: proper list index, where key should be insert
        """
        for i, k in enumerate(self.keys):
            if k >= key:
                return i
        return self.number_of_keys()

    def add_key_to_node(self, key: int):
        """
        Add key to node keys list.
        Args:
            key (int): element to add
        Returns:
            None
        """
        if isinstance(key, int):
            index = self.find_index_to_insert(key)
            self.keys.insert(index, key)

    def get_mid_index(self) -> int:
        """Return middle index, if number of indexes is odd round it down."""
        return self.number_of_keys() // 2

    def get_mid_key(self) -> int:
        """Return key at middle index."""
        return self.keys[self.get_mid_index()]

    def create_l_part(self) -> BTreeNode:  # previous name create_l_child
        """
        Creates new Node object containing all keys from 0 to middle index and all children from 0 to middle index + 1.
        Returns:
            BTreeNode: New created Node object
        """
        mid_index = self.get_mid_index()
        keys = self.keys[:mid_index]
        children = self.children[:mid_index + 1]
        return BTreeNode(keys, children, self.parent)

    def create_r_part(self) -> BTreeNode:
        """
        Creates new Node object containing all keys from middle index + 1  to the last one and all children from
        middle index + 1 to the last index.
        Returns:
            BTreeNode: New created Node object
        """
        mid_index = self.get_mid_index()
        keys = self.keys[mid_index + 1:]
        children = self.children[mid_index + 1:]
        return BTreeNode(keys, children, self.parent)

    def set_parent(self, parent: BTreeNode):
        """Set parent"""
        self.parent = parent

    def get_parent(self):
        return self.parent

    def set_parent_for_children(self, parent: BTreeNode = None):
        """
        Set parent for all children of current node.
        Args:
            parent (BTreeNode): parent to set
        """
        if parent is None:
            parent = self
        for child in self.children:
            child.set_parent(parent)

    def number_of_keys(self) -> int:
        """Return number of keys in self.keys"""
        return len(self.keys)

    def number_of_children(self) -> int:
        """Return number of children in self.children"""
        return len(self.children)

    def get_left_neighbour(self) -> Optional[BTreeNode]:
        """
        Get left_neighbour if this is possible. Left_neighbour is defined as node right before current node
        in children list in parent.
        Returns:
            BTreeNode: left_neighbour
        """
        index = self.find_position_in_parent()
        if index is None or self.is_extreme_left_child() or self.parent.number_of_children() < 2:
            return None
        return self.parent.children[index - 1]

    def get_right_neighbour(self) -> Optional[BTreeNode]:
        """
        Get right_neighbour if this is possible. Right_neighbour is defined as node right after current node
        in children list in parent.
        Returns:
            BTreeNode: right_neighbour
        """
        index = self.find_position_in_parent()
        if index is None or self.is_extreme_right_child() or self.parent.number_of_children() < 2:
            return None
        return self.parent.children[index + 1]

    def find_position_in_parent(self) -> Optional[int]:
        """
        Finds index which is parent.children[index] == self
        Returns:
            int: index
        """
        if self.have_parent():
            for i, child in enumerate(self.parent.children):
                if child is self:  # here is instead of ==
                    return i
        return None

    def is_extreme_left_child(self) -> bool:
        """
        Check if node is extreme left child, it means that parent.children[0] == node
        Returns:
            bool: True if node is extreme left child else False
        """
        if self.have_parent():
            return self is self.parent.children[0]
        return False

    def is_extreme_right_child(self) -> bool:
        """
        Check if node is extreme left child, it means that node is the last one in list of children in parent node.
        Returns:
            bool: True if node is extreme right child else False
        """
        if self.have_parent():
            return self is self.parent.children[-1]
        return False

    def have_parent(self):
        """Return True if node has parent else False"""
        return self.parent is not None

    def is_left_neighbour(self, neighbour: BTreeNode) -> bool:
        return True if self.get_left_neighbour() is neighbour else False

    def is_right_neighbour(self, neighbour: BTreeNode) -> bool:
        return True if self.get_right_neighbour() is neighbour else False

    def get_keys(self):
        return self.keys

    def get_children(self):
        return self.children

    def get_child_at(self, index):
        if 0 <= index < len(self.children):
            return self.children[index]
        return False

    def get_first_child(self) -> BTreeNode:
        return self.children[0]

    def get_last_child(self) -> BTreeNode:
        return self.children[-1]

    def have_any_keys(self):
        return self.number_of_keys()

    def have_any_child(self):
        return self.number_of_children()

    def set_coordinates(self, coordinates):
        if coordinates := self.check_coordinates(coordinates):
            self.x_up_l = int(coordinates[0])
            self.y_up_l = int(coordinates[1])
            self.x_d_r = int(coordinates[2])
            self.y_d_r = int(coordinates[3])

    @staticmethod
    def check_coordinates(coordinates):
        if len(coordinates) == 4:
            if coordinates[0] > coordinates[2]:
                coordinates[0], coordinates[2] = coordinates[2], coordinates[0]
            if coordinates[1] > coordinates[3]:
                coordinates[1], coordinates[3] = coordinates[3], coordinates[1]
            return coordinates
        return False

    def get_coordinates(self):
        return {
            'x_up_l': self.x_up_l,
            'y_up_l': self.y_up_l,
            'x_d_r': self.x_d_r,
            'y_d_r': self.y_d_r,
        }

    def get_middle_x_coordinates(self):
        return (self.x_d_r + self.x_up_l) / 2

    def get_x_span(self):
        return self.x_d_r - self.x_up_l

    def get_middle_y_coordinates(self):
        return (self.y_d_r + self.y_up_l) / 2

    def get_top_coordinates(self) -> int:
        return self.y_up_l

    def get_coordinate_xr(self) -> int:
        return self.x_d_r

    def get_coordinate_xl(self) -> int:
        return self.x_up_l

    def get_coordinate_yu(self):
        return self.y_up_l

    def get_coordinate_yd(self):
        return self.y_d_r

    def add_coordinates(self, coordinates):
        if len(coordinates) == 4:
            self.x_up_l += coordinates[0]
            self.y_up_l += coordinates[1]
            self.x_d_r += coordinates[2]
            self.y_d_r += coordinates[3]

    def is_coordinates_set(self):
        return all(self.get_coordinates().values())

    def get_height(self):
        if self.have_any_keys() or self.have_any_child():
            if self.have_any_child():
                return self.children[0].get_height_util(1)
            return 1
        return 0

    def get_height_util(self, current_height):
        if self.have_any_child():
            return self.children[0].get_height_util(current_height + 1)
        return current_height + 1

    def insert_children(self, index: int, children: list):
        insert_index = self.find_index_to_insert(index)
        self.add_key_to_node(index)
        self.children[insert_index:insert_index + 1] = children

    def move_key_form_left_neighbour(self):
        if left_neighbour := self.get_left_neighbour():
            key = left_neighbour.keys.pop()
            index = left_neighbour.find_position_in_parent()
            self.keys.insert(0, self.parent.keys[index])
            self.parent.keys[index] = key

            if not self.is_leaf():
                self.children.insert(0, left_neighbour.children.pop())

    def move_key_form_right_neighbour(self):
        if right_neighbour := self.get_right_neighbour():
            key = right_neighbour.keys.pop(0)
            index = self.find_position_in_parent()
            self.keys.append(self.parent.keys[index])
            self.parent.keys[index] = key

            if not self.is_leaf():
                self.children.append(right_neighbour.children.pop(0))

    def merge_with_left_neighbour(self):
        if left_neighbour := self.get_left_neighbour():
            index = left_neighbour.find_position_in_parent()
            key = self.parent.keys.pop(index)
            self.parent.children[index:index+2] = [BTreeNode(
                keys=left_neighbour.keys + [key] + self.keys,
                children=left_neighbour.children + self.children,
                parent=self.parent
            )]

    def merge_with_right_neighbour(self, index=None):
        if right_neighbour := self.get_right_neighbour():
            if index is None:
                index = self.find_position_in_parent()
            key = self.parent.keys.pop(index)
            self.parent.children[index:index+2] = [BTreeNode(
                keys=self.keys + [key] + right_neighbour.keys,
                children=self.children + right_neighbour.children,
                parent=self.parent
            )]

    def swap_key_from_extreme_right_leaf(self, index):
        node = self.get_child_at(index).swap_key_from_leaf(-1)
        self.keys[index] = node.keys.pop(-1)
        return node

    def swap_key_from_extreme_left_leaf(self, index):
        node = self.get_child_at(index+1).swap_key_from_leaf(0)
        self.keys[index] = node.keys.pop(0)
        return node

    # def swap_key_from_leaf(self, index: int) -> BTreeNode:
    #     node = self.children[index].swap_key_from_leaf_util()
    #     self.keys[index] = node.keys.pop()
    #     return node

    def swap_key_from_leaf(self, index) -> BTreeNode:
        if self.is_leaf():
            return self
        else:
            return self.children[index].swap_key_from_leaf(index)


if __name__ == '__main__':
    print('Hello ', type(BTreeNode()))
