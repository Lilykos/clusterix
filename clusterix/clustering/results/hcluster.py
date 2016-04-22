from scipy.cluster.hierarchy import to_tree


class HClusterTree(object):
    def __init__(self, Z):
        self.tree = to_tree(Z)

    def to_dict(self, id=None):
        if id is None:
            return self._add_node(self.tree, self.tree.dist)
        else:
            subtree = self.get_subtree(id)
            return self._add_node(subtree, subtree.dist)

    def get_subtree(self, id):
        return self._subtree(self.tree, id)

    def get_leaves(self, id=None):
        leaf_ids = lambda leaf: leaf.id
        return self.tree.pre_order(leaf_ids) if id is None \
            else self.get_subtree(id).pre_order(leaf_ids)

    @classmethod
    def _add_node(cls, node, dist):
        children = []
        if not node.is_leaf():
            left = node.get_left()
            right = node.get_right()

            children.append(cls._add_node(left, node.dist))
            children.append(cls._add_node(right, node.dist))

        return {
            'name': node.get_id(),
            'value': node.dist if node.dist > 0 else dist/2,
            'children': children
        }

    @classmethod
    def _subtree(cls, node, id):
        if node.id == id:
            return node
        else:
            if node.is_leaf():
                return False
            else:
                left = cls._subtree(node.left, id)
                right = cls._subtree(node.right, id)

        return left or right
