from flask import Blueprint, render_template, request, jsonify
from .. import save_file, process_and_save_dataframe
from ..config import algorithm_paths

main = Blueprint('main', __name__)


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
    return render_template(algorithm_paths[request.form['algorithm']])


@main.route('/load_file', methods=['POST'])
def load_file():
    """
    Load and save the file as a pickled dataframe, to be used later.
    Returns the rendered fields of the processing space.
    """
    file = request.files['file']
    save_file(file)

    fields_with_types, numeric_fields, has_text = process_and_save_dataframe(file.filename)
    return jsonify(**{
        'fields': render_template('processing/fields.html',
                                  fields={'all': fields_with_types.keys(), 'scatter': numeric_fields}),
        'algorithms': render_template('processing/algorithms.html'),
        'textOptions': render_template('processing/text.html'),
        'hasText': has_text
    })
