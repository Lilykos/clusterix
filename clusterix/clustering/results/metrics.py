import math
from collections import Counter
from operator import itemgetter
from ...db import get_db_items, get_item_with_attrs


def get_terms_json(clustered_ids):
    """
    By passing a list of clustered ids, we get the info below:
        {'term_frequencies': [
                [{'freq': 1, 'term': u'chicago', 'total': 1},
                 {'freq': 1, 'term': u'painter', 'total': 1},
                 {'freq': 1, 'term': u'tom', 'total': 1}],
                [{'freq': 3, 'term': u'paris', 'total': 3},
                 {'freq': 1, 'term': u'dev', 'total': 1},
                 {'freq': 1, 'term': u'sysadmin', 'total': 1},
                 {'freq': 1, 'term': u'joe', 'total': 1},
                 {'freq': 1, 'term': u'linda', 'total': 1},
                 {'freq': 1, 'term': u'professional', 'total': 1},
                 {'freq': 1, 'term': u'john', 'total': 1},
                 {'freq': 1, 'term': u'painting', 'total': 1},
                 {'freq': 1, 'term': u'software', 'total': 1}]],
         'tfidf': [
                [{'score': 0.56438, 'term': u'tom'},
                 {'score': 0.56438, 'term': u'painter'},
                 {'score': 0.56438, 'term': u'chicago'}],
                [{'score': 0.27273, 'term': u'paris'},
                 {'score': 0.15392, 'term': u'dev'},
                 {'score': 0.15392, 'term': u'sysadmin'},
                 {'score': 0.15392, 'term': u'joe'},
                 {'score': 0.15392, 'term': u'linda'},
                 {'score': 0.15392, 'term': u'professional'},
                 {'score': 0.15392, 'term': u'john'},
                 {'score': 0.15392, 'term': u'painting'},
                 {'score': 0.15392, 'term': u'software'}]]
        }
    :param clustered_ids:
    :return:
    """
    results = {
        'term_frequencies': [],
        'tfidf': []
    }

    for id in clustered_ids.keys():
        items = get_db_items(clustered_ids[id])

        # get the vocabulary of each item
        vocab = get_item_with_attrs('vocabulary', items, ['TITLE'])
        res = term_frequency(vocab)

    return results


def tfidf(docs_by_cluster, number=10):
    """
    Get the Tf-Idf score of words in clustered documents, by cluster.
    The total Idf is used (of all documents), and the Tf of the cluster.

    :param docs_by_cluster: list of clustered documents
    """
    def _tfidf(word, doc, doc_list):
        tf = float(doc.split().count(word)) / len(doc.split())
        idf = 1.0 + math.log(float(len(doc_list)) / (1 + _n_containing(word)))
        return tf * idf

    def _n_containing(word):
        return sum(1 for doc in doc_list if word in doc)

    doc_list = flat_list(docs_by_cluster)
    tf_idf_by_cluster = []

    for clustered_doc in docs_by_cluster:
        doc = ' '.join(clustered_doc)

        # Get the tf-idf scores
        scores = [(word, round(_tfidf(word, doc, doc_list), 5))  # tuple (word, score)
                  for word in set(doc.split())]

        items = []
        for item in sorted(scores, key=lambda x: x[1], reverse=True)[:number]:
            items.append({'term': item[0], 'score': item[1]})

        tf_idf_by_cluster.append(sorted(items, key=itemgetter('score'), reverse=True))
    return tf_idf_by_cluster