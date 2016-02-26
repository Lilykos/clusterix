import sys

from ..clusterers.utils import get_vectorizer, get_keys, get_field, create_input_transformer
from ..clusterers.d3json.bcluster import get_bcluster_json
from ..database.db_funcs import get_items_from_db
from ..utils.lang import preprocess_text

from beard.clustering import ScipyHierarchicalClustering, BlockClustering


def block_cluster(fields_with_scaling, block_by_field, timestamp, vectorizer='hashing'):
    """
    BlockClustering uses a specific field from the input data, to cluster based on that. The returned tree
    gets turned into a d3 compatible json, that can be used for heatmap visualization.

    So, from this csv here:
        Name,Job,City
        John,Software Dev.,Paris
        Tom,Painter,Chicago
        Joe,Painting Professional,Paris
        Linda,SysAdmin,Paris

    We will get this json:
        {
            'children':
                [{
                    'children':
                        [{
                            'children':
                                [{
                                    'children': [],
                                    'name': 'City:Paris, Job:Painting Professional, Name:Joe, ',
                                    'value': 5
                                },{
                                    'children': [{
                                                    'children': [],
                                                    'name': 'City:Paris, Job:Software Dev., Name:John, ',
                                                    'value': 5
                                                },{
                                                    'children': [],
                                                    'name': 'City:Paris, Job:SysAdmin, Name:Linda, ',
                                                    'value': 5
                                                }],
                                    'name': 3,
                                    'value': 2.23606797749979
                                }],
                            'name': 4,
                            'value': 2.342778860141484
                        }],
                    'name': 'Root'
                },{
                    'children': [],
                    'name': 'City:Chicago, Job:Painter, Name:Tom, ',
                    'value': 2
                }],
            'name': 'bcluster_node'
        }

    :param fields_with_scaling: A list of the fields to be used, with the scale that needs to be applied.
    :type fields_with_scaling: list

    :param block_by_field: The field that will be used as a basis for the block clustering.
    :type block_by_field: str

    :param vectorizer: The vectorizer type to be used (count, hashing, tfidf).
    :type vectorizer: str

    :param timestamp: The timestamp that will be the query basis, so that the data will not get mixed.
    :type timestamp: int

    :return: A d3 compatible dict, to be sent as json.
    :rtype: dict
    """
    sys.setrecursionlimit(10000)  # Overflow if we don't do that

    vectorizer = get_vectorizer(vectorizer)
    cluster_keys = get_keys(fields_with_scaling)
    items = get_items_from_db(timestamp)

    # We need 2 types of lists:
    #   1. Raw/original text and used for naming the json.
    #   2. Processed text for more accurate clustering (stemmed, without stopwords, etc).

    item_dict_list = []
    item_dict_list_processed = []
    for item in items:
        row_keys = {}
        row_keys_processed = {}

        # Iterate through all the metadata BUT use only the allowed keys provided by the app
        for metadata in item.input_item_metadata:
            if metadata.name in cluster_keys:
                row_keys[metadata.name] = metadata.value
                row_keys_processed[metadata.name] = preprocess_text(metadata.value)

        item_dict_list.append(row_keys)
        item_dict_list_processed.append(row_keys)

    # Create the transformer using a pipeline of pre-determined functions, and get the X matrix.
    transformer = create_input_transformer(fields_with_scaling, cluster_keys, vectorizer)
    X = transformer.transform(item_dict_list).toarray()

    # Cluster the data using the given block.
    clustering = ScipyHierarchicalClustering(method="average", affinity="euclidean", threshold=100.)
    block_clustering = BlockClustering(base_estimator=clustering, blocking="precomputed", verbose=3, n_jobs=4)

    blocks = get_field(item_dict_list, block_by_field)
    block_clustering.fit(X, blocks=blocks)

    # Get the json needed for d3 visualization.
    return get_bcluster_json(blocks, block_clustering, block_by_field, item_dict_list)
