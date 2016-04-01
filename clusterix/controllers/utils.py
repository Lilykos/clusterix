import json
import os
from werkzeug.utils import secure_filename

from ..config import TEMP_FILE_PATH
from ..utils.lang import strip_accents
from ..database.models import InputItem


def stringify_no_accents(text):
    """Turn the input into string and strip accents."""
    return strip_accents(str(text))


def get_attr_from_request(form, uploaded_files=None):
    """Get the attributes sent from the frontend."""
    attrs = {
        'algorithms': form.get('algorithms').split(','),
        'csv_fields': json.loads(form.get('csv_fields')),
        'block_by': form.get('block_by'),
        'delimiter': form.get('delimiter'),
        'vectorizer': form.get('vectorizer'),
        'k_num': form.get('k_num'),
        'bcluster_distance': form.get('bcluster_distance'),
        'affinity': form.get('affinity')
    }

    if uploaded_files is not None:
        attrs.update({
            'file': uploaded_files.to_dict()['file'],
            'type': form.get('type'),
            'timestamp': form.get('timestamp'),
        })

    return attrs


def save_file_to_disk(file):
    """Save file to the specified (in config) place."""
    saved_file_path = os.path.join(
        TEMP_FILE_PATH, secure_filename(file.filename)
    )
    file.save(saved_file_path)
    return saved_file_path


def get_last_timestamp():
    """Returns the last used timestamp, to check whether a new file is to be used."""
    result = InputItem.query.with_entities(InputItem.timestamp)\
        .distinct()\
        .order_by(InputItem.timestamp.desc())\
        .first()
    return result.timestamp \
        if result is not None else None