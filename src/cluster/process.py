import numpy as np
from .algorithms import cluster_algorithms
from .decomposition import dimension_reduction
from .utils import get_all_vectors, projection_exists
from ..config import logger, log
from ..utils import load_df, save_df, save_cluster_model, scatterplot, load_X


@log('Projection process started.')
def get_projection(attrs):
    """Project the data in a 2D space."""
    df = load_df()

    X = get_all_vectors(df, attrs)
    logger.info('- Data shape original: {}'.format(X.shape))

    X = X if isinstance(X, np.ndarray) else X.toarray()
    X = dimension_reduction(X, attrs['decomposition'], attrs['distanceMetric'])
    return X, df


@log('Clustering process started')
def cluster_data(attrs):
    """Retrieve items, cluster, and return the result dict."""
    if projection_exists(attrs):
        df = load_df()
        X = load_X()
    else:
        X, df = get_projection(attrs)

    # Execute clustering
    model = cluster_algorithms[attrs['algorithm']](X, attrs)
    labels = model.labels_ \
        if hasattr(model, 'labels_') \
        else model.predict(X)

    # Save clusters for tfidf and similar
    df['clx_cluster'] = labels

    save_df(df)
    save_cluster_model(model)
    return scatterplot(X, labels, df['clx_id'])


@log('Cluster prediction process started.')
def predict_data(attrs):
    pass
