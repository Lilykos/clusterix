from ..db import get_db_items, get_item_with_attrs
from ..utils.log import log_info
from ..clustering.utils import create_input_transformer
from ..clustering.algorithms import kmeans, block_clustering
from ..clustering.transformers import DecompositionTransformer


def cluster_data(data):
    """Retrieve items, cluster, and return the result dict."""
    fields = data['csvType']['fieldsWithScaling']
    field_names = [field['name'] for field in fields]

    vec_name = data['vectorizer']
    algorithms = data['algorithms']['algorithmsToUse']

    # Get the data and then retrieve the required fields only
    # Also retrieve the data needed from the db (to avoid preprocessing all over again)
    items = get_db_items()
    original_items = get_item_with_attrs('original', items, field_names)
    processed_items = get_item_with_attrs('processed', items, field_names)

    # Vectorize/transform/get the data array and do the transformation
    transformer = create_input_transformer(fields, vec_name)
    X = transformer.fit_transform(processed_items)
    X = DecompositionTransformer().fit_transform(X)

    log_info('Preprocessing complete.')

    result = {}
    for alg in algorithms:
        if alg == 'kmeans':
            result['kmeans'] = kmeans(X, original_items, data['algorithms']['kmeans'])
        if alg == 'bcluster':
            result['bcluster'] = block_clustering(X, original_items, data['algorithms']['bcluster'])

    log_info('Clustering complete.')
    return result


def predict_data():
    pass