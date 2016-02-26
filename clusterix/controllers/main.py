from flask import Blueprint, render_template, request, jsonify

from .input import read_save_to_db
from ..controllers.utils import get_attr_from_request, save_file_to_disk
from ..clusterers.block_clustering import block_cluster
from ..clusterers.kmeans import kmeans_cluster


main = Blueprint('main', __name__)


@main.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@main.route('/upload', methods=['POST'])
def data_file_input():
    attrs = get_attr_from_request(request.files, request.form)
    file_path = save_file_to_disk(attrs['file'])

    timestamp, block_by, csv_fields = \
        attrs['timestamp'], attrs['block_by'], attrs['csv_fields']

    # Read file and save data to the db.
    read_save_to_db(attrs, file_path, timestamp)

    # Get the algorithm results
    for alg in attrs['algorithms']:
        if alg == 'kmeans':
            result = kmeans_cluster()
        if alg == 'bcluster':
            result = block_cluster(csv_fields, block_by, timestamp, 'count')

    return jsonify(**result)
