from operator import itemgetter
from ...database.db import vocab_db

not_none = lambda item: item is not None
get_words = lambda ids: [vocab_db.get_vocab_by_id(id) for id in ids]
get_tfidf = lambda words: [vocab_db.tfidf(term) for term in words]


def tfidf_from_ids(clustered_ids):
    """
    Return tfidf scores (by cluster), for the words that belong to the provided ids. E.g:
    {0: [{'term': u'lubid', 'tfidf': 3.1364385032730837},
         {'term': u'gemma', 'tfidf': 3.1364385032730837},
         {'term': u'peeper', 'tfidf': 2.0909590021820557},
         ...]}
    """
    result = {}
    for cluster in clustered_ids.keys():
        total_words = set()
        word_lists = get_words(clustered_ids[cluster])
        for w_list in word_lists:
            total_words = total_words.union(w_list)

        # get the term-score pairs, sort them and return the first 10
        # check for None, as some values are missing - TODO: look into that
        tfidfs = filter(not_none, get_tfidf(total_words))
        result[cluster] = sorted(tfidfs, key=itemgetter('tfidf'), reverse=True)[:10]

    return result