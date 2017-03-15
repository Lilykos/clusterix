var Router = (function() {
    var defaultData = {
        fields: [],
        scatterFields: [],
        algorithm: 'kmeans',
        sampleFraction: '1',
        decomposition: 'svd',
        distanceMetric: 'euclidean',
        vectorizer: 'count',
        featureNumber: '500',
        stemming: true,
        stopwords: true,
        norm: 'none',
        kNumber: 1,
        affinity: 'euclidean',
        linkage: 'ward',
        binNumber: 5,
        clusterAll: false,
        minSamples: 20,
        eps: 0.3
    };

    function valOrDefault(id, key) {
        var value = $(id).val();
        if (value == null || value == "" || value == undefined) {
            return defaultData[key];
        }
        return value;
    }

    function getData() {
        var data = {
            // GENERAL
            fields:         valOrDefault('#multiple-fields-csv', 'fields'),
            scatterFields:  valOrDefault('#scatterplot-matrix-fields', 'scatterFields'),
            algorithm:      valOrDefault('#algorithms-selection', 'algorithm'),
            sampleFraction: valOrDefault('#sample-fraction', 'sampleFraction'),

            // DECOMPOSITION
            decomposition:  valOrDefault('#decomposition-selection', 'decomposition'),
            distanceMetric: valOrDefault('#decomposition-metric-selection', 'distanceMetric'),

            // TEXT
            vectorizer:     valOrDefault('#vectorizer-selection', 'vectorizer'),
            featureNumber:  valOrDefault('#feature-num', 'featureNumber'),
            norm:           valOrDefault('#norm-selection', 'norm'),
            stemming:       $('#stem-checkbox').hasClass('checked'),
            stopwords:      $('#stop-checkbox').hasClass('checked'),

            // Hierarchical (+ K-Means just for kNumber)
            kNumber:        valOrDefault('#kmeans-num', 'kNumber'),
            affinity:       valOrDefault('#affinity-selection', 'affinity'),
            linkage:        valOrDefault('#linkage-selection', 'linkage'),

            // Mean Shift
            binNumber:      valOrDefault('#bin-frequency', 'binNumber'),
            clusterAll:     $('#cluster-all').hasClass('checked'),

            // DBSCAN
            minSamples:     valOrDefault('#min-samples', 'minSamples'),
            eps:            valOrDefault('#eps', 'eps')
        };
        var formData = new FormData();
        formData.append('data', JSON.stringify(data));
        return formData;
    }

    return {

    /**
     * Uploads the attributes and returns the result.
     */
    init: function() {
        // Get cluster scatterplot
        $('#get-results').on('click', function () {
            $.ajax(ajaxConfig('/get_clustering_results', getData()));
            initLoadingScreen();
        });

        // Get projection scatterplot
        $('#projection-results').on('click', function () {
            $.ajax(ajaxConfig('/get_projection', getData()));
            initLoadingScreen();
        });

        // Scatterplot matrix
        $('#scatterplot-matrix-button').on('click', function() {
            $.ajax(ajaxConfigScatter('/scatterplot_matrix', getData()));
            initLoadingScreen();
        });

        // Get TF-IDF information
        $('body').on('tfidf-request', function (e, clusters) {
            var formData = getData();
            formData.append('clusters', JSON.stringify(clusters));

            $.ajax({type: 'POST', url: '/tfidf', data: formData,
                cache: false, contentType: false, processData: false,
                success: function(data){ drawTfidf(data['results']); }
            });

        // Get search results
        }).on('search-request', function (e, query) {
            $.ajax({type: 'POST',
                url: '/search',
                data: {query: query},
                dataType:'text',
                success: function (data) {
                    var ids = JSON.parse(data).results;
                    showSearchResults(ids);
                }
            });
        });
    }
}
})();