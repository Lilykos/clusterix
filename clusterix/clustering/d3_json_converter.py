from scipy.cluster.hierarchy import to_tree


def get_d3_json(linkage, labels, root_name):
    # Create a dict with ids/names to be used in newick or whatever else
    ids_to_names = {}
    id2name = dict(zip(range(len(labels)), labels))

    # Initialize nested dictionary for d3, then recursively iterate through tree
    tree = to_tree(linkage, rd=False)
    d3_dendro = dict(children=[], name=root_name, node_id="Root")  # value = 0

    def _add_node(node, parent):
        # First create the new node and append it to its parent's children
        new_node = dict(children=[],
                        value=node.dist if node.dist > 0 else 10,
                        node_id=node.id)
        parent["children"].append(new_node)

        # Recursively add the current node's children
        if node.left:
            _add_node(node.left, new_node)
        if node.right:
            _add_node(node.right, new_node)

    def _label_tree(node):
        # If not a leaf (has children), flatten all the leaves in the node's subtree
        # If it is a leaf, then we have its name
        if node["children"]:
            leaf_names = reduce(lambda ls, c: ls + _label_tree(c), node["children"], [])
        else:
            leaf_names = [id2name[node["node_id"]]]

        # Delete the node id since we don't need it anymore and
        # it makes for cleaner JSON
        # del node["node_id"]

        # Labeling convention: "-"-separated leaf names
        node["name"] = name = "-".join(sorted(map(str, leaf_names)))
        ids_to_names[node['node_id']] = name

        return leaf_names

    _add_node(tree, d3_dendro)
    _label_tree(d3_dendro["children"][0])

    return d3_dendro