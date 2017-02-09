from .algorithms import kmeans
from .utils import get_all_vectors
from ..misc import dim_reduction
from ..config import logger, log
from ..utils import load_df, save_df


@log('CLUSTERING PROCESS STARTED.')
def cluster_data(attrs):
    """Retrieve items, cluster, and return the result dict."""
    algorithm, decomp, metric = attrs['algorithm'], attrs['decomposition'], attrs['distanceMetric']
    df = load_df()

    X = get_all_vectors(df, attrs)
    logger.info('- Data shape original: {}'.format(X.shape))

    # Dimension reduction
    X = dim_reduction(X, decomp)

    # Execute clustering
    if algorithm == 'kmeans':
        labels, plot = kmeans(X, attrs)

    # Save the dataframe with the clusters for tfidf and similar
    df['cluster'] = labels
    save_df(df)
    return plot


@log('CLUSTER PREDICTION PROCESS STARTED.')
def predict_data(attrs):
    pass


@log('PROJECTION PROCESS STARTED.')
def get_projection(attrs):
    """Project the data without clustering."""
    df = load_df()
    X = get_all_vectors(df, attrs)
    X = dim_reduction(X, attrs['decomposition'], attrs['distanceMetric'])
    return [dict(x=x[0], y=x[1]) for x in X]

