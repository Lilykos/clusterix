from scipy.cluster.hierarchy import to_tree


def scatterplot(coords, labels, n_clusters, centroids=None):
    """Get a dictionary that will be converted to json, and contains all the scatterplot visualization data."""
    nodes = []
    for cluster in xrange(n_clusters):
        for i in xrange(len(labels)):
            # Add nodes
            if labels[i] == cluster:
                nodes.append({
                    'x': coords[i][0],
                    'y': coords[i][1],
                    'cluster': cluster,
                    'isCentroid': False,
                    'id': i
                })

        # For each label, also add the centroid
        if centroids is not None:
            nodes.append({
                'x': centroids[cluster][0],
                'y': centroids[cluster][1],
                'cluster': cluster,
                'isCentroid': True
            })

    return {
        'k_num': n_clusters,
        'nodes': nodes,
    }


class HClusterTree(object):
    """A class that provides useful methods for hierarchical clustering, tree manipulations, etc."""
    def __init__(self, Z):
        self.tree = to_tree(Z)

    def to_dict(self, id=None):
        """Return a dict representation of the h-clustered tree."""
        if id is None:
            return self._add_node(self.tree, self.tree.dist)
        else:
            subtree = self.get_subtree(id)
            return self._add_node(subtree, subtree.dist)

    def get_subtree(self, id):
        """Return a subtree starting from the node with the provided id."""
        return self._subtree(self.tree, id)

    def get_leaves(self, id=None):
        """Get the ids of all the leaves under a specific subtree/whole tree."""
        leaf_ids = lambda leaf: leaf.id
        return self.tree.pre_order(leaf_ids) if id is None \
            else self.get_subtree(id).pre_order(leaf_ids)

    @classmethod
    def _add_node(cls, node, dist):
        """Recursively create a dictionary from the provided tree."""
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
        """Traverses the tree recursively, and returns the subtree, starting from the node with the provided id."""
        if node.id == id:
            return node
        else:
            if node.is_leaf():
                return False
            else:
                left = cls._subtree(node.left, id)
                right = cls._subtree(node.right, id)

        return left or right