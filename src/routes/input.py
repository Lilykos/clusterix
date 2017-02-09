from flask import Blueprint, render_template, request, jsonify
from .. import save_file, process_and_save_dataframe
from ..cluster import cluster_data, get_projection, predict_data
from ..misc import tfidf
from ..utils import get_attrs
from ..config import algorithms

main = Blueprint('main', __name__)


############
# TEMPLATING
############
@main.route('/', methods=['POST', 'GET'])
def index():
    """Main page."""
    return render_template('index.html')


@main.route('/loading_screen', methods=['POST'])
def loading_screen():
    """Loading screen of Clusterix."""
    return render_template('loading.html')


@main.route('/algorithm_options', methods=['POST'])
def algorithm_options():
    """Render algorithm options."""
    return render_template(algorithms[request.form['algorithm']])


###################
# PROCESSING NEEDED
###################
@main.route('/load_file', methods=['POST'])
def load_file():
    """
    Load and save the file as a pickled dataframe, to be used later.
    Returns the rendered fields of the processing space.
    """
    file = request.files['file']
    save_file(file)

    fields_with_types, has_text = process_and_save_dataframe(file.filename)
    return jsonify(**{
        'fields': render_template('processing/fields.html', fields=fields_with_types.keys()),
        'algorithms': render_template('processing/algorithms.html'),
        'textOptions': render_template('processing/text.html'),
        'hasText': has_text
    })


@main.route('/get_clustering_results', methods=['POST'])
def get_clustering_results():
    """
    Returns a dict with the plot coordinates of the clusted data,
    and the TF-IDF scores, if we have text attributes.
    """
    attrs = get_attrs(request)
    return jsonify(**{
        'cluster_results': cluster_data(attrs),
        'tfidf': tfidf(attrs)
    })


@main.route('/get_projection', methods=['POST'])
def get_projection_results():
    """
    Returns a dict with the plot coordinates of the clusted data,
    and the TF-IDF scores, if we have text attributes.
    """
    attrs = get_attrs(request)
    return jsonify(**{'cluster_results': {'nodes': get_projection(attrs)}})


@main.route('/predict_cluster', methods=['POST'])
def predict_cluster():
    """Predict the cluster of the imput row."""
    # attrs = get_attrs(request)
    # return jsonify(**{'cluster_results': {'nodes': predict_data(attrs)}})
    pass
