from sklearn.decomposition import TruncatedSVD, PCA
from sklearn.manifold import MDS, TSNE
from ..config import log


@log('Decomposition started.')
def dimension_reduction(X, decomp, metric):
    """Dimension reduction and saving of the model."""
    if X.shape[1] > 2:
        if decomp == 'pca':
            return pca(X)
        elif decomp == 'tsne':
            return tsne(X, metric)
        elif decomp == 'mds':
            return mds(X, metric)
        else:
            return svd(X)
    return X


@log('- Using: PCA.')
def pca(X):
    return PCA().fit_transform(X)


@log('- Using: SVD.')
def svd(X):
    return TruncatedSVD().fit_transform(X)


@log('- Using: t-SNE')
def tsne(X, metric):
    return TSNE(learning_rate=100, perplexity=15, metric=metric).fit_transform(X)


@log('- Using: MDS')
def mds(X, metric):
    return MDS(dissimilarity=metric, random_state=42, n_jobs=-1).fit_transform(X)
