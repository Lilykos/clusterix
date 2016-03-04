from ..clusterers.utils import get_keys, get_data, get_vectorizer, create_input_transformer, svd
from ..clusterers.algorithms import kmeans, block_clustering


def get_cluster_result(attrs):
    """Retrieve attributes from user, and use the requested algorithms to create d3-compatible json results."""
    timestamp, block_by, csv_fields, algorithms, vectorizer = \
        attrs['timestamp'], attrs['block_by'], attrs['csv_fields'], attrs['algorithms'], attrs['vectorizer']

    # Get the keys that will be used for clustering and all the items from the db.
    #
    cluster_keys = get_keys(csv_fields)
    items = get_data(cluster_keys, timestamp)

    # We need to get 3 different data sets:
    # The original list of data, the processed one, and the vocabulary for each item.
    #
    original_item_list = map(lambda i: i['original'], items)
    processed_item_list = map(lambda i: i['processed'], items)
    vocab_list = map(lambda i: i['vocabulary'], items)

    # Create the transformer using a pipeline of pre-determined functions, and get the X matrix.
    #
    vectorizer = get_vectorizer(vectorizer, vocab_list)
    transformer = create_input_transformer(csv_fields, cluster_keys, vectorizer)
    X = transformer.transform(processed_item_list)

    # Get the results from all the requested algorithms
    #
    result = {}
    for alg in algorithms:
        if alg == 'kmeans':
            result['kmeans'] = kmeans(svd(X), original_item_list)
        if alg == 'bcluster':
            result['bcluster'] = block_clustering(X.toarray(), block_by, original_item_list)

    return result