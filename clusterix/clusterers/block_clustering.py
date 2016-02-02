from functools import partial

from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.pipeline import make_union, make_pipeline
from beard.clustering import ScipyHierarchicalClustering, BlockClustering

from ..clusterers.func_transformer import FuncTransformer
from ..database.input_item_properties import get_items_from_db
from ..utils.d3_converter import D3Converter


def get_labels(items, block_by, block):
    # labels = ['Survived:{} Class:{} Sex:{} Age:{}'.format(i['Survived'], i['Pclass'], i['Sex'], i['Age'])
    #           for i in item_dict_list
    #           if i[block_by_field] == block]
    labels = []
    for item in items:
        label_str = ''
        label_array = []

        for key in item:
            label_str += '{}:{}, '
            label_array.append(key)
            label_array.append(item[key])
        if item[block_by] == block:
            labels.append(label_str.format(*label_array))
    return labels


def get_keys(fields):
    return [i['name'] for i in fields]


def get_scale(fields, key):
    for field in fields:
        if field['name'] == key:
            return int(field['scale'])


def reweight(x, scale=1):
    """ Reweight the attributes"""
    return scale * x


def get_field(items, key):
    values = []
    for item in items:
        values.append(item[key])
    return values


def block_cluster(fields_with_scaling, block_by_field):
    import sys
    sys.setrecursionlimit(10000)

    hasher = HashingVectorizer(n_features=2**12, non_negative=True, norm=None)
    cluster_keys = get_keys(fields_with_scaling)

    #
    #
    # Create a list of dicts, needed for the block clustering computation
    #
    #
    items = get_items_from_db()
    item_dict_list = []
    for item in items[:400]:  # TODO REMOVE THAT
        row_keys = {}
        # Iterate through all the metadata
        # BUT use only the allowed keys provides by the app
        for metadata in item.input_item_metadata:
            if metadata.name in cluster_keys:
                row_keys[metadata.name] = metadata.value

        item_dict_list.append(row_keys)

    #
    #
    # Create a pipeline of functions
    #
    #
    pipeline = []
    for key in cluster_keys:
        pipeline.append(
            make_pipeline(
                FuncTransformer(partial(get_field, key=key)), hasher,  # allowed key
                FuncTransformer(partial(reweight, scale=get_scale(fields_with_scaling, key)))  # scaling from user
            ),
        )
    #
    #
    # Transform the data into a matrix, to use in the clustering
    #
    #
    tf = make_union(*pipeline)
    X = tf.transform(item_dict_list).toarray()

    clustering = ScipyHierarchicalClustering(method="average", affinity="euclidean", threshold=100.)
    block_clustering = BlockClustering(base_estimator=clustering, blocking="precomputed", verbose=3, n_jobs=5)

    blocks = get_field(item_dict_list, block_by_field)
    block_clustering.fit(X, blocks=blocks)

    #
    #
    # BLOCK CLUSTERING HAPPENS HERE
    #
    #
    children = []
    for block in set(blocks):
        labels = get_labels(item_dict_list, block_by_field, block)

        d3_converter = D3Converter(labels)
        clusterer = block_clustering.clusterers_[block]

        try:
            children.append(d3_converter.get_d3_json(clusterer.linkage_, block))
        except AttributeError:
            children.append({
                'name': labels[0],
                # 'node_id': labels[0] + '_id',
                'children': []
            })

    return {
        'name': 'BlockClusteringResult',
        # 'node_id': 'BlockClusteringID',
        'children': children
    }
