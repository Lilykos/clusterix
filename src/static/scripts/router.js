var Router = (function() {
    var defaultData = {
        fields: [],
        algorithm: 'kmeans',
        sampleFraction: '1',
        decomposition: 'svd',
        distanceMetric: 'euclidean',
        vectorizer: 'count',
        featureNumber: '500',
        stemming: true,
        stopwords: true,
        norm: null,
        kNumber: 1,
        affinity: 'euclidean',
        linkage: 'ward',
        binNumber: 5,
        clusterAll: false,
        minSamples: 20,
        eps: 0.3
    };

    function getData() {
        var data = {
            // GENERAL
            fields:         valOrDefault('#multiple-fields-csv', 'fields'),
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

            // Hierarchical (+ K-Means just for kNum)
            kNumber:        valOrDefault('#kmeans-num', 'kNumber'),
            affinity:       valOrDefault('#affinity-selection', 'affinity'),
            linkage:        valOrDefault('#linkage-selection', 'linkage'),

            // Mean Shift
            binNumber:      valOrDefault('#bin-frequency', 'binNumber'),
            clusterAll:     $('#cluster-all').hasClass('checked'),

            // DBSCAN
            minSamples:      valOrDefault('#min-samples', 'minSamples'),
            eps:            valOrDefault('#eps', 'eps')
        };
        var formData = new FormData();
        formData.append('data', JSON.stringify(data));
        return formData;
    }

    function valOrDefault(id, key) {
        var value = $(id).val();
        if (value == null || value == "" || value == undefined) {
            return defaultData[key];
        }
        return value;
    }

    function ajaxConfig(route, data) {
        return {
            type: 'POST',
            url: route,
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            success: function(data){
                Renderer.render(data);
                removeLoadingScreen();
            }
        }
    }

    return {

        /**
         * Uploads the attributes and returns the result.
         */
        init: function() {
            console.log('Router init');
            $('#get-results').on('click', function () {
                $.ajax(ajaxConfig('/get_clustering_results', getData()));
                initLoadingScreen();
            });

            $('#projection-results').on('click', function () {
                $.ajax(ajaxConfig('/get_projection', getData()));
                initLoadingScreen();
            });
        }
    }
})();