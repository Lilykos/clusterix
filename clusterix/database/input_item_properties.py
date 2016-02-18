from ..database.models import InputItem, InputItemMetadata


def get_keys_from_db():
    items = InputItemMetadata.query.distinct(InputItemMetadata.name)
    return [item.name for item in items.all()]


def get_items_from_db(timestamp, limit=None):
    return InputItem.query.filter_by(timestamp=timestamp).all() if limit is None \
        else InputItem.query.filter_by(timestamp=timestamp).limit(limit)
