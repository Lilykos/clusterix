from sklearn.externals.joblib import Parallel, delayed
from sklearn.pipeline import make_pipeline, make_union

from ..clustering.transformers import ItemSelector, Scaler, MissingValuesTransformer, Vectorizer
from ..utils.lang import tokenize_clean_text, stem

"""General clustering functions."""


def create_input_transformer(fields, vec_name):
    """Create a pipeline of input transformations, allowing to use scaling of input fields."""
    vectorizer = Vectorizer(vec_name)
    missing_val_transformer = MissingValuesTransformer()

    pipeline = []
    for field in fields:
        pipeline.append(
            make_pipeline(ItemSelector(field['name']),      # select the correct column
                          missing_val_transformer,          # fill empty values with NaN
                          vectorizer,                       # vectorize (depending on str/numeric input)
                          Scaler(field['scale']))           # scale column based on user input
        )

    return make_union(*pipeline)


def get_processed_data(data):
    """
    Returns the items from the db based on the timestamp, and processes it t create 3 distinct results:
        1. The original data dictionary.
        2. The preprocessed (stemmed etc) data dictionary, that will be used for clustering.
        3. The vocabulary of each item, for vectorizers.

    So, from this csv here:
        Name,Job,City
        John,Software Dev.,Paris

    We have this data list:
        [{
            u'original': {u'City': u'Paris', u'Job': u'Software Dev.', u'Name': u'John'},
            u'processed': {u'City': u'pari', u'Job': u'softwar dev', u'Name': u'john'},
            u'vocabulary': {u'City': u'paris', u'Job': u'software dev', u'Name': u'john'}
        }]

    :return: A list with the data/processed data/vocabulary of each item.
    :rtype: list
    """
    data_len = len(data.keys())

    parallel = Parallel(n_jobs=-1, backend='multiprocessing', verbose=1)
    return parallel(delayed(_process)(data[i]) for i in range(data_len))


def _process(item):
    """Process a single item. Return the original data, the processed/stemmed data and the vocabulary."""
    original = {}
    processed = {}
    vocabulary = {}

    for key in item.keys():
        # Differentiate between numbers and strings
        # Numbers need to be returned as they are, strings need to be processed
        #
        # from numbers import Number
        # if isinstance(item[key], Number):
        #     original[key] = item[key]
        #     processed[key] = item[key]
        #     vocabulary[key] = item[key]
        # else:
        #     tokenized_val = tokenize_clean_text(item[key])
        #     stemmed_tokenized_val = map(stem, tokenized_val)
        #
        #     original[key] = item[key]
        #     processed[key] = ' '.join(stemmed_tokenized_val)
        #     vocabulary[key] = ' '.join(tokenized_val)
        try:
            i = float(item[key])
            original[key] = i
            processed[key] = i
            vocabulary[key] = i
        except ValueError:
            tokenized_val = tokenize_clean_text(item[key])
            stemmed_tokenized_val = map(stem, tokenized_val)

            original[key] = item[key]
            processed[key] = ' '.join(stemmed_tokenized_val) if stemmed_tokenized_val != '' else 'NaN'
            vocabulary[key] = ' '.join(tokenized_val)

    return {
        'original': original,
        'processed': processed,
        'vocabulary': vocabulary,
    }
