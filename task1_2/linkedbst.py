"""
File: linkedbst.py
Author: Ken Lambert
"""
import math
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log2


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return lst

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return 0

            return max(height1(top.left), height1(top.right)) + 1

        return height1(self._root)

    def isBalanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        if self.height() < 2 * math.log2(self._size + 1) - 1:
            return True

        return False

    def rangeFind(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        nodes_lst = []
        for node in self:
            nodes_lst.append(node)

        nodes_lst.sort()

        def insert_middle(tree, nodes_lst):
            if not nodes_lst:
                return

            middle = len(nodes_lst) // 2
            tree.add(nodes_lst[middle])
            insert_middle(tree, nodes_lst[: middle])
            insert_middle(tree, nodes_lst[middle + 1:])


        new_tree = LinkedBST()
        insert_middle(new_tree, nodes_lst)
        return new_tree

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:

        >>> tree = LinkedBST()
        >>> tree.add(5)
        >>> tree.add(3)
        >>> tree.add(1)
        >>> tree.add(4)
        >>> tree.add(8)
        >>> tree.add(10)
        >>> tree.add(12)
        >>> tree.add(0)
        >>> tree.add(13)
        >>> tree.successor(5)
        8
        >>> tree.successor(14)

        >>> tree.successor(11)
        12
        >>> tree.successor(2)
        3
        >>> tree.successor(8)
        10
        >>> tree.successor(0)
        1
        """

        def recurse(node):
            if node.left is None and node.right is None:
                if node.data > item:
                    return node.data
                else:
                    return None

            if node.left is not None:
                if node.left.data > item:
                    return recurse(node.left)

            if node.data > item:
                return node.data

            if node.right is not None:
                return recurse(node.right)
            else:
                return None

        return recurse(self._root)

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:


        >>> tree = LinkedBST()
        >>> tree.add(5)
        >>> tree.add(3)
        >>> tree.add(1)
        >>> tree.add(4)
        >>> tree.add(8)
        >>> tree.add(10)
        >>> tree.add(12)
        >>> tree.add(0)
        >>> tree.add(13)
        >>> tree.predecessor(5)
        4
        >>> tree.predecessor(14)
        13
        >>> tree.predecessor(11)
        10
        >>> tree.predecessor(2)
        1
        >>> tree.predecessor(8)
        5
        >>> tree.predecessor(0)

        """

        def recurse(node):
            if node.left is None and node.right is None:
                if node.data < item:
                    return node.data
                else:
                    return None
            if node.right is not None:
                if node.right.data < item:
                    return recurse(node.right)

            if node.data < item:
                return node.data

            if node.left is not None:
                return recurse(node.left)

            else:
                return None

        return recurse(self._root)

    def range_find(self, start_int, finish_int):
        """
        Supports an inorder traversal on a view of self.
         >>> tree = LinkedBST()
        >>> tree.add(5)
        >>> tree.add(3)
        >>> tree.add(1)
        >>> tree.add(4)
        >>> tree.add(8)
        >>> tree.add(10)
        >>> tree.add(12)
        >>> tree.add(0)
        >>> tree.add(13)
        >>> tree.range_find(5, 10)
        [5, 8, 10]
        >>> tree.range_find(2, 10)
        [3, 4, 5, 8, 10]
        """
        lst = list()
        if not self.isBalanced():
            self_balance = self.rebalance()

        else:
            self_balance = self

        def recurse(root, start, finish):
            if root is None:
                return

            if start < root.data:
                recurse(root.left, start, finish)

            if start <= root.data and finish >= root.data:
                lst.append(root.data)

            if finish > root.data:
                recurse(root.right, start, finish)

        recurse(self_balance._root, start_int, finish_int)
        return lst
