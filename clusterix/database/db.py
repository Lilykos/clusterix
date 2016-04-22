import pandas as pd

from ..log import log_info
from ..database.utils import get_whoosh_fields, get_processed
from ..database import WhooshDB
from ..config import TEMP_RAW_INPUT, TEMP_PROCESSED_INPUT

original_db = WhooshDB(TEMP_RAW_INPUT)
processed_db = WhooshDB(TEMP_PROCESSED_INPUT)


def save_csv(file_path, attrs):
    """
    Save the items of a new file.
    1. Save original data.
    2. Save processed data for clustering.
    """
    df = pd.read_csv(file_path,
                     sep=attrs['csvType']['delimiter'],
                     error_bad_lines=False,
                     encoding='utf-8')

    # fill median for missing numbers, NaN for strings
    data = df.fillna(df.median())\
        .fillna(u'NaN')\
        .T.to_dict()

    # get fields and types both in Whoosh field types and pandas
    # they are used for different things
    dtypes = df.dtypes.apply(str).to_dict()
    fields = get_whoosh_fields(dtypes)

    # Save original data
    log_info('Creating Whoosh DB (raw data)...')
    original_db.initialize(fields, dtypes, data)

    # Save processed data
    processed_data = pd.DataFrame(
        get_processed(data, dtypes)
    ).T.to_dict()

    log_info('Creating Whoosh DB (processed data)...')
    processed_db.initialize(fields, dtypes, processed_data)