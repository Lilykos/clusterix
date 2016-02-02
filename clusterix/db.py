import pandas as pd
from tinydb import TinyDB
from sklearn.externals.joblib import Parallel, delayed

from .config import DB_PATH
from .clustering.utils import get_processed_data

db = TinyDB(DB_PATH)


def get_db_items(ids=None):
    """Get items from TinyDB."""
    return db.all() if ids is None \
        else [db.get(eid=i) for i in ids]


def save_csv_to_db(file_path, data):
    """Save the items of a new file."""
    delimiter = data['csvType']['delimiter']

    # fill median for missing numbers,
    # NaN for strings
    df = pd.read_csv(file_path, sep=delimiter, error_bad_lines=False)
    data = df.fillna(df.median())\
        .fillna('NaN')\
        .T.to_dict()

    # process each item and get a new dict with
    # original/processed/vocabulary values
    processed_items = get_processed_data(data)

    db.purge()
    db.insert_multiple(processed_items)


def get_item_with_attrs(attr, items, keys):
    items = [i[attr] for i in items]
    parallel = Parallel(n_jobs=-1, backend='multiprocessing', verbose=1)

    if attr == 'original':
        return parallel(delayed(_original)(item, i, keys) for i, item in enumerate(items))
    elif attr == 'processed':
        return parallel(delayed(_processed)(item, keys) for item in items)
    elif attr == 'vocabulary':
        return parallel(delayed(_vocabulary)(item, keys) for item in items)


def _processed(item, keys):
    return {key: item[key] for key in keys}


def _original(item, i, keys):
    res = {key: item[key] for key in keys}
    res['id'] = i + 1
    return res


def _vocabulary(item, keys):
    return ' '.join(item[key] for key in keys)