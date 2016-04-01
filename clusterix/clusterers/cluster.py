from timeit import default_timer as timer

from clusterix import log_info
from ..clusterers.utils import get_keys, get_data, get_vectorizer, create_input_transformer, svd
from ..clusterers.algorithms import kmeans, block_clustering


def get_cluster_result(attrs):
    """Retrieve attributes from user, and use the requested algorithms to create d3-compatible json results."""
    timestamp, block_by, csv_fields, algorithms, vectorizer_name, k_num, bcluster_distance, affinity = \
        attrs['timestamp'], attrs['block_by'], attrs['csv_fields'], attrs['algorithms'], \
        attrs['vectorizer'], attrs['k_num'], attrs['bcluster_distance'], attrs['affinity']

    start = timer()
    # Get the keys that will be used for clustering and all the items from the db.
    #
    cluster_keys = get_keys(csv_fields)
    items = get_data(cluster_keys, timestamp)

    # We need to get 4 different data sets:
    #   1. Original items, to send to the frontend for visualization
    #   2. Processed items (stemmed/no stopwords etc) for transforming and clustering
    #   3. Vocabulary (processed but NOT STEMMED) for stats purposes (e.g tf idf)
    #
    original_items = map(lambda i: i['original'], items)
    processed_items = map(lambda i: i['processed'], items)
    vocab_items = map(lambda i: i['vocabulary'], items)

    # Create the transformer using a pipeline of pre-determined functions, and get the X matrix.
    #
    vectorizer = get_vectorizer(vectorizer_name)
    transformer = create_input_transformer(csv_fields, cluster_keys, vectorizer)
    X = transformer.fit_transform(processed_items)

    end = timer()
    log_info('Preprocessing complete in {} sec.'.format(end - start))

    start = timer()
    # Get the results from all the requested algorithms
    #
    result = {}
    for alg in algorithms:
        if alg == 'kmeans':
            result['kmeans'] = kmeans(svd(X), original_items, vocab_items, int(k_num))
        if alg == 'bcluster':
            result['bcluster'] = block_clustering(X.toarray(), block_by, original_items, bcluster_distance, affinity)

    end = timer()
    log_info('Clustering complete in {} sec.'.format(end - start))

    return result