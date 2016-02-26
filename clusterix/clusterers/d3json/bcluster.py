from functools import reduce
from scipy.cluster.hierarchy import to_tree


def get_bcluster_json(blocks, block_clustering, block_by, item_dict_list):
    """
    Using the input, creates a D3 compatible dict, containing the hierarchical clustering results.

    :param blocks: The blocks that are used for the clustering.
    :type blocks: list

    :param block_clustering: An instance of the clusterer (BlockClustering) with all the info (linkage, etc).
    :type block_clustering: BlockClustering

    :param block_by: The input key that is used for creating the different clustering blocks.
    :type block_by: str

    :param item_dict_list: A list containing dictionaries of all the items (with their metadata).
    :type item_dict_list: list

    :return: A D3 compatible dict.
    :rtype: dict
    """
    def _get_labels(block):
        """Returns the labels of the dict, but only for the block we are currently clustering."""
        labels = []
        for item in item_dict_list:
            label_str = ''
            label_array = []

            if item[block_by] == block:
                for key in item:
                    label_str += '{}:{}, '
                    label_array.append(key)
                    label_array.append(item[key])
                labels.append(label_str.format(*label_array))
        return labels

    def _delete_keys_from_dict(dict_del):
        """Delete node_id, as it is not needed, and use the node_id as name for branches."""
        if dict_del['children']:
            dict_del['name'] = dict_del['node_id']
            for v in dict_del['children']:
                if isinstance(v, dict):
                    _delete_keys_from_dict(v)
        try:
            del dict_del['node_id']
        except KeyError:
            pass
        return dict_del

    def _add_node(node, parent):
        """Create the first node, and iterate the tree in order to create the dict."""
        new_node = dict(children=[], value=node.dist if node.dist > 0 else 5, node_id=node.id)  # TODO: FIND  NUM TO USE
        parent["children"].append(new_node)

        if node.left:
            _add_node(node.left, new_node)
        if node.right:
            _add_node(node.right, new_node)

    def _label_tree(node):
        """If not a leaf (has children), flatten the leaves in the subtree else it's a leaf, so we have its name"""
        if node["children"]:
            leaf_names = reduce(lambda ls, c: ls + _label_tree(c), node["children"], [])
        else:
            leaf_names = [id2name[node["node_id"]]]

        # Labeling convention: "-"-separated leaf names
        node["name"] = name = "-".join(sorted(map(str, leaf_names)))
        ids_to_names[node['node_id']] = name

        return leaf_names

    def _process_block():
        """Initialize nested dictionary for d3, then recursively iterate through tree and create the dict."""
        tree = to_tree(linkage, rd=False)
        bcluster_dendro = dict(children=[], name=block_by, node_id="Root")  # value = 0

        _add_node(tree, bcluster_dendro)
        _label_tree(bcluster_dendro["children"][0])
        return bcluster_dendro

    children = []
    for block in set(blocks):
        labels = _get_labels(block)
        clusterer = block_clustering.clusterers_[block]

        try:
            # Create a dict with ids/names to be used in newick or whatever else
            ids_to_names = {}
            id2name = dict(zip(range(len(labels)), labels))

            linkage = clusterer.linkage_
            children.append(_process_block())
        except AttributeError:
            children.append({'name': labels[0], 'value': 2, 'children': []})  # TODO: GET MEAN NUMBER OR SOMETHING HERE

    return _delete_keys_from_dict({
        'name': 'bcluster_node',
        'node_id': 'bcluster_node',
        'children': children
    })
