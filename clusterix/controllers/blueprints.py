import json
from flask import Blueprint, render_template, request, jsonify

from ..controllers.utils import get_attrs, save_file_if_exists
from ..clustering.cluster import cluster_data
from ..clustering.utils import get_clustered_ids
from ..clustering.results.metrics import tfidf_from_ids
from ..database.db import vocab_db

main = Blueprint('main', __name__)


@main.route('/', methods=['POST', 'GET'])
def index():
    """Main page."""
    return render_template('index.html')


@main.route('/upload_and_cluster', methods=['POST'])
def upload_and_cluster():
    """
    Read data attributes and save file (if it exists), do the clustering
    and return the correct results to the frontend.
    """
    attrs = get_attrs(request)
    save_file_if_exists(attrs)

    # Get the algorithm results
    result = cluster_data(attrs)
    return jsonify(**result)


@main.route('/tfidf', methods=['POST'])
def tfidf():
    """Get a list of id-cluster pairs, and return clustered term-tfidf pairs."""
    clustered_ids = get_clustered_ids(
        json.loads(request.form.get('ids'))
    )

    result = tfidf_from_ids(clustered_ids)
    return jsonify(**{'tfidf_metrics': result})


@main.route('/search', methods=['POST'])
def search():
    """Search a term and return the ids of the corresponding records."""
    result = vocab_db.search_for(request.data)
    return jsonify(**{'ids': result})


@main.route('/content', methods=['POST'])
def content():
    ids = json.loads(request.form.get('ids'))

    content = {}
    for id in ids:
        content[id] = {
            'text': ' '.join(vocab_db.get_vocab_by_id(id))
        }

    return jsonify(**{'content': content})
