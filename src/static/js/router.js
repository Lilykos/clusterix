var Router = (function() {
    var defaultData = {
        fields: [],
        sampleFraction: '1',
        decomposition: 'svd',
        distanceMetric: 'euclidean',
        vectorizer: 'count',
        featureNumber: '500',
        stemming: 'true',
        stopwords: 'true',
        norm: 'none',
        algorithm: 'kmeans',
        kNumber: 1
    };

    function getData() {
        var data = {
            // GENERAL
            fields:         valOrDefault('#multiple-fields-csv', 'fields'),
            sampleFraction: valOrDefault('#sample-fraction', 'sampleFraction'),

            // DECOMPOSITION
            decomposition:  valOrDefault('#decomposition-selection', 'decomposition'),
            distanceMetric: valOrDefault('#decomposition-metric-selection', 'distanceMetric'),

            // TEXT
            vectorizer:     valOrDefault('#vectorizer-selection', 'vectorizer'),
            featureNumber:  valOrDefault('#feature-num', 'featureNumber'),
            stemming: 'true',
            stopwords: 'true',
            norm:           valOrDefault('#norm-selection', 'norm'),

            // ALGORITHMS
            algorithm:      valOrDefault('#algorithms-selection', 'algorithm'),
            kNumber:        valOrDefault('#kmeans-num', 'kNumber')
        };
        var formData = new FormData();
        formData.append('data', JSON.stringify(data));
        return formData
    }

    function valOrDefault(id, key) {
        var value = $(id).val();
        if (value == null || value == "" || value == undefined) {
            return defaultData[key];
        }
        return value;
    }

    return {

        /**
         * Uploads the attributes and returns the result.
         */
        init: function() {
            console.log('Router init');
            $('#get-results').on('click', function () {
                var formData = getData();
                $.ajax({type: 'POST', url: '/get_clustering_results', data: formData,
                    cache: false, contentType: false, processData: false,
                    success: function(data){
                        Renderer.render(data);
                        removeLoadingScreen();
                    }
                });
                initLoadingScreen();
            });

            $('#projection-results').on('click', function () {
                var formData = getData();
                $.ajax({type: 'POST', url: '/get_projection', data: formData,
                    cache: false, contentType: false, processData: false,
                    success: function(data){
                        Renderer.render(data);
                        removeLoadingScreen();
                    }
                });
                initLoadingScreen();
            });
        }
    }
})();