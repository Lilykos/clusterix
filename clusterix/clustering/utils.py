try:
    import cPickle as pickle
except ImportError:
    import pickle
from sklearn.pipeline import make_pipeline, make_union

from ..clustering.transformers import ItemSelector, Scaler, Vectorizer
from ..database.db import processed_db
from ..config import CLUSTERER_PATH
"""General clustering functions."""


def create_input_transformer(fields, vec_name):
    """Create a pipeline of input transformations, allowing to use scaling of input fields."""
    pipeline = []
    for field in fields:
        field_name = field['name']
        field_scale = field['scale']
        field_type = processed_db.get_field_type(field_name)

        pipeline.append(
            make_pipeline(ItemSelector(field_name),             # select the correct column
                          Vectorizer(vec_name, field_type),     # vectorize (depending on str/numeric input)
                          Scaler(field_scale))                  # scale column based on user input
        )

    return make_union(*pipeline)


def get_clustered_ids(data):
    """
    Get a dict of id-cluster pairs and create a dict of cluster-list[ids]. E.g.
    From:   {u'1': 2, u'1006': 1, u'191': 1, u'2': 2, u'276': 1, u'3': 2, u'358': 1, u'6': 3}
    To:     {1: [1006, 191, 276, 358], 2: [1, 2, 3], 3: [6]}
    """
    clustered_ids = {}
    for key in data.keys():
        val = data[key]
        try:
            clustered_ids[val].append(int(key))
        except KeyError:
            clustered_ids[val] = [int(key)]

    return clustered_ids


def get_cluster_attrs(attrs):
    """Get some general attributes for clustering/predictions."""
    fields = attrs['csvType']['fieldsWithScaling']
    field_names = [field['name'] for field in fields]
    vec_name = attrs['vectorizer']
    algorithms = attrs['algorithms']['algorithmsToUse']

    return fields, field_names, vec_name, algorithms


def save_clusterer(clusterer):
    """Pickle clusterer object."""
    pickle.dump(clusterer, open(CLUSTERER_PATH, "wb"))


def load_clusterer():
    """Load pickled clusterer object."""
    return pickle.load(open(CLUSTERER_PATH, "rb"))