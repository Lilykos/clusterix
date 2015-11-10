from flask import Blueprint, jsonify
from ..affiliations.processing import process_affiliation

main = Blueprint('main', __name__)


@main.route('/add_affiliation/<path:affiliation>', methods=['POST'])
def add_affiliation(affiliation):
    aff = process_affiliation(affiliation)
    return jsonify(aff) if aff else 'FAILED'


@main.route('/upload_xml', methods=['POST'])
def upload_xml():
    # TODO: HANDLE XML UPLOAD AND CALL parse_xml function
    pass