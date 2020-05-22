from btnode import BSTNode
from abstractcollection import AbstractCollection


class BTree(AbstractCollection):
    def __init__(self, root, computer_mark, human_mark, sourceCollection=None):
        """Sets the initial state of self, which includes the
                contents of sourceCollection, if it's present."""
        self._root = root
        self.computer_mark = computer_mark
        self.human_mark = human_mark
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        AbstractCollection.__init__(self, sourceCollection)

    def add(self, coords, game_step):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node, node_id):
            if node.left is None:
                node.left = BSTNode(state, node_id)
            else:
                node_id += 1
                recurse(node.left, node_id)
            # New item is greater or equal,
            # go right until spot is found
            if node.right is None:
                node.right = BSTNode(state, node_id)
            else:
                node_id += 1
                recurse(node.right, node_id)

        state = self.board
        state[coords[0]][coords[1]] = self.computer_mark

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(state, game_step)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root, game_step)
