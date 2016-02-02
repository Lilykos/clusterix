from sklearn.base import TransformerMixin


class FuncTransformer(TransformerMixin):
    def __init__(self, func):
        self.func = func

    def fit(self, X, y):
        return self

    def transform(self, X):
        return self.func(X)