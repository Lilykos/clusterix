import os
from flask import json
from werkzeug.utils import secure_filename

from ..config import TEMP_FILE_PATH
from ..utils.lang import strip_accents_from_str
from ..database.database import save_csv_to_db, save_txt_to_db

import pandas as pd


def stringify_no_accents(input):
    return strip_accents_from_str(str(input))


def get_attr_from_request(files, form):
    file = files.to_dict()['file']
    type = form.get('type')
    timestamp = form.get('timestamp')
    algorithms = form.get('algorithms').split(',')
    csv_fields = json.loads(form.get('csv_fields'))
    block_by = form.get('block_by')

    return file, type, timestamp, algorithms, csv_fields, block_by


def save_file_to_disk(file):
    saved_file_path = os.path.join(
        TEMP_FILE_PATH, secure_filename(file.filename)
    )
    file.save(saved_file_path)
    return saved_file_path


def read_save_csv(file_path, timestamp):
    data = pd.read_csv(file_path)
    cols = data.columns

    for data_row in data.values:
        data_string_list = map(stringify_no_accents, data_row)

        raw_str = ','.join(data_string_list)
        data = zip(cols, data_string_list)
        save_csv_to_db(raw_str, data, timestamp)


def read_save_txt(file_path, timestamp):
    with open(file_path) as f:
        save_txt_to_db(f.readlines(), timestamp)
