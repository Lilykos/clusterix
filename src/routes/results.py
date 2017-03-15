import json
from flask import Blueprint, jsonify, request, render_template
from ..utils import get_attrs
from ..misc import search, tfidf, get_node_details

results = Blueprint('results', __name__)


@results.route('/search', methods=['POST'])
def search_data():
    """Render algorithm options."""
    query = request.form.get('query')
    return jsonify(**{'results': search(query)})


@results.route('/tfidf', methods=['POST'])
def tf_idf():
    """Returns the TF-IDF score per cluster."""
    attrs = get_attrs(request)
    clusters = json.loads(request.form.get('clusters'))
    return jsonify(**{'results': tfidf(attrs, clusters)})


@results.route('/node_details', methods=['POST'])
def node_details():
    _id = int(request.form.get('id'))
    fields, details = get_node_details(_id)
    return render_template('node_details.html', data={'fields': fields, 'details': details})
