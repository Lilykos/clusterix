from flask import Blueprint, render_template, request, jsonify


from .input import read_save_to_db
from ..controllers.utils import get_attr_from_request, save_file_to_disk
from ..clusterers.clustering import get_cluster_result


main = Blueprint('main', __name__)


@main.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@main.route('/upload', methods=['POST'])
def data_file_input():
    attrs = get_attr_from_request(request.files, request.form)
    file_path = save_file_to_disk(attrs['file'])

    # Read file and save data to the db.
    read_save_to_db(attrs, file_path, attrs['timestamp'])

    # Get the algorithm results
    result = get_cluster_result(attrs)
    return jsonify(**result)
