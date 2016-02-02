from flask import Blueprint, render_template, request, jsonify
from ..clusterers.block_clustering import block_cluster

from input import (save_file_to_disk,
                   get_attr_from_request,
                   read_save_csv,
                   read_save_txt)


main = Blueprint('main', __name__)


@main.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@main.route('/upload', methods=['POST'])
def data_file_input():
    file, type, timestamp, algorithms, csv_fields, block_by = get_attr_from_request(request.files, request.form)
    file_path = save_file_to_disk(file)

    # if type == 'text/plain':
    #     read_save_txt(file_path, timestamp)
    # elif type == 'text/csv':
    #     read_save_csv(file_path, timestamp)

    for alg in algorithms:
        if alg == 'kmeans':
            pass
        if alg == 'bcluster':
            result = block_cluster(csv_fields, block_by)


    return jsonify(**result)







# @main.route('/cluster_data', methods=['POST'])
# def get_country_cluster():
#     attrs = json.loads(request.form.get('csvFields'))
#     # algorithm = json.loads(request.form.get('algorithmData'))
#
#     result = BlockClusterer.cluster_data(attrs, 'Survived')
#     return jsonify(**result)
#
#
# @main.route('/add_affiliation/<path:affiliation>', methods=['POST'])
# def add_affiliation(affiliation):
#     pass
#     aff = process_affiliation(affiliation)
#     return jsonify(aff) if aff else 'FAILED'
