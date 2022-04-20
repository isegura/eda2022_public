from bst import BinarySearchTree
from bintree import BinaryNode

from slistHT import SList
import sys

class MyBST(BinarySearchTree):

    def get_parent(self, node):
        if node is None or self._root is None:
            return None

        if node == self._root:
            return None

        # we can use SList with tail and head
        list_nodes = SList()
        list_nodes.add_last(self._root)

        while len(list_nodes) > 0:  # loop will be executed the size of tree: n
            parent = list_nodes.remove_first()  # O(1)
            if parent.left == node or parent.right == node:
                return parent

            if parent.left is not None and node.elem < parent.elem:
                list_nodes.add_last(parent.left)  # O(1)
            if parent.right is not None and node.elem > parent.elem:
                list_nodes.add_last(parent.right)  # O(1)

        print('Not found ', node.elem)
        return None

    def check_cousins(self, x: int, y: int) -> bool:
        """returns True if x and y are cousins, and False eoc. Problema Examen Mayo 2020"""
        node_x = self.search(x)
        node_y = self.search(y)
        if node_x is None or node_y is None:
            return False

        parent_x = self.get_parent(node_x)
        parent_y = self.get_parent(node_y)

        if parent_x == parent_y:
            return False

        grand_parent_x = self.get_parent(parent_x)
        grand_parent_y = self.get_parent(parent_y)
        if grand_parent_x != grand_parent_y:
            return False

        return True

    def lwc(self, x: int, y: int) -> BinaryNode:
        """returns the lowest common ancestor of x and b, Junio 2020"""
        node_x = self.search(x)
        node_y = self.search(y)
        if node_x is None or node_y is None:
            return None
        return self._lwc(self._root, node_x, node_y)

    def _lwc(self, node: BinaryNode, node_a: BinaryNode, node_b: BinaryNode) -> BinaryNode:
        if node is None:
            return None

        if node_a.elem < node.elem and node_b.elem < node.elem:
            return self._lwc(node.left, node_a, node_b)

        if node_a.elem > node.elem and node_b.elem > node.elem:
            return self._lwc(node.right, node_a, node_b)

        return node.elem

    def is_zig_zag(self) -> bool:
        """returns True if the tree is a zizag-shaped tree, False eoc"""
        return self._is_zig_zag(self._root)

    def _is_zig_zag(self, node: BinaryNode) -> bool:
        if node is None:
            return True
        if node.left and node.right:
            return False

        parent = self.get_parent(node)

        if parent and parent.left is node and node.left is not None:
            return False

        if parent and parent.right is node and node.right is not None:
            return False

        return self._is_zig_zag(node.left) and self._is_zig_zag(node.right)

    def is_same_shape(self, other_tree: "MyBST") -> bool:
        """returns True if both trees have the same shape, False e.o.c"""
        if other_tree is None:
            return False

        return self._is_same_shape(self._root, other_tree._root)

    def _is_same_shape(self, node_1: BinaryNode, node_2: BinaryNode) -> bool:
        """returns True if both nodes have the same shape, False e.o.c"""
        if node_1 is None and node_2 is None:
            return True

        if node_1 is not None and node_2 is not None:
            return self._is_same_shape(node_1.left, node_2.left) and self._is_same_shape(node_1.right, node_2.right)

        return False

    def closest(self, value: int) -> int:
        """returns the closest element to value """
        return self._closest(self._root, value)

    def _closest(self, node: BinaryNode, value: int) -> int:
        if node is None:
            return None

        if node.elem == value:
            return value

        child = node.left if value < node.elem else node.right

        if not child:
            return node.elem

        closest_child = self._closest(child, value)
        if abs(value - node.elem) < abs(value - closest_child):
            return node.elem
        else:
            return closest_child

    def is_bst(self) -> bool:
        """checks if the tree is bst"""
        return self._is_bst(self._root, -sys.maxsize, sys.maxsize)

    def _is_bst(self, node: BinaryNode, min_value: int, max_value: int) -> bool:
        if node is None:
            return True

        if node.elem > min_value or node.elem < max_value:
            return False

        return self._is_bst(node.left, min_value, node.elem - 1) and self._is_bst(node.right, node.elem + 1, max_value)

    # def _is_bst(self, node: BinaryNode) -> bool:
    #     """checks if the node is bst"""
    #     if node is None:
    #         return True
    #     result_left = True
    #     if node.left:
    #         result_left = node.left.elem < node.elem and self._is_bst(node.left)
    #     result_right = True
    #     if node.right:
    #         result_right = node.right.elem > node.elem and self._is_bst(node.right)
    #
    #     return result_left and result_left

    def sum_tree(self):
        """change the value in each node to sum of all the values in the nodes in the left subtree including its own."""
        self._sum_tree(self._root)

    def _sum_tree(self, node):
        # Base cases
        if node is None:
            return 0
        print("changing: ", node.elem)
        if node.left is None and node.right is None:
            return node.elem

        # Update left and right subtrees
        left_sum = self._sum_tree(node.left)
        right_sum = self._sum_tree(node.right)

        # Add right_sum to current node
        node.elem += left_sum

        # Return sum of values under root
        return node.elem + right_sum


