import os
import json
import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename
from sklearn.externals import joblib
from .config import TEMP_PATH, DECOMPOSITION_MODEL_PATH, \
    DATAFRAME_PATH, CLUSTERER_PATH, X_PATH, log


# Clustering
@log('- Cluster model saved.')
def save_cluster_model(model):
    """Pickle cluster model."""
    joblib.dump(model, CLUSTERER_PATH)


@log('- Cluster model loaded.')
def load_cluster_model():
    """Load pickled cluster model."""
    return joblib.load(CLUSTERER_PATH)


# Decomposition
@log('- Decomposition model saved.')
def save_decomposition(model, name):
    """Pickle dec. model."""
    joblib.dump(model, DECOMPOSITION_MODEL_PATH.format(name))


@log('- Decomposition model loaded.')
def load_decomposition(name):
    """Load pickled dec. model."""
    return joblib.load(DECOMPOSITION_MODEL_PATH.format(name))


# Dataframe
@log('- Dataframe saved.')
def save_df(df):
    """Pickle dataframe."""
    pd.to_pickle(df, DATAFRAME_PATH)


@log('- Dataframe loaded.')
def load_df():
    """Load pickled dataframe."""
    return pd.read_pickle(DATAFRAME_PATH)


# X
@log('- X saved.')
def save_X(X):
    """Pickle X."""
    np.save(X_PATH, X)


@log('- X loaded.')
def load_X():
    """Load pickled X."""
    return np.load(X_PATH)


def get_attrs(req):
    """Get the data attributes."""
    return json.loads(req.form.get('data'))


@log('- File loaded.')
def save_file(file):
    """Save file to disk."""
    try:
        file_path = os.path.join(TEMP_PATH, secure_filename(file.filename))
        file.save(file_path)
    except KeyError:
        pass  # no file sent, abort


def process_and_save_dataframe(filename):
    """
    Create a dataframe from the file, and save the model to the disk.
    Returns a field-type dict, and a boolean of the appearance of text data.
    """
    df = read_file(filename)
    save_df(df)

    fields = df.drop(['clx_cluster', 'clx_id'], axis=1).columns
    types = list(map(str, df.dtypes))
    has_text = 'object' in types  # 'object' represents the text fields
    numeric_fields = [field for field in fields if df[field].dtype != 'object']

    return dict(list(zip(fields, types))), numeric_fields, has_text


def read_file(filename):
    """Process a file and return a dataframe."""
    df = pd.read_csv('{}{}'.format(TEMP_PATH, filename),
                     error_bad_lines=False,
                     encoding='latin-1')

    df.rename(columns=lambda x: x.strip().replace(" ", ""), inplace=True)
    df.fillna(df.median(), inplace=True)
    df.fillna(u'NaN', inplace=True)

    df['clx_id'] = df.index                             # index for search, etc
    df['clx_cluster'] = [0 for _ in range(len(df))]     # cluster init 0
    return df


@log('- Plot coordinates created.')
def scatterplot(coords, labels, ids):
    """
    Get a dictionary that will be converted to json, and contains all the scatterplot visualization data.
    Return example:
        {'nodes': [
               {'clx_cluster': 0, 'clx_id': 2, 'x': 2.658062848683116e-16, 'y': 1.7320508075688774},
               {'clx_cluster': 1, 'clx_id': 1, x': 1.5034503553765397, 'y': 0.0},
                ..............]}
    """
    nodes = [{
        'x': coord[0],
        'y': coord[1],
        'clx_cluster': int(label),
        'clx_id': int(_id)
        } for coord, label, _id in zip(coords, labels, ids)]
    return nodes
