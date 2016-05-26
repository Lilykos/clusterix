from ..database.db import processed_db
from ..clustering.utils import get_cluster_attrs, get_input_vector
from ..clustering.algorithms import kmeans, hcluster

from ..log import log_info


def cluster_data(attrs):
    """Retrieve items, cluster, and return the result dict."""
    fields, field_names, vec_name, algorithms = get_cluster_attrs(attrs)

    # Vectorize/transform/get the data array and do the transformation
    # Then, get the records using only the specified fields (for clustering certain columns)
    data = processed_db.get_records_with_fields(field_names)
    X = get_input_vector(fields, vec_name, data)

    result = {}
    for alg in algorithms:
        if alg == 'kmeans':
            result['kmeans'] = kmeans(X, attrs['algorithms']['kmeans'])
        if alg == 'hcluster':
            result['hcluster'] = hcluster(X, attrs['algorithms']['hcluster'])

    log_info('Clustering complete.')
    return result


def predict_cluster(attrs):
    # fields, field_names, vec_name, _ = get_cluster_attrs(attrs)
    # X = get_input_vector(fields, field_names, vec_name)
    #
    # clusterer = load_clusterer()
    # clusterer.predict(X)
    pass
