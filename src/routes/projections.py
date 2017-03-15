import json
from flask import Blueprint, jsonify, request
from ..cluster import cluster_data, get_projection, predict_data
from ..utils import get_attrs, scatterplot
from ..misc import get_field_data

projections = Blueprint('projections', __name__)


@projections.route('/get_clustering_results', methods=['POST'])
def get_clustering_results():
    """
    Returns a dict with the plot coordinates of the clusted data,
    and the TF-IDF scores, if we have text attributes.
    """
    attrs = get_attrs(request)
    return jsonify(**{'results': cluster_data(attrs)})


@projections.route('/get_projection', methods=['POST'])
def get_projection_results():
    """
    Returns a dict with the plot coordinates of the clusted data,
    and the TF-IDF scores, if we have text attributes.
    """
    attrs = get_attrs(request)
    coords, df = get_projection(attrs)
    return jsonify(**{'results': scatterplot(coords, [0 for _ in range(len(df))], df['clx_id'])})


@projections.route('/predict_cluster', methods=['POST'])
def predict_cluster():
    """Predict the cluster of the imput row."""
    # attrs = get_attrs(request)
    # return jsonify(**{'cluster_results': {'nodes': predict_data(attrs)}})
    pass


@projections.route('/scatterplot_matrix', methods=['POST'])
def get_scatterplot_coordinates():
    attrs = get_attrs(request)
    return jsonify(**{'results': get_field_data(attrs['scatterFields'])})
