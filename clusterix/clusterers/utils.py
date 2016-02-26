from functools import partial

from sklearn.base import TransformerMixin
from sklearn.feature_extraction.text import HashingVectorizer, TfidfVectorizer, CountVectorizer
from sklearn.pipeline import make_pipeline, make_union

"""General clustering functions."""


class FuncTransformer(TransformerMixin):
    """A FuncTransformer implementation, to use in pipeline creation."""
    def __init__(self, func):
        self.func = func

    def fit(self, X, y):
        return self

    def transform(self, X):
        return self.func(X)


def get_keys(fields):
    """Get the 'name' key from a list of dicts."""
    return [i['name'] for i in fields]


def get_scale(fields, key):
    """Get the scale of a specific field."""
    for field in fields:
        if field['name'] == key:
            return int(field['scale'])


def reweight(x, scale=1):
    """ Reweight the attributes."""
    return scale * x


def get_field(items, key):
    """Get all the values for a specified key."""
    for item in items:
        yield item[key]


def get_vectorizer(name):
    """Select the vectorizer to use."""
    vectorizers = {
        'hashing': HashingVectorizer(n_features=2**12, non_negative=True, norm=None),
        'tfidf': TfidfVectorizer(max_features=2**12, norm=None),
        'count': CountVectorizer(max_features=2**12)
    }
    return vectorizers[name]


def create_input_transformer(fields_with_scaling, cluster_keys, vectorizer):
    """Create a pipeline of input transformations, allowing to use scaling of input fields."""
    pipeline = []
    for key in cluster_keys:
        pipeline.append(
            make_pipeline(
                FuncTransformer(partial(get_field, key=key)), vectorizer,  # allowed key
                FuncTransformer(partial(reweight, scale=get_scale(fields_with_scaling, key)))  # scaling from user
            ),
        )
    return make_union(*pipeline)