if __name__ == "__main__":

    tree = MyBST()

    values = [25, 20, 36, 10, 22, 30, 40, 5, 12, 28, 38, 48]
    tree = MyBST()
    for x in values:
        tree.insert(x)

    tree.draw()
    print('5 and 15 are cousins?:', tree.check_cousins(5, 15))  # False, 15 does not exist
    print('5 and 22 are cousins?:', tree.check_cousins(5, 22))  # False, have different levels
    print('5 and 22 are cousins?:', tree.check_cousins(5, 22))  # False, have different levels
    print('36 and 48 are cousins?:', tree.check_cousins(36, 48))  # False, have different levels
    print('5 and 12 are cousins?:', tree.check_cousins(5, 12))  # False, are siblings
    print('20 and 36 are cousins?:', tree.check_cousins(20, 36))  # False, are siblings
    print('10 and 22 are cousins?:', tree.check_cousins(10, 22))  # False, are siblings
    print('5 and 28 are cousins?:', tree.check_cousins(5, 28))  # False, same level, their parents are not siblings
    print('12 and 28 are cousins?:', tree.check_cousins(12, 28))  # False, same level, their parents are not siblings
    print('10 and 30 are cousins?:', tree.check_cousins(10, 30))  # True, are cousins
    print('10 and 40 are cousins?:', tree.check_cousins(10, 30))  # True, are cousins
    print('22 and 30 are cousins?:', tree.check_cousins(22, 30))  # True, are cousins
    print('22 and 40 are cousins?:', tree.check_cousins(22, 40))  # True, are cousins
    print('28 and 38 are cousins?:', tree.check_cousins(28, 38))  # True, are cousins
    print('28 and 48 are cousins?:', tree.check_cousins(28, 48))  # True, are cousins

    print(tree.lwc(48, 38), 40)
    print(tree.lwc(48, 28), 36)
    print(tree.lwc(48, 30), 36)
    print(tree.lwc(40, 30), 36)
    print(tree.lwc(28, 22), 50)
    print(tree.lwc(22, 5), 20)

    print(tree.is_zig_zag())

    values = [50, 30, 40, 35]
    tree = MyBST()
    for x in values:
        tree.insert(x)
    tree.draw()

    print('is_zig_zag:', tree.is_zig_zag())

    values = [50, 80, 60, 65]
    tree = MyBST()
    for x in values:
        tree.insert(x)
    tree.draw()

    print('is_zig_zag:', tree.is_zig_zag())

    values = [50, 80, 60, 55, 65]
    tree = MyBST()
    for x in values:
        tree.insert(x)
    tree.draw()

    print('is_zig_zag:', tree.is_zig_zag())

    values = [50, 40, 80, 60, 55, 65]
    tree = MyBST()
    for x in values:
        tree.insert(x)
    tree.draw()

    print('is_zig_zag:', tree.is_zig_zag())

    values = [3, 5, 4, 2]

    tree = MyBST()
    for x in values:
        tree.insert(x)
    tree.draw()
    tree.sum_tree()
    tree.draw()
