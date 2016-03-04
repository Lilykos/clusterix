from functools import partial
from multiprocessing import cpu_count, Pool

from sklearn.base import TransformerMixin
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import HashingVectorizer, TfidfVectorizer, CountVectorizer
from sklearn.pipeline import make_pipeline, make_union

from ..database.db_funcs import get_items_from_db
from ..utils.lang import preprocess_text
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


def svd(X):
    """Return the input in 2 dimensions."""
    return TruncatedSVD().fit_transform(X)


def get_vectorizer(name, vocab_list):
    """Select the vectorizer to use."""
    if name == 'hasing':
        vec = HashingVectorizer(n_features=2**12, non_negative=True, norm=None)
    elif name == 'tfidf':
        vec = TfidfVectorizer(max_features=2**12, norm=None)
        vec.fit_transform(vocab_list)
    else:
        vec = CountVectorizer(max_features=2**12)
        vec.fit_transform(vocab_list)

    return vec


def create_input_transformer(fields_with_scaling, cluster_keys, vectorizer):
    """Create a pipeline of input transformations, allowing to use scaling of input fields."""
    pipeline = []
    for key in cluster_keys:
        pipeline.append(
            make_pipeline(
                FuncTransformer(partial(get_field, key=key)),  # allowed key
                vectorizer,
                FuncTransformer(partial(reweight, scale=get_scale(fields_with_scaling, key)))  # scaling from user
            ),
        )
    return make_union(*pipeline)


def get_data(cluster_keys, timestamp):
    """
    Returns the items from the db based on the timestamp, and processes it t create 3 distinct results:
        1. The original data dictionary.
        2. The preprocessed (stemmed etc) data dictionary, that will be used for clustering.
        3. The vocabulary of each item, for vectorizers.

    So, from this csv here:
        Name,Job,City
        John,Software Dev.,Paris
        Tom,Painter,Chicago

    We have this data list:
        [{
            'original': {u'City': u'Paris', u'Job': u'Software Dev.', u'Name': u'John'},
            'processed': {u'City': u'pari', u'Job': u'softwar dev', u'Name': u'john'},
            'vocabulary': u'john softwar dev pari'
        },{
            'original': {u'City': u'Chicago', u'Job': u'Painter', u'Name': u'Tom'},
            'processed': {u'City': u'chicago', u'Job': u'painter', u'Name': u'tom'},
            'vocabulary': u'tom painter chicago'
        }]

    :param cluster_keys: The keys that show which features will be used.
    :type cluster_keys: list

    :param timestamp: The timestamp for querying the data.
    :type timestamp: int

    :return: A list with the data/processed data/vocabulary of each item.
    :rtype: list
    """
    """
    Let's keep this here for debugging purposes (thread pool does not allow pdb)
        map(partial(_process, cluster_keys=cluster_keys), get_items_from_db(timestamp))
    """

    thread_pool = Pool(cpu_count())
    return thread_pool.map(partial(_process, cluster_keys=cluster_keys), get_items_from_db(timestamp))


def _process(item, cluster_keys):
    """This function is to be used by get_data(), it is put in this scope for multithreading."""
    row_keys = {}
    row_keys_processed = {}
    vocabulary = []

    # Iterate through all the metadata BUT use only the allowed keys provided by the app
    for metadata in item.input_item_metadata:
        if metadata.name in cluster_keys:
            meta_value = metadata.value
            processed_value = preprocess_text(meta_value)

            row_keys['id'] = item.id
            row_keys[metadata.name] = meta_value
            row_keys_processed[metadata.name] = ' '.join(processed_value)
            vocabulary += processed_value

    return {
        'original': row_keys,
        'processed': row_keys_processed,
        'vocabulary': ' '.join(vocabulary)
    }