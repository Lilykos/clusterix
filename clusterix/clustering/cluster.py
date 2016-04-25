from ..log import log_info

from ..database.db import processed_db
from ..clustering.utils import create_input_transformer, get_cluster_attrs, load_clusterer
from ..clustering.algorithms import kmeans, hcluster
from ..clustering.transformers import DecompositionTransformer


def get_input_vector(fields, vec_name, data):
    transformer = create_input_transformer(fields, vec_name)

    X = transformer.fit_transform(data)
    X = DecompositionTransformer().fit_transform(X)

    log_info('Transformation pipeline complete.')
    return X


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
