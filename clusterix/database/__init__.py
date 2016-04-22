import os
from whoosh.fields import Schema
from whoosh.index import create_in


# noinspection PyAttributeOutsideInit
class WhooshDB(object):
    def __init__(self, path):
        """Create the index folder and save the path."""
        if not os.path.exists(path):
            os.mkdir(path)
        self.path = path

    def initialize(self, fields, dtypes, data):
        """Actual initialization of WhooshDB."""
        self.dtypes = dtypes
        self.schema = Schema(**fields)
        self.index = create_in(self.path, self.schema)

        # Save all records to the db
        writer = self.index.writer()
        for key in data.keys():
            writer.add_document(**data[key])

        writer.commit()

        self.searcher = self.index.searcher()
        self.reader = self.index.reader()

    def get_field_type(self, field):
        """Get the field type by name (used in vectorization etc)."""
        return self.dtypes[field]

    def get_records_with_fields(self, fields):
        """Get a list of all the records, but containing only the requested fields."""
        results = self.get_all()
        for item in results:
            [item.pop(key, None) for key in item.keys() if key not in fields]

        return results

    def get_all(self):
        """Return all records."""
        return [item[1] for item in self.reader.iter_docs()]

    def get_records_by_id(self, ids):
        """Return records based of the provided ids."""
        # TODO: Fix this, as the id field was removed, not working properly
        _ids = [str(i) for i in ids]
        return [item[1] for item in self.reader.iter_docs()
                if str(item[0]) in _ids]

    def search_for(self, words):
        pass