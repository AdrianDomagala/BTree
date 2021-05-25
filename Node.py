class Node:
    """
    The Node object contains list of keys, list of children and reference to parent node.

    Args:
        keys (list): list of keys where any key is a integer number
        children (list): list of children any child is a another Node object
        parent (Node): reference to another Node object

    Attributes:
        keys (list): sorted list of keys where any key is a integer number
        children (list): list of children any child is a another Node object
        parent (Node): reference to another Node object
    """

    def __init__(self, keys=None, children=None, parent=None):
        if children is None:
            children = []
        if keys is None:
            keys = []
        self.keys = keys
        self.children = children
        self.parent = parent

    def __str__(self):
        """Return string representation of Node object."""
        return f'Id: {id(self)} \t ' \
               f'keys: {self.keys} \t ' \
               f'children: {[id(child) for child in self.children]} \t ' \
               f'parent id: {id(self.parent)}'

    def __eq__(self, other):
        """Return True if both node object are equal else return False."""
        if isinstance(other, Node):
            if self.is_leaf() and other.is_leaf():
                return self.keys == other.keys
            return self.keys == other.keys \
                   and self.number_of_children() == other.number_of_children() \
                   and self.all_children_are_equal(other)

    def all_children_are_equal(self, other):
        """
        Function to compare two Node object.
        Args:
            other (Node): Node object to compare with self
        Returns:
            bool: True if all children of compare nodes are equal else False
        """
        for child, other_child in zip(self.children, other.children):
            if not child == other_child:
                return False
        return True

    def show_node(self):
        """
        Build str (string) showing all node keys.
        Returns:
            string: str
        """
        return '|\t' + '\t|\t'.join(str(k) for k in self.keys) + '\t|'

    def is_leaf(self):
        """
        Check if node have no child.
        Returns:
            bool: True if has no children else False
        """
        return not bool(self.children)

    def find_index_to_insert(self, key):
        """
        Finds specific index to insert key so as to node keys stay in order.
        Args:
            key (int): element to insert
        Returns:
            int: proper list index, where key should be insert
        """
        for i, k in enumerate(self.keys):
            if k >= key:
                return i
        return self.number_of_keys()

    def add_key_to_node(self, key):
        """
        Add key to node keys.
        Args:
            key (int): element to add
        Returns:
            None
        """
        if isinstance(key, int):
            index = self.find_index_to_insert(key)
            self.keys.insert(index, key)

    def get_mid_index(self):
        """Return middle index, if number of indexes is odd round it down."""
        return self.number_of_keys() // 2

    def get_mid_key(self):
        """Return key at middle index."""
        return self.keys[self.get_mid_index()]

    def create_l_part(self):            #previous name create_l_child
        """
        Creates new Node object containing all keys from 0 to middle index and all children from 0 to middle index + 1.
        Returns:
            Node: New created Node object
        """
        mid_index = self.get_mid_index()
        keys = self.keys[:mid_index]
        children = self.children[:mid_index + 1]
        return Node(keys, children)

    def create_r_part(self):
        """
        Creates new Node object containing all keys from middle index + 1  to the last one and all children from
        middle index + 1 to the last index.
        Returns:
            Node: New created Node object
        """
        mid_index = self.get_mid_index()
        keys = self.keys[mid_index + 1:]
        children = self.children[mid_index + 1:]
        return Node(keys, children)

    def set_parent(self, parent):
        """Set parent"""
        self.parent = parent

    def set_parent_for_children(self, parent):
        """
        Set parent for all children of current node.
        Args:
            parent (Node): parent to set
        Returns:
            None
        """
        for child in self.children:
            child.set_parent(parent)

    def number_of_keys(self):
        """Return number of keys in self.keys"""
        return len(self.keys)

    def number_of_children(self):
        """Return number of children in self.children"""
        return len(self.children)

    def get_left_neighbour(self):
        """
        Get left_neighbour if this is possible. Left_neighbour is defined as node right before current node
        in children list in parent.
        Returns:
            Node: left_neighbour
        """
        index = self.find_position_in_parent()
        if index is None or self.is_extreme_left_child() or self.parent.number_of_children() < 2:
            return None
        return self.parent.children[index - 1]

    def get_right_neighbour(self):
        """
        Get right_neighbour if this is possible. Right_neighbour is defined as node right after current node
        in children list in parent.
        Returns:
            Node: right_neighbour
        """
        index = self.find_position_in_parent()
        if index is None or self.is_extreme_right_child() or self.parent.number_of_children() < 2:
            return None
        return self.parent.children[index + 1]

    def find_position_in_parent(self):
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

    def is_extreme_left_child(self):
        """
        Check if node is extreme left child, it means that parent.children[0] == node
        Returns:
            bool: True if node is extreme left child else False
        """
        if self.have_parent():
            return self is self.parent.children[0]
        return False

    def is_extreme_right_child(self):
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

    # is it needed?
    def at_left_from_parent(self):
        return self.find_position_in_parent() < self.parent.get_mid_index() + 1


if __name__ == '__main__':
    print('Hello ', type(Node()))
