from sklearn.decomposition import TruncatedSVD, PCA
from sklearn.manifold import MDS, TSNE
from sklearn.metrics.pairwise import pairwise_distances
from src.config import log
from ..utils import save_decomposition, save_X


@log('- Using: PCA.')
def pca(X):
    return PCA().fit(X)


@log('- Using: SVD.')
def svd(X):
    return TruncatedSVD().fit(X)


@log('- Using: t-SNE')
def tsne(X, metric):
    return TSNE(learning_rate=100, perplexity=15, metric=metric).fit(X)


@log('- Using: MDS')
def mds(X, metric):
    X = pairwise_distances(X, metric=metric)
    return MDS(dissimilarity='precomputed', random_state=42, n_jobs=-1).fit(X)


@log('Decomposition started.')
def dimension_reduction(X, decomp, metric):
    """Dimension reduction and saving of the model."""
    if X.shape[1] > 2:
        if decomp == 'pca':
            model = pca(X)
        elif decomp == 'tsne':
            model = tsne(X, metric)
        elif decomp == 'mds':
            model = mds(X, metric)
        else:
            model = svd(X)

        save_decomposition(model, decomp)
        X = model.transform(X) \
            if hasattr(model, 'transform') \
            else model.embedding_

    save_X(X)
    return X
