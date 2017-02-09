from flask import Blueprint, jsonify
from ..misc import search

results = Blueprint('results', __name__)


@results.route('/search', methods=['POST'])
def search_data():
    """Render algorithm options."""
    return jsonify(**{'nodes': search(query)})
