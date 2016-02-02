from ..database.models import InputItem, InputItemMetadata


def get_keys_from_db():
    items = InputItemMetadata.query.distinct(InputItemMetadata.name)
    return [item.name for item in items.all()]


def get_items_from_db(limit=None):
    return InputItem.query.all() if limit is None \
        else InputItem.query.limit(limit)

# class InputItemProperties():
#
#     @staticmethod
#     def get_keys():
#         items = InputItemMetadata.query.distinct(InputItemMetadata.name)
#         return [item.name for item in items.all()]
#
#     @staticmethod
#     def get_values(field, X=None):
#         items = InputItemMetadata.query.filter_by(name=field).all()
#         return [item.value for item in items]
#
#     @staticmethod
#     def get_all_raw_string():
#         items = InputItem.query.all()
#         return [item.raw_string for item in items]