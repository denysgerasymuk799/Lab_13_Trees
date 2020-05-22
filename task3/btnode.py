class BSTNode:
    """Represents a node for a linked binary search tree."""

    def __init__(self, state, node_id, left=None, right=None):
        self.left = left
        self.right = right
        self.board = state
        self._id = node_id

    def __str__(self):
        return str(self.board)