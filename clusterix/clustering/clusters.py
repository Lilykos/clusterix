from functools import partial

from sklearn.base import TransformerMixin
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.pipeline import make_union, make_pipeline

from ..affiliations.affiliation_props import AffiliationProperties
from d3_json_converter import get_d3_json


class FuncTransformer(TransformerMixin):
    def __init__(self, func):
        self.func = func

    def fit(self, X, y):
        return self

    def transform(self, X):
        return self.func(X)


def cluster_data(root_name):

    def _reweight(x, scale=1):
        """ Reweight the attributes"""
        return scale * x

    hasher = HashingVectorizer(n_features=2**12, non_negative=True, norm=None)

    props = AffiliationProperties

    tf = make_union(

        # Countries / cities are a priority
        make_pipeline(FuncTransformer(props.get_country_code), hasher,
                      FuncTransformer(partial(_reweight, scale=1))),

        make_pipeline(FuncTransformer(props.get_region), hasher,
                      FuncTransformer(partial(_reweight, scale=70))),

        make_pipeline(FuncTransformer(props.get_settlement), hasher,
                      FuncTransformer(partial(_reweight, scale=50))),


        # First institutes then departments
        make_pipeline(FuncTransformer(props.get_institution), hasher,
                      FuncTransformer(partial(_reweight, scale=50))),

        make_pipeline(FuncTransformer(props.get_department), hasher,
                      FuncTransformer(partial(_reweight, scale=20))),

        make_pipeline(FuncTransformer(props.get_laboratory), hasher,
                      FuncTransformer(partial(_reweight, scale=10))),
    )

    affiliations = props.get_all_affiliations()
    X = tf.transform(affiliations).toarray()

    from beard.clustering import ScipyHierarchicalClustering, BlockClustering
    clustering = ScipyHierarchicalClustering(method="average", affinity="cityblock", threshold=100.)

    block_clustering = BlockClustering(base_estimator=clustering, blocking="precomputed", verbose=3, n_jobs=5)
    block_clustering.fit(X, blocks=[i.country for i in affiliations])

    country = block_clustering.clusterers_[root_name]
    labels = [i.raw_string for i in affiliations if i.country == root_name]

    return get_d3_json(country.linkage_, labels, root_name)
