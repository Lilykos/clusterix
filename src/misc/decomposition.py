from sklearn.decomposition import TruncatedSVD, PCA
from sklearn.manifold import MDS, TSNE
from sklearn.metrics.pairwise import pairwise_distances
from ..config import log


@log('Decomposition started.')
def dim_reduction(X, decomp, metric):
    """Dimension reduction and saving of the model."""
    if X.shape[1] > 2:
        if decomp == 'pca':
            return pca(X)
        elif decomp == 'mds':
            return mds(X, metric)
        elif decomp == 'tsne':
            return tsne(X, metric)
        else:
            return svd(X)
    return X


@log('- Using: PCA.')
def pca(X):
    return PCA().fit_transform(X.toarray())


@log('- Using: SVD.')
def svd(X):
    return TruncatedSVD().fit_transform(X)


@log('- Using: t-SNE')
def tsne(X, metric):
    # reduce dimensions first
    X = PCA(40).fit_transform(X.toarray())
    # then use tsne
    return TSNE(metric=metric).fit_transform(X)


@log('- Using: MDS')
def mds(X, metric):
    X = PCA(40).fit_transform(X.toarray())
    X = pairwise_distances(X, metric=metric)
    return MDS(n_jobs=-1, dissimilarity='precomputed').fit_transform(X)
