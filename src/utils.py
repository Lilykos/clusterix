import os
import json
import pandas as pd
from werkzeug.utils import secure_filename
from sklearn.externals import joblib
from .config import TEMP_PATH, DATAFRAME_PATH, CLUSTERER_PATH, log


@log('File loaded.')
def save_file(file):
    """Save file to disk."""
    try:
        file_path = os.path.join(TEMP_PATH, secure_filename(file.filename))
        file.save(file_path)
    except KeyError:
        pass  # that means that there was no file sent, so abort


@log('Cluster model saved.')
def save_cluster_model(cluster_model):
    """Pickle cluster model."""
    joblib.dump(cluster_model, CLUSTERER_PATH)


@log('Cluster model loaded.')
def load__cluster_model():
    """Load pickled cluster model."""
    return joblib.load(CLUSTERER_PATH)


@log('Dataframe saved.')
def save_df(df):
    """Pickle dataframe."""
    pd.to_pickle(df, DATAFRAME_PATH)


@log('Dataframe loaded.')
def load_df():
    """Load pickled dataframe."""
    return pd.read_pickle(DATAFRAME_PATH)


def get_attrs(req):
    """Get the data attributes."""
    return json.loads(req.form.get('data'))


def process_and_save_dataframe(filename):
    """
    Create a dataframe from the file, and save the model to the disk.
    Returns a field-type dict, and a boolean of the appearance of text data.
    """
    df = read_file(filename)

    fields = df.columns
    types = list(map(str, df.dtypes))
    has_text = 'object' in types  # object represents the text fields

    save_df(df)
    return dict(list(zip(fields, types))), has_text


def read_file(filename):
    """Process a file and return a dataframe."""
    df = pd.read_csv('{}{}'.format(TEMP_PATH, filename),
                     error_bad_lines=False,
                     encoding='latin-1')

    df.rename(columns=lambda x: x.strip().replace(" ", ""), inplace=True)
    df.fillna(df.median(), inplace=True)
    df.fillna(u'NaN', inplace=True)
    return df
