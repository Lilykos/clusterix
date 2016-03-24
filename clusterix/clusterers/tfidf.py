import math
from collections import Counter
from operator import itemgetter

flat_list = lambda l: [item for sub_list in l for item in sub_list]


def term_frequency(vocab_by_cluster, number=10):
    """
    Get the term frequency by cluster, using the vocabulary.

    :param vocab_by_cluster: A list o lists, each list representing a cluster.
    :param number: The top N terms to return.
    """
    flat_vocab = ' '.join(flat_list(vocab_by_cluster)).split()
    total_words = dict(Counter(flat_vocab))

    term_freq_by_cluster = []
    for cluster in vocab_by_cluster:
        words = ' '.join([item for item in cluster]).split()
        counter = dict(Counter(words).most_common(number))

        items = []
        for key in counter.keys():
            items.append({'term': key, 'freq': counter[key], 'total': total_words[key]})

        term_freq_by_cluster.append(sorted(items, key=itemgetter('total'), reverse=True))
    return term_freq_by_cluster


def tfidf(word, doc, doc_list):
    def _n_containing(word):
        return sum(1 for doc in doc_list if word in doc)

    tf = float(doc.split().count(word)) / len(doc.split())
    idf = 1.0 + math.log(float(len(doc_list)) / (1 + _n_containing(word)))

    return tf * idf


def get_tfidf(docs_by_cluster, number=10):
    """
    Get the Tf-Idf score of words in clustered documents, by cluster.
    The total Idf is used (of all documents), and the Tf of the cluster.

    :param docs_by_cluster: list of clustered documents
    """
    doc_list = flat_list(docs_by_cluster)

    tf_idf_by_cluster = []
    for cluster in docs_by_cluster:
        doc = ' '.join(cluster)

        # Get the tf-idf scores
        scores = [(word, round(tfidf(word, doc, doc_list), 5))  # tuple (word, score)
                  for word in set(doc.split())]

        items = []
        for item in sorted(scores, key=lambda x: x[1], reverse=True)[:number]:
            items.append({'term': item[0], 'score': item[1]})

        tf_idf_by_cluster.append(sorted(items, key=itemgetter('score'), reverse=True))
    return tf_idf_by_cluster