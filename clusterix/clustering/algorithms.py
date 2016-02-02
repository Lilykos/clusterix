from multiprocessing import cpu_count
from beard.clustering import ScipyHierarchicalClustering, BlockClustering
from sklearn.cluster import KMeans

from ..clustering.results.bcluster import get_bcluster_json
from ..clustering.results.kmeans import get_kmeans_json
"""All the algorithms here return a d3 compatible json. The example input used is this csv:
        Name,Job,City
        John,Software Dev.,Paris
        Tom,Painter,Chicago
        Joe,Painting Professional,Paris
        Linda,SysAdmin,Paris
"""


def kmeans(X, original_items, data):
    """
    K-Means clustering.
    Return example:
        {'k_num': 2,
         'nodes': [
               {'cluster': 0, 'isCentroid': False, 'id': 2,
                'content': {u'City': u'Chicago', u'Job': u'Painter', u'Name': u'Tom', 'id': 145466},
                'x': 2.658062848683116e-16, 'y': 1.7320508075688774},
               {'cluster': 0, 'isCentroid': True,
                'x': 2.220446049250313e-16, 'y': 1.7320508075688774},
               {'cluster': 1, 'isCentroid': False, 'id': 1,
                'content': {u'City': u'Paris', u'Job': u'Software Dev.', u'Name': u'John', 'id': 145465},
                'x': 1.5034503553765397, 'y': 0.0},
                ..............]}

    :param X: The X array used for clustering (n_samples * n_features).
    :type X: list

    :param original_items: The field with the original features, to create the node labels.
    :type original_items: list

    :param data: K-Means data
    :type data: dict

    :return: A d3 compatible dict, to be sent as json.
    :rtype: dict
    """
    n_clusters = int(data['kNumber'])
    km = KMeans(n_clusters=n_clusters, n_jobs=-1)
    km.fit(X)

    labels = km.labels_
    centroids = km.cluster_centers_

    return get_kmeans_json(X, labels, centroids, n_clusters, original_items)


def block_clustering(X, original_items, data):
    """
    Block Clustering uses a specific field from the input data, to cluster based on that. The returned tree
    gets turned into a d3 compatible json, that can be used for heat map visualization.
    Return Example:
        {'children': [
                {'children': [
                        {'children': [],
                         'content': {u'City': u'Paris', u'Job': u'Painting Professional', u'Name': u'Joe', 'id': 4277},
                         'value': 1},
                        {'children': [
                                {'children': [],
                                 'content': {u'City': u'Paris', u'Job': u'Software Dev.', u'Name': u'John', 'id': 4275},
                                 'value': 1},
                                {'children': [],
                                 'content': {u'City': u'Paris', u'Job': u'SysAdmin', u'Name': u'Linda', 'id': 4278},
                                 'value': 1}],
                         'name': 3,
                         'value': 2.23606797749979}],
                 'name': 4,
                 'value': 2.342778860141484},
                {'children': [],
                 'content': {u'City': u'Chicago', u'Job': u'Painter', u'Name': u'Tom', 'id': 4276},
                 'value': 2}],
         'name': 'Root'}

    :param X: The X array used for clustering (n_samples * n_features).
    :type X: list

    :param original_items: The list with all the items.
    :type original_items: list

    :param data: Block Clustering data.
    :type data: dict

    :return: A d3 compatible dict, to be sent as json.
    :rtype: dict
    """
    # Cluster the data using the given block.
    clustering = ScipyHierarchicalClustering(method=data['distance'],
                                             affinity=data['affinity'],
                                             threshold=100.)
    bcluster = BlockClustering(base_estimator=clustering,
                               blocking="precomputed",
                               verbose=3,
                               n_jobs=cpu_count() - 1)

    block_key = data['blockBy']
    blocks = [item[block_key] for item in original_items]

    bcluster.fit(X, blocks=blocks)

    # Get the json needed for d3 visualization.
    return get_bcluster_json(blocks, bcluster, block_key, original_items)