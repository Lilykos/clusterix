def get_kmeans_json(n_clusters, labels, centroids, items, coords):
    d3_items = []
    centroid_items = []

    for cluster in xrange(n_clusters):
        for i in xrange(len(labels)):

            if labels[i] == cluster:
                d3_items.append({
                    'x': coords[i][0],
                    'y': coords[i][1],
                    'content': items[i],
                    'cluster': cluster
                })

        centroid_items.append({
            'x': centroids[cluster][0],
            'y': coords[cluster][1],
            'cluster': cluster
        })

    return {
        'k_num': n_clusters,
        'items': d3_items,
        'centroids': centroid_items
    }