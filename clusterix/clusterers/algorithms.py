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


def kmeans(X, original_items, vocab_items, n_clusters):
    """
    K-Means clustering.
    Return example:
        {'k_num': 2,
         'nodes': [{'cluster': 0,
                    'content': {u'City': u'Chicago', u'Job': u'Painter', u'Name': u'Tom', 'id': 145466},
                    'isCentroid': False, 'x': 2.658062848683116e-16, 'y': 1.7320508075688774},
                   {'cluster': 0,
                    'isCentroid': True, 'x': 2.220446049250313e-16, 'y': 1.7320508075688774},
                   {'cluster': 1,
                    'content': {u'City': u'Paris', u'Job': u'Software Dev.', u'Name': u'John', 'id': 145465},
                    'isCentroid': False, 'x': 1.5034503553765397, 'y': 0.0},
                   {'cluster': 1,
                    'content': {u'City': u'Paris', u'Job': u'Painting Professional', u'Name': u'Joe', 'id': 145467},
                    'isCentroid': False, 'x': 1.5034503553765406, 'y': 1.1537776118301384e-15},
                   {'cluster': 1,
                    'content': {u'City': u'Paris', u'Job': u'SysAdmin', u'Name': u'Linda', 'id': 145468},
                    'isCentroid': False, 'x': 1.100602046793112, 'y': -1.5383701491068513e-15},
                   {'cluster': 1,
                    'isCentroid': True, 'x': 1.3691675858487307, 'y': -1.1102230246251565e-16}],
         'term_frequencies': [[{'freq': 1, 'term': u'chicago', 'total': 1},
                               {'freq': 1, 'term': u'painter', 'total': 1},
                               {'freq': 1, 'term': u'tom', 'total': 1}],
                              [{'freq': 3, 'term': u'paris', 'total': 3},
                               {'freq': 1, 'term': u'dev', 'total': 1},
                               {'freq': 1, 'term': u'sysadmin', 'total': 1},
                               {'freq': 1, 'term': u'joe', 'total': 1},
                               {'freq': 1, 'term': u'linda', 'total': 1},
                               {'freq': 1, 'term': u'professional', 'total': 1},
                               {'freq': 1, 'term': u'john', 'total': 1},
                               {'freq': 1, 'term': u'painting', 'total': 1},
                               {'freq': 1, 'term': u'software', 'total': 1}]],
         'tfidf': [[{'score': 0.56438, 'term': u'tom'},
                    {'score': 0.56438, 'term': u'painter'},
                    {'score': 0.56438, 'term': u'chicago'}],
                   [{'score': 0.27273, 'term': u'paris'},
                    {'score': 0.15392, 'term': u'dev'},
                    {'score': 0.15392, 'term': u'sysadmin'},
                    {'score': 0.15392, 'term': u'joe'},
                    {'score': 0.15392, 'term': u'linda'},
                    {'score': 0.15392, 'term': u'professional'},
                    {'score': 0.15392, 'term': u'john'},
                    {'score': 0.15392, 'term': u'painting'},
                    {'score': 0.15392, 'term': u'software'}]]}

    :param X: The X array used for clustering (n_samples * n_features).
    :type X: list

    :param original_items: The field with the original features, to create the node labels.
    :type original_items: list

    :param vocab_items: A list containing the vocabulary of each document.
    :type vocab_items: list

    :param n_clusters: The number of K clusters.

    :return: A d3 compatible dict, to be sent as json.
    :rtype: dict
    """
    km = KMeans(n_clusters=n_clusters, n_jobs=-1)
    km.fit(X)

    labels = km.labels_
    centroids = km.cluster_centers_

    return get_kmeans_json(X, labels, centroids, n_clusters, original_items, vocab_items)


def block_clustering(X, block_by, original_item_list, bcluster_distance, affinity):
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
    clustering = ScipyHierarchicalClustering(method=bcluster_distance,
                                             affinity=affinity,
                                             threshold=100.)
    bcluster = BlockClustering(base_estimator=clustering,
                               blocking="precomputed",
                               verbose=3,
                               n_jobs=cpu_count())

    blocks = list(get_field(original_item_list, block_by))
    bcluster.fit(X, blocks=blocks)

    # Get the json needed for d3 visualization.
    return get_bcluster_json(blocks, bcluster, block_by, original_item_list)