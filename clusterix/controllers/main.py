from flask import Blueprint, jsonify, render_template
from ..affiliations.processing import process_affiliation
from ..clustering.clusters import cluster_data

main = Blueprint('main', __name__)


@main.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@main.route('/cluster_country/<path:root_name>', methods=['GET'])
def get_country_cluster(root_name):
    return jsonify(**cluster_data(root_name))


@main.route('/add_affiliation/<path:affiliation>', methods=['POST'])
def add_affiliation(affiliation):
    aff = process_affiliation(affiliation)
    return jsonify(aff) if aff else 'FAILED'
