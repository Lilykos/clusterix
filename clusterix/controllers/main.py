from flask import Blueprint, render_template, request, jsonify
import clusterix

from .input import read_save_to_db
from ..controllers.utils import get_attr_from_request, get_attr_from_request_with_files, save_file_to_disk
from ..clusterers.cluster import get_cluster_result


main = Blueprint('main', __name__)


@main.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@main.route('/update', methods=['GET'])
def update():
    return clusterix.update_msg


@main.route('/upload', methods=['POST'])
def data_file_input():
    # re-init the update message for the loading screen
    clusterix.update_msg = ''

    attrs = get_attr_from_request_with_files(request.files, request.form)
    file_path = save_file_to_disk(attrs['file'])

    # Read file and save data to the db.
    read_save_to_db(attrs, file_path, attrs['timestamp'])

    # Get the algorithm results
    result = get_cluster_result(attrs)
    return jsonify(**result)


@main.route('/upload_data', methods=['POST'])
def upload_data():
    pass
    # attrs = get_attr_from_request(request.form)
