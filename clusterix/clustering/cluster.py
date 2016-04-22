from ..log import log_info

from ..database.db import processed_db
from ..clustering.utils import create_input_transformer
from ..clustering.algorithms import kmeans, hierarchical_clustering
from ..clustering.transformers import DecompositionTransformer


def cluster_data(attrs):
    """Retrieve items, cluster, and return the result dict."""
    fields = attrs['csvType']['fieldsWithScaling']
    field_names = [field['name'] for field in fields]

    vec_name = attrs['vectorizer']
    algorithms = attrs['algorithms']['algorithmsToUse']

    # Vectorize/transform/get the data array and do the transformation
    # Then, get the records using only the specified fields (for clustering certain columns)
    transformer = create_input_transformer(fields, vec_name)
    X = transformer.fit_transform(
        processed_db.get_records_with_fields(field_names)
    )

    X = DecompositionTransformer().fit_transform(X)
    log_info('Preprocessing complete.')

    result = {}
    for alg in algorithms:
        if alg == 'kmeans':
            result['kmeans'] = kmeans(X, attrs['algorithms']['kmeans'])
        if alg == 'hcluster':
            result['hcluster'] = hierarchical_clustering(X, attrs['algorithms']['hcluster'])

    log_info('Clustering complete.')
    return result


def predict_cluster():
    pass