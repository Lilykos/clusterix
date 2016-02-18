from functools import reduce
from scipy.cluster.hierarchy import to_tree


class D3Converter():

    def __init__(self, labels):
        # Create a dict with ids/names to be used in newick or whatever else
        self.ids_to_names = {}
        self.id2name = dict(zip(range(len(labels)), labels))

    def _add_node(self, node, parent):
        # First create the new node and append it to its parent's children
        new_node = dict(children=[],
                        value=node.dist if node.dist > 0 else 10,
                        node_id=node.id
                        )
        parent["children"].append(new_node)

        # Recursively add the current node's children
        if node.left:
            self._add_node(node.left, new_node)
        if node.right:
            self._add_node(node.right, new_node)

    def _label_tree(self, node):
        # If not a leaf (has children), flatten all the leaves in the node's subtree
        # If it is a leaf, then we have its name
        if node["children"]:
            leaf_names = reduce(lambda ls, c: ls + self._label_tree(c), node["children"], [])
        else:
            leaf_names = [self.id2name[node["node_id"]]]

        # Labeling convention: "-"-separated leaf names
        node["name"] = name = "-".join(sorted(map(str, leaf_names)))
        self.ids_to_names[node['node_id']] = name

        # Delete the node id since we don't need it anymore and
        # it makes for cleaner JSON
        # del node["node_id"]

        return leaf_names

    def get_d3_json(self, linkage, root_name):
        # Initialize nested dictionary for d3, then recursively iterate through tree
        tree = to_tree(linkage, rd=False)
        d3_dendro = dict(children=[], name=root_name, node_id="Root")  # value = 0

        self._add_node(tree, d3_dendro)
        self._label_tree(d3_dendro["children"][0])

        return d3_dendro