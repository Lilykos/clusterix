import json
import os
from werkzeug.utils import secure_filename

from ..config import TEMP_PATH
from ..database.db import save_csv


def get_attrs(request):
    """Get the attributes sent from the frontend."""
    attrs = json.loads(request.form.get('data'))

    if request.files:
        attrs.update({
            'file': request.files.to_dict()['file'],
            'type': request.form.get('type'),
            'timestamp': request.form.get('timestamp'),
        })

    return attrs


def save_file_if_exists(attrs):
    """Save file to disk, and according to the type, save to the DB."""
    try:
        f = attrs['file']
        file_path = os.path.join(TEMP_PATH, secure_filename(f.filename))
        f.save(file_path)

        if attrs['type'] == 'text/csv':
            save_csv(file_path, attrs)

    except KeyError:
        pass  # that means that there was no file sent, so abort
