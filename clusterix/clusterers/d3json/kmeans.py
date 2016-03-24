from ..tfidf import term_frequency, get_tfidf


def get_kmeans_json(coords, labels, centroids, n_clusters, items, vocab):
    """Get a dictionary that will be converted to json, and contains all the visualization data."""
    nodes = []
    docs_by_cluster = []

    for cluster in xrange(n_clusters):
        # init word counter for each cluster
        docs_by_cluster.append([])

        for i in xrange(len(labels)):
            # Add nodes
            if labels[i] == cluster:
                nodes.append({
                    'x': coords[i][0],
                    'y': coords[i][1],
                    'content': items[i],
                    'cluster': cluster,
                    'isCentroid': False
                })

                # Add words for tf-related statistics
                docs_by_cluster[cluster].append(vocab[i])

        # For each label, also add the centroid
        nodes.append({
            'x': centroids[cluster][0],
            'y': centroids[cluster][1],
            'cluster': cluster,
            'isCentroid': True
        })

    term_freq = term_frequency(docs_by_cluster)
    tfidf = get_tfidf(docs_by_cluster)

    return {
        'k_num': n_clusters,
        'nodes': nodes,
        'term_frequencies': term_freq,
        'tfidf': tfidf,
    }