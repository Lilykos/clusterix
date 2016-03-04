from scipy.cluster.hierarchy import to_tree


def get_bcluster_json(blocks, bcluster, block_by, items):
    """
    Using the input, creates a D3 compatible dict, containing the hierarchical clustering results.

    :param blocks: The blocks that are used for the clustering. E.g. by country, by sex, by age, etc.
    :type blocks: list

    :param bcluster: An instance of the clusterer (BlockClustering) with all the info (linkage, etc).
    :type bcluster: BlockClustering

    :param block_by: The input key that is used for creating the different clustering blocks.
    :type block_by: str

    :param items: A list containing dictionaries of all the items (with their metadata).
    :type items: list

    :return: A D3 compatible dict.
    :rtype: dict
    """
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
        new_node = {'children': [], 'value': node.dist if node.dist > 0 else 1, 'node_id': node.id}
        parent['children'].append(new_node)

        if node.left:
            _add_node(node.left, new_node)
        if node.right:
            _add_node(node.right, new_node)

    def _label_tree(node):
        if node['children']:
            map(_label_tree, node['children'])
            node['name'] = node['node_id']
        else:
            node['content'] = id2content[node['node_id']]

    def _process_block():
        """Initialize nested dictionary for d3, then recursively iterate through tree and create the dict."""
        tree = to_tree(linkage, rd=False)

        _add_node(tree, bcluster_dendro)
        _label_tree(bcluster_dendro["children"][-1])  # get the last element
        return bcluster_dendro

    # Create a root for the tree
    # and start iterating through the blocks to get the subtrees.
    bcluster_dendro = {'children': [], 'name': block_by, 'node_id': 'Root'}
    single_children = []

    for block in set(blocks):
        content = [item for item in items if item[block_by] == block]
        clusterer = bcluster.clusterers_[block]

        try:
            id2content = dict(zip(range(len(content)), content))
            linkage = clusterer.linkage_

            # Create a cluster from the current block and append it to the dendrogram
            # else (on the exception) get the item and add it immediately
            _process_block()
        except AttributeError:
            single_children.append({'content': content[0], 'value': 2, 'children': []})  # TODO: GET MEAN NUMBER OR SOMETHING HERE

    bcluster_dendro['children'] += single_children
    return _delete_keys_from_dict(bcluster_dendro)
