def get_kmeans_json(coords, labels, centroids, n_clusters):
    """Get a dictionary that will be converted to json, and contains all the visualization data."""
    nodes = []
    for cluster in xrange(n_clusters):

        for i in xrange(len(labels)):
            # Add nodes
            if labels[i] == cluster:
                nodes.append({
                    'x': coords[i][0],
                    'y': coords[i][1],
                    'cluster': cluster,
                    'isCentroid': False,
                    'id': i
                })

        # For each label, also add the centroid
        nodes.append({
            'x': centroids[cluster][0],
            'y': centroids[cluster][1],
            'cluster': cluster,
            'isCentroid': True
        })

    return {
        'k_num': n_clusters,
        'nodes': nodes,
    }