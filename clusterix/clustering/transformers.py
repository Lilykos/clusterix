import numpy as np

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import HashingVectorizer, TfidfVectorizer, CountVectorizer

TOKEN_PATTERN = r"\b\w+\b"  # Keeps single letter attrs
vectorizers = {
    'hashing': HashingVectorizer(n_features=2 ** 12, non_negative=True, norm=None),
    'tfidf': TfidfVectorizer(max_features=2 ** 12, norm=None, token_pattern=TOKEN_PATTERN),
    'count': CountVectorizer(max_features=2 ** 12, token_pattern=TOKEN_PATTERN)
}


class ItemSelector(BaseEstimator, TransformerMixin):
    """Selects items from a list of dicts, based on the key."""
    def __init__(self, key):
        self.key = key

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return [item[self.key] for item in X]


class MissingValuesTransformer(BaseEstimator, TransformerMixin):
    """Replace missing values according to the type"""
    @staticmethod
    def _empty_to_nan(i):
        return 'NaN' if i == '' else i

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return [self._empty_to_nan(item) for item in X]


class Vectorizer(BaseEstimator, TransformerMixin):
    """If the values of the list are numeric, it returns them as they are, else it uses a vectorizer."""
    def __init__(self, vec_name, field_type):
        self.vectorizer = vectorizers[vec_name]
        self.type = field_type

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        if self.type == 'object':
            return self.vectorizer.fit_transform(X)
        else:
            return np.array([[i] for i in X])


class Scaler(BaseEstimator, TransformerMixin):
    """Scales a list of features by the provided number."""
    def __init__(self, scale):
        self.scale = int(scale)

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return self.scale * X


class DecompositionTransformer(BaseEstimator, TransformerMixin):
    """Transforms to 2D."""
    def __init__(self, decomposition_instance=None):
        self.to_2d = decomposition_instance if decomposition_instance \
            else TruncatedSVD()

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return self.to_2d.fit_transform(X)
