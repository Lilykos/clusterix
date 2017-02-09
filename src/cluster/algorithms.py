from sklearn.cluster import KMeans
from ..config import log
from ..misc import scatterplot
from ..utils import save_cluster_model


@log('K-Means clustering started.')
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
    k_means = KMeans(n_clusters=n_clusters, n_jobs=-1)
    k_means.fit(X)

    labels = k_means.labels_
    centroids = k_means.cluster_centers_

    save_cluster_model(k_means)
    return labels, scatterplot(X, labels, n_clusters, centroids=centroids)


# def hcluster(X, attrs):
#     """
#     Hierarchical Clustering.
#     Return Example:
#         {'children': [
#             {'children': [], 'name': 2, 'value': 150.0039243544126},
#             {'children': [
#                 {'children': [], 'name': 1, 'value': 2.509279181210386},
#                 {'children': [
#                     {'children': [], 'name': 0, 'value': 2.4987419269136737},
#                     {'children': [], 'name': 3, 'value': 2.4987419269136737}
#                 ], 'name': 4,'value': 4.997483853827347}
#             ], 'name': 5, 'value': 5.018558362420772}
#         ], 'name': 6, 'value': 300.0078487088252}
#     """
#     n_clusters = int(attrs['kNumber'])
#     hcluster = ScipyHierarchicalClustering(method=attrs['distance'],
#                                            affinity=attrs['affinity'],
#                                            n_clusters=n_clusters)
#
#     hcluster.fit(X)
#     labels = hcluster.labels_
#
#     # Z = hcluster.linkage_
#     # return HClusterTree(Z).to_dict()
#
#     # save_clusterer(hcluster)
#     return scatterplot(X, labels, n_clusters)
