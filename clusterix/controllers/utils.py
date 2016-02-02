import json
from os.path import join
from werkzeug.utils import secure_filename

from ..config import TEMP_FILE_PATH


def get_data(form, uploaded_files=None):
    """Get the attributes sent from the frontend."""
    data = json.loads(form.get('data'))

    if uploaded_files is not None:
        data.update({
            'file': uploaded_files.to_dict()['file'],
            'type': form.get('type'),
            'timestamp': form.get('timestamp'),
        })

    return data


def save_file_to_disk(file):
    """Save file to the specified (in config) place."""
    saved_file_path = join(TEMP_FILE_PATH, secure_filename(file.filename))
    file.save(saved_file_path)

    return saved_file_path


def get_clustered_ids(data):
    """
    Get a dict of id-cluster pairs and create a dict of cluster-list[ids]. E.g.
    From:   {u'1': 2, u'1006': 1, u'191': 1, u'2': 2, u'276': 1, u'3': 2, u'358': 1, u'6': 3}
    To:     {1: [1006, 191, 276, 358], 2: [1, 2, 3], 3: [6]}
    """
    clustered_ids = {}
    for key in data.keys():
        val = data[key]
        try:
            clustered_ids[val].append(int(key))
        except KeyError:
            clustered_ids[val] = [int(key)]

    return clustered_ids
