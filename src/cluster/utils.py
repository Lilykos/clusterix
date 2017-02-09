from scipy.sparse import hstack
from ..misc import get_vectorizer, stem_text_input
from ..config import logger, log


@log('Vectorization started.')
def get_vectorized_text(dataframe, columns, attrs):
    """Vectorize the text columns of a dataframe. Append them in a single matrix"""
    vec = get_vectorizer(attrs)
    stem = True if attrs['stemming'] == 'true' else False

    X = []
    for column in columns:
        logger.info('- Vectorizing field: {}...'.format(column))
        text = dataframe[column].values

        if stem:
            text = stem_text_input(text)

        X_new = vec.fit_transform(text)
        X = hstack([X, X_new]) if X != [] else X_new
    return X


def get_dataframe_fields(df, fields):
    """Returns the numerical/text field names to be used in this iteration."""
    text_labels = list(df.select_dtypes(include=['object']).columns)
    num_columns = [field for field in fields if field not in text_labels]
    text_columns = [field for field in fields if field in text_labels]
    return num_columns, text_columns


def get_all_vectors(df, attrs):
    """Returna a matrix of the numerical and text vectors (text after vectorisation)."""
    num_columns, text_columns = get_dataframe_fields(df, attrs['fields'])
    X = df[num_columns].values  # Get the numerical fields (ready to use)

    # Check if there are any text columns, and vectorize them
    return hstack([X, get_vectorized_text(df, text_columns, attrs)]) \
        if text_columns else X
