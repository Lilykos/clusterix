import pandas as pd
import numpy as np

from ..controllers.utils import get_last_timestamp
from ..utils.clx_logging import log_info
from ..database.db_funcs import save_csv_to_db, save_txt_to_db


def read_save_to_db(attrs, file_path, timestamp):
    if timestamp != get_last_timestamp():
        log_info(
            'New timestamp {} sent. Saving to db...'.format(timestamp))

        if attrs['type'] == 'text/plain':
            read_save_txt(file_path, timestamp)
        elif attrs['type'] == 'text/csv':
            read_save_csv(file_path, timestamp, attrs['delimiter'])
    else:
        log_info(
            'No new timestamp sent, using the most recent {}...'.format(get_last_timestamp()))


def read_save_csv(file_path, timestamp, delimiter):
    """Read csv file using pandas, and save it to the database."""
    data = pd.read_csv(file_path, sep=delimiter)
    data = data.replace(np.nan, '', regex=True)
    save_csv_to_db(data.columns, data.values, timestamp)


def read_save_txt(file_path, timestamp):
    """Read text file and save it to the database."""
    with open(file_path) as f:
        save_txt_to_db(f.readlines(), timestamp)
