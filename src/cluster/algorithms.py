from sklearn.cluster import KMeans, DBSCAN, MeanShift, AgglomerativeClustering
from ..config import log


@log('- K-Means clustering started.')
def kmeans(X, attrs):
    return KMeans(n_clusters=int(attrs['kNumber']), n_init=100, algorithm='full', n_jobs=-1).fit(X)


@log('- DBSCAN clustering started.')
def dbscan(X, attrs,):
    return DBSCAN(min_samples=int(attrs['minSamples']), eps=float(attrs['eps']), n_jobs=-1).fit(X)


@log('- Mean Shift clustering started.')
def meanshift(X, attrs):
    return MeanShift(cluster_all=attrs['clusterAll'], min_bin_freq=int(attrs['binNumber']), n_jobs=-1).fit(X)


@log('- Hierarchical clustering started.')
def hcluster(X, attrs):
    return AgglomerativeClustering(n_clusters=int(attrs['kNumber']), linkage=attrs['linkage'], affinity=attrs['affinity']).fit(X)


cluster_algorithms = {
    'kmeans': kmeans,
    'dbscan': dbscan,
    'hcluster': hcluster,
    'meanshift': meanshift
}
