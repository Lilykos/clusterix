from beard.clustering import ScipyHierarchicalClustering
from sklearn.cluster import KMeans

from ..clustering.results.kmeans import get_kmeans_json
from ..clustering.results.hcluster import HClusterTree


def kmeans(X, attrs):
    """
    K-Means clustering.
    Return example:
        {'k_num': 2,
         'nodes': [
               {'cluster': 0, 'isCentroid': False, 'id': 2,
                'x': 2.658062848683116e-16, 'y': 1.7320508075688774},
               {'cluster': 0, 'isCentroid': True,
                'x': 2.220446049250313e-16, 'y': 1.7320508075688774},
               {'cluster': 1, 'isCentroid': False, 'id': 1,
                'x': 1.5034503553765397, 'y': 0.0},
                ..............]}
    """
    n_clusters = int(attrs['kNumber'])
    km = KMeans(n_clusters=n_clusters, n_jobs=-1)
    km.fit(X)

    labels = km.labels_
    centroids = km.cluster_centers_

    return get_kmeans_json(X, labels, centroids, n_clusters)


def hierarchical_clustering(X, attrs):
    """
    Hierarchical Clustering.
    Return Example:
        {'children': [
            {'children': [], 'name': 2, 'value': 150.0039243544126},
            {'children': [
                {'children': [], 'name': 1, 'value': 2.509279181210386},
                {'children': [
                    {'children': [], 'name': 0, 'value': 2.4987419269136737},
                    {'children': [], 'name': 3, 'value': 2.4987419269136737}
                ], 'name': 4,'value': 4.997483853827347}
            ], 'name': 5, 'value': 5.018558362420772}
        ], 'name': 6, 'value': 300.0078487088252}
    """
    hcluster = ScipyHierarchicalClustering(method=attrs['distance'],
                                           affinity=attrs['affinity'])

    hcluster.fit(X)
    Z = hcluster.linkage_

    return HClusterTree(Z).to_dict()


# def block_clustering(X, original_items, data):
#     # Cluster the data using the given block.
#     clustering = ScipyHierarchicalClustering(method=data['distance'],
#                                              affinity=data['affinity'],
#                                              threshold=100.)
#     bcluster = BlockClustering(base_estimator=clustering,
#                                blocking="precomputed",
#                                verbose=3,
#                                n_jobs=cpu_count() - 1)
#
#     block_key = data['blockBy']
#     blocks = [item[block_key] for item in original_items]
#
#     bcluster.fit(X, blocks=blocks)
#
#     # Get the json needed for d3 visualization.
#     return get_bcluster_json(blocks, bcluster, block_key, original_items)
