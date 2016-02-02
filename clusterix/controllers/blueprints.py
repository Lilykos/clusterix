import json
from flask import Blueprint, render_template, request, jsonify

from ..db import save_csv_to_db
from ..controllers.utils import get_data, save_file_to_disk, get_clustered_ids
from ..clustering.cluster import cluster_data
from ..clustering.results.metrics import get_terms_json

main = Blueprint('main', __name__)


@main.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@main.route('/upload_with_file', methods=['POST'])
def upload_file():
    data = get_data(request.form, request.files)
    file_path = save_file_to_disk(data['file'])

    # Read file and save data to the db.
    if data['type'] == 'text/csv':
        save_csv_to_db(file_path, data)

    # Get the algorithm results
    result = cluster_data(data)
    return jsonify(**result)


@main.route('/upload_data_only', methods=['POST'])
def upload_data():
    data = get_data(request.form)

    # Get the algorithm results
    result = cluster_data(data)
    return jsonify(**result)


@main.route('/metrics', methods=['POST'])
def get_term_info():
    clustered_ids = get_clustered_ids(json.loads(request.data))

    result = get_terms_json(clustered_ids)
    return jsonify(**result)