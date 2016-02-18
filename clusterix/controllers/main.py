from flask import Blueprint, render_template, request, jsonify
from ..clusterers.block_clustering import block_cluster
from ..clusterers.kmeans import kmeans_cluster

from .input import (save_file_to_disk,
                    get_attr_from_request,
                    read_save_csv,
                    read_save_txt)


main = Blueprint('main', __name__)
current_timestamp = 0


@main.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@main.route('/upload', methods=['POST'])
def data_file_input():
    file, type, timestamp, algorithms,\
        csv_fields, block_by, delimiter = get_attr_from_request(request.files, request.form)
    file_path = save_file_to_disk(file)

    global current_timestamp

    if timestamp != current_timestamp:
        if type == 'text/plain':
            read_save_txt(file_path, timestamp)
        elif type == 'text/csv':
            read_save_csv(file_path, timestamp, delimiter)
        current_timestamp = timestamp

    for alg in algorithms:
        if alg == 'kmeans':
            result = kmeans_cluster()
        if alg == 'bcluster':
            result = block_cluster(csv_fields, block_by, timestamp)

    return jsonify(**result)
