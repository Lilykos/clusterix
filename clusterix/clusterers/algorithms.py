from multiprocessing import cpu_count
from beard.clustering import ScipyHierarchicalClustering, BlockClustering
from sklearn.cluster import KMeans

from ..clusterers.d3json.bcluster import get_bcluster_json
from ..clusterers.d3json.kmeans import get_kmeans_json
from ..clusterers.utils import get_field
"""All the algorithms here return a d3 compatible json. The example input used is this csv:
        Name,Job,City
        John,Software Dev.,Paris
        Tom,Painter,Chicago
        Joe,Painting Professional,Paris
        Linda,SysAdmin,Paris
"""


def kmeans(X, original_item_list, n_clusters=2):
    """
    K-Means clustering.
    Return example:
        {'centroids': [{'cluster': 0,
                        'x': 1.5034503553765401, 'y': 1.2247448713915896},
                       {'cluster': 1,
                        'x': 0.8680174673898841, 'y': 1.9229626863835638e-16}],
         'items': [{'cluster': 0,
                    'content': {u'City': u'Paris', u'Job': u'Software Dev.', u'Name': u'John', 'id': 4275},
                    'x': 1.5034503553765401, 'y': 1.2247448713915896},
                   {'cluster': 1,
                    'content': {u'City': u'Chicago', u'Job': u'Painter', u'Name': u'Tom', 'id': 4276},
                    'x': 0.0, 'y': 1.9229626863835638e-16},
                   {'cluster': 1,
                    'content': {u'City': u'Paris', u'Job': u'Painting Professional', u'Name': u'Joe', 'id': 4277},
                    'x': 1.5034503553765401, 'y': -1.2247448713915878},
                   {'cluster': 1,
                    'content': {u'City': u'Paris', u'Job': u'SysAdmin', u'Name': u'Linda', 'id': 4278},
                    'x': 1.100602046793112, 'y': -1.7306664177452074e-15}],
         'k_num': 2}

    :param X: The X array used for clustering (n_samples * n_features).
    :type X: list

    :param original_item_list: The field with the original features, to create the node labels.
    :type original_item_list: list

    :param n_clusters: The number of K clusters.

    :return: A d3 compatible dict, to be sent as json.
    :rtype: dict
    """
    km = KMeans(n_clusters=n_clusters, n_jobs=-1)
    km.fit(X)

    labels = km.labels_
    centroids = km.cluster_centers_

    return get_kmeans_json(n_clusters, labels, centroids, original_item_list, X)


def block_clustering(X, block_by, original_item_list):
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

    :param block_by: The field that will be used as a basis for the block clustering.
    :type block_by: str

    :param original_item_list: The list with all the items.
    :type original_item_list: list

    :return: A d3 compatible dict, to be sent as json.
    :rtype: dict
    """
    # Cluster the data using the given block.
    clustering = ScipyHierarchicalClustering(method="average",
                                             affinity="euclidean",
                                             threshold=100.)
    bcluster = BlockClustering(base_estimator=clustering,
                               blocking="precomputed",
                               verbose=3,
                               n_jobs=cpu_count())

    blocks = list(get_field(original_item_list, block_by))
    bcluster.fit(X, blocks=blocks)

    # Get the json needed for d3 visualization.
    return get_bcluster_json(blocks, bcluster, block_by, original_item_list)