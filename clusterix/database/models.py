import os
from math import log
from copy import deepcopy

from whoosh.fields import Schema, TEXT
from whoosh.index import create_in
from whoosh.qparser import QueryParser

from ..log import log_warn


# noinspection PyAttributeOutsideInit
class WhooshProcessedDB(object):
    def __init__(self, path):
        """Create the index folder and save the path."""
        if not os.path.exists(path):
            os.mkdir(path)
        self.path = path

    def initialize(self, fields, dtypes, data):
        """Actual initialization of WhooshDB."""
        self.schema = Schema(**fields)
        self.index = create_in(self.path, self.schema)

        writer = self.index.writer()
        for key in data.keys():
            writer.add_document(**data[key])
        writer.commit()

        # Various relevant attributes
        self.field_names = dtypes.keys()
        self.dtypes = dtypes
        self.searcher = self.index.searcher()
        self.reader = self.index.reader()
        self.all_documents = [item[1] for item in self.reader.iter_docs()]

    def get_field_type(self, field):
        """Get the field type by name (used in vectorization etc)."""
        return self.dtypes[field]

    def get_records_with_fields(self, fields):
        """Get a list of all the records, but containing only the requested fields."""
        results = deepcopy(self.all_documents)
        for item in results:
            for key in item.keys():
                if key not in fields:
                    item.pop(key, None)
        return results

    def get_records_by_id(self, ids):
        """Return records based of the provided ids."""
        return [item[1] for item in self.reader.iter_docs() if item[0] in ids]


# noinspection PyAttributeOutsideInit
class WhooshVocabularyDB(object):
    def __init__(self, path):
        """Create the index folder and save the path."""
        if not os.path.exists(path):
            os.mkdir(path)
        self.path = path

    def initialize(self, data):
        """Initialize with the vocabulary data."""
        self.schema = Schema(content=TEXT(stored=True))
        self.index = create_in(self.path, self.schema)

        writer = self.index.writer()
        for doc in data:
            writer.add_document(content=doc)
        writer.commit()

        self.searcher = self.index.searcher()
        self.reader = self.index.reader()
        self.doc_num = self.reader.doc_count()
        self.parser = QueryParser('content', schema=self.schema)

        self.data = [row.split() for row in data]
        self.words_per_doc = [len(row) for row in self.data]

        self.containing = lambda term: 1 + self.searcher.doc_frequency("content", term)

    def get_vocab_by_id(self, id):
        return self.data[id]

    def search_for(self, term):
        query = self.parser.parse(term)
        result = self.searcher.search(query, limit=None)
        return list(result.docs())

    def get_relevant_terms(self, term):
        docs = self.searcher.document_numbers(content=term)
        return self.searcher.key_terms(docs, 'content', numterms=10)

    def tfidf(self, term):
        try:
            docs = self.search_for(term)
            total_words = sum(self.words_per_doc[i] for i in docs)

            # TF: frequency if the term/total words in docs the term appears in
            # IDF: total docs/docs containing this word
            tf = self.searcher.frequency('content', term) / (total_words * 1.0)
            idf = log(self.doc_num / self.containing(term))

            return {
                'term': term,
                'tfidf': tf * idf
            }
        except Exception:
            log_warn(u'Term not found: {}'.format(term))
            return None
