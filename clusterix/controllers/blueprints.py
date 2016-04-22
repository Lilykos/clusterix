from flask import Blueprint, render_template, request, jsonify

from ..controllers.utils import get_attrs, save_file_if_exists
from ..clustering.cluster import cluster_data

main = Blueprint('main', __name__)


@main.route('/', methods=['POST', 'GET'])
def index():
    """Main page."""
    return render_template('index.html')


@main.route('/upload_and_cluster', methods=['POST'])
def upload_file():
    """
    Read data attributes and save file (if it exists), do the clustering
    and return the correct results to the frontend.
    """
    attrs = get_attrs(request)
    save_file_if_exists(attrs)

    # Get the algorithm results
    result = cluster_data(attrs)
    return jsonify(**result)


@main.route('/metrics', methods=['POST'])
def get_term_info():
    pass
    # clustered_ids = get_clustered_ids(json.loads(request.data))
    #
    # result = get_terms_json(clustered_ids)
    # return jsonify(**result)