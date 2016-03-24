from clusterix import log_info
from ..controllers.utils import stringify_no_accents
from .models import db, InputItem, InputItemMetadata
"""Functions that save/retrieve data to the database."""


def save_csv_to_db(cols, data, timestamp):
    """
    Get the csv file as a @D array of features, and save them to the db.
    More info on how they are saved can be found in the InputItem docs.

    The array looks like this:
        array([['John', 'Software Dev.', 'Paris'],
               ['Tom', 'Painter', 'Chicago'],
               ['Joe', 'Painting Professional', 'Paris'],
               ['Linda', 'SysAdmin', 'Paris']], dtype=object)

    And the tuples created are:
        [('Name', 'John'), ('Job', 'Software Dev.'), ('City', 'Paris')]

    which is then saved to the db.

    :param cols: The columns/features to be saved.
    :type cols: list

    :param data: An list containing lists of the csv features.
    :type data: numpy array

    :param timestamp: The timestamp of the sent data.
    :type timestamp: int
    """
    for data_row in data:
        data_string_list = map(stringify_no_accents, data_row)
        raw_str = ','.join(data_string_list)
        data_tuples = zip(cols, data_string_list)

        input_item = InputItem(raw_string=raw_str, timestamp=timestamp)
        for datum in data_tuples:
            input_item.input_item_metadata.append(
                InputItemMetadata(name=datum[0], value=datum[1], type='text')
            )
            db.session.add(input_item)

    log_info('Saved {} input items in the db.'.format(len(data)))
    db.session.commit()


def save_txt_to_db(lines, timestamp):
    """Save txt to database"""
    for line in lines:  # TODO: not fully done/tested. Do not use yet.
        db.session.add(InputItem(raw_string=line, timestamp=timestamp))
    db.session.commit()


def get_items_from_db(timestamp, limit=None):
    """Get all the items in the db, specified by the timestamp."""
    return InputItem.query.filter_by(timestamp=timestamp).all()\
        if limit is None \
        else InputItem.query.filter_by(timestamp=timestamp).limit(limit)